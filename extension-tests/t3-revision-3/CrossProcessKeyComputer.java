package com.enterprise.ai.runtime.cache.response;

import com.enterprise.ai.runtime.common.context.ExecutionContext;
import com.enterprise.ai.runtime.common.model.CallerIdentity;
import com.enterprise.ai.runtime.common.model.ChatInvocation;
import com.enterprise.ai.runtime.common.model.Message;
import com.enterprise.ai.runtime.common.testing.RuntimeFixtures;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * Child-process entry point for {@link ResponseCacheKeyCrossProcessTest}.
 *
 * <p>Computes cache keys for {@link #HISTORIES} and writes one line per case:
 * {@code id <TAB> key <TAB> legacy}, where {@code legacy} is the value the key
 * factory used before the T3 repair ({@code history().hashCode()}). The legacy
 * value is reported only so the test can confirm that its perturbation really
 * changes identity-based hashes; it is not part of the key.
 *
 * <p>With the argument {@code perturb}, the process first draws many identity
 * hash codes on the main thread and on other threads, so that the {@code Role}
 * enum constants receive different identity hashes than in an unperturbed
 * process. That gives the two processes genuinely different execution histories.
 *
 * <p>Usage: {@code CrossProcessKeyComputer plain|perturb <output-file>}
 */
public final class CrossProcessKeyComputer {

    /** Includes pairs that differ only by role and only by order. */
    static final List<List<Message>> HISTORIES = List.of(
            List.of(),
            List.of(Message.user("What is the refund window?")),
            List.of(Message.user("Same text")),
            List.of(Message.assistant("Same text")),
            List.of(Message.user("first"), Message.user("second")),
            List.of(Message.user("second"), Message.user("first")),
            List.of(Message.system("Answer briefly."), Message.user("Reset my password."),
                    Message.assistant("I have sent a reset link."), Message.user("It expired.")));

    private CrossProcessKeyComputer() {
    }

    public static void main(String[] args) throws Exception {
        if ("perturb".equals(args[0])) {
            perturbIdentityHashes();
        }
        ResponseCacheKeyFactory factory = new ResponseCacheKeyFactory();
        List<String> lines = new ArrayList<>();
        for (int i = 0; i < HISTORIES.size(); i++) {
            List<Message> history = HISTORIES.get(i);
            lines.add(i + "\t" + factory.key(contextFor(history)) + "\t"
                    + Integer.toHexString(history.hashCode()));
        }
        try (PrintWriter out = new PrintWriter(Files.newBufferedWriter(Path.of(args[1]), StandardCharsets.UTF_8))) {
            lines.forEach(out::println);
        }
    }

    /** Built as ResponseCacheKeyFactoryTest builds its contexts, plus history. */
    static ExecutionContext contextFor(List<Message> history) {
        CallerIdentity caller = new CallerIdentity("trace", "req", RuntimeFixtures.APPLICATION,
                RuntimeFixtures.USE_CASE, RuntimeFixtures.ENVIRONMENT, RuntimeFixtures.REGION,
                "user-1", RuntimeFixtures.TENANT, "session-1", Map.of());
        ChatInvocation invocation = ChatInvocation.builder()
                .promptId("customer-summary")
                .variables(Map.of("customerId", "cust-42"))
                .modelProfile("enterprise-chat")
                .history(history)
                .build();
        ExecutionContext context = new ExecutionContext(caller, invocation, false);
        context.prompt(RuntimeFixtures.prompt());
        context.policies(RuntimeFixtures.policies());
        context.composedPrompt(RuntimeFixtures.composedPrompt());
        return context;
    }

    private static void perturbIdentityHashes() throws InterruptedException {
        long sink = 0;
        for (int i = 0; i < 200_000; i++) {
            sink += System.identityHashCode(new Object());
        }
        List<Thread> threads = new ArrayList<>();
        for (int t = 0; t < 4; t++) {
            Thread thread = new Thread(() -> {
                for (int i = 0; i < 50_000; i++) {
                    System.identityHashCode(new Object());
                }
            });
            threads.add(thread);
            thread.start();
        }
        for (Thread thread : threads) {
            thread.join();
        }
        if (sink == 42) {
            System.out.print("");   // keeps the loop from being optimised away
        }
    }
}

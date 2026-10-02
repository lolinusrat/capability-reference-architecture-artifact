import com.enterprise.ai.runtime.cache.response.ResponseCacheKeyFactory;
import com.enterprise.ai.runtime.common.context.ExecutionContext;
import com.enterprise.ai.runtime.common.model.CallerIdentity;
import com.enterprise.ai.runtime.common.model.ChatInvocation;
import com.enterprise.ai.runtime.common.model.Message;
import com.enterprise.ai.runtime.common.model.Role;
import com.enterprise.ai.runtime.common.testing.RuntimeFixtures;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.io.InputStream;
import java.io.PrintWriter;
import java.lang.management.ManagementFactory;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.HexFormat;
import java.util.List;
import java.util.Map;

/**
 * T3 assertion B5-keys: records the cache keys this JVM computes.
 *
 * <p>Run once in each of two separate JVM processes (see run-key-probe.sh) and
 * compare the two output files history by history. The probe calls the unchanged
 * {@link ResponseCacheKeyFactory} from the runtime's own build output, builds each
 * context the way ResponseCacheKeyFactoryTest does, and reads every history from
 * the fixed data file. It records which factory class it loaded, and that class's
 * digest, so each output proves which key construction produced it.
 *
 * <p>Usage: {@code java KeyProbe <t3-histories.json> <output-file>}
 */
public final class KeyProbe {

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("usage: KeyProbe <t3-histories.json> <output-file>");
            System.exit(2);
        }
        Path historiesFile = Path.of(args[0]);
        Path output = Path.of(args[1]);

        JsonNode root = new ObjectMapper().readTree(historiesFile.toFile());
        JsonNode histories = root.get("histories");
        if (histories == null || histories.size() != 20) {
            throw new IllegalStateException("expected exactly 20 histories in " + historiesFile);
        }

        ResponseCacheKeyFactory factory = new ResponseCacheKeyFactory();
        try (PrintWriter out = new PrintWriter(Files.newBufferedWriter(output, StandardCharsets.UTF_8))) {
            out.println("# T3 B5-keys probe output");
            out.println("# jvm " + ManagementFactory.getRuntimeMXBean().getName());
            out.println("# histories-file-sha256 " + sha256(Files.readAllBytes(historiesFile)));
            out.println("# key-factory-class " + ResponseCacheKeyFactory.class.getProtectionDomain()
                    .getCodeSource().getLocation());
            out.println("# key-factory-class-sha256 " + classDigest(ResponseCacheKeyFactory.class));
            for (JsonNode history : histories) {
                out.println(history.get("id").asText() + "\t" + factory.key(contextFor(messages(history))));
            }
        }
    }

    private static List<Message> messages(JsonNode history) {
        List<Message> messages = new ArrayList<>();
        for (JsonNode message : history.get("messages")) {
            messages.add(new Message(Role.valueOf(message.get("role").asText()),
                    message.get("content").asText()));
        }
        return messages;
    }

    /** Built exactly as ResponseCacheKeyFactoryTest builds its contexts, plus history. */
    private static ExecutionContext contextFor(List<Message> history) {
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

    private static String classDigest(Class<?> type) throws Exception {
        String resource = type.getName().replace('.', '/') + ".class";
        try (InputStream in = type.getClassLoader().getResourceAsStream(resource)) {
            return sha256(in.readAllBytes());
        }
    }

    private static String sha256(byte[] bytes) throws Exception {
        return HexFormat.of().formatHex(MessageDigest.getInstance("SHA-256").digest(bytes));
    }
}

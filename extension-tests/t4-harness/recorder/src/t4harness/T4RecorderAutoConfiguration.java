package t4harness;

import com.enterprise.ai.runtime.common.context.ExecutionContext;
import com.enterprise.ai.runtime.common.retrieval.RetrievedContext.RetrievedDocument;
import com.enterprise.ai.runtime.common.spi.Retriever;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.atomic.AtomicLong;
import java.util.function.Supplier;
import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.boot.autoconfigure.AutoConfiguration;
import org.springframework.context.annotation.Bean;
import reactor.core.publisher.Flux;

/**
 * T4 test-only recorder. Harness-owned; not part of the runtime's source tree.
 *
 * <p>Loaded from outside through PropertiesLauncher and {@code loader.path}. It
 * wraps every {@link Retriever} bean and records, one JSON line per event:
 * {@code recorder-installed}, {@code retrieve-called} (request id, topK),
 * {@code retrieve-returned} (the documents the engine returned: id, version,
 * source, metadata, score) and {@code retrieve-error} (the failure's class and
 * message).
 *
 * <p><b>Non-interference</b>, as in T3: every recording step is guarded and never
 * throws into the retrieval. The delegate's own publisher is returned, with the
 * recording attached through side effects that cannot throw. Failures go to
 * standard error as {@code T4-RECORDER-ERROR} lines; every event carries a
 * sequence number.
 *
 * <p>Output: system property {@code t4.recorder.out}; instance label:
 * {@code t4.instance}.
 */
@AutoConfiguration
public class T4RecorderAutoConfiguration {

    @Bean
    static BeanPostProcessor t4RetrieverRecorder() {
        return new BeanPostProcessor() {
            @Override
            public Object postProcessAfterInitialization(Object bean, String beanName) {
                if (bean instanceof Retriever retriever) {
                    return new Recording(retriever, bean.getClass().getName());
                }
                return bean;
            }
        };
    }

    static final class Recording implements Retriever {
        private static final AtomicLong SEQUENCE = new AtomicLong();
        private final Retriever delegate;
        private final String realization;
        private final Path out = Path.of(System.getProperty("t4.recorder.out", "t4-recorder.jsonl"));
        private final String instance = System.getProperty("t4.instance", "?");

        Recording(Retriever delegate, String realization) {
            this.delegate = delegate;
            this.realization = realization;
            record("recorder-installed", () -> "");
        }

        @Override
        public String strategy() {
            return delegate.strategy();
        }

        @Override
        public boolean supports(ExecutionContext context) {
            return delegate.supports(context);
        }

        @Override
        public Flux<RetrievedDocument> retrieve(ExecutionContext context, int topK) {
            String requestId = safe(context::requestId);
            record("retrieve-called", () -> ",\"request\":" + json(requestId) + ",\"topK\":" + topK);
            List<RetrievedDocument> seen = new ArrayList<>();
            return delegate.retrieve(context, topK)
                    .doOnNext(document -> {
                        try {
                            seen.add(document);
                        } catch (Throwable t) {
                            diagnostic("collect", t);
                        }
                    })
                    .doOnComplete(() -> record("retrieve-returned", () -> ",\"request\":" + json(requestId)
                            + ",\"documents\":" + documents(seen)))
                    .doOnError(failure -> record("retrieve-error", () -> ",\"request\":" + json(requestId)
                            + ",\"error\":" + json(failure.getClass().getName() + ": " + failure.getMessage())));
        }

        private String safe(Supplier<String> value) {
            try {
                return value.get();
            } catch (Throwable t) {
                diagnostic("request id", t);
                return null;
            }
        }

        private void record(String event, Supplier<String> fields) {
            long seq = SEQUENCE.incrementAndGet();
            try {
                String line = "{\"seq\":" + seq + ",\"at\":" + json(Instant.now().toString())
                        + ",\"instance\":" + json(instance) + ",\"realization\":" + json(realization)
                        + ",\"strategy\":" + json(safe(delegate::strategy))
                        + ",\"event\":" + json(event) + fields.get() + "}\n";
                synchronized (Recording.class) {
                    Files.writeString(out, line, StandardCharsets.UTF_8,
                            StandardOpenOption.CREATE, StandardOpenOption.APPEND);
                }
            } catch (Throwable t) {
                diagnostic(event + " seq " + seq, t);
            }
        }

        private void diagnostic(String what, Throwable t) {
            try {
                System.err.println("T4-RECORDER-ERROR instance=" + instance + " " + what + ": " + t);
            } catch (Throwable ignored) {
                // Nothing further is safe to do without risking the retrieval.
            }
        }
    }

    static String documents(List<RetrievedDocument> documents) {
        StringBuilder b = new StringBuilder("[");
        for (RetrievedDocument d : documents) {
            if (b.length() > 1) {
                b.append(',');
            }
            b.append("{\"id\":").append(json(d.id())).append(",\"version\":").append(json(d.version()))
                    .append(",\"source\":").append(json(d.source())).append(",\"score\":").append(d.score())
                    .append(",\"metadata\":{");
            boolean first = true;
            for (Map.Entry<String, String> e : new TreeMap<>(d.metadata()).entrySet()) {
                b.append(first ? "" : ",").append(json(e.getKey())).append(':').append(json(e.getValue()));
                first = false;
            }
            b.append("}}");
        }
        return b.append(']').toString();
    }

    static String json(String s) {
        if (s == null) {
            return "null";
        }
        StringBuilder b = new StringBuilder("\"");
        for (char c : s.toCharArray()) {
            switch (c) {
                case '"' -> b.append("\\\"");
                case '\\' -> b.append("\\\\");
                case '\n' -> b.append("\\n");
                case '\r' -> b.append("\\r");
                case '\t' -> b.append("\\t");
                default -> {
                    if (c < 0x20) {
                        b.append(String.format("\\u%04x", (int) c));
                    } else {
                        b.append(c);
                    }
                }
            }
        }
        return b.append('"').toString();
    }
}

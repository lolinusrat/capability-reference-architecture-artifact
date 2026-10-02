package t3harness;

import com.enterprise.ai.runtime.common.context.ExecutionContext;
import com.enterprise.ai.runtime.common.model.ChatOutcome;
import com.enterprise.ai.runtime.common.spi.ResponseCache;
import java.lang.reflect.RecordComponent;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.time.Instant;
import java.util.Collection;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.atomic.AtomicLong;
import java.util.function.Supplier;
import org.springframework.beans.factory.config.BeanPostProcessor;
import org.springframework.boot.autoconfigure.AutoConfiguration;
import org.springframework.context.annotation.Bean;
import reactor.core.publisher.Mono;

/**
 * T3 test-only recorder. Harness-owned; not part of the runtime's source tree.
 *
 * <p>Loaded into a runtime process from outside, through Spring Boot's
 * PropertiesLauncher and {@code loader.path}. It wraps whichever
 * {@link ResponseCache} bean the runtime selected and records, one JSON line per
 * event:
 * <ul>
 *   <li>{@code store-called}: a key and the outcome handed to {@code store},
 *       before the realization serializes it;</li>
 *   <li>{@code lookup-called}: a key for the lookup;</li>
 *   <li>{@code lookup-returned}: the outcome {@code lookup} returned, after the
 *       realization deserialized it with the runtime's own serializer.</li>
 * </ul>
 *
 * <p><b>Non-interference.</b> Recording never affects a cache operation. Every
 * recording step (key computation, rendering and writing) runs inside a guard
 * that catches any {@link Throwable}; a failure is reported on the diagnostic
 * channel and the cache call proceeds exactly as it would without the recorder.
 * {@code store} always reaches the delegate, and {@code lookup} always returns
 * the delegate's own publisher, with the recording attached to it by a
 * side-effect that cannot throw.
 *
 * <p><b>Diagnostic channel.</b> Each recording failure is written to standard
 * error as one line beginning {@code T3-RECORDER-ERROR}. Standard error is
 * captured in the runtime's log, a separate channel from the event file that may
 * be the thing failing. Every event also carries a sequence number, so a missing
 * event shows up as a gap even if its error line were lost.
 *
 * <p><b>What the recorded key is.</b> The realizations compute the key they use
 * internally with {@code keyFactory.key(context)}; their {@code key(context)}
 * method returns the same factory's result for the same context. The recorder
 * calls {@code key(context)} separately, so the recorded key is a <i>separately
 * computed observation</i> by the same factory on the same context, not a value
 * captured from inside the cache operation. For Redis, the harness cross-checks it
 * against the key Redis MONITOR shows the instance actually issued.
 *
 * <p>Outcomes are rendered by reflection over record components, never through
 * Jackson, so the rendering is independent of the serializer under test.
 *
 * <p>Output file: system property {@code t3.recorder.out}. Instance label:
 * system property {@code t3.instance}.
 */
@AutoConfiguration
public class T3RecorderAutoConfiguration {

    @Bean
    static BeanPostProcessor t3ResponseCacheRecorder() {
        return new BeanPostProcessor() {
            @Override
            public Object postProcessAfterInitialization(Object bean, String beanName) {
                if (bean instanceof ResponseCache cache) {
                    return new Recording(cache, bean.getClass().getName());
                }
                return bean;
            }
        };
    }

    static final class Recording implements ResponseCache {
        private final ResponseCache delegate;
        private final String realization;
        private final Path out = Path.of(System.getProperty("t3.recorder.out", "t3-recorder.jsonl"));
        private final String instance = System.getProperty("t3.instance", "?");
        private final AtomicLong sequence = new AtomicLong();

        Recording(ResponseCache delegate, String realization) {
            this.delegate = delegate;
            this.realization = realization;
            record("recorder-installed", () -> "");
        }

        @Override
        public Mono<ChatOutcome> lookup(ExecutionContext context) {
            String key = safeKey(context);
            record("lookup-called", () -> ",\"key\":" + jsonOrNull(key));
            return delegate.lookup(context).doOnNext(outcome ->
                    record("lookup-returned", () -> ",\"key\":" + jsonOrNull(key)
                            + ",\"outcome\":" + render(outcome)));
        }

        @Override
        public Mono<Void> store(ExecutionContext context, ChatOutcome outcome) {
            String key = safeKey(context);
            record("store-called", () -> ",\"key\":" + jsonOrNull(key) + ",\"outcome\":" + render(outcome));
            return delegate.store(context, outcome);
        }

        @Override
        public String key(ExecutionContext context) {
            return delegate.key(context);
        }

        /** The recorder's own key computation; a failure here never reaches the caller. */
        private String safeKey(ExecutionContext context) {
            try {
                return delegate.key(context);
            } catch (Throwable t) {
                diagnostic("key", t);
                return null;
            }
        }

        /** Records one event. Never throws: every failure goes to the diagnostic channel. */
        private void record(String event, Supplier<String> fields) {
            long seq = sequence.incrementAndGet();
            try {
                String line = "{\"seq\":" + seq + ",\"at\":" + json(Instant.now().toString())
                        + ",\"instance\":" + json(instance) + ",\"realization\":" + json(realization)
                        + ",\"event\":" + json(event) + fields.get() + "}\n";
                synchronized (this) {
                    Files.writeString(out, line, StandardCharsets.UTF_8,
                            StandardOpenOption.CREATE, StandardOpenOption.APPEND);
                }
            } catch (Throwable t) {
                diagnostic(event + " seq " + seq, t);
            }
        }

        private void diagnostic(String what, Throwable t) {
            try {
                System.err.println("T3-RECORDER-ERROR instance=" + instance + " " + what + ": " + t);
            } catch (Throwable ignored) {
                // Nothing further is safe to do without risking the cache operation.
            }
        }
    }

    static String jsonOrNull(String s) {
        return s == null ? "null" : json(s);
    }

    /** Reflection-based JSON rendering; deliberately not Jackson. */
    static String render(Object value) {
        if (value == null) {
            return "null";
        }
        if (value instanceof BigDecimal d) {
            return "{\"decimal\":" + json(d.toString()) + ",\"scale\":" + d.scale() + "}";
        }
        if (value instanceof String || value instanceof Character) {
            return json(value.toString());
        }
        if (value instanceof Number || value instanceof Boolean) {
            return json(value.toString());
        }
        if (value instanceof Enum<?> e) {
            return json(e.name());
        }
        if (value instanceof Map<?, ?> map) {
            StringBuilder b = new StringBuilder("{");
            new TreeMap<>(stringKeys(map)).forEach((k, v) ->
                    b.append(b.length() > 1 ? "," : "").append(json(k)).append(':').append(render(v)));
            return b.append('}').toString();
        }
        if (value instanceof Collection<?> items) {
            StringBuilder b = new StringBuilder("[");
            for (Object item : items) {
                b.append(b.length() > 1 ? "," : "").append(render(item));
            }
            return b.append(']').toString();
        }
        if (value.getClass().isRecord()) {
            StringBuilder b = new StringBuilder("{\"_record\":" + json(value.getClass().getSimpleName()));
            for (RecordComponent c : value.getClass().getRecordComponents()) {
                try {
                    b.append(',').append(json(c.getName())).append(':').append(render(c.getAccessor().invoke(value)));
                } catch (ReflectiveOperationException e) {
                    throw new IllegalStateException(e);
                }
            }
            return b.append('}').toString();
        }
        return json(value.getClass().getName() + ":" + value);
    }

    private static Map<String, Object> stringKeys(Map<?, ?> map) {
        Map<String, Object> out = new TreeMap<>();
        map.forEach((k, v) -> out.put(String.valueOf(k), v));
        return out;
    }

    static String json(String s) {
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

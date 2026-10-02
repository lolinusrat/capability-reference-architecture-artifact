package com.enterprise.ai.runtime.cache.response;

import com.enterprise.ai.runtime.common.context.ExecutionContext;
import com.enterprise.ai.runtime.common.model.ChatInvocation;
import com.enterprise.ai.runtime.common.prompt.PromptDefinition;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Map;
import java.util.TreeMap;

/**
 * Derives the response cache key.
 *
 * <p>Small, separate and public because cache-key bugs are the silent kind:
 * every one of them produces a plausible answer to a question nobody asked, and
 * none of them fails a health check. Isolating the derivation makes it directly
 * testable — a test can pin exactly which inputs change the key and, more
 * usefully, assert that changing a tenant or re-indexing a corpus does.
 *
 * <p>Every input that can change the answer is in the key:
 *
 * <table border="1">
 *   <caption>Key components and the bug each one prevents</caption>
 *   <tr><th>Component</th><th>Omitting it means</th></tr>
 *   <tr><td>tenant</td><td>one tenant is served another's answer — a data breach, not a cache miss</td></tr>
 *   <tr><td>prompt id and version</td><td>a revised prompt keeps serving the old answer until the TTL expires</td></tr>
 *   <tr><td>model profile</td><td>repointing a profile changes nothing until the cache drains</td></tr>
 *   <tr><td>variables</td><td>every customer gets the first customer's summary</td></tr>
 *   <tr><td>retrieval fingerprint</td><td>a re-indexed corpus keeps answering from the old index</td></tr>
 *   <tr><td>response schema</td><td>a structured caller receives an unstructured cached answer</td></tr>
 *   <tr><td>generation parameters</td><td>a deterministic request is served a high-temperature answer</td></tr>
 * </table>
 *
 * <p>User id is deliberately <em>not</em> a component. Caching per user would
 * push the hit rate to nearly zero for the shared-question workloads that make
 * a response cache worth having; tenant is the isolation boundary that matters,
 * and per-user variation already enters the key through the variables.
 */
public final class ResponseCacheKeyFactory {

    private static final String NAMESPACE = "eair:v1";

    /** Written out rather than inlined: a raw control character in source is invisible to a reviewer. */
    private static final char UNIT_SEPARATOR = '\u001f';
    private static final char RECORD_SEPARATOR = '\u001e';

    /**
     * Builds the key for a request.
     *
     * @param context a request whose prompt has been resolved and composed
     * @return a namespaced, hashed key safe to use in Redis
     */
    public String key(ExecutionContext context) {
        PromptDefinition prompt = context.requirePrompt();
        ChatInvocation invocation = context.invocation();

        StringBuilder material = new StringBuilder(256);
        append(material, "tenant", context.tenant());
        append(material, "prompt", prompt.promptId());
        append(material, "version", prompt.version());
        append(material, "profile", context.requirePolicies().modelProfile().name());
        append(material, "vars", canonicalise(invocation.variables()));
        append(material, "retrieval", context.retrievedContext().fingerprint());
        append(material, "schema", invocation.responseSchema());
        append(material, "maxTokens", invocation.maxOutputTokens());
        append(material, "temperature", invocation.temperature());

        // An inline prompt has no meaningful version, so the text itself has to
        // enter the key or every ad hoc call would collide with every other.
        if (prompt.isInline()) {
            append(material, "inline", context.requireComposedPrompt().fullText());
        }
        // History changes the answer, but hashing every turn's text keeps the key
        // bounded regardless of how long a conversation runs.
        append(material, "history", Integer.toHexString(invocation.history().hashCode()));

        return NAMESPACE + ":" + sha256(material.toString());
    }

    /**
     * Renders variables in a stable order.
     *
     * <p>Without this, two identical requests whose variable maps iterate in
     * different orders produce different keys, and the cache quietly never hits.
     * That failure mode is invisible: the service is correct, just slower and
     * more expensive than the dashboard says it should be.
     */
    private String canonicalise(Map<String, Object> variables) {
        if (variables == null || variables.isEmpty()) {
            return "";
        }
        StringBuilder rendered = new StringBuilder();
        new TreeMap<>(variables).forEach((name, value) ->
                rendered.append(name).append('=').append(value).append(';'));
        return rendered.toString();
    }

    /**
     * Appends one labelled component, delimited by characters that cannot occur
     * in the values themselves.
     *
     * <p>The delimiters matter. With a plain separator the component lists
     * {@code ("ab", "c")} and {@code ("a", "bc")} hash identically, so two
     * genuinely different requests would share one cache entry. ASCII unit and
     * record separators are used because no prompt id, variable value or corpus
     * fingerprint can contain them.
     */
    private void append(StringBuilder material, String label, Object value) {
        material.append(label).append(UNIT_SEPARATOR)
                .append(value == null ? "" : value).append(RECORD_SEPARATOR);
    }

    private String sha256(String material) {
        try {
            byte[] digest = MessageDigest.getInstance("SHA-256")
                    .digest(material.getBytes(StandardCharsets.UTF_8));
            StringBuilder hex = new StringBuilder(digest.length * 2);
            for (byte b : digest) {
                hex.append(Character.forDigit((b >> 4) & 0xf, 16)).append(Character.forDigit(b & 0xf, 16));
            }
            return hex.toString();
        } catch (NoSuchAlgorithmException e) {
            // SHA-256 is mandated by the JLS for every conformant JRE.
            throw new IllegalStateException("SHA-256 is unavailable on this JVM", e);
        }
    }
}

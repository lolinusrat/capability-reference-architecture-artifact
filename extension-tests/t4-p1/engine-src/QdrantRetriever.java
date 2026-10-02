package com.enterprise.ai.runtime.retrieval.engine;

import com.enterprise.ai.runtime.common.context.ExecutionContext;
import com.enterprise.ai.runtime.common.retrieval.RetrievedContext.RetrievedDocument;
import com.enterprise.ai.runtime.common.spi.Retriever;
import com.fasterxml.jackson.databind.JsonNode;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;

/**
 * Vector retrieval from Qdrant, over its REST API.
 *
 * <p>Uses a {@link WebClient}, already present in the runtime, rather than a
 * Qdrant client library. Results are restricted to the caller's tenant through a
 * payload filter, the only isolation information the {@link Retriever} contract
 * carries; finer entitlements cannot be applied, for the same reason as in
 * {@link PgVectorRetriever}.
 */
public class QdrantRetriever implements Retriever {

    private final WebClient http;
    private final QueryEmbedder embedder;
    private final String collection;

    public QdrantRetriever(WebClient http, QueryEmbedder embedder, String collection) {
        if (!collection.matches("[A-Za-z0-9_-]+")) {
            throw new IllegalArgumentException("invalid collection name: " + collection);
        }
        this.http = http;
        this.embedder = embedder;
        this.collection = collection;
    }

    @Override
    public String strategy() {
        return "qdrant";
    }

    @Override
    public Flux<RetrievedDocument> retrieve(ExecutionContext context, int topK) {
        String query = QueryEmbedder.queryOf(context);
        String tenant = QueryEmbedder.tenantOf(context);
        if (query == null || tenant == null) {
            return Flux.empty();
        }
        return embedder.embed(context, query)
                .flatMap(vector -> http.post()
                        .uri("/collections/{collection}/points/search", collection)
                        .contentType(MediaType.APPLICATION_JSON)
                        .bodyValue(searchBody(vector, tenant, topK))
                        .retrieve()
                        .bodyToMono(JsonNode.class))
                .flatMapMany(response -> Flux.fromIterable(response.path("result")))
                .map(QdrantRetriever::toDocument);
    }

    private static Map<String, Object> searchBody(List<Double> vector, String tenant, int topK) {
        Map<String, Object> body = new LinkedHashMap<>();
        body.put("vector", vector);
        body.put("limit", topK);
        body.put("with_payload", true);
        body.put("filter", Map.of("must", List.of(Map.of("key", "tenant", "match", Map.of("value", tenant)))));
        return body;
    }

    private static RetrievedDocument toDocument(JsonNode point) {
        JsonNode payload = point.path("payload");
        Map<String, String> metadata = new LinkedHashMap<>();
        metadata.put("title", payload.path("title").asText(null));
        if (payload.hasNonNull("classification")) {
            metadata.put("classification", payload.path("classification").asText());
        }
        return new RetrievedDocument(payload.path("doc_id").asText(), payload.path("version").asText("0"),
                payload.path("content").asText(""), point.path("score").asDouble(),
                payload.path("source").asText(null), metadata);
    }
}

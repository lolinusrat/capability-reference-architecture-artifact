package com.enterprise.ai.runtime.retrieval.engine;

import com.enterprise.ai.runtime.common.context.ExecutionContext;
import com.enterprise.ai.runtime.inference.gateway.GatewayProtocol;
import com.enterprise.ai.runtime.inference.gateway.ModelGatewayClient;
import java.util.List;
import reactor.core.publisher.Mono;

/**
 * Embeds a query through Model Services, using the existing gateway client.
 *
 * <p>The embedding request carries only what the contract defines: the profile,
 * the input text, and the request's identity attributes for the gateway's own
 * accounting. It deliberately carries no embedding purpose. The contract has no
 * field for one, and putting it in {@code attributes} would hide a semantic
 * parameter in a channel meant for accounting (T4 protocol §4.4).
 */
public class QueryEmbedder {

    private final ModelGatewayClient gateway;
    private final EngineProperties properties;

    public QueryEmbedder(ModelGatewayClient gateway, EngineProperties properties) {
        this.gateway = gateway;
        this.properties = properties;
    }

    public Mono<List<Double>> embed(ExecutionContext context, String text) {
        GatewayProtocol.EmbeddingRequest request = new GatewayProtocol.EmbeddingRequest(
                properties.getEmbeddingProfile(), List.of(text), context.asAttributes());
        return gateway.embeddings(request, properties.getEmbeddingTimeout())
                .map(response -> response.embeddings().get(0));
    }

    /** The query the caller asked retrieval to answer, or null when none was given. */
    static String queryOf(ExecutionContext context) {
        String query = context.invocation().retrieval().query();
        return query == null || query.isBlank() ? null : query;
    }

    /** The caller's tenant, the only isolation information the contract provides. */
    static String tenantOf(ExecutionContext context) {
        String tenant = context.caller().tenantId();
        return tenant == null || tenant.isBlank() ? null : tenant;
    }
}

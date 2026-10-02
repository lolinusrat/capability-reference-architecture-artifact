package com.enterprise.ai.runtime.retrieval.engine;

import com.enterprise.ai.runtime.common.context.ExecutionContext;
import com.enterprise.ai.runtime.common.retrieval.RetrievedContext.RetrievedDocument;
import com.enterprise.ai.runtime.common.spi.Retriever;
import io.r2dbc.spi.Connection;
import io.r2dbc.spi.ConnectionFactory;
import io.r2dbc.spi.Row;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Vector retrieval from PostgreSQL with pgvector, over R2DBC.
 *
 * <p>Results are restricted to the caller's tenant, the only isolation
 * information the {@link Retriever} contract carries. Finer entitlements (roles,
 * document classifications) cannot be applied, because the contract gives the
 * retriever no Security decision to apply.
 */
public class PgVectorRetriever implements Retriever {

    private final ConnectionFactory connections;
    private final QueryEmbedder embedder;
    private final String table;

    public PgVectorRetriever(ConnectionFactory connections, QueryEmbedder embedder, String table) {
        if (!table.matches("[A-Za-z_][A-Za-z0-9_]*")) {
            throw new IllegalArgumentException("invalid table name: " + table);
        }
        this.connections = connections;
        this.embedder = embedder;
        this.table = table;
    }

    @Override
    public String strategy() {
        return "pgvector";
    }

    @Override
    public Flux<RetrievedDocument> retrieve(ExecutionContext context, int topK) {
        String query = QueryEmbedder.queryOf(context);
        String tenant = QueryEmbedder.tenantOf(context);
        if (query == null || tenant == null) {
            return Flux.empty();
        }
        String sql = "SELECT id, version, content, source, title, classification, "
                + "1 - (embedding <=> $1::vector) AS score FROM " + table
                + " WHERE tenant = $2 ORDER BY embedding <=> $1::vector LIMIT $3";
        return embedder.embed(context, query)
                .flatMapMany(vector -> Flux.usingWhen(
                        Mono.from(connections.create()),
                        connection -> Flux.from(connection.createStatement(sql)
                                        .bind("$1", literal(vector))
                                        .bind("$2", tenant)
                                        .bind("$3", topK)
                                        .execute())
                                .flatMap(result -> result.map((row, metadata) -> toDocument(row))),
                        Connection::close));
    }

    private static RetrievedDocument toDocument(Row row) {
        Map<String, String> metadata = new LinkedHashMap<>();
        metadata.put("title", row.get("title", String.class));
        String classification = row.get("classification", String.class);
        if (classification != null) {
            metadata.put("classification", classification);
        }
        Double score = row.get("score", Double.class);
        return new RetrievedDocument(row.get("id", String.class), row.get("version", String.class),
                row.get("content", String.class), score == null ? 0d : score,
                row.get("source", String.class), metadata);
    }

    private static String literal(List<Double> vector) {
        return vector.stream().map(String::valueOf).collect(Collectors.joining(",", "[", "]"));
    }
}

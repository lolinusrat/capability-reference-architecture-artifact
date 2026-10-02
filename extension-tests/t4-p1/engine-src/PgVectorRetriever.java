package com.enterprise.ai.runtime.retrieval.engine;

import com.enterprise.ai.runtime.common.context.ExecutionContext;
import com.enterprise.ai.runtime.common.retrieval.RetrievedContext.RetrievedDocument;
import com.enterprise.ai.runtime.common.spi.Retriever;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.core.scheduler.Schedulers;

/**
 * Vector retrieval from PostgreSQL with pgvector.
 *
 * <p>Uses the PostgreSQL JDBC driver, with each query run on Reactor's
 * bounded-elastic scheduler so the blocking call never occupies a request thread.
 * JDBC rather than R2DBC because the R2DBC driver activates Spring Boot's R2DBC
 * auto-configuration across the whole application (T4 finding P1-1).
 *
 * <p>Results are restricted to the caller's tenant, the only isolation
 * information the {@link Retriever} contract carries. Finer entitlements (roles,
 * document classifications) cannot be applied, because the contract gives the
 * retriever no Security decision to apply.
 */
public class PgVectorRetriever implements Retriever {

    private final EngineProperties.PgVector settings;
    private final QueryEmbedder embedder;
    private final String sql;

    public PgVectorRetriever(EngineProperties.PgVector settings, QueryEmbedder embedder) {
        if (!settings.getTable().matches("[A-Za-z_][A-Za-z0-9_]*")) {
            throw new IllegalArgumentException("invalid table name: " + settings.getTable());
        }
        this.settings = settings;
        this.embedder = embedder;
        this.sql = "SELECT id, version, content, source, title, classification, "
                + "1 - (embedding <=> ?::vector) AS score FROM " + settings.getTable()
                + " WHERE tenant = ? ORDER BY embedding <=> ?::vector LIMIT ?";
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
        return embedder.embed(context, query)
                .flatMap(vector -> Mono.fromCallable(() -> search(literal(vector), tenant, topK))
                        .subscribeOn(Schedulers.boundedElastic()))
                .flatMapMany(Flux::fromIterable);
    }

    private List<RetrievedDocument> search(String vector, String tenant, int topK) throws SQLException {
        try (Connection connection = DriverManager.getConnection(
                settings.getUrl(), settings.getUsername(), settings.getPassword());
             PreparedStatement statement = connection.prepareStatement(sql)) {
            statement.setString(1, vector);
            statement.setString(2, tenant);
            statement.setString(3, vector);
            statement.setInt(4, topK);
            List<RetrievedDocument> documents = new ArrayList<>();
            try (ResultSet rows = statement.executeQuery()) {
                while (rows.next()) {
                    documents.add(toDocument(rows));
                }
            }
            return documents;
        }
    }

    private static RetrievedDocument toDocument(ResultSet row) throws SQLException {
        Map<String, String> metadata = new LinkedHashMap<>();
        metadata.put("title", row.getString("title"));
        String classification = row.getString("classification");
        if (classification != null) {
            metadata.put("classification", classification);
        }
        return new RetrievedDocument(row.getString("id"), row.getString("version"),
                row.getString("content"), row.getDouble("score"), row.getString("source"), metadata);
    }

    private static String literal(List<Double> vector) {
        return vector.stream().map(String::valueOf).collect(Collectors.joining(",", "[", "]"));
    }
}

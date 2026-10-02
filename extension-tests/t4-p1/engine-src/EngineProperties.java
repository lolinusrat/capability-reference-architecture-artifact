package com.enterprise.ai.runtime.retrieval.engine;

import java.time.Duration;
import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * Settings for the retrieval engines, bound from {@code runtime.retrieval.engines.*}.
 *
 * <p>The engine itself is selected by {@code runtime.retrieval.engine}
 * ({@code pgvector} or {@code qdrant}); with neither set, no engine is active and
 * the context builder behaves exactly as before.
 */
@ConfigurationProperties(prefix = "runtime.retrieval.engines")
public class EngineProperties {

    /** The Model Services profile used to embed queries. */
    private String embeddingProfile = "enterprise-embeddings";

    private Duration embeddingTimeout = Duration.ofSeconds(5);

    private final PgVector pgvector = new PgVector();

    private final Qdrant qdrant = new Qdrant();

    public String getEmbeddingProfile() {
        return embeddingProfile;
    }

    public void setEmbeddingProfile(String embeddingProfile) {
        this.embeddingProfile = embeddingProfile;
    }

    public Duration getEmbeddingTimeout() {
        return embeddingTimeout;
    }

    public void setEmbeddingTimeout(Duration embeddingTimeout) {
        this.embeddingTimeout = embeddingTimeout;
    }

    public PgVector getPgvector() {
        return pgvector;
    }

    public Qdrant getQdrant() {
        return qdrant;
    }

    /** PostgreSQL with pgvector, reached over JDBC (see PgVectorRetriever). */
    public static class PgVector {
        private String url = "jdbc:postgresql://localhost:5432/knowledge";
        private String username = "knowledge";
        private String password = "";
        private String table = "documents";

        public String getUrl() {
            return url;
        }

        public void setUrl(String url) {
            this.url = url;
        }

        public String getUsername() {
            return username;
        }

        public void setUsername(String username) {
            this.username = username;
        }

        public String getPassword() {
            return password;
        }

        public void setPassword(String password) {
            this.password = password;
        }

        public String getTable() {
            return table;
        }

        public void setTable(String table) {
            this.table = table;
        }
    }

    /** Qdrant, reached over its REST API. */
    public static class Qdrant {
        private String url = "http://localhost:6333";
        private String collection = "documents";

        public String getUrl() {
            return url;
        }

        public void setUrl(String url) {
            this.url = url;
        }

        public String getCollection() {
            return collection;
        }

        public void setCollection(String collection) {
            this.collection = collection;
        }
    }
}

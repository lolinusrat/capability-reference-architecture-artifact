package com.enterprise.ai.runtime.retrieval.engine;

import com.enterprise.ai.runtime.inference.gateway.ModelGatewayClient;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Activates the pgvector engine when {@code runtime.retrieval.engine=pgvector}.
 *
 * <p>Connections are opened by the retriever itself; no connection or data-source
 * bean is exposed, so no other part of the application acquires a database
 * dependency through this engine.
 */
@Configuration(proxyBeanMethods = false)
@ConditionalOnProperty(name = "runtime.retrieval.engine", havingValue = "pgvector")
@EnableConfigurationProperties(EngineProperties.class)
public class PgVectorEngineConfiguration {

    @Bean
    PgVectorRetriever pgVectorRetriever(ModelGatewayClient gateway, EngineProperties properties) {
        return new PgVectorRetriever(properties.getPgvector(), new QueryEmbedder(gateway, properties));
    }
}

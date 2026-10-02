package com.enterprise.ai.runtime.retrieval.engine;

import com.enterprise.ai.runtime.inference.gateway.ModelGatewayClient;
import io.r2dbc.spi.ConnectionFactories;
import io.r2dbc.spi.ConnectionFactory;
import io.r2dbc.spi.ConnectionFactoryOptions;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * Activates the pgvector engine when {@code runtime.retrieval.engine=pgvector}.
 *
 * <p>The connection factory is created here and handed to the retriever rather
 * than exposed as a bean, so no other part of the application acquires a database
 * dependency through this engine.
 */
@Configuration(proxyBeanMethods = false)
@ConditionalOnProperty(name = "runtime.retrieval.engine", havingValue = "pgvector")
@EnableConfigurationProperties(EngineProperties.class)
public class PgVectorEngineConfiguration {

    @Bean
    PgVectorRetriever pgVectorRetriever(ModelGatewayClient gateway, EngineProperties properties) {
        EngineProperties.PgVector settings = properties.getPgvector();
        ConnectionFactory connections = ConnectionFactories.get(ConnectionFactoryOptions.parse(settings.getUrl())
                .mutate()
                .option(ConnectionFactoryOptions.USER, settings.getUsername())
                .option(ConnectionFactoryOptions.PASSWORD, settings.getPassword())
                .build());
        return new PgVectorRetriever(connections, new QueryEmbedder(gateway, properties), settings.getTable());
    }
}

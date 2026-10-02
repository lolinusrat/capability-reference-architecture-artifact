package com.enterprise.ai.runtime.retrieval.engine;

import com.enterprise.ai.runtime.inference.gateway.ModelGatewayClient;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;

/** Activates the Qdrant engine when {@code runtime.retrieval.engine=qdrant}. */
@Configuration(proxyBeanMethods = false)
@ConditionalOnProperty(name = "runtime.retrieval.engine", havingValue = "qdrant")
@EnableConfigurationProperties(EngineProperties.class)
public class QdrantEngineConfiguration {

    @Bean
    QdrantRetriever qdrantRetriever(ModelGatewayClient gateway, EngineProperties properties,
                                    WebClient.Builder builder) {
        EngineProperties.Qdrant settings = properties.getQdrant();
        return new QdrantRetriever(builder.clone().baseUrl(settings.getUrl()).build(),
                new QueryEmbedder(gateway, properties), settings.getCollection());
    }
}

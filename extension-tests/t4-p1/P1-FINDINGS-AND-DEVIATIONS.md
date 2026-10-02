# T4-P1 Findings and Deviations

Recorded as they occurred. The frozen P0 record (`t4.frozen.sha256.md`) is unchanged.

## Finding P1-1 (2 October 2026): an engine's driver broke every deployment through the classpath

**What happened.** The pgvector adapter was first built as frozen decision 2
specified, over R2DBC: `r2dbc-postgresql` was added to `runtime-retrieval/pom.xml`
(a permitted surface), and the adapter's four files were added in the `engine`
package (permitted).

The runtime was then started **with no engine selected**. It **failed to start**:

> Failed to configure a ConnectionFactory: 'url' attribute is not specified and no
> embedded database could be configured. Reason: Failed to determine a suitable
> R2DBC Connection URL

The driver's presence on the classpath activated Spring Boot's R2DBC
auto-configuration and the actuator's R2DBC health contributor, which demanded a
database URL. **A Knowledge Services driver choice therefore broke the
application for every deployment**, including those that never select pgvector.

**Why this matters for the method.** No protected file changed: the build file is
permitted, and the code is in the permitted `engine` package. **The interface
inventory could not have detected this coupling**, because it travels through the
classpath and the framework's auto-configuration, not through any interface file.
This is a blind spot of file-based containment measurement, and it is reported as
such. It parallels T3's packaging finding, from the opposite direction: there, a
needed dependency was absent from the deployable; here, an added dependency changed
the deployable's behaviour globally.

**Evidence:** `r2dbc-attempt/`. It holds the adapter files and build file as first
written, the startup log (and an excerpt with the local path redacted), and the
log's SHA-256.

## Deviation P1-D1: pgvector reached over JDBC instead of R2DBC

**Frozen decision 2 said R2DBC.** Two ways to continue were considered:

| Option | Effect | Chosen? |
|:---|:---|:---|
| Keep R2DBC and exclude Spring Boot's R2DBC auto-configuration from inside the `engine` package, for example with an additional `@EnableAutoConfiguration(exclude = …)`, whose exclusions apply application-wide | Passes the file-based inventory, but **changes application-wide behaviour from inside a component**, hiding exactly the coupling Finding P1-1 exposes | **No** |
| Keep R2DBC and require every deployment to set `spring.autoconfigure.exclude` | Pushes a Knowledge Services choice into every deployment's configuration, including those not using pgvector | **No** |
| **Use the PostgreSQL JDBC driver** (`org.postgresql:postgresql`), with blocking calls on Reactor's bounded-elastic scheduler | The application does not contain `spring-jdbc`, so no JDBC auto-configuration or health contributor activates. The engine's effect stays confined to the adapter. | **Yes** |

**Consequences, stated in advance:**

- the pgvector adapter is blocking I/O moved off the request threads, rather than
  natively reactive;
- the result answers whether the contract can be implemented over pgvector, not
  whether R2DBC is usable.

**What the deviation does not change:** the protocol's failure conditions, surfaces,
assertions and inputs. The startup check is repeated with no engine selected, and
with pgvector selected, before P1 continues.

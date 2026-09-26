# Technology-Substitution Protocol — fixed before the substitution is performed

This file fixes the question, the definition of failure, the surfaces that will
be measured and the reporting rules for the F3 falsification condition
(*technology independence*) **before** the substitution is carried out, so that
the result cannot be shaped by what the substitution turns out to do.

It is a companion to `falsification-assessment.md`, which currently records F3
as **not tested**. If this exercise is run, that entry is replaced by the
outcome reported here. If it is abandoned under §8, the entry stays as it is and
the paper is submitted with its existing disclosure.

**Chronology.** F1 and F2 were formulated *after* the evaluation was carried
out; `falsification-assessment.md` §1 says so, and the paper repeats it in
§11.2. F3 is different: this protocol and the interface inventory it references
are frozen before the substitution. That is a stronger evidentiary position than
the other two conditions enjoy, and the write-up should claim it plainly and
only that far.

## 1 The question

> Does substituting a materially different realization of one capability domain
> require an interface change outside that domain?

This is the test the paper's E2 argument asserts analytically and has not so far
performed:

> for each domain, materially different realizations should be substitutable
> without requiring changes to the interfaces of other capability domains.

## 2 Scope

**One substitution, in one domain: Model Services.**

| | |
|:---|:---|
| **Domain under substitution** | Model Services |
| **Realization A** | `provider-openai` — commercial hosted, `https://api.openai.com/v1` |
| **Realization B** | `provider-ollama` — self-hosted, local runtime |

The two realizations differ in wire format, authentication scheme, deployment
topology and declared capability set. That difference is the point: a
substitution between two realizations of the same vendor API would not test
anything, and neither would one between two OpenAI-compatible endpoints.

**Why Ollama and not vLLM.** `provider-vllm` is also present and also
self-hosted, but vLLM exposes an OpenAI-compatible API. Substituting it exercises
much less of the adapter boundary, and a reader would be right to say the easy
case had been chosen. Ollama carries its own request and response mappers
(`OllamaWire`, `OllamaRequestMapper`, `OllamaResponseMapper`) and its own error
shapes. It is the harder of the two available substitutions and it is the one
used.

**A second substitution was considered and excluded, before running the first.**
Knowledge Services was the candidate: `Cohort Brain` holds both a vector and a
graph retrieval implementation, in `src/retrieval/vector_rag.py` and
`src/retrieval/graph_rag.py`. They do not sit behind a common contract. The two
expose differently named entry points — `answer_question_vector` and
`answer_question` — every caller (`src/ui/app.py`, `src/mcp_server.py`,
`main.py`) imports both by name and selects between them explicitly, and
graph-only operations such as `run_cypher` are imported directly by
`src/mcp_server.py`. Substituting one for the other would therefore require
changing call sites in the consuming code, and there is no pre-existing
interface against which to measure. Introducing one now, for the purpose of the
experiment, would be engineering the test to fit the architecture. The exclusion
is recorded here rather than omitted, so that it cannot later look like a second
attempt that was dropped after it failed.

## 3 What counts as failure

**F3 is met — technology independence fails — if performing the substitution
requires any of the following outside Model Services:**

1. a change to a neighbouring domain's public interface: a type, method
   signature, or field that a consumer in another domain can name;
2. a change to an HTTP contract between domains: route, method, request or
   response schema, status-code semantics;
3. a new or changed **required** configuration key in a neighbouring domain;
4. a change to the error contract: a new error type crossing a domain boundary,
   or a change to the meaning of an existing one.

Any one of these is sufficient. The condition is met at the first instance; it
is not a matter of degree.

## 4 What does not count as failure

These are stated in advance because each is a way the test could be argued into
being unfalsifiable after the fact:

1. **Change inside Model Services.** New or modified code and configuration
   within the gateway — adapters, mappers, credential handling, catalogue
   entries, routing policy, token accounting — is expected and permitted. It is
   reported (§6), not counted against F3.
2. **Capability differences surfaced through the declared mechanism.** The
   `ModelProvider` SPI already declares `ProviderCapabilities` and already
   rejects unimplemented operations with `CapabilityNotSupportedException`. A
   realization that supports less than another, and says so through that
   mechanism, is exercising the contract, not changing it.
3. **Configuration *values*.** Endpoint URLs, model identifiers, credentials and
   deployment ids are expected to differ between realizations. A new *required
   key* in another domain is a failure under §3.3; a different value for an
   existing key is not.
4. **Behavioural and quality differences.** Latency, throughput, cost and answer
   quality will differ between a hosted frontier model and a local one. None of
   these is an architectural result and none is measured here. This is not a
   benchmark.

## 5 The frozen interface inventory

Five surfaces are inventoried — the four neighbouring capability domains that
consume Model Services, and Model Services' own outward-facing contract.

| Surface | Realized by | Files |
|:---|:---|---:|
| Developer Experience | `Enterprise_AI_SDK` `sdk-core/.../ai/api` | 16 |
| AI Runtime | `Enterprise_AI_Runtime_Service` `runtime-api`, `runtime-inference/.../gateway` | 13 |
| Governance and Security | `Enterprise_AI_Guardrail_Service` `guardrail-common` | 34 |
| Evaluation | `Enterprise_AI_Runtime_Service` `runtime-evaluation` | 5 |
| Model Services (outward contract) | `Model_Gateway` `gateway-api`, `gateway-common/.../model`, `gateway-capabilities` | 43 |

`freeze_interface_inventory.py` records a SHA-256 for every file and one
aggregate digest per surface. The pre-substitution run is
`technology-substitution.before.sha256`, whose aggregates are:

```
70fa9a28445347210d1b65f245f04ccb9260655ac5132830058d07c5ec75aef3  Developer Experience
1a32b91abbeb680858ff00116eb00d0fca47a4ba983313c39063e453d6a76cb5  AI Runtime
ba1b34efe900b84b01233f106d62cdaa51d06650ce4d0f0908344a1652c82fff  Governance and Security
46a384c1af348fca0c43180c8d076415b10e2a7b1a4b2275571c3ab9dc1ce503  Evaluation
f60994b09b54b3ba022200a7dd511c1fc99a2a9e3d9e622aa17ead3010d93f3a  Model Services (outward contract)
```

The inventory covers *contract* packages, not implementation packages, and
excludes test sources and build output. The choice of surface is the load-bearing
methodological decision in this protocol: a surface drawn narrowly enough would
be unable to record a failure. These five were selected as the packages a
consumer in another domain can name, and they are fixed here so that the
selection precedes the result.

## 6 Procedure

1. Freeze this protocol and the before-inventory. Record both digests in
   `technology-substitution-frozen.sha256.md`.
2. Stand up realization B locally.
3. Perform the substitution. Record **every** file touched, with its domain.
4. Exercise the platform end to end through the Developer Experience surface —
   not by calling the gateway directly — so that the request crosses the
   Developer Experience → AI Runtime → Model Services boundaries under
   Governance, as a consuming application would. Run the existing integration
   suites against realization B.
5. Re-run `freeze_interface_inventory.py after`. Diff against the
   before-inventory.
6. Run the discrimination case (§7).
7. Write `technology-substitution-results.md`. **That file does not exist until
   this step**; its absence is what shows the protocol preceded the result.

## 7 The discrimination case

A test that cannot distinguish an architecture that holds from one that does not
is not evidence. One case is therefore run deliberately against the grain:
**request embeddings from a realization that does not implement them.**

The pre-registered expectation is that this surfaces as
`CapabilityNotSupportedException` through the already-declared
`ProviderCapabilities` mechanism, propagating to the caller as an existing error
type — a §4.2 non-failure. **If instead it requires a new error type crossing a
domain boundary, a signature change, or a caller-side special case, that is a
§3.1 or §3.4 failure and F3 is met.** Both outcomes are reportable; the second
is the more interesting one and must not be quietly reframed as a limitation.

## 8 Abandonment

The exercise is dropped, and F3 stays "not tested", if realization B cannot be
stood up within a day's work, or if standing it up requires changing a
neighbouring domain *before* the substitution proper begins. The second case is
itself a finding and is reported as one rather than silently absorbed.

## 9 Reporting rules

Two footprints are reported, always both:

- **Cross-boundary change footprint** — files changed outside Model Services.
  The claim rests on this being zero.
- **Within-domain change footprint** — files changed inside Model Services.
  This is expected to be non-zero, and reporting it is what makes the first
  number meaningful.

The claim the results file is permitted to make is:

> implementation change was **confined to the capability boundary**

and not:

> nothing changed.

The paper's F3 row becomes, if the result is clean: *tested on one materially
heterogeneous substitution; no cross-domain interface change observed* — not
*technology independence established*. One substitution in one domain does not
establish a property of ten.

## 10 Threats to validity, stated in advance

**This is a self-instantiation test, not independent validation.** The prototype
platform and the reference architecture were built by the same researcher. The
substitution therefore tests the architecture against an instantiation that was
constructed in the knowledge of it, and a favourable result is partly a
statement about how that instantiation was written. It is weaker evidence than
the 40-cell commercial comparison and the 36-cell documentary study, both of
which use third-party evidence, and the paper must say so where it reports the
result. The intended description is **a controlled self-instantiation test of
technology substitution**.

**One domain, one substitution pair.** E2 asserts substitutability for every
domain. This tests Model Services. It does not generalise, and the write-up must
not imply that it does.

**One researcher.** As with the documentary coding, the person performing the
substitution is the person who decides what counts as a change. §3 and §4 exist
to constrain that judgement in advance, but they do not remove it.

**The protocol was written with a prior about the answer.** Before §3 and §4
were drafted, the prototype repositories were surveyed for vendor coupling
across the four neighbouring domains. That survey found seven files naming a
model vendor at all, six of them in Javadoc — four of which assert the absence
of coupling in as many words — and one executable case, `SecretGuardrail`'s
regexes for detecting leaked API keys, which is an independent dependency on
vendor identity rather than one a substitution would propagate. The substitution
itself has not been performed and no result has been seen, so this protocol is
still frozen in the sense that matters. But the failure definition was not
written in ignorance of how the code was structured, and a reader is entitled to
weigh that. The disclosure is here rather than omitted because the alternative —
presenting §3 as if drawn blind — would misstate how it was arrived at.

**Reproducibility is partial.** The prototype repositories are not included in
this artifact. A reader can verify the recorded digests and change lists for
internal consistency, but cannot re-run the substitution without those
repositories.

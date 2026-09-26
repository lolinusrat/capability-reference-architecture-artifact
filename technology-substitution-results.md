# Technology-Substitution Results — F3

Executed 5 September 2026, against the protocol frozen in
`technology-substitution-protocol.md` (SHA-256
`eaf260db41121e9666ca6d749d43002b888d1a4ec32c2f2a309b4bc55a372c11`). The
protocol was not modified after the substitution began. Every number below is
reported as observed, including the two failures and the two deviations.

## 1 Outcome

> **The pre-registered F3 technology-independence failure condition was NOT
> MET.** Replacing a hosted commercial Model Services realization with a
> materially different self-hosted realization required **one changed file, in
> configuration, inside Model Services**, and **zero interface changes outside
> the domain**.

| | |
|:---|---:|
| **Cross-boundary change footprint** | **0 files** |
| **Within-domain change footprint** | **1 file** (0 Java, 1 YAML) |

The claim this supports is that implementation change was **confined to the
capability boundary** — not that nothing changed. §4 records what did change.

## 2 The realizations

| | Realization A | Realization B |
|:---|:---|:---|
| Deployment | `openai-prod` | `ollama-local` |
| Adapter | `provider-openai` | `provider-ollama` |
| Wire protocol | `openai-chat-completions` | `ollama-chat` |
| Endpoint | `https://api.openai.com/v1`, hosted | `http://localhost:11434`, self-hosted |
| Credential | API key, `Authorization` header | none |

Realization B identity, recorded for reproducibility: **Ollama 0.32.3**, model
**`llama3.2:1b`**, digest `baf6a787fdff`, 1.2B parameters, quantization `Q8_0`.
The model was chosen to be small and ordinary. Model quality is not the
independent variable and was not measured.

`provider-vllm` was available and rejected in the protocol as the easier case,
because vLLM is OpenAI-compatible. That judgement was borne out incidentally:
the gateway reports `vllm` and `openai` as sharing one wire protocol
(`openai-chat-completions`), while `ollama` has its own (`ollama-chat`).

## 3 Baseline

Realization A, before substitution: **170 tests, 0 failures, 0 errors**
(`mvn test`, whole gateway reactor, Java 21.0.12).

**Deviation 1 — realization A was never invoked live.** No OpenAI credential was
available in the environment. A's evidence is therefore its contract and
integration tests, which stub the upstream at the wire level, not a live call to
`api.openai.com`. B was exercised live. The asymmetry is recorded because it
weakens the "same suite passes against both, both live" claim to "same suite
passes against both, one live".

## 4 The substitution

The complete change footprint is one file,
`Model_Gateway/gateway-api/src/main/resources/application.yml`:

1. `openai-prod` and `anthropic-prod` set `enabled: false`.
2. `ollama-local` set `enabled: true`.
3. The `enterprise-chat` profile's routes replaced with a single `ollama-local`
   route on `llama3.2:1b`, with its declared capability set and context window.
4. Price entries added for the self-hosted routes (see §4.1).

No Java file was created, deleted or modified in any module, in any repository.

### 4.1 A within-domain failure, caught by the domain's own invariant

The first build after the substitution **failed**: 152 tests ran and
`ContextLoadTest.enabledRoutesArePriced` failed with *"price for
vllm/text-embedding-3-large"*. The gateway asserts that every enabled route's
model has a catalogued price, because an unpriced model does not fail a request
— it silently reports zero spend.

This is a real consequence of realization heterogeneity: **a self-hosted
realization has no per-token vendor price, and the catalogue distinguishes
"free" from "unpriced".** It was resolved inside Model Services by adding
explicit zero-cost entries, so that a self-hosted route reports zero spend by
declaration rather than by omission. Under protocol §4.1 this is a permitted
within-domain change; it is reported rather than absorbed because it is the most
interesting thing the substitution surfaced.

After the fix: **170 tests, 0 failures, 0 errors** — the same count as baseline.

## 5 Live invocation under realization B

`POST /internal/chat`, profile `enterprise-chat`:

```json
{"content":[{"type":"text","text":"SUBSTITUTION OK"}],
 "modelProfile":"enterprise-chat","provider":"ollama","deployment":"ollama-local",
 "model":"llama3.2:1b","finishReason":"STOP",
 "usage":{"inputTokens":33,"outputTokens":5,"totalTokens":38},
 "cost":{"totalCost":0E-10,"currency":"USD"},
 "latencyMillis":1369,"attempts":1,
 "routingTrail":[{"provider":"ollama","outcome":"SUCCESS"}]}
```

The response envelope, usage normalisation, cost record and routing trail are
the same structures the contract defines for any provider. The caller names a
logical profile; the wire protocol has no field in which a provider or vendor
model could be named, which is where technology independence is enforced rather
than merely asserted.

## 6 Interface inventory

`freeze_interface_inventory.py after` was run and diffed against the frozen
before-inventory. **All five surface aggregates are byte-identical**, across 111
interface files:

```
70fa9a28…  Developer Experience              (16 files)   unchanged
1a32b91a…  AI Runtime                        (13 files)   unchanged
ba1b34ef…  Governance and Security           (34 files)   unchanged
46a384c1…  Evaluation                        ( 5 files)   unchanged
f60994b0…  Model Services (outward contract) (43 files)   unchanged
```

Independently, a filesystem check over the four neighbouring repositories found
**0 files modified** since the freeze, and exactly one modified file inside
`Model_Gateway` excluding build output — the configuration file of §4.

Neighbouring test suites, re-run after the substitution:

| Domain | Result |
|:---|:---|
| Developer Experience (`Enterprise_AI_SDK`) | 94 tests, 0 failures |
| AI Runtime (`Enterprise_AI_Runtime_Service`) | 596 tests, 0 failures |
| Governance and Security (`Enterprise_AI_Guardrail_Service`) | compiles clean; **the repository contains no tests**, so this surface rests on compilation and the unchanged inventory alone |

## 7 Discrimination case

The protocol required requesting embeddings from a realization that does not
implement them, and pre-registered the expected outcome as rejection through the
declared capability mechanism rather than an interface change.

It took **three attempts to isolate capability from reachability**, and the two
failed attempts are the reason the result means anything — they show the
mechanism returns *different, distinguishable* errors for different causes:

| Attempt | Configuration | Result |
|:---|:---|:---|
| 1 | `vllm-internal` at an unresolvable host | `provider_unavailable`, HTTP 503 — **reachability**, not capability |
| 2 | `vllm-internal` at a reachable endpoint | `provider_error`, HTTP 502, upstream 404 — **model absence**; the vllm adapter inherits embeddings from `OpenAICompatibleProvider`, so it is not capability-less |
| 3 | `anthropic-prod` at a reachable endpoint, which declares no `embeddings` | `model_not_found`, HTTP 404, *"no enabled deployment of this profile does embeddings"* |

Attempt 3 is the discrimination case proper. The request was **rejected at
admission, before any provider was dialled**, through an existing error type on
the existing contract. No new error type crossed a domain boundary, no signature
changed, and no caller-side special case was required. Under protocol §4.2 this
is a non-failure.

The authoritative capability declarations were read from the running gateway's
`/internal/providers`: `anthropic` and `bedrock` declare no embeddings; the other
five do. This corrected an earlier assumption, made from source inspection, that
`vllm` lacked them — it inherits them.

## 8 Deviations from the protocol

**Deviation 1 — no live invocation of realization A.** §3 above.

**Deviation 2 — §6.4 was not satisfied.** The protocol required the platform to
be exercised end to end *through the Developer Experience surface*, so that a
request crosses Developer Experience → AI Runtime → Model Services. The Runtime
Service was built, started against the live gateway, and confirmed healthy, but
every request was refused by its own governance layer — first
`policy_violation` (*"model profile 'enterprise-chat' is not published to this
environment"*), then `prompt_not_found` for each configured prompt id. This is a
local provisioning gap in the Runtime Service's standalone configuration. It is
**not attributable to the substitution**: realization A would meet the identical
gate.

The refusals could have been cleared by editing the Runtime Service's
configuration. That was declined, because doing so would have placed a file in
the cross-boundary change footprint that the experiment exists to measure. The
end-to-end path was therefore verified at the Model Services contract directly,
and the AI Runtime boundary is evidenced by its 596 passing tests and by the
service running against the live gateway — not by a completed request. A future
run should provision the runtime's tenant and prompt bindings *before* freezing,
so that §6.4 can be met without touching a neighbouring domain during the
experiment.

## 9 What this does and does not establish

**Establishes.** Under a failure criterion fixed before the substitution, one
materially heterogeneous substitution of the Model Services realization —
different wire protocol, different authentication, different deployment topology
— propagated no interface change into the four neighbouring capability domains
that consume it, and the capability difference it did expose was absorbed by the
existing declaration and error mechanisms.

**Does not establish.** That technology independence holds for the other nine
domains; E2 asserts it for all ten and one substitution tests one. That it holds
for substitutions other than this pair. That the architecture would survive a
substitution in an instantiation built by someone else.

**This is a controlled self-instantiation test, not independent validation.** The
prototype platform and the reference architecture were built by the same
researcher, so a favourable result is partly a statement about how that
instantiation was written. It is weaker evidence than the 40-cell commercial
comparison and the 36-cell documentary study, both of which rest on third-party
evidence. The manuscript must say so where it reports this result.

**Reproducibility is partial.** The prototype repositories are not part of this
artifact. The digests, change lists, test counts and transcripts above are
internally checkable; re-running the substitution requires the repositories.

## 10 Revision to `falsification-assessment.md`

The F3 row becomes:

| Condition | Evidence | Outcome |
|:---|:---|:---|
| **F3** Technology independence | one substitution, `provider-openai` → `provider-ollama`, against a criterion frozen beforehand | **Not met** — 0 cross-boundary interface changes; 1 within-domain configuration change; one capability difference absorbed by the declared mechanism |

## 11 Screening for a second substitution (performed after this experiment)

Recorded because a reader is entitled to know whether a single substitution
reflects a limit of the architecture, of this instantiation, or of effort. It
reflects the instantiation.

The protocol's conditions for a substitution candidate are: **(a)** a contract
that existed before the experiment was contemplated, **(b)** at least two
realizations that deliver the same capability through it, and **(c)** consumers
that name only the contract. Model Services met all three. Three further
candidates were examined after the F3 result was recorded. None did.

| Candidate | Contract | Realizations | Outcome |
|:---|:---|:---|:---|
| Retrieval in the separate research application | None; callers import each implementation by name | Vector and graph retrieval | Excluded **before** the experiment (protocol §2) |
| `Retriever` SPI, AI Runtime | Pre-existing SPI | **None** | Excluded: the contract has no realizations behind it |
| `GuardrailExecutor` SPI, AI Runtime | Pre-existing SPI | Remote service client; local heuristic | Excluded; see below |

**Record clarification (25 September 2026).** The sentence above stating that
all three further candidates were examined after the F3 result was recorded is
inaccurate. As the table records, the first candidate was excluded before the
experiment (protocol §2); the other two were examined after the F3 result was
recorded. This corrects the chronology only; it does not change the screening
outcome or the F3 result.

### 11.1 Why the guardrail candidate was excluded

Two reasons, either sufficient on its own.

**The second realization is a declared development fixture, not a comparable
realization of the same capability.** Its constructor logs that it "is a
development fixture, not a security control"; its detection patterns carry the
comment "Crude, and known to be crude"; and four of the checks the contract
admits — content policy, hallucination, citation validation and content safety —
are not implemented, because they require a model. Substituting it would not hold
the capability constant while changing the technology. It would narrow what the
guardrail can decide. F3 asks whether a boundary confines technology-specific
change, which presupposes the same capability on both sides of the substitution.

**The outcome would be structurally predetermined rather than measured.** Both
realizations are produced by a single factory method in
`RuntimeGuardrailConfiguration`, selected by whether one configuration property
is set. No consuming code names either realization, so no neighbouring interface
*could* change, whatever the substitution did. An experiment whose favourable
outcome is guaranteed by its own selection mechanism measures nothing.

The rule classes inside the Guardrail Service — four `GuardrailRule`, three
`InputGuardrail`, five `OutputGuardrail` implementations — are composed checks
that run together, not interchangeable realizations of one capability, so they
are not substitution candidates either.

### 11.2 What a valid second substitution would require

A capability boundary satisfying (a), (b) and (c) above. No domain in the present
instantiation other than Model Services does. Constructing one now would satisfy
the letter of the criteria and defeat their purpose, for the reason protocol §2
gives for the first exclusion: a contract introduced for the experiment measures
the experiment, not the architecture.

This screening was performed after the experiment reported above and is recorded
here, outside the frozen protocol, so that it cannot be read as having been part
of the pre-registered design.


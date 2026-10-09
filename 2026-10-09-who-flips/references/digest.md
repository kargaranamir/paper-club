# Evidence digest: Who Flips?

Primary source: [arXiv:2606.16011v2](https://arxiv.org/abs/2606.16011v2), revised 30 August 2026. Read against the PDF and LaTeX source. This deck reports published values; it does not rerun the inference experiments.

Paper: *Who Flips? Self- and Cross-Model Counterarguments Reveal Answer Instability in LLMs*. Author details are available through the linked paper.

Links: [PDF](https://arxiv.org/pdf/2606.16011v2), [source](https://arxiv.org/src/2606.16011v2), [code](https://github.com/nafisenik/WhoFlips), [data](https://huggingface.co/datasets/nafisehNik/WhoFlips).

## Source snapshot

- Retrieved 9 October 2026. Unversioned PDF/source URLs resolved to v2, verified from PDF title page and current arXiv metadata.
- Original PDF SHA-256: `6e3b0d776ae33e60723a6b270cb226b37ed60bd2becf3e4a1fab62780e40f403`.
- Source archive SHA-256: `7a35e96db7754571c41f413c707b399d9cc492e5af4011f74c71edfca84eb70a`.
- Numbers below use v2 table/figure numbering. The older v1 HTML has a different ordering.

## Protocol and experimental setup (§§3–4, Appendix A)

- Stage I generates a committed k-sentence argument for a specified wrong option in an isolated session. A fixed refusal marker excludes unsuccessful generation attempts.
- Stage II uses a fresh target session. Retain initially correct answers, show a generated wrong argument, then score whether the final answer is incorrect. Any incorrect final choice counts, not only the defended choice.
- AFR = P(final incorrect | initial correct and argument exists). Blind: same source anonymously. Self: same source with explicit prior-self attribution. Cross: a different source anonymously.
- 2,052 MMLU questions, 57 subjects, seven models, three wrong options, k in {1, 3, 5, 10}. Same-source blind/self use all k. Cross uses blind k = 10 only.
- Temperature 0, reasoning modes disabled. Open-weight models served via vLLM; closed model via API.
- Unless stated otherwise: 95% confidence intervals, 2,000 question-cluster bootstrap replicates. ± below is a reported CI half-width, in percentage points.
- Illustrative exhaustive cost exceeds 1.7 million calls at p_b = p_c = .8; implemented study exceeds 500K calls (Limitations). These are reported costs, not runs performed for this deck.

## Model identifiers (Table 1)

| label | identifier |
| --- | --- |
| Llama-3.1-8B | llama-3.1-8b-instruct |
| Llama-3.3-70B | llama-3.3-70b-instruct |
| Qwen3.5-4B | qwen3.5-4b |
| Qwen3.5-9B | qwen3.5-9b |
| GPT-5.1 | gpt-5.1 |
| Gemma-4-26B | gemma-4-26b-a4b-it |
| Qwen3.5-35B | qwen3.5-35b-a3b |

## Blind AFR (Table 2)

| model | k=1 | k=3 | k=5 | k=10 | mean | coverage | k10-k1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Llama-3.1-8B | 97.1 ± 0.9 | 97.5 ± 0.9 | 97.7 ± 0.9 | 96.8 ± 1.1 | 97.3 ± 0.5 | 59% | -0.3 pp |
| Llama-3.3-70B | 76.6 ± 2.1 | 69.6 ± 2.4 | 76.3 ± 2.0 | 79.3 ± 2.0 | 75.8 ± 1.7 | 80% | +2.7 pp |
| Qwen3.5-4B | 61.4 ± 2.3 | 61.6 ± 2.4 | 62.1 ± 2.3 | 71.9 ± 2.2 | 64.3 ± 1.9 | 78% | +10.5 pp |
| Qwen3.5-9B | 36.3 ± 2.3 | 36.0 ± 2.4 | 39.2 ± 2.2 | 45.8 ± 2.2 | 39.3 ± 1.9 | 81% | +9.5 pp |
| GPT-5.1 | 25.1 ± 2.0 | 24.0 ± 1.9 | 23.3 ± 1.8 | 21.3 ± 1.9 | 23.4 ± 1.8 | 89% | -3.8 pp |
| Gemma-4-26B | 23.4 ± 2.0 | 24.3 ± 2.1 | 23.8 ± 2.0 | 20.7 ± 1.9 | 23.0 ± 1.6 | 87% | -2.7 pp |
| Qwen3.5-35B | 19.1 ± 2.0 | 18.2 ± 1.8 | 17.1 ± 1.7 | 15.7 ± 1.6 | 17.5 ± 1.4 | 83% | -3.4 pp |

Reported across-model means by k: 48.4, 47.3, 48.5, 50.2%. Overall mean: 48.7%. Coverage mean: 80%. Coverage describes eligible questions, not baseline accuracy.

## Self-attribution (Table 3)

| model | blind AFR | self AFR | reported SAD | p |
| --- | --- | --- | --- | --- |
| Llama-3.1-8B | 97.3 | 97.8 | +0.5 ± 0.4 | <.05 |
| Llama-3.3-70B | 75.8 | 80.4 | +4.6 ± 0.9 | <.001 |
| Qwen3.5-4B | 64.3 | 83.0 | +18.7 ± 1.4 | <.001 |
| Qwen3.5-9B | 39.3 | 54.3 | +15.0 ± 1.4 | <.001 |
| GPT-5.1 | 23.4 | 30.4 | +7.0 ± 0.9 | <.001 |
| Gemma-4-26B | 23.0 | 24.0 | +0.9 ± 0.9 | <.05 |
| Qwen3.5-35B | 17.5 | 20.3 | +2.9 ± 0.9 | <.001 |

Reported means: blind 48.7%, self 55.7%, SAD +7.1 pp.

## Refusal (Table 4)

| model | CRR | CRR correct | CRR incorrect | RSS (pp) | AFR blind+self |
| --- | --- | --- | --- | --- | --- |
| Llama-3.1-8B | 41.3 | 40.5 | 43.3 | -2.9 | 97.5 |
| Llama-3.3-70B | 17.1 | 17.1 | 17.1 | +0.0 | 78.1 |
| Qwen3.5-4B | 11.0 | 12.3 | 6.1 | +6.2 | 73.7 |
| Qwen3.5-9B | 5.3 | 5.4 | 4.9 | +0.5 | 46.8 |
| GPT-5.1 | 0.1 | 0.1 | 0.0 | +0.1 | 26.9 |
| Gemma-4-26B | 4.6 | 5.0 | 2.0 | +3.0 | 23.5 |
| Qwen3.5-35B | 13.1 | 14.0 | 8.1 | +5.9 | 18.9 |

Reported means: CRR 13.2%, CRR correct 13.5%, CRR incorrect 11.6%, RSS +1.8 pp, AFR blind+self 52.2%.

## Linguistic correlates (§5.4, Figure 2, Appendix B)

- Flipped responses contain roughly 6x as many capitulation markers; held responses more resistance phrases.
- Held responses are about 1,800 versus 1,150 characters after challenge.
- Before challenge, higher baseline hedge density and longer baseline responses associate with later flips.
- Held items associate with higher coercion-argument confidence, complicating a monotonic confidence account.
- The authors report item-level p < .005 for the described differences. Manually curated lexicons and case-insensitive substring matching yield descriptive correlates, not causal explanations.

## Subject extremes (Table 5)

| group | subject | AFR ± CI | category |
| --- | --- | --- | --- |
| highest | Moral disputes | 80.8 ± 2.1 | Humanities |
| highest | Security studies | 80.6 ± 2.1 | Social Sci. |
| highest | Professional law | 74.7 ± 2.4 | Humanities |
| highest | Moral scenarios | 74.1 ± 2.3 | Humanities |
| highest | Human aging | 72.1 ± 2.3 | Health |
| highest | Virology | 69.2 ± 2.7 | Health |
| highest | Public relations | 66.4 ± 2.6 | Social Sci. |
| highest | Jurisprudence | 63.3 ± 2.3 | Humanities |
| highest | Global facts | 62.6 ± 2.9 | Other |
| highest | Econometrics | 59.2 ± 2.6 | Social Sci. |
| lowest | HS government and politics | 38.4 ± 2.2 | Social Sci. |
| lowest | HS computer science | 38.3 ± 2.2 | STEM |
| lowest | HS physics | 36.1 ± 2.4 | STEM |
| lowest | Abstract algebra | 34.9 ± 2.6 | STEM |
| lowest | Conceptual physics | 34.2 ± 2.2 | STEM |
| lowest | Miscellaneous | 34.1 ± 2.3 | Other |
| lowest | College physics | 32.6 ± 2.2 | STEM |
| lowest | College mathematics | 30.4 ± 2.6 | STEM |
| lowest | HS mathematics | 25.8 ± 2.2 | STEM |
| lowest | Elementary mathematics | 20.9 ± 1.9 | STEM |

Subject results average across models, lengths and attribution conditions. Figure 3 reports a positive subject-level association between coercion success and AFR; no causal coefficient is inferred here.

## Cross vs same source, blind k=10 (Table 6)

| target | same source | cross average | reported change ± CI |
| --- | --- | --- | --- |
| Llama-3.1-8B | 96.8 | 99.0 | +2.2 ± 1.1 |
| Llama-3.3-70B | 79.3 | 83.3 | +4.0 ± 2.2 |
| Qwen3.5-4B | 71.9 | 61.7 | -10.2 ± 2.8 |
| Qwen3.5-9B | 45.8 | 48.8 | +3.0 ± 2.9 |
| GPT-5.1 | 21.3 | 15.5 | -5.8 ± 2.4 |
| Gemma-4-26B | 20.7 | 18.1 | -2.6 ± 2.4 |
| Qwen3.5-35B | 15.7 | 13.6 | -2.1 ± 2.1 |

Means: 50.2% same-source, 48.6% cross-source, -1.6 pp difference. Qwen-35B change not significant; Qwen-9B and Gemma p < .05; other deltas p < .001.

## Rounded cross matrix (Figure 4)

| source / target | GPT-5.1 | Gemma-4-26B | Llama-3.1-8B | Llama-3.3-70B | Qwen3.5-35B | Qwen3.5-4B | Qwen3.5-9B |
| --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-5.1 | 21 | 30 | 100 | 94 | 22 | 71 | 62 |
| Gemma-4-26B | 17 | 21 | 100 | 89 | 16 | 72 | 54 |
| Llama-3.1-8B | 11 | 6 | 97 | 57 | 6 | 36 | 25 |
| Llama-3.3-70B | 16 | 14 | 99 | 79 | 11 | 56 | 44 |
| Qwen3.5-35B | 17 | 21 | 98 | 87 | 16 | 71 | 51 |
| Qwen3.5-4B | 16 | 17 | 98 | 85 | 14 | 72 | 51 |
| Qwen3.5-9B | 15 | 18 | 99 | 82 | 11 | 57 | 46 |

Values are whole percentages transcribed from the source PDF figure. Diagonal: same-source blind. Other cells: cross. The deck recolors by absolute AFR rather than the paper’s delta color scale. Do not substitute rounded-cell averages for Table 6.

## Variance and source/target roles (§5.6, Figure 5)

- Target susceptibility: 76.7% of reported total variance, 95% CI [74.8, 78.7]. Source: 12.0% [10.1, 14.5]. Subject: 9.3% [9.2, 13.6]. The listed components sum to 98.0%; no remainder label is inferred.
- EP averages off-diagonal column values (target susceptibility). EA averages off-diagonal row values (source efficacy). These are behavioral summaries, not measures of factual authority.
- Paper describes GPT, Qwen-35B and Gemma as strong exporters. Llama-8B has rounded EP 99%, EA 24%. The deck reproduces the vector marker positions from Figure 5; extraction provenance is recorded separately.

## MaxFlip (Table 7)

| model | standard AFR | curated AFR | reported gain ± CI | producer share |
| --- | --- | --- | --- | --- |
| Llama-3.1-8B | 96.8 | 99.9 | +3.1 ± 1.1 | 3.7% |
| Llama-3.3-70B | 79.3 | 94.1 | +14.8 ± 2.1 | 8.8% |
| Qwen3.5-4B | 71.9 | 84.0 | +12.1 ± 2.8 | 13.9% |
| Qwen3.5-9B | 45.8 | 69.4 | +23.6 ± 3.2 | 7.9% |
| GPT-5.1 | 21.3 | 23.6 | +2.4 ± 2.8 | 24.4% |
| Gemma-4-26B | 20.7 | 31.2 | +10.5 ± 2.9 | 21.5% |
| Qwen3.5-35B | 15.7 | 28.1 | +12.4 ± 2.8 | 15.9% |

Standard = same-source blind k=10. Mean AFR 50.2% to 61.5%, reported mean gain +11.3 pp. GPT +2.4 ± 2.8 pp is not significant; other gains p < .001.

MaxFlip (§5.7) chooses one argument per question from the cross-model pool, maximizing the number of baseline models flipped, with random tie-breaking. The deck flags that selection and evaluation use the observed pool; transfer to unseen targets requires a separate evaluation.

## Source audit and interpretation

1. Table 2 mean at k=3 is 47.3%, outside the prose’s stated 48.4–50.2 range. Use all four table values.
2. Table 2 Llama-70B varies from 69.6 to 79.3 (9.7 pp). Thus “below 4 pp for five of seven” is inconsistent with full within-model ranges; four models have ranges below 4 pp.
3. Table 5 lists eight STEM subjects in the lowest ten, whereas §5.5 says nine. Its extremes differ by 59.9 pp using printed values, rather than strictly more than 60.
4. Figure 4 Llama-70B target column spans 57–94% (37 pp), inconsistent with §5.6’s claim of all column ranges at most 10 pp. Qwen-4B also has a large column range.
5. Table 7 producer shares sum to 96.1%. No unexplained 3.9% category is invented and no normalization is applied.
6. Preserve the reported deltas rather than subtract rounded endpoints: Gemma SAD 0.9 vs displayed endpoint difference 1.0, Qwen-35B SAD 2.9 vs 2.8, GPT MaxFlip 2.4 vs 2.3. Small discrepancies can arise from rounding.
7. Table 6 Gemma cross average is 18.1%, whereas the EP prose uses a bound of at most 18%. Avoid that exact bound.
8. Conditional AFR describes eligible challenges. Conditioning does not by itself establish a lower bound on unconditional vulnerability or eliminate selection effects. Common-subset checks are a proposed follow-up.
9. “Self-source” is not “self-attributed.” Tables 6 and 7 use same-source blind k=10 as their baseline.
10. Do not infer causal effects from lexical associations or subject categories; do not interpret target/source variance shares as causal shares of individual errors.

## Limitations and follow-up

Authors: MMLU only, a single challenge, no tested mitigation, no incorrect-to-correct experiment; other languages, human arguments and open-ended tasks remain outside scope. Reasoning modes were disabled. Reviewer proposals: held-out target selection for MaxFlip, valid-correction controls, explicit verification and common eligible subsets.

## Slide map

1. title
2. toy-example
3. two-stage-protocol
4. afr-denominator
5. blind-afr
6. argument-length
7. self-attribution
8. subject-domains
9. two-roles
10. cross-matrix
11. source-and-target-roles
12. cross-vs-same
13. maxflip-selection
14. maxflip-results
15. maxflip-producers
16. refusal-vs-resistance
17. limitations
18. held-out-transfer
19. balanced-revision
20. takeaways
21. experimental-setup (backup)
22. three-conditions (backup)
23. all-model-lengths (backup)
24. coverage-and-ci (backup)
25. model-scale (backup)
26. linguistic-correlates (backup)
27. variance-decomposition (backup)
28. source-audit (backup)

## Revised Excalidraw presentation

The main talk has 20 slides plus eight backups. It uses point-and-interval charts, model trajectories, a sequential cross-model matrix, role comparisons and editable protocol/selection diagrams. Source values and confidence intervals are preserved. The MaxFlip schematic uses explicitly illustrative candidates and outcomes.

The source/target plot reproduces Figure 5 positions recovered from the original vector PDF, using tick locations to calibrate marker centers. See [ea-ep-provenance.json](ea-ep-provenance.json). These are graphical reconstructions, not new raw-data estimates. They replace the previous approximation that averaged Figure 4's rounded whole-percent cells. The original figure, Table 6 and rounded-cell means are kept distinct.

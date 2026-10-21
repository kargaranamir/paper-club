# Numbers used in the slides, with their sources

Source: Yuhan Zhu, Xiangyu Zeng, … Limin Wang. *VideoJev: System One Model for Video Understanding and
Interaction.* arXiv:2610.18615v1 (13 Oct 2026). Read from the arXiv HTML version (via the Hugging Face papers
mirror); ablation tables 3, 5–8 from arxiv.org/html/2610.18615. Code: github.com/MCG-NJU/VideoJev.
Affiliations: NJU, JD.com, UCAS, THU, XMU, SJTU, USTC, FDU (corresponding: Limin Wang).

## Background: System One and Jev
- Jev (TypeSafe AI, refs [2], [38]): "typed probabilistic judgments that software can use directly, without
  generating answers token by token" (paper §1). From the TypeSafe blog: named after Kahneman's System 1 /
  System 2 and after the economist Jevons; trained with "Reinforcement Learning for Calibrated Decisions";
  vendor claims 70–500 ms per decision. Image versions: Visual Jev [48], PixelJev [58].
- VideoJev §3.5: "Jev explicitly optimizes [calibration] through reinforcement learning; VideoJev receives no
  calibration-specific training."

## Method (§2)
- Backbones: Qwen3.5-4B (dense) and Qwen3.6-35B-A3B (MoE, 3B active).
- Remove the final MLP; replace the LM head by a candidate scorer. New tokens <|option_end|> (one per candidate)
  and <|decide|> (one per query), both initialised from <|im_end|>.
- Eq. 1: u = norm(W_q h_d + b_q), v_i = norm(W_k h_i + b_k), 512-d; s_i = 10 · uᵀv_i + b (b learned).
- Input order: video tokens → task instruction → query → candidates (each ends with <|option_end|>) → <|decide|>.
- Grounding: one candidate per frame pair (twofold temporal compression), timestamp text copied from the video
  prefix; label y_i = 1 if the pair's mean timestamp t_i is inside the annotated event; p_i = sigmoid(s_i);
  multi-label BCE (Eq. 2) + soft IoU, duration-weighted (Eq. 3).
- Decoding (Eq. 4): maximise Σ [s_i − log(τ/(1−τ))] over contiguous ranges (Kadane, O(K)); τ = 0.25, smoothing
  window 1, fixed for all experiments. If all adjusted logits are negative: interval of the best candidate.
- QA: softmax over option logits, cross-entropy (Eq. 5); answer-independent option permutation in training.
- Cached inference: encode + prefill the video once, each query branches from the cached prefix.
  Joint inference: all queries (each with its own <|decide|>) after one prefix, one causal forward; standard
  causal attention (no custom mask), later queries see earlier queries and candidates but no answers.
- Training data: TimeLens-100K + TimeLens2-93K (grounding); internally curated ~240K multiple-choice questions
  over 19K videos (4 min to nearly 2 h; 4–5 options).
- Two stages: (1) head only, backbone and marker embeddings frozen, 30% of videos, BCE / CE, 160 updates;
  (2) backbone + markers + head on the other 70%, BCE + 2·SoftIoU / CE, 375 updates. Vision encoder and merger
  frozen. 64 H200 GPUs, BF16, global batch 64 packed sequences, 2 fps, 144K-token sequences.
  Head LR 3e-4 (stage 1), 1e-4 (stage 2); backbone LR 5e-6 (4B), 2e-6 (35B-A3B).

## README demo (VideoJev-4B, 10-second video "eating spaghetti", query "The woman in green eats pasta.")
- Grounding probabilities: 0.0058, 0.0109, 0.0261, 0.9046, 0.9880, 0.9888, 0.9896, 0.9849, 0.8335, 0.3304
  → interval [3.0, 10.0] s with the default threshold 0.25.
- QA "What is the woman in green eating?" A. Pasta 0.99992, B. Rice 0.00006, C. Soup 0.00003.

## Table 1, temporal grounding (mean mIoU over Charades-TL / ActivityNet-TL / QVHighlights-TL; latency s/query)
| model | latency | Charades mIoU | ActivityNet mIoU | QVHighlights mIoU | Avg |
|---|---|---|---|---|---|
| GPT-5 | – | 40.5 | 42.9 | 56.8 | 46.7 |
| Gemini-2.5-Pro | – | 52.8 | 58.1 | 70.4 | 60.4 |
| Molmo2-4B | 0.636 | 34.7 | 40.9 | 60.8 | 45.5 |
| Qwen3-VL-4B | 0.703 | 49.4 | 50.7 | 62.3 | 54.1 |
| Mage-VL | 1.437 | 55.0 | 51.6 | 63.4 | 56.7 |
| Qwen3.5-4B | 0.763 | 52.3 | 55.6 | 67.9 | 58.6 |
| VideoChat3-4B | 1.067 | 56.1 | 54.6 | 67.0 | 59.2 |
| Video-ORA-4B | 2.347 | 56.8 | 57.3 | 67.5 | 60.5 |
| TimeLens2-4B | 0.646 | 57.7 | 59.0 | 69.3 | 62.0 |
| **VideoJev-4B** | **0.276** | 60.1 | 62.8 | 73.2 | **65.3** |
| Nemotron-3-Nano-Omni-30B-A3B | 3.882 | 45.3 | 40.6 | 52.6 | 46.2 |
| Qwen3-VL-30B-A3B | 1.055 | 48.1 | 49.4 | 63.2 | 53.6 |
| Qwen3.5-35B-A3B | 1.021 | 46.0 | 54.4 | 64.3 | 54.9 |
| Qwen3.6-35B-A3B | 1.054 | 47.3 | 56.0 | 67.5 | 56.9 |
| **VideoJev-35B-A3B** | **0.336** | 63.7 | 65.5 | 74.0 | **67.7** |
R1@0.7 (Charades/ActivityNet/QVH): TimeLens2-4B 37.5/47.2/60.0; VideoJev-4B 40.3/51.4/64.8.
Latency: full Charades test (1,313 videos, 3,363 queries), one H200, batch 1, model forward time only.

## Table 2, multiple-choice video QA (accuracy; MLVU M-Avg; latency s/question on full LVBench)
| model | latency | LVBench | Video-MME | LongVideoBench | MLVU | Avg |
|---|---|---|---|---|---|---|
| Molmo2-4B | 0.748 | 53.9 | 69.6 | 68.0 | 74.3 | 66.5 |
| VideoChat3-4B | 1.210 | 56.7 | 70.1 | 64.1 | 73.8 | 66.2 |
| Qwen3-VL-4B Instruct | 3.012 | 56.2 | 69.3 | 66.5 | 75.3 | 66.8 |
| Qwen3-VL-4B Thinking | 19.713 | 53.5 | 68.9 | 63.4 | 75.7 | 65.4 |
| Qwen3.5-4B Instruct | 1.355 | 60.0 | 70.6 | 61.2 | 73.3 | 66.3 |
| Qwen3.5-4B Thinking | 144.929 | 66.4 | 76.9 | 73.6 | 82.8 | 74.9 |
| **VideoJev-4B** | **1.123** | 67.9 | 75.0 | 73.6 | 80.6 | **74.3** |
| Nemotron-30B-A3B Instruct | 1.106 | 54.9 | 70.8 | 67.5 | 77.2 | 67.6 |
| Nemotron-30B-A3B Thinking | 229.095 | 52.2 | 72.2 | 69.6 | 79.6 | 68.4 |
| Qwen3-VL-30B-A3B Instruct | 4.817 | 62.5 | 74.5 | 70.9 | 81.3 | 72.3 |
| Qwen3-VL-30B-A3B Thinking | 9.637 | 59.2 | 73.3 | 69.1 | 78.9 | 70.1 |
| Qwen3.5-35B-A3B Instruct | 1.683 | 58.8 | 74.4 | 65.7 | 77.4 | 69.1 |
| Qwen3.5-35B-A3B Thinking | 164.730 | 71.4 | 82.5 | 74.5 | 85.6 | 78.5 |
| Qwen3.6-35B-A3B Instruct | 2.379 | 66.0 | 77.1 | 72.4 | 79.5 | 73.8 |
| Qwen3.6-35B-A3B Thinking | 149.777 | 71.4 | 82.5 | 74.9 | 86.2 | 78.8 |
| **VideoJev-35B-A3B** | **1.493** | 73.4 | 81.8 | 77.1 | 85.9 | **79.5** |
Speedups over Thinking: 144.929 / 1.123 = 129×; 149.777 / 1.493 = 100×. Latency: full LVBench test
(103 videos, 1,549 questions). Inputs: frames only, no subtitles or audio.

## Ablations (VideoJev-4B unless noted; grounding avg mIoU / QA avg)
- Table 3, same data, single stage: VideoJev-4B 65.4 / 74.7; autoregressive Qwen3.5-4B SFT 64.1 / 72.8
  (−1.3 / −1.9). Per benchmark AR: Charades 61.0 (+0.4), ActivityNet 61.3, QVH 70.0, LVBench 66.9, Video-MME
  74.5, LongVideoBench 71.4; the MLVU cell is empty in the HTML table.
- Table 4, Joint vs Cached inference: 4B 65.3 / 74.3 vs 64.5 / 73.8; 35B-A3B 67.7 / 79.5 vs 67.4 / 78.8.
  13 of 14 comparisons favour Joint (only exception QVHighlights at 35B, −0.1 for Joint).
- Table 5, joint vs single-task: TG-only 64.6 (−0.7); QA-only 73.0 (−1.3; LongVideoBench −1.9).
- Table 6, Soft IoU: BCE/CE only 60.7 / 73.9 → with Soft IoU 65.3 / 74.3 (+4.6 / +0.4; Charades +6.8).
- Table 7, keeping the final MLP: 65.1 / 74.1 (−0.2 / −0.2).
- Table 8, single-stage on 100% of videos: 65.4 / 74.7 (+0.1 / +0.4, mostly MLVU +2.0) vs two-stage 65.3 / 74.3.

## Multi-query scaling (§3.5, Fig. 3, 4B, 1–10 queries per video, 40 videos per task)
- Joint inference adds 55 ms (grounding) and 31 ms (QA) from 1 to 10 queries.
- 10 queries: Joint 0.39 s (grounding) / 1.64 s (QA); Cached 0.85 s / 2.17 s.
- Autoregressive Direct QA: 60.0% (Cached) → 58.7% (Joint), 1.67 s; VideoJev 67.9% at 1.64 s.
- Qwen3.5-4B Instruct: 5.98 s for ten grounding queries at 52.3 mIoU (VideoJev 0.39 s, 60.1).
- Qwen Thinking: 1,393 s for ten QA queries at 66.4%.

## Calibration (§3.5, Fig. 4)
- 35B-A3B on LVBench: 95.8% accuracy on the 591 predictions with confidence ≥ 99% (73.4% overall).
- Mean ECE over four QA benchmarks (10 bins): 8.65 pp (4B), 8.13 pp (35B-A3B); probabilities overestimate
  correctness. No calibration-specific training.

## Appendix details used in the critique
- Latency excludes video loading/decoding, preprocessing, transfers, postprocessing (A.1).
- Generative baselines reuse visual encoding and prefix prefill, decode from independent query branches (A.1).
- Direct autoregressive baseline: with empty answer histories, later LVBench questions returned <|im_end|>
  for 1,418 of 1,446 questions unless answers were inserted (A.4).

# Numbers used in the slides, with their sources

Every number on a slide comes from this file. "V2" = QARM V2 (arXiv:2602.08559v1, LaTeX source);
"V1" = QARM (arXiv:2411.11739, HTML version on arxiv.org).

## Setting (V2, §1)
- Kuaishou: more than 400 million daily active users; tens of millions of new items uploaded every day.
- Accumulated interaction sequence exceeds 100,000 per active user.
- LLM vocabulary: "fewer than 20,000 token IDs" (V2 text, §1) vs "Z is about 1e5" (V2 Figure 1). Inconsistent.
- ID vocabulary: "X, Y > 1e9, ID number increasing along time" (V2 Figure 1).
- Figure 1: RecSys cross-transformer "always 1 layer"; LLM "Stacked Transformer (40+ layers)".

## QARM V1 (arXiv:2411.11739)
- Deployed since March 2024, 400 million daily active users.
- Item alignment: Item2Item pairs from the Swing model; User2Item pairs: for each clicked target, the most
  similar item (ID space) among the user's latest 50 positive clicks. Batch contrastive loss.
- Codes: VQ code = top-K nearest items (K = 25); RQ code = Res-Kmeans, L = 6 levels; dimension d = 64.
- Table 1 (Advertising CTR, AUC): + IA Rep +0.02%; + VQ code +0.11%; + RQ code +0.10%; + VQ & RQ +0.18%.
- Table 3 (online, Advertising#1): cold-start Revenue +9.704%; others Revenue +3.147%.
- Table 4 (online, Shopping): Shopping#1 GMV +2.296%, Orders +1.396%; Shopping#2 GMV +1.568%, Orders +0.716%.
- Table 6 (online GMV by purchase-frequency group): L1 (long tail) +8.035%, L6 (most popular) +3.984%.

## QARM V2 method (§1, §3)
- Reasoning filter: Qwen3-0.6B for Item2Item Swing pairs, Qwen3-8B for User2Item two-tower pairs; input =
  title and attributes only. Rejects 10%+ of Item2Item pairs and 70%+ of User2Item pairs.
- QA generation: Gemini and Qwen2.5-VL-72B; prompt asks for ten QA pairs per item (title, attributes,
  images, OCR, ASR).
- Examples: (soy sauce, laundry detergent) = biased hot-popular pair from Item2Item; (toothpaste, dental
  floss) = different but related; Figure 2: (fashion boots, down jacket) -> "yes" (seasonal transitions).
- Three-segment input: Input segment; Compression segment (several `<EMB>`, attend to input only); QA
  segment (attends to former segments only). Contrastive (in-batch, on the mean of `<EMB>` states,
  Figure 3) + generative (next-token) loss. Gradient cache; warm start that anneals QA->input attention to 0.
  Figure 3: frozen ViT, trained projector.
- Res-Kmeans in QARM: "more than 30% of Semantic IDs have multiple item candidates in the Shopping scenario".
- Res-KmeansFSQ: N > 10,000,000 item embeddings; K = 8192 (e.g.) per K-means level; two K-means levels;
  third level FSQ: Z = round(L * sigmoid(M2 W)), W in R^{d x 13}, L = 2 (e.g.). LLM embedding dim 3,000+.
- GSU: inner product top-k over LLM embeddings (PCA-reduced for storage).
- ESU: ItemID + three SIDs (c1, c2, c3) as lookup embeddings; target attention; MoE; multi-task BCE.

## QARM V2 results (§4)
- Table 1 Amazon Book AUC: DIN 67.69, SIM-hard 67.15, SIM-soft 69.57, QARM V2 70.33. Setup: rating >= 4
  positive; users with >= 20 interactions; one positive + one negative per user; 15% of users in test;
  top-50 retrieved for ESU.
- Table 2 Advertising CTCVR (AUC/UAUC/GAUC): 87.02/62.98/63.06 -> 87.43/63.97/64.16.
  Shopping#1 CTR 81.70/70.67/71.45 -> 81.79/70.85/71.63; CVR 89.52/71.61/72.50 -> 89.69/71.83/72.76;
  CTCVR 90.39/74.99/74.97 -> 90.59/75.34/75.37.
- Table 3 Shopping#2 CTR (AUC/UAUC/WUAUC) 85.95/65.75/65.97 -> 86.10/65.94/66.18;
  CVR 87.29/69.5/69.18 -> 87.38/69.58/69.34. Shopping#3 CTR 86.77/64.96/66.41 -> 86.82/65.08/66.53;
  CVR 89.41/65.38/67.54 -> 89.46/65.44/67.59.
- Table 4 Live-streaming (AUC/UAUC/GAUC): Click 82.68/63.48/63.61 -> 82.78/63.60/63.87;
  Gift 97.65/70.02/70.33 -> 97.69/70.11/70.55; Long View 83.70/67.28/67.26 -> 83.80/67.60/67.76;
  Follow 83.70/66.83/66.82 -> 83.76/66.94/67.10.
- "about 0.1% improvement is enough to contribute business gains". No sequence deduplication; in
  live-streaming top-100 interactions have only 23 unique authors on average.
- Table 5 online Advertising: Exposure +1.321%, Cost +3.942%, Revenue +4.873%.
- Table 6 online Shopping (GMV/Order/Exposure): #1 +3.208/+1.919/+0.427; #2 +5.612/+4.834/+3.739;
  #3 +1.037/+1.221/+1.487 (%). Multi-week A/B tests.
- Table 7 online Live-streaming (Click, Watch Time, Watch Count, Gift Count, Like, Comment, Follow):
  #1 cold-start +3.231 +2.961 +1.609 +1.807 - - -; #1 others +0.611 +0.753 +0.489 +2.917 +3.215 +1.184 +1.158;
  #2 cold-start +0.890 +0.998 +0.998 +0.918 - - -; #2 others +0.304 +0.482 +0.434 +2.917 +0.464 +0.826 +0.418.
- Table 8 retrieval HR (Click HR@200/HR@500, Order HR@200/HR@500): QARM 7.77/9.7/11.3/13.0;
  QARM V2 12.5/15.4/20.0/23.0. Text says order HR@500 "from 20.0% to 23.0%" (table: 13.0). Setup: last 10
  clicked triggers x 50 candidates = up to 500; ground truth = real-time clicks and orders.
- Table 9 code conflict (Collision, EdgeNum, HR@1, HR@10): QARM ResKmeans 77.92%/129.33/80.3%/97.79%;
  QARM V2 ResKmeans 52.25%/8.41/91.9%/99.75%; QARM V2 ResKmeansFSQ 32.39%/2.5/95.2%/99.9%. All "3 * 4096".
  Per-element MSE: about 0.37 / 0.26 / 0.20 at levels 1/2/3.
- Table 10 GSU exclusive retrieve rate: Click (Top50) 63.6%, Order (Top30) 57.9%, Exposure (Top30) 65.1%.
- Case study: baseline ID-based SIM retrieves e.g. unrelated jewelry for a phone-accessory target.

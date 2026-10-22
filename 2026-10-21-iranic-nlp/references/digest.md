# Number digest: Computationally Invisible (Iranic NLP survey)

Every number used on the slides and the poster, with where it appears in the paper (SilkRoadNLP submission 25,
LaTeX source). "Table 1" = `tables/language_overview.tex`, "Table 2" = `tables/linguistic_resources.tex`,
"Table 3" = the parallel-data matrix (`tab:parallel_matrix`), "Appendix A" = `tables/app_longlist.tex`.

## Scope and method (§1, §3)

| Value | Source |
|---|---|
| 101 ISO 639-3 coded varieties; over 200 million speakers | abstract, §1 |
| 4 macrolanguage codes (`fas`, `kur`, `pus`, `bal`); 97 individual codes | §2.1 |
| Appendix A by branch: Northwestern 40, Southwestern 31, Eastern 17, Ossetic 2, extinct/historical 11 (sum 101) | Appendix A, counted from the table rows |
| Appendix A by type: 50 dialects, 36 languages, 11 historical, 4 macrolanguages | Appendix A, counted |
| Search: Google Scholar, ACL Anthology, Semantic Scholar; final search May 2026 | §3 |
| 5,878 candidate publications (2020–2026) → 495 papers | §3 |
| Two-stage pipeline with Qwen3.5-9B: (1) relevance filter, (2) annotation of language(s), task, resource type, availability, year, venue | §3 |
| All annotations checked by two authors; a third author arbitrates disagreements | §3 |
| "Does not exist" = no publicly documented resource found within the search | §3 |

## Coverage (§3, Figures 2–4)

| Value | Source |
|---|---|
| Persian 394 papers = 80% of 495; Persian ≈ 60% of the family's speakers | §3 |
| Kurdish 93, Pashto 29, Luri/Laki 5, Balochi 4, Mazanderani/Gilaki 4 papers | §3, Figure 2 |
| Papers covering several languages count once per language (totals exceed 495) | Figure 2 caption |
| Papers per year: 2020 54, 2021 43, 2022 64, 2023 85, 2024 87, 2025 131, 2026 65 (to May) | Figure 3 (values read from the figure; 54 and 131 also in §3) |
| Tasks: sentiment 116, text classification 70, language modeling 59, QA 59, MT 41, NER 38, IE 36, morphology & syntax 32, IR 25, lexical semantics 24, summarization 10, dialogue 10, text generation 9 | Figure 4 (sentiment 116, classification 70 also in caption) |

## Languages (Table 1, §2.2)

| Language | Branch | L1 (Table 1) | Script(s) | NLP level |
|---|---|---|---|---|
| Persian | SW | 91M (L2 35M) | Perso-Arabic, Cyrillic | High |
| Dari | SW | 15M (L2 18M) | Perso-Arabic | Medium |
| Tajik | SW | 8M | Cyrillic | Low |
| Luri / Bakhtiari | SW | 5M | Perso-Arabic | Very low |
| Hazaragi | SW | 3M | Perso-Arabic | Very low |
| Laki | SW | 0.7M | Perso-Arabic | Very low |
| Kurdish | NW | 26M | Perso-Arabic / Latin / Cyrillic | Low |
| Balochi | NW | 9M | Perso-Arabic | Very low |
| Mazanderani | NW | 1.4M | Perso-Arabic | Very low |
| Gilaki | NW | 3M | Perso-Arabic | Very low |
| S. Kurdish | NW | 3M | Perso-Arabic | Very low |
| Zazaki | NW | 2–4M | Latin | Very low |
| Talysh | NW | 0.8M | Perso-Arabic / Cyrillic / Latin | Very low |
| Gorani | NW | 0.4M | Perso-Arabic | Very low |
| Pashto | E | 51M (L2 5M) | Perso-Arabic | Low |
| Shughni | E | 0.1M | Cyrillic, Latin | Very low |
| Wakhi | E | 0.06M | Perso-Arabic / Cyrillic / Latin | Very low |
| Yaghnobi | E | 0.01M | Cyrillic | Very low |
| Ossetic | Ossetic | 0.6M | Cyrillic | Very low |

§2.2: Persian macrolanguage ≈ 130M speakers; Pashto 51–60M; Yaghnobi ≈ 13K; Shughni ≈ 95K; Wakhi ≈ 60K.

**To align before the camera-ready version:** Mazanderani is 1.4M in Table 1, ≈ 4M in §2.2 and §6, and 20/6
in Table 2. Balochi is 9M in Table 1 and §6, 8.8M in §2.2 and the Figure 2 caption. Kurdish is 26M in Table 1 and
26–30M in §2.2. The slides and poster use Table 1.

## Digital infrastructure (Table 2, §4)

| Language | FineWeb2 | Wikipedia | Wiktionary | UniMorph lemmata / forms | GlotLID V3 F1 | Parallel pairs (all) | Grammar / WordNet / spell / ASR |
|---|---|---|---|---|---|---|---|
| Arabic (ref.) | 106 GB | 1,293K | 74,093 | 4,134 / 140,003 | 0.845 | — | ✓ ✓ ✓ ✓ |
| Turkish (ref.) | 135 GB | 658K | 43,253 | 3,579 / 275,460 | 0.972 | — | ✓ ✓ ✓ ✓ |
| Persian | 102 GB | 1,075K | 19,248 | 273 / 37,128 | 0.922 | 612M | ✓ ✓ ✓ ✓ |
| Tajik | — | 118K | 430 | 0 / 0 | 0.996 | — | ✗ ✗ ✗ ✗ |
| N. Kurdish | 979 MB | 92K | 8,254 | 15,083 / 216,370 | 0.997 | 848K | ✓ ✓ ✓ ✓ |
| C. Kurdish | — | 82K | — | 274 / 24,317 | 0.969 | — | ✓ ✓ ✓ ✓ |
| S. Kurdish | — | 15K | — | 1 / 189 | 0.982 | — | ✓ ✗ ✗ ✗ |
| Pashto | — | 21K | 1,100 | 395 / 6,945 | 0.990 (pbt) | — | ✗ ✗ ✗ ✗ |
| Mazanderani | 1.7 MB | 65K | 337 | 0 / 0 | 0.958 | 18.9K | ✗ ✗ ✗ ✗ |
| Gilaki | 16.4 MB | 48K | 34 | 0 / 0 | 0.968 | 18.6K | ✓ ✗ ✗ ✗ |
| Balochi | — | 1.2K | 429 | 0 / 0 | 0.990 (bcc) | 175 | ✗ ✗ ✗ ✗ |
| Talysh | 3.0 MB | 10K | 302 | 0 / 0 | 0.993 | 8.7K | ✓ ✗ ✗ ✗ |
| Zazaki | — | 43K | 1,083 | 0 / 0 | 0.987 | 12.1K | ✓ ✗ ✗ ✗ |
| Gorani | 38.7 MB | Incubator | 211 | 0 / 0 | 0.982 | 36.8K | ✓ ✗ ✗ ✗ |
| N. Luri | 82.7 KB | — | 5 | 0 / 0 | 0.909 | — | ✓ ✗ ✗ ✗ |
| Laki | 57.7 KB | Incubator | 85 | 0 / 0 | 0.800 | 15.2K | ✓ ✗ ✗ ✗ |

§4 text: 10 Iranic Wikipedias, 11 more varieties in the Wikimedia Incubator, 76 of the 97 individual varieties with
no Wikipedia presence. Persian has nearly 60 million FineWeb2 documents (§2.1). GlotCC, EMMA-500 and MADLAD-400 cover
8–16 Iranic variety-script pairs. GlotLID V3 covers 16 Iranic variety-script pairs; PALI covers six Iranic varieties.
Northern Luri Wikipedia was abandoned after review found Persian with light lexical substitution.

## Parallel data (Table 3, §4)

Pairs with English: Persian 612M, Kurdish 511K, Gorani 22K, Gilaki 9K, Laki 4.6K, Mazanderani 4.5K, Zazaki 4.4K,
Talysh 2.1K, S. Luri 2K, Balochi 110. Persian–Kurdish 326K. Between smaller varieties: at most a few thousand pairs
(e.g. Mazanderani–Laki 3K, Gorani–Gilaki 2K); Zazaki has 0 pairs with Gilaki, Mazanderani, Talysh, Laki, S. Luri,
Gorani; Balochi has 30 with Persian, 35 with Kurdish, 0 with the others. Every variety below Kurdish has fewer than
40K pairs in total. The Kurmanji–Sorani corpus is the only substantial intra-Iranic MT resource.

## Tasks (§5)

- LM: ParsBERT; Matina corpus 73B tokens; FarsInstruct 21 instruction datasets; HarfoSokhan 6M colloquial-to-formal
  pairs; Kurdish KuBERT, KurdBERT; Pashto Ps-BERT; no monolingual transformer for any other variety.
- Benchmarks: ParsiNLU 14,500+ instances, six tasks, natively authored; Khayyam 50+ domains; Belebele covers Persian,
  Tajik, Sorani, Southern Pashto (translated); APARSIN = first benchmark beyond the five most resourced varieties.
- QA: PQuAD 80K, PersianMHQA 7K, PersianMedQA 20K; 25+ Persian QA datasets; one Sorani news QA dataset.
- Sentiment: 116 papers; MirasOpinion 938K reviews; TaarofBench: LLMs 40–48% below native speakers.
- Speech: DeepMine 480+ h; ParsVoice 3,526 h; DOLMA 40+ h for six varieties (Zazaki 0.2 h), Whisper WER 37.9–89.5%;
  no speech resources for Balochi, Luri, Talysh, Shughni, Wakhi, Yaghnobi.
- OCR: GlotOCR Bench 158 scripts; most models good on fewer than ten scripts.

## Transfer (§6) and challenges and priorities (§7)

Six challenges with one priority each; three immediate priorities (raw text, FLORES+ — grew from about 200 to 230
varieties but still the same six Iranic varieties as FLORES-200: pes, prs, tgk, ckb, kmr, pbt, about 2K sentences
per variety — and natively authored evaluation).

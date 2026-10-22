"""Speaker notes, keyed by slide slug (file name without the number). Used by make_deck.py.

Each note: "Terms" (technical words on the slide, in plain words), "Say" (a short script), and a "Bridge" to the
next slide. STORY goes at the top of slides/speaker-notes.md.
"""

STORY = """The story in six sentences:

1. The Iranic family has 101 ISO 639-3 coded varieties and over 200 million speakers, from the Caucasus to Xinjiang and from Russia to Oman.
2. We surveyed 495 NLP papers from 2020 to May 2026 (filtered from 5,878 candidates with an LLM, every label checked by two of us).
3. 394 of the 495 papers (80%) are about one variety, Iranian Persian; Pashto (51M speakers) has 29 papers and Balochi (9M) has 4.
4. The gap starts below the papers: most varieties have little or no web text, dictionary data, morphology resources, LID quality or parallel data, and ISO labels and inconsistent Unicode hide varieties from pipelines.
5. Persian itself is saturating on standard tasks; its open problems are cultural and pragmatic competence, while every other variety still needs its first benchmark.
6. The cheapest next steps are tagged web text, FLORES+ sentences and one natively written benchmark per variety."""

NOTES = {
    "title": """Terms: Iranic = the Iranian branch of Indo-European (Persian, Kurdish, Pashto, Balochi, and many smaller varieties).

Say: Our paper is a survey: "Computationally Invisible: Charting the NLP Landscape of Iranic Languages", joint work between Isfahan University of Technology, LMU Munich, TU Munich and CUNY. The row of boxes is the whole story: 101 varieties and over 200 million speakers; 495 papers; 394 of them about Iranian Persian. For most other varieties we found nothing.

Bridge: Here is the survey in one slide.""",

    "tldr": """Terms: survey paper = a paper that collects and organizes existing work instead of running new experiments.

Say: The question: where does NLP stand for the whole Iranic family? What we did: a systematic search, 5,878 candidates, an LLM filter and annotation checked by two humans, 495 papers kept, plus an audit of corpora, Wikipedia, morphology, language identification and parallel data. What we found: a severe imbalance. 80% of the papers are on Persian; Pashto, with 51 million speakers, has 29 papers; Balochi, with 9 million, has 4.

Bridge: A few terms first.""",

    "glossary": """Terms: as on the slide.

Say: Three terms matter most. ISO 639-3 codes are how datasets and models label languages; a macrolanguage code like fas covers several individual codes. "Variety" is the neutral word we use so we do not have to decide what is a language and what is a dialect. LID, language identification, is the filter every web corpus goes through. Taarof and ZWNJ come back later as concrete examples.

Bridge: Let us look at the family itself.""",

    "family": """Terms: branch = a subgroup of related languages; historical = no living speakers.

Say: The 101 codes split into four living branches plus historical languages. Northwestern is the largest by count, 40 codes: Kurdish, Balochi, the Caspian languages Mazanderani and Gilaki, Zazaki, Gorani, Talysh. Southwestern has 31: Persian, Dari, Tajik, Luri, Laki. Eastern has 17: Pashto and the Pamir languages. Ossetic has 2. Eleven are historical, like Old Persian and Avestan. By type, half of the codes are dialects.

Bridge: Which of these are the big ones?""",

    "languages": """Terms: L1 = first-language speakers. NLP level = our rating of available resources.

Say: This is Table 1 of our paper. Persian has 91 million L1 speakers and is the only variety rated high. Dari is medium, Tajik, Kurdish and Pashto are low, and everything else is very low, including Balochi with 9 million speakers. Note the scripts: Perso-Arabic dominates, but Tajik, Ossetic and Yaghnobi use Cyrillic, Zazaki uses Latin, and Kurdish, Talysh and Wakhi use several.

Point to the footer: speaker numbers are approximations; sources differ, especially for contested varieties.

Bridge: Even the labels are not simple.""",

    "labels": """Terms: macrolanguage = an ISO code that groups several individual codes.

Say: fas, Persian, covers Iranian Persian and Dari but not Tajik, which is written in Cyrillic and official in Tajikistan, although the three are largely mutually intelligible. kur, Kurdish, covers Kurmanji, Sorani and Southern Kurdish, which are only partly mutually intelligible and use different scripts. So a paper that just says "Kurdish" is ambiguous. And whether Laki or Bakhtiari count as separate languages is contested. These choices decide what data gets labelled and which communities get tools.

Bridge: How did we build the survey?""",

    "method": """Terms: annotation = assigning labels (language, task, …) to each paper.

Say: We searched Google Scholar, the ACL Anthology and Semantic Scholar with every Iranic language name and ISO code combined with NLP task terms. That gave 5,878 candidates. Qwen3.5-9B filtered for relevance and then annotated six fields per paper. Two of us checked every annotation, with a third as arbiter. After deduplication, 495 papers remained. An important convention: when we say a resource does not exist, we mean none was found in our search.

Bridge: So what does the landscape look like?""",

    "papers-vs-speakers": """Terms: papers per million speakers = paper count divided by L1 speakers.

Say: Persian has 394 papers, 80% of the corpus, while it is about 60% of the family's speakers. Kurdish, with 93 papers, does relatively well. Pashto is the outlier: 51 million speakers, twice Kurdish, but only 29 papers. Balochi has 4 papers for 9 million speakers. Red marks fewer than one paper per million speakers.

Bridge: Is this changing over time?""",

    "timeline": """Terms: none new.

Say: Output grows from 54 papers in 2020 to 131 in 2025. But the growth is almost entirely Persian; Kurdish and Pashto grow modestly and the other varieties stay near zero. The 2026 bar is partial because the search ended in May.

Bridge: Which tasks do these papers work on?""",

    "tasks": """Terms: text classification = assigning a label to a text; information extraction = pulling structured facts out of text.

Say: Sentiment analysis leads with 116 papers, then text classification with 70, language modeling and question answering with 59 each. Generation-style tasks are rare: summarization and dialogue about 10 each, text generation 9. Most attention goes to Persian; for the other varieties, machine translation is the most active area.

Bridge: Papers are the top of the pyramid. What is underneath?""",

    "footprint": """Terms: FineWeb2 = a large multilingual web corpus. UniMorph forms = inflected word forms in the UniMorph database. Tools = grammar, WordNet, spell checker, ASR.

Say: Arabic and Turkish are reference points. Persian is comparable to them: 102 GB of web text, over a million Wikipedia articles, all four tools. Northern Kurdish is surprisingly strong in morphology. Below them the columns thin out fast: no FineWeb2 data for Tajik, Pashto or Balochi, a few kilobytes for Laki and Northern Luri, zero UniMorph forms, and no tools.

Bridge: Wikipedia deserves a closer look.""",

    "wikipedia": """Terms: Wikimedia Incubator = a test area for Wikipedias that are not yet approved. Wiktionary = the dictionary sister project.

Say: Of the 97 individual varieties, 10 have an active Wikipedia, 11 only an Incubator entry, and 76 nothing at all. And article counts can mislead: Mazanderani and Gilaki have tens of thousands of articles but only 337 and 34 Wiktionary entries; we call this a hollow digital presence. The Northern Luri Wikipedia was abandoned because reviewers found it was Persian with a few Luri words.

Bridge: Next, morphology.""",

    "morphology": """Terms: paradigm = all inflected forms of one word. Ezafe = a Persian linking vowel between noun and modifier. Split ergativity = case marking that changes with tense.

Say: These languages are morphologically rich, so morphological resources matter. UniMorph shows a striking asymmetry: Northern Kurdish has 15,083 paradigms, Persian only 273 despite all its text, and many varieties zero. Persian has analysis tools like Hazm, DadmaTools and Parsivar; no other variety has an equivalent. Treebanks exist only for Persian and two Kurdish varieties.

Bridge: Before any of this, a corpus has to be built, which starts with language identification.""",

    "lid": """Terms: F1 = combination of precision and recall. False positive = text wrongly assigned to a language.

Say: Iranic LID is hard because Persian, Dari and Tajik share most vocabulary, and Luri and Talysh are easily confused with Persian and Azerbaijani. GlotLID V3 covers 16 Iranic variety-script pairs; most F1 scores are high, but Laki is at 0.800 and Northern Luri at 0.909. GlotLID shows elevated false-positive rates for precarious pairs: for a small language, a few mislabelled Persian sentences can dominate its corpus.

Bridge: Next, parallel data for translation.""",

    "parallel-english": """Terms: sentence pair = one sentence and its translation.

Say: Three tiers. Persian has over 600 million pairs with English. Kurdish has about 511 thousand. Everyone else has under 40 thousand in total; Gorani has 22 thousand from a literary corpus, and Balochi has 110. The axis is logarithmic: each grid line is a factor of 100.

Bridge: And between the Iranic varieties themselves?""",

    "parallel-matrix": """Terms: intra-Iranic = between two Iranic varieties.

Say: This is our parallel-data matrix. Below Persian and Kurdish, every pair has at most a few thousand sentences. Zazaki has zero pairs with all six smaller varieties, and Balochi has 30 with Persian, 35 with Kurdish and zero with the rest. The Kurmanji–Sorani corpus is the only substantial intra-Iranic resource. So translation between neighbours goes through Persian or English.

Bridge: Now the tasks themselves.""",

    "task-status": """Terms: natively written = created in the language, not translated from English.

Say: Row by row. Pretraining: Persian has ParsBERT, the 73-billion-token Matina corpus and LLMs; Kurdish and Pashto have a few BERT models; everyone else relies on multilingual models. Benchmarks: Persian has ParsiNLU and Khayyam; the others have translated Belebele items, and APARSIN is the first benchmark beyond the top five varieties. QA: 25 Persian datasets versus one Sorani news dataset. Speech: thousands of hours for Persian; for six other varieties about 40 hours together, with Whisper error rates of 38 to 90 percent. OCR and classic tasks: nothing outside Persian.

Bridge: Even Persian has open problems.""",

    "saturation": """Terms: saturation = models score so high that the benchmark no longer separates them. Pragmatics = meaning that depends on social context.

Say: Standard Persian sentiment, Wikipedia reading comprehension and NER are near saturation, and many benchmarks are translated from English. The open frontier is cultural and pragmatic competence. The example is taarof, Persian ritual politeness: on TaarofBench, LLMs score 40 to 48 percent below native speakers. For the other varieties the frontier is simpler: build the first benchmark.

Bridge: How do people work around the lack of data?""",

    "transfer": """Terms: zero-shot transfer = using a model trained on one language for another without training data in it.

Say: The main strategy is transfer from relatives. Lexical proximity: Persian, Dari and Tajik share most vocabulary. Script proximity: Perso-Arabic varieties share tokenization conventions, but Unicode differences silently hurt. Grammatical proximity: Kurmanji helps Sorani. In practice, transfer runs through Persian or English, and a model covering Persian does not cover Dari unless Dari data was included. Systematic intra-family transfer studies are missing.

Bridge: That brings us to the challenges, starting with the script problem.""",

    "script": """Terms: code point = the number Unicode assigns to a character.

Say: Here is a concrete example of the script problem. The same visible letter can be stored as different characters: the Farsi yeh and the Arabic yeh, or keheh and the Arabic kaf. Ya and kaf code points differ across Persian, Pashto and Dari text, so matching, deduplication and tokenization fail silently. Add zero-width non-joiners in Persian compounds and Kurmanji written in three scripts. Our priority: one shared Iranic normalization library. The code points on the slide are an illustration.

Bridge: Here are all six challenges.""",

    "challenges": """Terms: dialect continuum = neighbouring varieties that blend gradually into each other.

Say: Six challenges, one priority each. Resource concentration: shared tasks and data hubs, as in African NLP. Script heterogeneity: a normalization library. Dialectal fragmentation: benchmarks for colloquial and regional varieties. Cultural misalignment: benchmarks co-created with native speakers. Endangered varieties: multilingual speech models and community recording. Structural inequity: sanctions limit compute, API access and travel, so compute and access programs are needed.

Bridge: Of these, three things can start right now.""",

    "priorities": """Terms: FLORES+ / OLDI = the community-maintained version of the FLORES translation benchmark.

Say: First, raw text: publish Iranic text on the open web with correct language tags, because untagged text is invisible to LID-filtered crawls. Second, translation benchmarks: FLORES+ grew to about 230 varieties, but its Iranic coverage is still the same six as FLORES-200. Each new variety needs about 2,000 sentences and a pull request. Third, at least one natively written benchmark per variety, ideally through shared tasks.

Bridge: What the survey contributes, and what comes next.""",

    "scope": """Terms: grey literature = work outside indexed venues (local journals, theses).

Say: What does the survey add? It is the first systematic map of the whole family; it audits the infrastructure underneath the papers, not only the papers; it uses conservative wording, "not found" rather than "does not exist"; and it ends with concrete, low-cost priorities, plus a companion website and public code. On scope: we searched indexed venues in English, so Persian-language journals are a natural next addition to the live index. Screening was LLM-assisted and checked by people; auditing the filter's recall is future work. The NLP levels are a quick summary; a scoring rule would make them reproducible. And paper counts show attention, not quality: they also reflect sanctions and limited access, which we discuss in the paper.

Bridge: To finish, five takeaways.""",

    "takeaways": """Say: One: Iranic NLP is mostly Persian NLP, 80% of the papers. Two: the gap starts below the papers, in web text, dictionaries, morphology and parallel data. Three: labels and scripts are part of the problem. Four: Persian needs new kinds of tests, the other varieties need a first test. Five: small contributions, like tagged web text, FLORES+ sentences and one native benchmark, go far. The companion website and code are at sigiranic.github.io.

Then thank the audience and invite questions; a good opener: which variety could your group help with?""",
}

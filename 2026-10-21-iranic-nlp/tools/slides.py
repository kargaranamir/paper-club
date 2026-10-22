"""Iranic NLP survey paper-club deck: one function per slide; the order is the SLIDES list at the bottom.

Numbers come only from references/digest.md (which cites the paper's tables and sections).
Colour code: branches SW = orange, NW = blue, Eastern = green, Ossetic = purple, historical = gray.
Red = missing or very low, yellow = takeaway.
"""
import math

from slidekit import P, Slide, W, text_width

PART1 = "Part I · The family"
PART2 = "Part II · How the survey was built"
PART3 = "Part III · The research landscape"
PART4 = "Part IV · Digital infrastructure"
PART5 = "Part V · Tasks"
PART6 = "Part VI · Challenges and priorities"
PART7 = "Part VII · Discussion"
SRC = "Computationally Invisible (SilkRoadNLP submission)"

BR = {"SW": "orange", "NW": "blue", "E": "green", "Oss": "purple", "Hist": "gray"}
LV = {"H": ("green", "high"), "M": ("yellow", "medium"), "L": ("orange", "low"), "VL": ("red", "very low")}


def panel(s, x, y, w, h, head, body, c, hfs=26, bfs=22, fill=None):
    s.box(x, y, w, h, None, c, fill=fill or P[c]["soft"])
    s.text(x + 22, y + 16, head, hfs, P[c]["text"])
    if body:
        s.text(x + 22, y + 16 + hfs * 1.25 + 14, body, bfs, P["ink"])


def chip(s, x, y, label, c, fs=21, h=46, pad=18, mono=False, fill=None):
    w = text_width(label, fs, mono) + 2 * pad
    s.box(x, y, w, h, label, c, fs, mono=mono, fill=fill)
    return x + w


def harrow(s, x0, x1, y, c=None, dashed=False):
    s.arrow([(x0, y), (x1, y)], c or P["ink"], dashed=dashed)


def varrow(s, x, y0, y1, c=None):
    s.arrow([(x, y0), (x, y1)], c or P["ink"])


def logx(v, lo, hi, x, w):
    return x + (math.log10(v) - math.log10(lo)) / (math.log10(hi) - math.log10(lo)) * w


BADGE = {"H": ("#d3f9d8", "#37b24d", "#2b8a3e"), "M": ("#fff3bf", "#f0c330", "#8a6d00"),
         "L": ("#ffd8a8", "#f08c00", "#a85c00"), "VL": ("#e03131", "#c92a2a", "#ffffff")}


def badge(s, x, y, lvl, w=120, h=34, fs=18):
    fill, stroke, tc = BADGE[lvl]
    s.box(x, y, w, h, LV[lvl][1], "gray", fs, fill=fill, stroke=stroke, tcolor=tc, round_=True, sw=1.5)


# ======================================================================= opening
def s_title(n):
    s = Slide("01-title", n)
    s.text(70, 120, "SURVEY · 495 PAPERS · 2020–2026", 20, P["muted"])
    s.text(70, 165, "Computationally Invisible", 80)
    s.text(72, 275, "Charting the NLP Landscape of Iranic Languages", 38)
    s.text(72, 345, "Hojjat Mokhtarabadi*, Amir Hossein Kargaran*, Ali Shakeri, Saba Shafiei, Nafiseh Nikeghbal,\n"
                    "Mohammad Hossein Manshaei  ·  Isfahan University of Technology, LMU Munich, TU Munich, CUNY\n"
                    "* equal contribution", 22, P["muted"])
    s.text(72, 470, "SilkRoadNLP submission  ·  companion website: sigiranic.github.io", 20, P["muted"], mono=True)
    # one row: the family, the papers, the skew
    y = 580
    s.box(72, y, 260, 100, "101 varieties\n200M+ speakers", "gray", 24)
    harrow(s, 336, 392, y + 50)
    s.box(396, y, 260, 100, "495 papers\n2020–2026", "purple", 24)
    harrow(s, 660, 716, y + 50)
    s.box(720, y, 400, 100, "394 of them (80%)\nare about Iranian Persian", "orange", 24)
    s.text(1160, y + 14, "For most of the other varieties,\nno paper, benchmark or tool was found.", 24, P["red"]["text"])
    s.footer("Slides drawn in Excalidraw; every number is from our paper (see references/digest.md)")
    return s


def s_tldr(n):
    s = Slide("02-tldr", n)
    s.title("Our survey in one slide")
    cols = [("Question", "blue",
             "Where does NLP stand for the\nIranic language family?\n\n"
             "• 101 ISO 639-3 coded varieties\n• over 200 million speakers\n"
             "• from the Caucasus to Xinjiang,\n  from Russia to Oman\n• four living branches"),
            ("What we did", "purple",
             "A systematic survey:\n\n• 5,878 candidate papers,\n  2020 – May 2026\n"
             "• LLM filter + annotation\n  (Qwen3.5-9B), checked by\n  two of us\n• 495 papers kept\n"
             "• audit of corpora, Wikipedia,\n  morphology, LID, parallel data"),
            ("What we found", "red",
             "Severe imbalance:\n\n• Persian: 394 papers (80%)\n• Pashto: 51M speakers, 29 papers\n"
             "• Balochi: 9M speakers, 4 papers\n• most varieties: nothing found\n\n"
             "Persian itself is saturating on\nstandard tasks; the rest need\ntheir first benchmark.")]
    for i, (h, c, b) in enumerate(cols):
        panel(s, 70 + i * 495, 160, 465, 560, h, b, c, 32, 25)
    s.takeaway("Iranic NLP is mostly Persian NLP; the other varieties are computationally invisible.", y=745)
    s.footer(SRC + ": abstract, §1, §3, §8")
    return s


def s_glossary(n):
    s = Slide("03-glossary", n)
    s.title("Glossary")
    rows = [["ISO 639-3", "international three-letter language codes, e.g. pes = Iranian Persian, ckb = Sorani"],
            ["macrolanguage", "one ISO code that covers several individual codes, e.g. fas covers pes and prs"],
            ["variety", "neutral word for a language or dialect; avoids deciding which one it is"],
            ["FineWeb2", "large multilingual web-text corpus; a proxy for how much text a language has online"],
            ["Wiktionary · UniMorph", "community dictionary · database of inflected word forms (paradigms)"],
            ["LID", "language identification: which language is this text? Needed to build corpora"],
            ["parallel data", "the same sentences in two languages; the raw material of machine translation"],
            ["FLORES+", "standard translation benchmark, about 2K sentences per language"],
            ["pivot language", "translating through a third language (here Persian or English)"],
            ["ZWNJ", "zero-width non-joiner: an invisible character that splits Persian compound words"],
            ["taarof", "Persian ritual politeness (e.g. refusing an offer before accepting it)"]]
    s.table(70, 150, [330, 1130], rows, header=["term", "meaning"], fs=20, rh=55, hc="gray", aligns=["l", "l"],
            colors=[[P["blue"]["text"], P["ink"]]] * len(rows))
    s.footer(SRC + ", §2, §4, §7")
    return s


# ======================================================================= Part I: family
def s_family(n):
    s = Slide("04-family", n)
    s.title("101 coded varieties in four living branches", "Counted from the appendix table of all 101 ISO 639-3 codes",
            part=PART1, pc="gray")
    data = [("Northwestern", 40, "NW", "Kurdish, Balochi, Mazanderani, Gilaki,\nZazaki, Gorani, Talysh, Tatic varieties"),
            ("Southwestern", 31, "SW", "Persian, Dari, Tajik, Luri, Bakhtiari,\nLaki, Central Plateau dialects"),
            ("Eastern", 17, "E", "Pashto, Pamir languages:\nShughni, Wakhi, Yaghnobi"),
            ("Ossetic", 2, "Oss", "Iron and Digor (North and\nSouth Ossetia)"),
            ("Historical", 11, "Hist", "Old Persian, Avestan, Middle Persian,\nSogdian, Bactrian, …")]
    x0, y0, sc = 330, 175, 18
    for i, (name, k, b, ex) in enumerate(data):
        y = y0 + i * 100
        c = BR[b]
        s.text(310, y + 20, name, 26, P[c]["text"], "r")
        s.box(x0, y + 8, k * sc, 56, None, c, round_=False)
        s.text(x0 + k * sc + 14, y + 20, str(k), 28, P["ink"])
        s.text(1130, y + 10, ex, 20, P["muted"])
    s.text(330, 690, "Types: 50 dialects · 36 languages · 11 historical · 4 macrolanguages (fas, kur, pus, bal)", 23)
    s.takeaway("Most codes are small Northwestern and Southwestern varieties, many of them dialects.", y=745)
    s.footer(SRC + ", §2.2 and Appendix A")
    return s


def s_languages(n):
    s = Slide("05-languages", n)
    s.title("The major modern languages", "L1 speakers, script and NLP resource level (Table 1)", part=PART1,
            pc="gray")
    groups = [("SW", [("Persian", "91M", "Perso-Arabic, Cyrillic", "H"), ("Dari", "15M", "Perso-Arabic", "M"),
                      ("Tajik", "8M", "Cyrillic", "L"), ("Luri / Bakhtiari", "5M", "Perso-Arabic", "VL"),
                      ("Hazaragi", "3M", "Perso-Arabic", "VL"), ("Laki", "0.7M", "Perso-Arabic", "VL")]),
              ("E", [("Pashto", "51M", "Perso-Arabic", "L"), ("Shughni", "0.1M", "Cyrillic, Latin", "VL"),
                     ("Wakhi", "0.06M", "Perso-Ar., Cyr., Latin", "VL"), ("Yaghnobi", "0.01M", "Cyrillic", "VL")]),
              ("NW", [("Kurdish", "26M", "Perso-Ar., Latin, Cyr.", "L"), ("Balochi", "9M", "Perso-Arabic", "VL"),
                      ("Gilaki", "3M", "Perso-Arabic", "VL"), ("S. Kurdish", "3M", "Perso-Arabic", "VL"),
                      ("Zazaki", "2–4M", "Latin", "VL"), ("Mazanderani", "1.4M", "Perso-Arabic", "VL"),
                      ("Talysh", "0.8M", "Perso-Ar., Cyr., Latin", "VL"), ("Gorani", "0.4M", "Perso-Arabic", "VL")]),
              ("Oss", [("Ossetic", "0.6M", "Cyrillic", "VL")])]
    names = {"SW": "Southwestern", "E": "Eastern", "NW": "Northwestern", "Oss": "Ossetic"}
    cols = [[groups[0], groups[1]], [groups[2], groups[3]]]
    rh = 42
    for ci, col in enumerate(cols):
        x = 70 + ci * 750
        y = 160
        for b, rows in col:
            c = BR[b]
            s.text(x, y, names[b], 24, P[c]["text"])
            y += 36
            for r, (lang, sp, scr, lv) in enumerate(rows):
                if r % 2 == 0:
                    s.box(x, y, 720, rh, None, "gray", fill="#f8f9fa", stroke="transparent", round_=False, sw=1,
                          roughness=0)
                s.text(x + 12, y + rh / 2, lang, 23, P["ink"], "l", "m")
                s.text(x + 285, y + rh / 2, sp, 23, P["ink"], "r", "m")
                s.text(x + 310, y + rh / 2, scr, 19, P["muted"], "l", "m")
                badge(s, x + 585, y + 4, lv, 130, rh - 8, 17)
                y += rh
            y += 14
    s.text(70, 742, "NLP level is our rating of available resources. One language is rated high, one medium, three low and the rest"
                    " very low.", 21, P["muted"])
    s.footer(SRC + ", Table 1. Speaker numbers are approximations from several sources")
    return s


def s_labels(n):
    s = Slide("06-labels", n)
    s.title("What counts as one language?", "The ISO labels do not match how the varieties are used",
            part=PART1, pc="gray")
    # fas
    s.box(90, 170, 220, 64, "fas · Persian", "orange", 24)
    for i, (c, lab) in enumerate([("pes", "Iranian Persian"), ("prs", "Dari (Afghanistan)")]):
        s.line([(200, 234), (200, 268 + i * 70 + 25), (240, 268 + i * 70 + 25)], P["orange"]["stroke"], 2)
        s.box(240, 268 + i * 70, 300, 50, f"{c} · {lab}", "orange", 21, fill=P["orange"]["soft"])
    s.box(240, 420, 300, 50, "tgk · Tajik", "gray", 21, fill="#ffffff", dashed=True)
    s.text(560, 418, "not in fas: Cyrillic script,\nofficial in Tajikistan", 19, P["muted"])
    s.text(90, 495, "Largely mutually intelligible;\nwhether they are one language is\npolitically charged.", 21)
    # kur
    s.box(830, 170, 220, 64, "kur · Kurdish", "blue", 24)
    for i, (c, lab) in enumerate([("kmr", "Kurmanji"), ("ckb", "Sorani"), ("sdh", "Southern Kurdish")]):
        s.line([(940, 234), (940, 268 + i * 70 + 25), (980, 268 + i * 70 + 25)], P["blue"]["stroke"], 2)
        s.box(980, 268 + i * 70, 300, 50, f"{c} · {lab}", "blue", 21, fill=P["blue"]["soft"])
    s.text(830, 495, "Limited mutual intelligibility, Latin and\nArabic-based scripts: an unqualified\n"
                     "'Kurdish' in a paper is ambiguous.", 21)
    s.box(70, 615, 1460, 110, None, "gray", fill=P["gray"]["soft"])
    s.text(95, 630, "Language or dialect?", 24, P["gray"]["text"])
    s.text(95, 668, "Laki: a Kurdish dialect to some, a separate language to others.  Bakhtiari: its own code, yet Persian "
                    "speakers\nsometimes treat all Luri as Persian.  These choices decide what data is labelled and who gets "
                    "tools.", 20)
    s.takeaway("A model trained on 'fas' or 'Kurdish' may not serve the people the label suggests.", y=745)
    s.footer(SRC + ", §2.1")
    return s


# ======================================================================= Part II: method
def s_method(n):
    s = Slide("07-method", n)
    s.title("From 5,878 candidates to 495 papers", part=PART2, pc="purple")
    y = 200
    s.box(70, y, 270, 170, "Search\nGoogle Scholar\nACL Anthology\nSemantic Scholar", "gray", 21)
    harrow(s, 344, 394, y + 85)
    s.box(398, y, 230, 170, "5,878\ncandidates\n2020 – May 2026", "purple", 23)
    harrow(s, 632, 682, y + 85)
    s.box(686, y, 270, 170, "Qwen3.5-9B\nstage 1:\nrelevance filter", "blue", 22)
    harrow(s, 960, 1010, y + 85)
    s.box(1014, y, 270, 170, "Qwen3.5-9B\nstage 2:\nannotate 6 fields", "blue", 22)
    harrow(s, 1288, 1338, y + 85)
    s.box(1342, y, 190, 170, "495\npapers", "green", 30)
    s.text(70, 395, "Query: every Iranic language name and ISO code × NLP task terms (sentiment, QA, summarization, "
                    "benchmark, corpus, …),\nplus targeted searches and citation tracing.", 20, P["muted"])
    panel(s, 70, 475, 700, 240, "The six annotated fields",
          "1 language(s)   2 NLP task   3 resource type\n4 public availability   5 year   6 venue\n\n"
          "then deduplication; multilingual papers\ncount once per language", "blue", 25, 21)
    panel(s, 800, 475, 730, 240, "Quality control and caveat",
          "• every annotation checked by two of us;\n  a third author breaks ties\n"
          "• prompts and code are public\n• 'no resource exists' means: none publicly\n"
          "  documented was found in this search", "purple", 25, 21)
    s.takeaway("An LLM does the first pass; humans check every label.", y=745)
    s.footer(SRC + ", §3")
    return s


# ======================================================================= Part III: landscape
def s_papers(n):
    s = Slide("08-papers-vs-speakers", n)
    s.title("Papers do not follow speakers", "Paper count and L1 speakers for the major languages", part=PART3,
            pc="red")
    rows = [("Persian", 394, 91), ("Kurdish", 93, 26), ("Pashto", 29, 51), ("Luri / Laki", 5, 5), ("Balochi", 4, 9),
            ("Mazanderani / Gilaki", 4, 5)]
    xl, xp, xs = 330, 360, 900
    s.text(xp, 160, "papers, 2020–2026", 21, P["purple"]["text"])
    s.text(xs, 160, "L1 speakers (millions)", 21, P["orange"]["text"])
    s.text(1500, 160, "papers per\nmillion speakers", 19, P["muted"], "r")
    for i, (l, p, sp) in enumerate(rows):
        y = 225 + i * 80
        s.text(xl, y + 18, l, 23, P["ink"], "r")
        wp = max(4, p / 394 * 440)
        s.box(xp, y, wp, 52, None, "purple", round_=False)
        s.text(xp + wp + 12, y + 12, str(p), 23)
        ws = max(4, sp / 91 * 380)
        s.box(xs, y, ws, 52, None, "orange", round_=False)
        s.text(xs + ws + 12, y + 12, f"{sp}M", 23)
        r = p / sp
        s.text(1500, y + 12, f"{r:.1f}", 26, P["red"]["text"] if r < 1 else P["ink"], "r")
    s.line([(xp, 210), (xp, 700)], P["ink"], 2)
    s.line([(xs, 210), (xs, 700)], P["ink"], 2)
    s.text(70, 712, "Persian: 80% of the papers, about 60% of the family's speakers. Red: fewer than one paper per "
                    "million speakers.", 21, P["muted"])
    s.takeaway("Pashto has twice Kurdish's speakers but a third of its papers.", y=760, h=58)
    s.footer(SRC + ", §3 and Figure 2; speakers from Table 1. Multilingual papers count once per language")
    return s


def s_timeline(n):
    s = Slide("09-timeline", n)
    s.title("The field is growing, but mostly in Persian", "Surveyed papers per year", part=PART3, pc="red")
    yrs = [(2020, 54), (2021, 43), (2022, 64), (2023, 85), (2024, 87), (2025, 131), (2026, 65)]
    x, y, w, h = 160, 190, 900, 470
    Y = s.axes(x, y, w, h, 0, 150, [0, 50, 100, 150], fs=19)
    slot = w / len(yrs)
    for i, (yr, v) in enumerate(yrs):
        bx = x + i * slot + 22
        part = yr == 2026
        s.box(bx, Y(v), slot - 44, Y(0) - Y(v), None, "gray" if part else "purple", round_=False, dashed=part,
              fill="#ffffff" if part else None)
        s.text(bx + (slot - 44) / 2, Y(v) - 8, str(v), 24, P["ink"], "c", "b")
        s.text(bx + (slot - 44) / 2, y + h + 12, str(yr) + ("\nto May" if part else ""), 20, P["ink"], "c")
    panel(s, 1110, 190, 420, 470, "Reading the bars",
          "• 54 papers in 2020,\n  131 in 2025\n\n• growth is driven almost\n  entirely by Persian\n\n"
          "• Kurdish and Pashto grow\n  modestly; the other\n  varieties stay near zero\n\n"
          "• 2026 is partial: the\n  search ended in May", "purple", 26, 21)
    s.takeaway("More papers do not mean more languages.", y=745)
    s.footer(SRC + ", §3 and Figure 3 (values read from the figure)")
    return s


def s_tasks(n):
    s = Slide("10-tasks", n)
    s.title("Which tasks get studied", "Papers per NLP task; a paper with several tasks counts once per task",
            part=PART3, pc="red")
    tasks = [("Sentiment analysis", 116), ("Text classification", 70), ("Language modeling", 59),
             ("Question answering", 59), ("Machine translation", 41), ("Named entities", 38),
             ("Information extraction", 36), ("Morphology & syntax", 32), ("Information retrieval", 25),
             ("Lexical semantics", 24), ("Summarization", 10), ("Dialogue", 10), ("Text generation", 9)]
    x0 = 400
    for i, (t, v) in enumerate(tasks):
        y = 165 + i * 43
        s.text(x0 - 16, y + 4, t, 21, P["ink"], "r")
        wv = v / 116 * 560
        s.box(x0, y, wv, 34, None, "yellow" if i else "orange", round_=False, sw=1.5,
              fill=None if i else P["orange"]["fill"])
        s.text(x0 + wv + 10, y + 3, str(v), 21)
    panel(s, 1080, 165, 450, 545, "What stands out",
          "• classification-style tasks\n  dominate: sentiment alone\n  has 116 papers\n\n"
          "• generation and dialogue\n  have about 10 each\n\n• most attention goes to\n  Persian in every task\n\n"
          "• for non-Persian varieties,\n  machine translation is the\n  most active area", "gray", 26, 21)
    s.takeaway("Classification dominates; generation and dialogue are barely studied.", y=745)
    s.footer(SRC + ", §1, §3 and Figure 4")
    return s


# ======================================================================= Part IV: infrastructure
def s_footprint(n):
    s = Slide("11-footprint", n)
    s.title("The digital footprint behind the papers", "Selected rows of our resource table (Table 2), with Arabic and"
            " Turkish for reference", part=PART4, pc="blue")
    rows = [["Arabic (ref.)", "106 GB", "1,293K", "74,093", "140,003", "✓ ✓ ✓ ✓"],
            ["Turkish (ref.)", "135 GB", "658K", "43,253", "275,460", "✓ ✓ ✓ ✓"],
            ["Persian", "102 GB", "1,075K", "19,248", "37,128", "✓ ✓ ✓ ✓"],
            ["N. Kurdish", "979 MB", "92K", "8,254", "216,370", "✓ ✓ ✓ ✓"],
            ["Tajik", "—", "118K", "430", "0", "✗ ✗ ✗ ✗"],
            ["Pashto", "—", "21K", "1,100", "6,945", "✗ ✗ ✗ ✗"],
            ["Gilaki", "16.4 MB", "48K", "34", "0", "✓ ✗ ✗ ✗"],
            ["Mazanderani", "1.7 MB", "65K", "337", "0", "✗ ✗ ✗ ✗"],
            ["Balochi", "—", "1.2K", "429", "0", "✗ ✗ ✗ ✗"],
            ["Laki", "57.7 KB", "Incubator", "85", "0", "✓ ✗ ✗ ✗"],
            ["N. Luri", "82.7 KB", "—", "5", "0", "✓ ✗ ✗ ✗"]]
    red = P["red"]["text"]
    colors = []
    for r in rows:
        colors.append([P["ink"]] + [red if v in ("—", "0", "34", "5", "85", "Incubator") else P["ink"] for v in r[1:5]]
                      + [P["green"]["text"] if r[5].startswith("✓ ✓") else red])
    s.table(70, 160, [260, 220, 220, 220, 260, 280], rows,
            header=["language", "FineWeb2 web text", "Wikipedia articles", "Wiktionary entries",
                    "UniMorph forms", "grammar · WordNet\nspell · ASR"],
            fs=21, rh=42, hc="blue", aligns=["l", "r", "r", "r", "r", "c"], colors=colors, hl_rows={2: "orange"})
    s.text(70, 722, "— = no data. Red = absent or tiny. Tools: ✓ available, ✗ absent.", 19, P["muted"])
    s.takeaway("Below Persian and Kurmanji, the columns thin out fast.", y=760, h=58)
    s.footer(SRC + ", Table 2 (Appendix)")
    return s


def s_wiki(n):
    s = Slide("12-wikipedia", n)
    s.title("Wikipedia: present, absent, or hollow", part=PART4, pc="blue")
    # 97 individual varieties bar
    s.text(70, 150, "The 97 individual varieties (May 2026)", 24)
    x, y, sc = 70, 195, 15
    for k, lab, c in [(10, "10 active\nWikipedias", "green"), (11, "11 Incubator\nonly", "yellow"),
                      (76, "76 with no Wikipedia presence", "red")]:
        s.box(x, y, k * sc, 60, None, c, round_=False)
        s.text(x + k * sc / 2, y + 72, lab, 19, P[c]["text"] if c != "yellow" else P["muted"], "c")
        x += k * sc
    # hollow
    s.text(70, 365, "Hollow presence: many articles, almost no dictionary", 24)
    langs = [("Persian", 1075000, 19248), ("N. Kurdish", 92000, 8254), ("Mazanderani", 65000, 337),
             ("Gilaki", 48000, 34)]
    X0, XW = 280, 560
    for i, (l, wp, wt) in enumerate(langs):
        yy = 420 + i * 62
        hol = l in ("Mazanderani", "Gilaki")
        s.text(X0 - 14, yy + 6, l, 22, P["red"]["text"] if hol else P["ink"], "r")
        s.box(X0, yy, logx(wp, 10, 2e6, X0, XW) - X0, 40, None, "blue", round_=False)
        s.box(logx(wt, 10, 2e6, X0, XW) - 9, yy + 11, 18, 18, None, "orange", shape="ellipse")
        s.text(logx(wp, 10, 2e6, X0, XW) + 10, yy + 6, f"{wp // 1000:,}K / {wt:,}", 20, P["muted"])
    s.box(X0, 676, 30, 20, None, "blue", round_=False)
    s.text(X0 + 40, 672, "Wikipedia articles", 19)
    s.box(X0 + 250, 677, 18, 18, None, "orange", shape="ellipse")
    s.text(X0 + 278, 672, "Wiktionary entries (log scale)", 19)
    panel(s, 1110, 365, 420, 330, "A failed Wikipedia",
          "The Northern Luri Wikipedia\nwas abandoned: reviewers\nfound Persian with light\nword substitution, not\n"
          "native Luri grammar.", "red", 25, 21)
    s.takeaway("Article counts can hide how little real language data there is.", y=745)
    s.footer(SRC + ", §4 and Table 2")
    return s


def s_morph(n):
    s = Slide("13-morphology", n)
    s.title("Morphology: rich languages, thin resources", part=PART4, pc="blue")
    panel(s, 70, 150, 560, 400, "Why morphology matters here",
          "• Persian: Ezafe construction and\n  rich verb inflection\n• Kurdish: split ergativity\n"
          "• Pashto: verbs agree with several\n  arguments at once\n• Pamir languages: up to five\n  agreement slots per verb",
          "gray", 26, 21)
    s.text(680, 150, "UniMorph paradigms (lemmata)", 24)
    rows = [("N. Kurdish", 15083), ("Pashto", 395), ("C. Kurdish", 274), ("Persian", 273), ("S. Kurdish", 1)]
    X0, XW = 880, 560
    for i, (l, v) in enumerate(rows):
        yy = 205 + i * 62
        s.text(X0 - 14, yy + 6, l, 22, P["ink"], "r")
        wv = logx(v, 0.8, 20000, X0, XW) - X0
        s.box(X0, yy, max(4, wv), 40, None, "orange" if l == "Persian" else "blue", round_=False)
        s.text(X0 + max(4, wv) + 10, yy + 6, f"{v:,}", 22)
    s.text(X0, 520, "log scale", 18, P["muted"])
    s.text(680, 565, "Zero: Balochi, Talysh, Mazanderani, Gilaki, Gorani, Luri, Laki, Tajik, Zazaki", 21,
           P["red"]["text"])
    s.box(70, 615, 1460, 100, None, "gray", fill=P["gray"]["soft"])
    s.text(95, 630, "Tools: Persian has Hazm, DadmaTools and Parsivar; no equivalent exists for any other variety.\n"
                    "Treebanks: Persian UD, Kurmanji UD and Central Kurdish–Mukri only.", 21)
    s.takeaway("Persian has the text but only 273 paradigms; Kurmanji has 15,083.", y=745)
    s.footer(SRC + ", §4 and Table 2")
    return s


def s_lid(n):
    s = Slide("14-lid", n)
    s.title("Language identification: the first filter", "Every web corpus is built by LID; confusable pairs make it hard",
            part=PART4, pc="blue")
    pairs = [("Persian", "Dari", "Tajik"), ("Luri", "Persian", None), ("Talysh", "Azerbaijani", None)]
    y = 170
    s.text(70, y, "Hard to tell apart", 24)
    for i, p in enumerate(pairs):
        yy = y + 50 + i * 75
        x = 70
        for j, l in enumerate([q for q in p if q]):
            if j:
                s.text(x + 8, yy + 8, "↔", 26, P["red"]["text"])
                x += 46
            x = chip(s, x, yy, l, "gray", 21, fill="#ffffff") + 4
    s.text(70, 420, "Shared vocabulary (Persian, Dari, Tajik)\nor heavy contact (Luri, Talysh).", 21, P["muted"])
    s.text(70, 510, "GlotLID V3 covers 16 Iranic\nvariety-script pairs; PALI is a LID\nbenchmark for Perso-Arabic "
                    "script\nwith six Iranic varieties.", 21)
    # F1 bars
    f1 = [("Laki", .800), ("N. Luri", .909), ("Persian", .922), ("Mazanderani", .958), ("Gilaki", .968),
          ("C. Kurdish", .969), ("Gorani", .982), ("S. Kurdish", .982), ("Zazaki", .987), ("Pashto", .990),
          ("Balochi", .990), ("Talysh", .993), ("Tajik", .996), ("N. Kurdish", .997)]
    s.text(820, 160, "GlotLID V3 F1 (axis starts at 0.75)", 22)
    X0, XW = 990, 450
    for i, (l, v) in enumerate(f1):
        yy = 205 + i * 37
        s.text(X0 - 12, yy + 2, l, 19, P["ink"], "r")
        wv = (v - 0.75) / 0.25 * XW
        low = v < 0.93
        s.box(X0, yy, wv, 28, None, "red" if low else "blue", round_=False, sw=1)
        s.text(X0 + wv + 8, yy + 1, f"{v:.3f}", 19, P["red"]["text"] if low else P["ink"])
    s.takeaway("Even a high F1 can hide false positives that swamp a small language's corpus.", y=745)
    s.footer(SRC + ", §4 and Table 2 (Pashto and Balochi F1 reported for pbt and bcc)")
    return s


def s_parallel(n):
    s = Slide("15-parallel-english", n)
    s.title("Parallel data with English: three tiers", "Sentence pairs with English, log scale", part=PART4, pc="blue")
    par = [("Persian", 612200000, "612M"), ("Kurdish", 510633, "511K"), ("Gorani", 22497, "22K"),
           ("Gilaki", 9030, "9K"), ("Laki", 4633, "4.6K"), ("Mazanderani", 4483, "4.5K"), ("Zazaki", 4401, "4.4K"),
           ("Talysh", 2106, "2.1K"), ("S. Luri", 1997, "2K"), ("Balochi", 110, "110")]
    X0, XW = 300, 760
    for t in (10, 1e3, 1e5, 1e7, 1e9):
        xx = logx(t, 10, 1e9, X0, XW)
        s.line([(xx, 165), (xx, 640)], P["grid"], 1, roughness=0)
        s.text(xx, 648, {10: "10", 1e3: "1K", 1e5: "100K", 1e7: "10M", 1e9: "1B"}[t], 18, P["muted"], "c")
    for i, (l, v, lab) in enumerate(par):
        yy = 170 + i * 47
        c = "orange" if i == 0 else "blue" if i == 1 else "red" if l == "Balochi" else "gray"
        s.text(X0 - 14, yy + 3, l, 22, P["ink"], "r")
        s.box(X0, yy, logx(v, 10, 1e9, X0, XW) - X0, 36, None, c, round_=False, sw=1.5,
              fill=None if c != "gray" else P["blue"]["soft"], stroke=None if c != "gray" else P["blue"]["stroke"])
        s.text(logx(v, 10, 1e9, X0, XW) + 10, yy + 3, lab, 22)
    panel(s, 1120, 165, 410, 500, "Three tiers",
          "1  Persian: over 600M pairs\n   (web crawls, subtitles,\n   NLLB-200)\n\n"
          "2  Kurdish: about 511K\n   (Kurdish Parallel Corpus,\n   plus SMOL and PARME)\n\n"
          "3  everyone else: under 40K\n   in total; Balochi: 110", "blue", 26, 21)
    s.takeaway("Persian has over five million times as many English pairs as Balochi.", y=745)
    s.footer(SRC + ", §4 and Table 3")
    return s


def s_matrix(n):
    s = Slide("16-parallel-matrix", n)
    s.title("Between the smaller varieties: almost nothing", "Parallel sentence pairs between Iranic varieties",
            part=PART4, pc="blue")
    codes = ["en", "fas", "kur", "glk", "mzn", "tly", "lki", "luz", "hac", "diq"]
    rowsc = ["fas", "kur", "glk", "mzn", "tly", "lki", "luz", "hac", "diq", "bal"]
    M = {"fas": [612200000], "kur": [510633, 325834], "glk": [9030, 5496, 488], "mzn": [4483, 5127, 1644, 1108],
         "tly": [2106, 2106, 1581, 54, 851], "lki": [4633, 3412, 994, 437, 3011, 849],
         "luz": [1997, 1997, 994, 39, 1396, 785, 1235], "hac": [22497, 7792, 1574, 1957, 1284, 409, 723, 934],
         "diq": [4401, 4401, 3331, 0, 0, 0, 0, 0, 0], "bal": [110, 30, 35, 0, 0, 0, 0, 0, 0, 0]}

    def lab(v):
        if v >= 1e6:
            return f"{v / 1e6:.0f}M"
        if v >= 1e4:
            return f"{v / 1e3:.0f}K"
        if v >= 1e3:
            return f"{v / 1e3:.1f}K".replace(".0K", "K")
        return str(v)

    def col(v):
        if v == 0:
            return "#f1f3f5", P["red"]["text"]
        if v > 1e5:
            return "#1c4f8f", "#ffffff"
        if v > 1e4:
            return "#4a7fc4", "#ffffff"
        if v > 1e3:
            return "#a9c8ee", P["ink"]
        return "#e3eefb", P["ink"]

    x0, y0, cw, ch = 170, 190, 78, 50
    for j, c in enumerate(codes):
        s.text(x0 + j * cw + cw / 2, y0 - 34, c, 20, P["muted"], "c", mono=True)
    for i, r in enumerate(rowsc):
        s.text(x0 - 14, y0 + i * ch + ch / 2, r, 20, P["muted"], "r", "m", mono=True)
        for j, v in enumerate(M[r]):
            fill, tc = col(v)
            s.box(x0 + j * cw + 2, y0 + i * ch + 2, cw - 4, ch - 4, None, "gray", fill=fill, stroke="#ffffff",
                  round_=False, sw=1)
            s.text(x0 + j * cw + cw / 2, y0 + i * ch + ch / 2, lab(v), 17, tc, "c", "m")
    panel(s, 1000, 175, 530, 520, "What the matrix shows",
          "• below Persian and Kurdish,\n  at most a few thousand\n  pairs for any pair\n\n"
          "• Zazaki: 0 pairs with all six\n  smaller varieties\n\n• Balochi: 30 with Persian,\n  35 with Kurdish, 0 otherwise\n\n"
          "• Kurmanji–Sorani is the only\n  substantial intra-Iranic\n  MT corpus", "blue", 26, 21)
    s.text(170, 712, "fas = Persian, kur = Kurdish, glk = Gilaki, mzn = Mazanderani, tly = Talysh, lki = Laki,\n"
                     "luz = S. Luri, hac = Gorani, diq = Zazaki, bal = Balochi", 18, P["muted"])
    s.takeaway("Translation between neighbours has to go through Persian or English.", y=770, h=58)
    s.footer(SRC + ", Table 3 and §4")
    return s


# ======================================================================= Part V: tasks
def s_task_status(n):
    s = Slide("17-task-status", n)
    s.title("Task by task: Persian and everyone else", part=PART5, pc="green")
    rows = [("Pretraining", "ParsBERT; Matina corpus (73B tokens) and LLM;\nFarsInstruct (21 instruction datasets)",
             "Kurdish: KuBERT, KurdBERT; Pashto: Ps-BERT.\nOthers: no monolingual model; XLM-R, Glot500"),
            ("Benchmarks", "ParsiNLU (14,500+ items, natively written);\nKhayyam (50+ domains); cultural benchmarks",
             "Belebele (translated): Tajik, Sorani, S. Pashto.\nAPARSIN: first beyond the top five varieties"),
            ("Question answering", "25+ datasets: PQuAD (80K), PersianMHQA (7K),\nPersianMedQA (20K)",
             "one Sorani news dataset;\nno natively written QA for any other variety"),
            ("Speech", "DeepMine (480+ h ASR), ParsVoice (3,526 h TTS)",
             "Sorani: JIRA, CORDI. DOLMA: 40+ h for six varieties\n(Zazaki 0.2 h); Whisper WER 37.9–89.5%"),
            ("OCR, vision", "VQA, captioning, printed/handwritten OCR", "essentially absent"),
            ("NER, classification,\nsummarization", "well studied", "no annotated data")]
    x, y = 70, 150
    s.box(x + 270, y, 590, 44, "Persian", "orange", 22, round_=False, sw=1)
    s.box(x + 870, y, 590, 44, "other Iranic varieties", "red", 22, round_=False, sw=1)
    y += 54
    for i, (t, a, b) in enumerate(rows):
        h = 86 if i < 4 else 62
        s.box(x, y, 1460, h, None, "gray", fill="#f8f9fa" if i % 2 == 0 else "#ffffff", stroke="transparent",
              round_=False, sw=1)
        s.text(x + 12, y + h / 2, t, 21, P["green"]["text"], "l", "m")
        s.text(x + 285, y + h / 2, a, 20, P["ink"], "l", "m")
        s.text(x + 885, y + h / 2, b, 20, P["red"]["text"] if b in ("essentially absent", "no annotated data")
               else P["ink"], "l", "m")
        y += h + 6
    s.takeaway("For most varieties, the first dataset of any kind is still to be built.", y=760, h=58)
    s.footer(SRC + ", §5")
    return s


def s_saturation(n):
    s = Slide("18-saturation", n)
    s.title("Persian: saturating and still open", part=PART5, pc="green")
    panel(s, 70, 160, 700, 300, "Approaching saturation",
          "• standard sentiment classification\n• Wikipedia-based reading comprehension\n• named entity recognition\n\n"
          "Many benchmarks are translated from\nEnglish (ParSQuAD from SQuAD).", "gray", 28, 22)
    panel(s, 830, 160, 700, 300, "Open frontiers",
          "• cultural and pragmatic competence\n• multi-hop reasoning\n• code-switching\n• robustness to dialects and"
          " colloquial\n  Persian (HarfoSokhan: 6M colloquial→\n  formal pairs)", "green", 28, 22)
    s.box(70, 490, 1460, 220, None, "orange", fill=P["orange"]["soft"])
    s.text(95, 505, "Example: taarof (ritual politeness)", 26, P["orange"]["text"])
    s.text(95, 550, "TaarofBench: LLMs score 40–48% below native Persian speakers on taarof scenarios.\n"
                    "Frontier models do well on factual recall but show gaps in cultural knowledge and pragmatic judgment\n"
                    "(Khayyam, FarsEval-PKBETS, ELAB). Taarof is absent from all existing evaluation frameworks.", 22)
    s.takeaway("Persian needs new kinds of tests; the other varieties need a first test.", y=745)
    s.footer(SRC + ", §5–§7")
    return s


def s_transfer(n):
    s = Slide("19-transfer", n)
    s.title("Transfer from relatives: the main strategy", part=PART5, pc="green")
    items = [("lexical", "Persian, Dari and Tajik share most\nvocabulary: strong zero-shot transfer,\n"
                         "given correct script normalization", "orange"),
             ("script", "all Perso-Arabic varieties share\ntokenization conventions, but Unicode\n"
                        "differences silently degrade transfer", "blue"),
             ("grammatical", "varieties in one branch share\nmorphology, e.g. Kurmanji → Sorani MT;\n"
                             "script normalization helps Kurdish", "green")]
    for i, (h, b, c) in enumerate(items):
        panel(s, 70 + i * 495, 160, 465, 270, h + " proximity", b, c, 28, 22)
    s.box(70, 470, 1460, 240, None, "gray", fill=P["gray"]["soft"])
    s.text(95, 485, "In practice", 26, P["gray"]["text"])
    s.text(95, 530, "• cross-lingual transfer runs almost entirely through Persian or English as pivots\n"
                    "• a multilingual model that covers Persian does not cover Dari unless Dari data was included\n"
                    "• tokenizers are calibrated for high-resource languages and over-segment related varieties\n"
                    "• systematic intra-family transfer studies are still lacking", 22)
    s.takeaway("Relatedness is an asset, but nobody has measured it systematically yet.", y=745)
    s.footer(SRC + ", §6 and §7")
    return s


# ======================================================================= Part VI: challenges
def s_script(n):
    s = Slide("20-script", n)
    s.title("Same letter, different bytes", "Script heterogeneity: a concrete source of silent failures",
            part=PART6, pc="red")
    ex = [("yeh", "ی", "U+06CC Farsi yeh", "ي", "U+064A Arabic yeh"),
          ("kaf", "ک", "U+06A9 keheh", "ك", "U+0643 Arabic kaf")]
    for i, (nm, a, ca, b, cb) in enumerate(ex):
        y = 170 + i * 150
        s.text(70, y + 40, nm, 26, P["muted"])
        s.box(190, y, 130, 120, None, "gray", fill="#ffffff")
        s.text(255, y + 60, a, 60, P["ink"], "c", "m")
        s.text(340, y + 44, ca, 21, P["ink"], mono=True)
        s.text(640, y + 44, "≠", 40, P["red"]["text"])
        s.box(720, y, 130, 120, None, "gray", fill="#ffffff")
        s.text(785, y + 60, b, 60, P["ink"], "c", "m")
        s.text(870, y + 44, cb, 21, P["ink"], mono=True)
    s.text(70, 480, "In practice, ya and kaf code points differ across Persian, Pashto and Dari text, so string matching, "
                    "deduplication\nand tokenization break without any error message. (Code points shown here as an"
                    " illustration.)", 20, P["muted"])
    panel(s, 1180, 160, 350, 290, "More of the same",
          "• ZWNJ inside Persian\n  compounds\n• right-to-left mixed\n  with Latin text\n• Kurmanji in Latin,\n"
          "  Arabic or Cyrillic", "red", 25, 20)
    s.box(70, 560, 1460, 150, None, "gray", fill=P["gray"]["soft"])
    s.text(95, 575, "Scripts in use", 24, P["gray"]["text"])
    s.text(95, 615, "About a dozen scripts across the family, most only historical. Living varieties use Perso-Arabic,"
                    " Latin and\nCyrillic, often in parallel; Tajik uses Cyrillic only. Priority: one shared Iranic"
                    " normalization library.", 21)
    s.takeaway("Normalize before you train, or related varieties look unrelated.", y=745)
    s.footer(SRC + ", §7 (script heterogeneity)")
    return s


def s_challenges(n):
    s = Slide("21-challenges", n)
    s.title("Six open challenges, one priority each", part=PART6, pc="red")
    items = [("Resource concentration", "Persian ≈ 80% of papers; Pashto (51M)\nhas fewer resources than Kurdish",
              "shared tasks and central data hubs"),
             ("Script heterogeneity", "Perso-Arabic, Latin, Cyrillic;\ninconsistent code points; ZWNJ",
              "a unified Iranic normalization library"),
             ("Dialectal fragmentation", "most benchmarks test only the\nstandard written form",
              "colloquial and regional benchmarks"),
             ("Cultural misalignment", "translated benchmarks; Persian\nsentiment, QA, NER near saturation",
              "benchmarks co-created with speakers"),
             ("Endangered varieties", "Pamir and Central Plateau varieties\nmay disappear within decades",
              "multilingual speech models,\ncommunity recording"),
             ("Structural inequity", "sanctions limit compute, API access\nand travel for many researchers",
              "compute and access programs")]
    for i, (h, b, p) in enumerate(items):
        x = 70 + (i % 3) * 495
        y = 160 + (i // 3) * 290
        s.box(x, y, 465, 265, None, "red", fill=P["red"]["soft"])
        s.text(x + 20, y + 16, h, 27, P["red"]["text"])
        s.text(x + 20, y + 62, b, 22, P["ink"])
        s.box(x + 15, y + 145, 435, 105, None, "green", fill=P["green"]["soft"], sw=1.5)
        s.text(x + 30, y + 153, "priority", 18, P["green"]["text"])
        s.text(x + 30, y + 182, p, 22, P["ink"])
    s.footer(SRC + ", §7")
    return s


def s_priorities(n):
    s = Slide("22-priorities", n)
    s.title("Three things the community can do now", part=PART6, pc="red")
    items = [("1 · Raw text", "orange",
              "Put Iranic text on the open web,\nin identifiable form.\n\nWeb crawls feed every corpus;\n"
              "untagged or mistagged text is\ninvisible to LID-filtered\npipelines."),
             ("2 · Translation benchmarks", "blue",
              "Contribute to FLORES+ / OLDI.\n\nFLORES+ grew from about 200\nto 230 varieties, but still has\n"
              "the same 6 Iranic ones as\nFLORES-200: pes, prs, tgk,\nckb, kmr, pbt."),
             ("3 · Evaluation beyond MT", "green",
              "At least one natively written\nbenchmark per variety.\n\nShared tasks are the most\n"
              "plausible way to get them.")]
    for i, (h, c, b) in enumerate(items):
        panel(s, 70 + i * 495, 160, 465, 450, h, b, c, 30, 24)
    s.box(70, 630, 1460, 90, None, "gray", fill=P["gray"]["soft"])
    s.text(95, 645, "About 2K sentences per variety and an open pull-request process: the bottleneck is people, not"
                    "\ninfrastructure. The lesson from African NLP: community shared tasks and data hubs catalyse progress.",
           20)
    s.takeaway("None of these needs a new model; they need contributors.", y=745)
    s.footer(SRC + ", §7 (priorities box)")
    return s


# ======================================================================= Part VII: discussion
def s_critique(n):
    s = Slide("23-scope", n)
    s.title("Contributions, scope and next steps", part=PART7, pc="yellow")
    panel(s, 70, 160, 680, 580, "What this survey contributes",
          "• the first systematic map of NLP for\n  the whole family (101 codes)\n\n"
          "• beyond paper counts: an audit of\n  corpora, Wikipedia, morphology,\n  LID and parallel data\n\n"
          "• conservative wording: 'not found'\n  rather than 'does not exist'\n\n"
          "• concrete, low-cost priorities, plus a\n  companion website and public code", "green", 30, 23)
    panel(s, 780, 160, 750, 580, "Scope, and where we go next",
          "• we searched indexed venues in English;\n  Persian-language journals are a natural\n  next addition to the live index\n\n"
          "• LLM-assisted screening, checked by people;\n  a recall audit of the filter is future work\n\n"
          "• the NLP levels summarise resources at a\n  glance; a scoring rule would make them\n  reproducible\n\n"
          "• paper counts show attention, not quality,\n  and reflect sanctions and access limits", "blue", 30, 22)
    s.footer(SRC + ", §3, Limitations, Ethical considerations")
    return s


def s_takeaways(n):
    s = Slide("24-takeaways", n)
    s.title("Takeaways", part=PART7, pc="yellow")
    items = [("red", "1 · One variety gets the attention", "Iranian Persian: 394 of 495 papers (80%). Pashto (51M) "
                                                          "has 29, Balochi (9M) has 4."),
             ("blue", "2 · The gap starts below the papers", "Little or no web text, dictionary entries, UniMorph paradigms or "
                                                            "tools for most varieties; under 40K parallel pairs."),
             ("purple", "3 · Labels and scripts are part of the problem", "Macrolanguage codes, contested "
                                                                         "dialect status and inconsistent Unicode "
                                                                         "hide varieties from pipelines."),
             ("green", "4 · Persian needs new tests, the rest need first tests", "Persian is saturating on standard "
                                                                               "tasks; cultural and pragmatic "
                                                                               "competence is open."),
             ("orange", "5 · Small contributions go far", "Tagged web text, FLORES+ sentences, one native "
                                                       "benchmark per variety.")]
    for i, (c, a, b) in enumerate(items):
        y = 150 + i * 122
        s.box(70, y, 1460, 106, None, c, fill=P[c]["soft"])
        s.text(95, y + 14, a, 26, P[c]["text"])
        s.text(95, y + 54, b, 21, P["ink"])
    s.text(70, 775, "sigiranic.github.io  ·  github.com/sigiranic/sigiranic.github.io", 21, P["muted"], mono=True)
    s.footer("")
    return s


SLIDES = [s_title, s_tldr, s_glossary,
          s_family, s_languages, s_labels,
          s_method,
          s_papers, s_timeline, s_tasks,
          s_footprint, s_wiki, s_morph, s_lid, s_parallel, s_matrix,
          s_task_status, s_saturation, s_transfer,
          s_script, s_challenges, s_priorities,
          s_critique, s_takeaways]

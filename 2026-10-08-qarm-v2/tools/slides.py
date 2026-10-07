"""QARM V2 paper-club deck: one function per slide; the order is the SLIDES list at the bottom.

Numbers come only from references/digest.md (which cites the paper's tables and sections).
Colour code: orange = problem / ID-based baseline, blue = QARM V2, gray = QARM (2024) / neutral,
green = gain, purple = measurement / evaluation, yellow = takeaway.
"""
import math
import random

from slidekit import P, Slide, W, text_width

PART1 = "Part I · Background"
PART2 = "Part II · GSU side: reasoning item alignment"
PART3 = "Part III · ESU side: Res-KmeansFSQ semantic IDs"
PART4 = "Part IV · Results"
PART5 = "Part V · Discussion"
V2 = "QARM V2 (arXiv:2602.08559)"
V1 = "QARM (arXiv:2411.11739)"


def panel(s, x, y, w, h, head, body, c, hfs=26, bfs=22, fill=None):
    s.box(x, y, w, h, None, c, fill=fill or P[c]["soft"])
    s.text(x + 22, y + 16, head, hfs, P[c]["text"])
    if body:
        s.text(x + 22, y + 16 + hfs * 1.25 + 14, body, bfs, P["ink"])


def chip(s, x, y, label, c, fs=21, h=46, pad=18, mono=False):
    w = text_width(label, fs, mono) + 2 * pad
    s.box(x, y, w, h, label, c, fs, mono=mono)
    return x + w


def harrow(s, x0, x1, y, c=None, dashed=False):
    s.arrow([(x0, y), (x1, y)], c or P["ink"], dashed=dashed)


def varrow(s, x, y0, y1, c=None):
    s.arrow([(x, y0), (x, y1)], c or P["ink"])


# ======================================================================= opening
def s_title(n):
    s = Slide("01-title", n)
    s.text(70, 120, "PAPER CLUB · 8 OCTOBER 2026", 20, P["muted"])
    s.text(70, 165, "QARM V2", 84)
    s.text(72, 280, "Quantitative Alignment Multi-Modal Recommendation\nfor Reasoning User Sequence Modeling", 36, P["ink"])
    s.text(72, 400, "Tian Xia, Jiaqi Zhang, Yueyang Liu, Hongjian Dou, Tingya Yin, Jiangxia Cao, et al. (28 authors)\n"
                    "Kuaishou Technology, Beijing", 22, P["muted"])
    s.text(72, 470, "arXiv:2602.08559 (Feb 2026)   ·   predecessor QARM: arXiv:2411.11739 (Nov 2024)", 20, P["muted"], mono=True)
    # the idea in one row
    y = 600
    x = 72
    for i, (t, c) in enumerate([("item: title, images, OCR", "gray"), ("fine-tuned LLM", "blue"),
                                ("embedding  →  GSU", "blue"), ("semantic IDs  →  ESU", "blue"),
                                ("CTR / CVR", "green")]):
        x2 = chip(s, x, y, t, c, 22, 60, 22)
        if i < 4:
            harrow(s, x2 + 6, x2 + 40, y + 30)
        x = x2 + 46
    s.text(72, 700, "How to make LLM item understanding useful inside an industrial ranking model.", 26, P["blue"]["text"])
    s.footer("Slides drawn in Excalidraw; all numbers are from the two papers (see references/digest.md)")
    return s


def s_tldr(n):
    s = Slide("02-tldr", n)
    s.title("The paper in one slide")
    cols = [("Problem", "orange",
             "LLM item embeddings help a\nrecommender only a little:\n\n• their notion of 'similar' is\n  not the business notion\n  (representation unmatch)\n\n• cached embeddings are frozen,\n  so the ranker cannot learn them\n  (representation unlearning)"),
            ("Two fixes", "blue",
             "GSU (retrieval):\n• a reasoning LLM filters the\n  item pairs used for alignment\n• one LLM, three segments:\n  contrastive + next-token loss\n\nESU (ranking):\n• 2 × Res-Kmeans + 1 × FSQ\n  → semantic IDs, fewer collisions"),
            ("Evidence", "green",
             "Online A/B, multi-week:\n• ads revenue +4.873%\n• shopping GMV +1.0 to +5.6%\n\nOffline:\n• GAUC +0.05 to +1.10 points\n• SID collision 77.92% → 32.39%\n• retrieval HR@200 (click)\n  7.77% → 12.5%")]
    for i, (h, c, b) in enumerate(cols):
        panel(s, 70 + i * 495, 160, 465, 545, h, b, c, 32, 25)
    s.takeaway("An industrial paper: strong deployment evidence, few ablations, several loose ends to discuss.", y=735)
    s.footer(V2 + ": abstract, Tables 5, 6, 8, 9")
    return s


# ======================================================================= background
def s_setting(n):
    s = Slide("03-setting", n)
    s.title("Setting: Kuaishou, short video and live streaming", part=PART1, pc="gray")
    stats = [("400M+", "daily active users", "gray"), ("10M+", "new items uploaded\nevery day", "gray"),
             ("100,000+", "interactions in the history\nof each active user", "orange")]
    for i, (a, b, c) in enumerate(stats):
        x = 70 + i * 495
        s.box(x, 165, 465, 220, None, c, fill=P[c]["soft"])
        s.text(x + 232, 190, a, 64, P[c]["text"] if c != "gray" else P["ink"], "c")
        s.text(x + 232, 285, b, 24, P["ink"], "c")
    s.text(70, 430, "One ranking model serves ads, shopping and live streaming. It predicts CTR, CVR, gifts, follows …", 26)
    s.text(70, 480, "It should use the whole history, but scoring 100,000 items per candidate in streaming training is", 26)
    s.text(70, 518, "not affordable. Every lifelong model therefore first cuts the history down.", 26)
    s.box(70, 600, 1460, 150, None, "blue", fill=P["blue"]["soft"])
    s.text(95, 618, "Where LLMs come in", 26, P["blue"]["text"])
    s.text(95, 662, "Items are videos, live streams and products with titles, images, OCR and speech. An LLM can read them.\n"
                    "The question of both papers: how do we turn that understanding into something the ranker can use?", 23)
    s.footer(V2 + ", §1 (\"tens of millions of fresh new items … every day\")")
    return s


def s_gsu_esu(n):
    s = Slide("04-gsu-esu", n)
    s.title("Lifelong sequences: search first, then attend", "The two-stage paradigm of SIM and TWIN", part=PART1, pc="gray")
    # history strip
    s.text(70, 175, "user history (100,000+ items)", 22, P["muted"])
    for i in range(34):
        s.box(70 + i * 22, 210, 18, 34, None, "gray", round_=False, sw=1, roughness=0,
              fill=P["blue"]["fill"] if i in (3, 9, 17, 22, 30) else P["gray"]["fill"])
    s.text(830, 213, "…", 28, P["muted"])
    # target
    s.box(1100, 195, 230, 64, "target item", "green", 23)
    # GSU
    s.box(330, 320, 520, 120, None, "gray", fill=P["gray"]["soft"])
    s.text(350, 335, "GSU · General Search Unit", 26, P["ink"])
    s.text(350, 377, "keep the top-K history items most\nrelated to the target (cheap, not trained)", 21, P["muted"])
    varrow(s, 450, 250, 318)
    s.arrow([(1215, 262), (1215, 290), (840, 290), (790, 318)], P["ink"])
    # top-K
    s.text(70, 480, "top-K subsequence", 22, P["muted"])
    for i in range(5):
        s.box(330 + i * 40, 470, 32, 40, None, "blue", round_=False, sw=1, roughness=0)
    varrow(s, 430, 442, 466)
    # ESU
    s.box(330, 560, 520, 120, None, "blue", fill=P["blue"]["soft"])
    s.text(350, 575, "ESU · Exact Search Unit", 26, P["blue"]["text"])
    s.text(350, 617, "target attention over the K items\n(expensive, trained end-to-end)", 21, P["muted"])
    varrow(s, 430, 514, 558)
    s.arrow([(1215, 262), (1215, 588), (854, 588)], P["ink"])
    harrow(s, 852, 905, 662)
    s.box(910, 628, 280, 68, "MoE → CTR, CVR, …", "green", 22)
    # right explanation
    s.box(1250, 330, 290, 350, None, "orange", fill=P["orange"]["soft"])
    s.text(1270, 345, "What is 'related'?", 24, P["orange"]["text"])
    s.text(1270, 395, "SIM-hard: same tag\nSIM-soft / TWIN:\nsimilar ID embedding\n\nQARM V2:\nGSU → LLM embedding\nESU → semantic IDs", 21)
    s.takeaway("Both stages need an item similarity. QARM V2 supplies it from an LLM instead of from ID embeddings.", y=740)
    s.footer(V2 + ", §1 and §4.1 (SIM-hard / SIM-soft definitions)")
    return s


def s_ids_vs_llm(n):
    s = Slide("05-ids-vs-llm", n)
    s.title("Why not just IDs? Three weaknesses of ID embeddings", part=PART1, pc="gray")
    rows = [["Information units", "billions of user / item IDs,\ngrowing every day", "a fixed token vocabulary"],
            ["Knowledge storage", "in ID embeddings; one\ncross-attention layer", "in a deep transformer\n(40+ layers)"],
            ["Generalization", "needs real-time streaming\ntraining; stops → drops", "train once; stable\nlong-term inference"]]
    s.table(70, 170, [330, 520, 520], rows, header=["", "ID-based RecSys (weak)", "LLM (strong)"], fs=24, rh=95,
            hc="gray", aligns=["l", "l", "l"],
            colors=[[P["ink"], P["orange"]["text"], P["blue"]["text"]]] * 3)
    s.box(70, 600, 1460, 170, None, "gray", fill=P["paper"])
    s.text(95, 618, "Long-tail problem, made concrete", 25, P["ink"])
    s.text(95, 662, "A new item has no interactions yet, so its ID embedding is random: it cannot beat old, hot items.\n"
                    "Once an item is no longer distributed, everything its embedding learned is thrown away ('knowledge isolation').\n"
                    "An LLM reads the title and the images, so it knows what a new item is on day one.", 22)
    s.footer(V2 + ", §1 and Figure 1. Vocabulary size: '< 20,000 token IDs' in the text, '~1e5' in Figure 1")
    return s


def s_naive_llm(n):
    s = Slide("06-naive-llm", n)
    s.title("But plugging in LLM embeddings gives little", "The common practice: cache one embedding per item, add it as a feature", part=PART1, pc="orange")
    # unmatch
    s.box(70, 170, 715, 470, None, "orange", fill=P["orange"]["soft"])
    s.text(95, 188, "1 · Representation unmatch", 28, P["orange"]["text"])
    s.text(95, 240, "Pre-training learns image–text matching, captions,\nQA. The ranker needs click and purchase similarity.", 22)
    # toothpaste vs ointment
    for i, (lab, use) in enumerate([("toothpaste", "brush teeth"), ("ointment", "treat skin")]):
        x = 140 + i * 320
        s.box(x, 360, 210, 60, lab, "gray", 22, fill="#ffffff")
        s.text(x + 105, 435, use, 20, P["muted"], "c")
    s.arrow([(352, 390), (458, 390)], P["orange"]["stroke"], start="arrow")
    s.text(405, 335, "look alike", 19, P["orange"]["text"], "c")
    s.text(95, 500, "Same tube packaging → close embeddings.\nDifferent usage → should be far apart.", 22)
    # unlearning
    s.box(815, 170, 715, 470, None, "orange", fill=P["orange"]["soft"])
    s.text(840, 188, "2 · Representation unlearning", 28, P["orange"]["text"])
    s.text(840, 240, "A cached embedding is a fixed input. No gradient\nreaches it, so it cannot adapt to the ranking task\nor to the business as it drifts.", 22)
    s.box(880, 400, 180, 60, "LLM vector", "gray", 21, fill="#ffffff")
    harrow(s, 1064, 1170, 430)
    s.box(1175, 400, 230, 60, "ranking model", "blue", 21)
    s.text(1118, 365, "no gradient", 19, P["orange"]["text"], "c")
    s.line([(1100, 400), (1135, 460)], P["orange"]["stroke"], 3)
    s.takeaway("\"Our goal is not to recommend look-alike items users have already seen,\nbut to discover new items of interest expanded from their historical behaviors.\"",
               y=670, h=100, fs=24)
    s.footer(V2 + ", §1 (toothpaste / ointment example and quote)")
    return s


def s_qarm_v1(n):
    s = Slide("07-qarm-v1", n)
    s.title("The predecessor: QARM (2024)", "Already attacked both problems; deployed at Kuaishou since March 2024", part=PART1, pc="gray")
    # alignment
    s.box(70, 170, 700, 440, None, "gray", fill=P["gray"]["soft"])
    s.text(95, 188, "Item alignment → fixes unmatch", 26, P["ink"])
    chip(s, 95, 250, "Item2Item pairs (Swing)", "gray", 21)
    chip(s, 95, 312, "User2Item pairs (two-tower)", "gray", 21)
    s.arrow([(420, 273), (470, 300)], P["ink"])
    s.arrow([(420, 335), (470, 310)], P["ink"])
    s.box(480, 270, 250, 70, "contrastive\nfine-tuning of MLLM", "blue", 20)
    varrow(s, 605, 342, 400)
    s.box(480, 405, 250, 60, "aligned embedding m", "blue", 20)
    s.text(95, 500, "pairs: items clicked together (Swing), and a clicked\nitem + the most similar of the last 50 clicks", 20, P["muted"])
    # codes
    s.box(830, 170, 700, 440, None, "gray", fill=P["gray"]["soft"])
    s.text(855, 188, "Quantitative codes → fixes unlearning", 26, P["ink"])
    s.box(855, 250, 300, 90, "VQ code: IDs of the\nK = 25 nearest items", "purple", 20)
    s.box(1185, 250, 320, 90, "RQ code: Res-Kmeans,\nL = 6 levels", "purple", 20)
    varrow(s, 1005, 342, 400)
    varrow(s, 1345, 342, 400)
    s.box(855, 405, 650, 60, "codes = new ID features with learnable embeddings", "blue", 21)
    s.text(855, 500, "used as item, user-sequence and target-aware\ncross features in the ranker (d = 64)", 20, P["muted"])
    s.takeaway("Key lesson of v1: the aligned embedding as a frozen feature gave +0.02 AUC; as learnable codes, +0.18.", y=660)
    s.footer(V1 + ": §3, Table 1 (Advertising CTR AUC); K, L, d from the hyper-parameter section")
    return s


def s_qarm_v1_results(n):
    s = Slide("08-qarm-v1-results", n)
    s.title("QARM (2024) in numbers: the long tail gains most", part=PART1, pc="gray")
    s.text(70, 160, "Offline, Advertising CTR (AUC gain over the production model)", 24, P["purple"]["text"])
    rows = [["+ aligned embedding (frozen feature)", "+0.02"], ["+ VQ code", "+0.11"], ["+ RQ code", "+0.10"],
            ["+ VQ & RQ code", "+0.18"]]
    s.table(70, 205, [460, 160], rows, header=["variant", "AUC"], fs=22, rh=50, hc="purple",
            hl_rows={3: "green"})
    s.text(840, 160, "Online A/B (QARM vs production)", 24, P["purple"]["text"])
    rows2 = [["Advertising#1 revenue, cold-start items", "+9.704%"], ["Advertising#1 revenue, other items", "+3.147%"],
             ["Shopping#1 GMV", "+2.296%"], ["Shopping#2 GMV", "+1.568%"]]
    s.table(840, 205, [520, 170], rows2, header=["service · metric", "gain"], fs=22, rh=50, hc="purple")
    # long-tail bars
    s.text(70, 490, "Shopping#2 GMV by item popularity (L1 = least purchased, L6 = most)", 22, P["muted"])
    vals = [8.035, 2.617, 1.207, 3.054, 1.317, 3.984]
    x0, yb, bw = 110, 790, 120
    sc = 25
    s.line([(x0 - 20, yb), (x0 + 6 * (bw + 30), yb)], P["ink"], 2, roughness=0)
    for i, v in enumerate(vals):
        x = x0 + i * (bw + 30)
        c = "green" if i == 0 else "gray"
        s.box(x, yb - v * sc, bw, v * sc, None, c, round_=False)
        s.text(x + bw / 2, yb - v * sc - 30, f"+{v:.3f}%", 19, P[c]["text"], "c")
        s.text(x + bw / 2, yb + 8, f"L{i + 1}", 19, P["muted"], "c")
    s.box(1060, 560, 470, 220, None, "yellow")
    s.text(1080, 578, "What QARM V2 builds on", 24)
    s.text(1080, 622, "the alignment idea, Res-Kmeans\ncodes, the same services. It\nchanges the data, the LLM training\nand the quantizer.", 21)
    s.footer(V1 + ": Tables 1, 3, 4, 6")
    return s


def s_diff(n):
    s = Slide("09-what-changes", n)
    s.title("QARM → QARM V2: what changes", part=PART1, pc="gray")
    rows = [["Alignment data", "raw item pairs from the\nretrieval models", "pairs filtered by a reasoning\nLLM + generated QA pairs"],
            ["Embedding LLM", "multimodal LLM,\ncontrastive loss", "decoder-only LLM, three-segment\nmask: contrastive + next-token"],
            ["Semantic IDs", "VQ (25 neighbours)\n+ Res-Kmeans (6 levels)", "Res-Kmeans (2 levels)\n+ FSQ (1 level)"],
            ["Use in the ranker", "code features (item,\nuser, cross)", "embedding → GSU retrieval\nSIDs → ESU target attention"]]
    s.table(70, 165, [330, 520, 610], rows, header=["", "QARM (2024)", "QARM V2 (2026)"], fs=23, rh=104, hc="gray",
            aligns=["l", "l", "l"], colors=[[P["ink"], P["muted"], P["blue"]["text"]]] * 4)
    s.text(70, 700, "Part II covers the first two rows (GSU side), Part III the last two (ESU side).", 24, P["muted"])
    s.footer(V1 + " §3; " + V2 + " §1, §3")
    return s


# ======================================================================= GSU side
def s_noisy_pairs(n):
    s = Slide("10-noisy-pairs", n)
    s.title("The alignment pairs are noisy", "Item pairs exported from retrieval models are the training signal, and some are wrong", part=PART2, pc="blue")
    data = [("(a) Item2Item · Swing (exploitation)", "soy sauce", "laundry detergent",
             "condiment for cooking  vs\ncleaning product for clothes", "→ \"no\": reject", "orange",
             "co-clicked because both are hot:\nexposure bias, no real relation"),
            ("(b) User2Item · two-tower (exploration)", "fashion boots", "down jacket",
             "bought together during seasonal\ntransitions (autumn, winter)", "→ \"yes\": keep", "green",
             "different look, same occasion:\nexactly what we want to learn")]
    for i, (h, a, b, why, verdict, c, note) in enumerate(data):
        x = 70 + i * 740
        s.box(x, 170, 715, 540, None, "gray", fill="#ffffff")
        s.text(x + 25, 188, h, 24, P["ink"])
        s.box(x + 40, 250, 260, 70, a, "gray", 24)
        s.box(x + 415, 250, 260, 70, b, "gray", 24)
        s.arrow([(x + 304, 285), (x + 411, 285)], P["muted"], start="arrow", dashed=True)
        s.line([(x + 25, 350), (x + 690, 350)], P["faint"], 1, dashed=True)
        s.text(x + 25, 370, "reasoning LLM:", 21, P["muted"])
        s.text(x + 25, 405, why, 23, P["blue"]["text"])
        s.box(x + 25, 490, 300, 56, verdict, c, 24)
        s.text(x + 25, 580, note, 22, P["ink"])
    s.text(70, 735, "More examples from the paper: (toothpaste, dental floss) and (fishing rod, parasol) are related; "
                    "(soy sauce, detergent) is not.", 22, P["muted"])
    s.footer(V2 + ", §1 and Figure 2 (reasoning traces shortened)")
    return s


def s_pipeline(n):
    s = Slide("11-data-pipeline", n)
    s.title("Reasoning data pipeline", "A small LLM for easy pairs, a bigger one for hard pairs, a VLM for QA data", part=PART2, pc="blue")
    # filtering rows
    s.text(70, 165, "A · Filter item pairs (input: title + attributes only)", 24, P["blue"]["text"])
    rows = [("Item2Item Swing pairs", "Qwen3-0.6B", "10%+ rejected"), ("User2Item two-tower pairs", "Qwen3-8B", "70%+ rejected")]
    for i, (a, m, r) in enumerate(rows):
        y = 215 + i * 90
        s.box(70, y, 330, 64, a, "gray", 21)
        harrow(s, 404, 460, y + 32)
        s.box(465, y, 210, 64, m, "blue", 23)
        harrow(s, 679, 735, y + 32)
        s.box(740, y, 220, 64, r, "orange", 22)
    s.box(70, 410, 890, 210, None, "gray", fill=P["paper"], dashed=True)
    s.text(90, 425, "prompt (abridged)", 19, P["muted"])
    s.text(90, 460, "Item-1: #Title, #Attributes …   Item-2: #Title, #Attributes …\n"
                    "Analyze the potential correlation: semantic (similar concepts\n"
                    "or uses) or complementary purchase (bought or used together).\n"
                    "e.g. (fishing rod, parasol): highly related usage scenarios\n"
                    "Reply <answer>Yes</answer> or <answer>No</answer>.", 20, P["ink"], mono=True)
    # QA generation
    s.text(1010, 165, "B · Generate QA pairs per item", 24, P["blue"]["text"])
    s.box(1010, 215, 520, 64, "title, attributes, images, OCR, ASR", "gray", 21)
    varrow(s, 1270, 283, 320)
    s.box(1010, 325, 520, 64, "Gemini · Qwen2.5-VL-72B", "blue", 23)
    varrow(s, 1270, 393, 430)
    s.box(1010, 435, 520, 120, None, "green", fill=P["green"]["soft"])
    s.text(1030, 450, "ten diverse QA pairs per item, e.g.", 20, P["muted"])
    s.text(1030, 485, "Q: What is the item category?\nA: Spicy food", 20, P["ink"], mono=True)
    s.text(1010, 580, "Only questions the model can answer\nconfidently. Used for the generative loss.", 21, P["muted"])
    s.takeaway("Exploration pairs are mostly noise: 70%+ of User2Item pairs are rejected.", y=700)
    s.footer(V2 + ", §3.1.1 (prompts, models, rejection rates) and Figure 3")
    return s


def s_three_segment(n):
    s = Slide("12-three-segment", n)
    s.title("Three-segment trick: one LLM, two losses", "Turn a decoder-only LLM into an embedding model without giving up next-token prediction", part=PART2, pc="blue")
    seg = ["i"] * 4 + ["e"] * 3 + ["q"] * 4
    col = {"i": "gray", "e": "orange", "q": "green"}
    N = len(seg)
    cs = 36
    gx, gy = 120, 210

    def see(r, c):
        a, b = seg[r], seg[c]
        if a == "i":
            return b == "i" and c <= r
        if a == "e":
            return b == "i" or (b == "e" and c <= r)
        return b == "e" or (b == "q" and c <= r)
    s.text(gx, gy - 40, "attention mask (row attends to column)", 19, P["muted"])
    for k in range(N):
        s.box(gx + k * cs + 4, gy, cs - 8, cs - 8, None, col[seg[k]], round_=False, sw=1, roughness=0)
        s.box(gx - cs, gy + (k + 1) * cs + 4, cs - 8, cs - 8, None, col[seg[k]], round_=False, sw=1, roughness=0)
    for r in range(N):
        for c in range(N):
            ok = see(r, c)
            s.box(gx + c * cs + 4, gy + (r + 1) * cs + 4, cs - 8, cs - 8, None, "blue" if ok else "gray",
                  fill=P["blue"]["stroke"] if ok else "#f1f3f5", stroke="transparent", round_=False, sw=1, roughness=0)
    ly = gy + (N + 1) * cs + 16
    for i, (t, c) in enumerate([("input", "gray"), ("<EMB>", "orange"), ("QA", "green")]):
        s.box(gx + i * 140, ly, 26, 26, None, c, round_=False, sw=1, roughness=0)
        s.text(gx + i * 140 + 34, ly - 2, t, 20, P["ink"], mono=(t == "<EMB>"))
    # right: token sequence and losses
    x0 = 650
    s.text(x0, 175, "Input", 22, P["muted"])
    s.box(x0, 205, 330, 70, "title, OCR, attributes,\nimage tokens (ViT + projector)", "gray", 19)
    s.text(x0 + 350, 175, "Compression", 22, P["orange"]["text"])
    for k in range(3):
        s.box(x0 + 350 + k * 78, 205, 70, 70, "EMB", "orange", 18, mono=True)
    s.text(x0 + 600, 175, "QA", 22, P["green"]["text"])
    s.box(x0 + 600, 205, 280, 70, "Q: What is this?\nA: Cartoon quilt.", "green", 19)
    s.box(x0, 300, 880, 64, "decoder-only LLM (fine-tuned)", "blue", 26)
    for xx in (x0 + 465, x0 + 740):
        varrow(s, xx, 368, 410)
    s.box(x0 + 330, 415, 270, 90, "mean of <EMB> states\n→ item embedding m", "orange", 20, fill=P["orange"]["soft"])
    s.box(x0 + 620, 415, 260, 90, "next-token loss\non the answer", "green", 20, fill=P["green"]["soft"])
    varrow(s, x0 + 465, 508, 545)
    s.box(x0 + 330, 550, 270, 80, "in-batch contrastive\nloss with paired item", "purple", 20)
    s.box(x0, 655, 880, 120, None, "yellow")
    s.text(x0 + 20, 670, "Why it works: the QA tokens cannot see the input, only the <EMB> tokens.\n"
                         "To answer, all item information must flow through the embedding.\n"
                         "Warm start: QA may see the input at first; that attention is annealed to zero.", 21)
    s.footer(V2 + ", §3.1.2 and Figure 3. Gradient cache is used for large contrastive batches")
    return s


# ======================================================================= ESU side
def _cloud(seed=7, n=420):
    r = random.Random(seed)
    pts = []
    for _ in range(n):
        # long-tail catalogue: a dense core and a sparse halo
        if r.random() < 0.85:
            pts.append((r.gauss(0, 0.18), r.gauss(0, 0.18)))
        else:
            pts.append((r.uniform(-0.95, 0.95), r.uniform(-0.95, 0.95)))
    return [(max(-0.98, min(0.98, a)), max(-0.98, min(0.98, b))) for a, b in pts]


def _kmeans(pts, k=16, it=30, seed=3):
    r = random.Random(seed)
    cs = r.sample(pts, k)
    for _ in range(it):
        groups = [[] for _ in cs]
        for p in pts:
            j = min(range(k), key=lambda j: (p[0] - cs[j][0]) ** 2 + (p[1] - cs[j][1]) ** 2)
            groups[j].append(p)
        cs = [(sum(a for a, _ in g) / len(g), sum(b for _, b in g) / len(g)) if g else cs[j] for j, g in enumerate(groups)]
    return cs


def s_collision(n):
    s = Slide("13-collisions", n)
    s.title("Why semantic IDs collide", "A long-tail catalogue has dense and sparse regions; K-means follows the density", part=PART3, pc="purple")
    pts = _cloud()
    cs = _kmeans(pts)
    half = 250
    for i, (head, c) in enumerate([("(a) K-means: data-dependent", "orange"), ("(b) FSQ: data-independent grid", "blue")]):
        cx, cy = 330 + i * 560, 470
        s.box(cx - half, cy - half, 2 * half, 2 * half, None, "gray", fill="#ffffff", round_=False, sw=1, roughness=0)
        s.text(cx, cy - half - 44, head, 24, P[c]["text"], "c")
        if i == 1:
            for g in range(1, 8):
                v = -half + g * 2 * half / 8
                s.line([(cx + v, cy - half), (cx + v, cy + half)], P["blue"]["stroke"], 1, roughness=0)
                s.line([(cx - half, cy + v), (cx + half, cy + v)], P["blue"]["stroke"], 1, roughness=0)
        for a, b in pts:
            s.box(cx + a * half - 3, cy + b * half - 3, 6, 6, None, "gray", fill=P["muted"], stroke="transparent",
                  round_=False, sw=1, roughness=0, shape="ellipse")
        if i == 0:
            for a, b in cs:
                s.box(cx + a * half - 9, cy + b * half - 9, 18, 18, None, "orange", fill=P["red"]["stroke"],
                      stroke=P["ink"], sw=1, round_=False, roughness=0, shape="ellipse")
    k_in = sum(1 for a, b in cs if a * a + b * b < 0.4 ** 2)
    share = round(100 * math.pi * 0.4 ** 2 / 4)
    s.box(330 - 0.4 * half, 470 - 0.4 * half, 0.8 * half, 0.8 * half, None, "orange", fill="transparent",
          stroke=P["orange"]["stroke"], dashed=True, shape="ellipse", sw=2)
    s.text(1170, 230, "K-means minimises the distance\nto the nearest centroid only.\n\n"
                      f"Here {k_in} of {len(cs)} centroids sit in the\ndashed circle, {share}% of the area.\n"
                      "Tail items far out share a few\ncentroids → same semantic ID.", 21)
    s.text(1170, 520, "FSQ rounds each dimension to\nfixed levels: the grid does not\ndepend on the data, so sparse\nregions keep their own cells.", 21, P["blue"]["text"])
    s.takeaway("In QARM's 3-level Res-Kmeans, more than 30% of semantic IDs map to several items (Shopping).", y=760)
    s.footer("Illustration: 420 synthetic points, 16 K-means centroids, 8×8 grid. " + V2 + ", §1 and Figure 4")
    return s


def s_reskmeansfsq(n):
    s = Slide("14-res-kmeans-fsq", n)
    s.title("Res-KmeansFSQ: two K-means levels, then a grid", part=PART3, pc="purple")
    y = 220
    s.box(70, y, 200, 90, "LLM item\nembedding m", "blue", 22)
    harrow(s, 274, 320, y + 45)
    s.box(325, y, 270, 90, "level 1: K-means\nC¹ (K = 8192)", "purple", 22)
    harrow(s, 599, 645, y + 45)
    s.box(650, y, 270, 90, "level 2: K-means\non residual M¹", "purple", 22)
    harrow(s, 924, 970, y + 45)
    s.box(975, y, 300, 90, "level 3: FSQ\non residual M²", "blue", 22)
    harrow(s, 1279, 1325, y + 45)
    s.box(1330, y, 200, 90, "SID =\n(c¹, c², c³)", "green", 22, mono=False)
    for x, t in [(460, "c¹"), (785, "c²"), (1125, "c³")]:
        s.text(x, y + 100, t, 22, P["muted"], "c")
    s.box(325, 360, 595, 70, "category and usage: adaptive to the data", "purple", 21, fill=P["purple"]["soft"])
    s.box(975, 360, 300, 70, "item-specific detail", "blue", 21, fill=P["blue"]["soft"])
    # equations
    s.box(70, 470, 900, 230, None, "gray", fill=P["paper"])
    s.text(95, 485, "as in the paper", 20, P["muted"])
    s.text(95, 520, "M¹ = M − NearestRep(M, C¹)        C² = Kmeans(M¹, K)\n"
                    "M² = M¹ − NearestRep(M¹, C²)\n"
                    "Z  = round( L · sigmoid(M² W) ),   W ∈ R^(d×13),  L = 2\n"
                    "fit on N > 10,000,000 sampled item embeddings (d = 3,000+)", 22, P["ink"], mono=True)
    s.box(1010, 470, 520, 230, None, "orange", fill=P["orange"]["soft"])
    s.text(1030, 485, "Check the sizes", 24, P["orange"]["text"])
    s.text(1030, 530, "§3.2: K = 8192, 13 FSQ dims, L = 2.\n13 binary dims → 2¹³ = 8192 codes.\nBut round(2·σ) gives 3 values per dim.\n§4.5 runs everything as '3 × 4096'.", 21)
    s.footer(V2 + ", §1 and §3.2 (Eq. 2–3)")
    return s


def s_usage(n):
    s = Slide("15-usage", n)
    s.title("How the two outputs enter the ranker", part=PART3, pc="purple")
    # GSU
    s.box(70, 160, 715, 560, None, "blue", fill=P["blue"]["soft"])
    s.text(95, 178, "GSU: LLM embedding m", 28, P["blue"]["text"])
    s.text(95, 230, "Store m for every item (PCA-reduced).\nFor a target item, keep the k history items\nwith the highest inner product ⟨mᵢ, m⟩.", 22)
    for i in range(14):
        hit = i in (1, 5, 8, 12)
        s.box(105 + i * 44, 400, 36, 44, None, "blue" if hit else "gray", round_=False, sw=1, roughness=0)
    s.text(105, 360, "history", 20, P["muted"])
    s.box(270, 520, 300, 64, "target embedding m", "green", 21)
    for i in (1, 5, 8, 12):
        s.line([(420, 518), (123 + i * 44, 448)], P["blue"]["stroke"], 1, dashed=True)
    s.text(95, 620, "Retrieval is now semantic, not ID-based:\nnew items find related history from day one.", 21, P["muted"])
    # ESU
    s.box(815, 160, 715, 560, None, "purple", fill=P["purple"]["soft"])
    s.text(840, 178, "ESU: semantic IDs (c¹, c², c³)", 28, P["purple"]["text"])
    s.text(840, 230, "Each item = ItemID + three SIDs, each looked\nup in its own trainable embedding table.", 22)
    s.box(850, 340, 290, 70, "target (I, c¹, c², c³)\n= query", "green", 20)
    s.box(1180, 340, 320, 70, "top-k history (I, c¹, c², c³)\n= keys, values", "blue", 20)
    s.arrow([(995, 414), (1100, 470)], P["ink"])
    s.arrow([(1340, 414), (1240, 470)], P["ink"])
    s.box(1000, 475, 340, 60, "target attention", "purple", 22)
    varrow(s, 1170, 539, 575)
    s.box(1000, 580, 340, 60, "MoE → CTR, CVR, …", "green", 22)
    s.text(840, 665, "Multi-task BCE; SID embeddings learned end-to-end.", 21, P["muted"])
    s.footer(V2 + ", §3.3 (Eq. 4–6)")
    return s


# ======================================================================= results
def s_amazon(n):
    s = Slide("16-amazon", n)
    s.title("Public data: Amazon Book", "The only public benchmark in the paper", part=PART4, pc="green")
    names = ["DIN", "SIM-hard", "SIM-soft", "QARM V2"]
    vals = [67.69, 67.15, 69.57, 70.33]
    x, y, w, h = 160, 190, 820, 520
    Y = s.axes(x, y, w, h, 66, 71, [66, 67, 68, 69, 70, 71], ylabel="AUC (%)")
    slot = w / 4
    for i, (nm, v) in enumerate(zip(names, vals)):
        c = "blue" if i == 3 else "gray"
        bx = x + i * slot + 40
        s.box(bx, Y(v), slot - 80, Y(66) - Y(v), None, c, round_=False)
        s.text(bx + (slot - 80) / 2, Y(v) - 34, f"{v:.2f}", 22, P[c]["text"], "c")
        s.text(bx + (slot - 80) / 2, y + h + 12, nm, 22, P["ink"], "c")
    s.box(1060, 190, 470, 330, None, "gray", fill=P["paper"])
    s.text(1080, 208, "Setup", 24)
    s.text(1080, 252, "rating ≥ 4 → positive\nusers with ≥ 20 interactions\none positive + one negative\nper user; 15% of users = test\ntop-50 items retrieved for ESU\n\nDIN: latest items\nSIM-hard: same tag\nSIM-soft: ID-embedding top-k", 21)
    s.text(70, 780, "+0.76 AUC over SIM-soft. Note the y-axis starts at 66. No TWIN or semantic-ID baselines (TIGER, OneRec).", 22, P["muted"])
    s.footer(V2 + ", Table 1 and §4.1")
    return s


def s_offline(n):
    s = Slide("17-offline", n)
    s.title("Offline at Kuaishou: small but consistent gains", "GAUC gain over the production model, in percentage points", part=PART4, pc="green")
    data = [("Ads\nCTCVR", 63.06, 64.16), ("Shop1\nCTR", 71.45, 71.63), ("Shop1\nCVR", 72.50, 72.76),
            ("Shop1\nCTCVR", 74.97, 75.37), ("Shop2\nCTR*", 65.97, 66.18), ("Shop2\nCVR", 69.18, 69.34),
            ("Shop3\nCTR", 66.41, 66.53), ("Shop3\nCVR", 67.54, 67.59), ("Live\nClick", 63.61, 63.87),
            ("Live\nGift", 70.33, 70.55), ("Live\nLong View", 67.26, 67.76), ("Live\nFollow", 66.82, 67.10)]
    x, y, w, h = 140, 190, 1390, 470
    Y = s.axes(x, y, w, h, 0, 1.2, [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2], fmt="+{:.1f}", ylabel="GAUC gain (points)")
    s.line([(x, Y(0.1)), (x + w, Y(0.1))], P["green"]["stroke"], 2, dashed=True, roughness=0)
    s.line([(x + w - 560, Y(1.13)), (x + w - 500, Y(1.13))], P["green"]["stroke"], 2, dashed=True, roughness=0)
    s.text(x + w - 490, Y(1.13), "≈ 0.1 point: 'enough to contribute business gains'", 19, P["green"]["text"], "l", "m")
    slot = w / len(data)
    for i, (lab, a, b) in enumerate(data):
        d = round(b - a, 2)
        c = "blue"
        bx = x + i * slot + 18
        s.box(bx, Y(d), slot - 36, Y(0) - Y(d), None, c, round_=False)
        s.text(bx + (slot - 36) / 2, Y(d) - 28, f"+{d:.2f}", 18, P[c]["text"], "c")
        s.text(x + i * slot + slot / 2, y + h + 10, lab, 17, P["ink"], "c")
    s.text(70, 755, "Advertising CTCVR: GAUC 63.06 → 64.16, UAUC 62.98 → 63.97. All twelve tasks improve on AUC, UAUC and GAUC. "
                    "No error bars.", 20, P["muted"])
    s.footer(V2 + ", Tables 2–4. *Shopping#2 CTR reports WUAUC instead of GAUC")
    return s


def s_online(n):
    s = Slide("18-online-ads-shop", n)
    s.title("Online A/B: advertising and shopping", "Multi-week tests on main traffic", part=PART4, pc="green")
    s.table(70, 175, [300, 220, 220, 220], [["Advertising", "+1.321%", "+3.942%", "+4.873%"]],
            header=["", "Exposure", "Cost", "Revenue"], fs=24, rh=64, hc="green", hl_rows={},
            colors=[[P["ink"], P["ink"], P["ink"], P["green"]["text"]]])
    s.table(70, 360, [300, 220, 220, 220],
            [["Shopping#1", "+3.208%", "+1.919%", "+0.427%"], ["Shopping#2", "+5.612%", "+4.834%", "+3.739%"],
             ["Shopping#3", "+1.037%", "+1.221%", "+1.487%"]],
            header=["", "GMV", "Order", "Exposure"], fs=24, rh=64, hc="green", hl_rows={1: "green"})
    s.box(1100, 175, 430, 330, None, "yellow")
    s.text(1120, 195, "Reading the numbers", 25)
    s.text(1120, 240, "Revenue grows faster than\ncost in ads (+4.873% vs\n+3.942%).\n\nShopping#2 gains most on\nall three metrics.\n\nNo confidence intervals\nor traffic sizes are given.", 21)
    s.text(70, 640, "For comparison, QARM (2024) on Shopping: GMV +2.296% (#1) and +1.568% (#2), measured against\n"
                    "a different, earlier production model.", 21, P["muted"])
    s.footer(V2 + ", Tables 5 and 6; " + V1 + ", Table 4")
    return s


def s_online_live(n):
    s = Slide("19-online-live", n)
    s.title("Online A/B: live streaming, cold-start items gain most", part=PART4, pc="green")
    rows = [["#1 cold-start", "+3.231%", "+2.961%", "+1.609%", "+1.807%", "–", "–", "–"],
            ["#1 others", "+0.611%", "+0.753%", "+0.489%", "+2.917%", "+3.215%", "+1.184%", "+1.158%"],
            ["#2 cold-start", "+0.890%", "+0.998%", "+0.998%", "+0.918%", "–", "–", "–"],
            ["#2 others", "+0.304%", "+0.482%", "+0.434%", "+2.917%", "+0.464%", "+0.826%", "+0.418%"]]
    s.table(70, 175, [220, 170, 170, 170, 170, 170, 170, 170], rows,
            header=["Live-streaming", "Click", "Watch time", "Watch count", "Gift count", "Like", "Comment", "Follow"],
            fs=22, rh=64, hc="green", hl_rows={0: "green", 2: "green"})
    s.text(290, 140, "core metrics", 19, P["muted"])
    s.text(980, 140, "interaction metrics", 19, P["muted"])
    s.box(70, 540, 1460, 180, None, "gray", fill=P["paper"])
    s.text(95, 558, "Two things to notice", 24)
    s.text(95, 602, "Live-streaming#1 clicks: +3.231% for cold-start streams vs +0.611% for the rest (about 5×): content knowledge helps new items.\n"
                    "Gift count is +2.917% in both 'others' rows: a coincidence, or a copy error in the table?", 22)
    s.footer(V2 + ", Table 7 (largest live-stream traffic)")
    return s


def s_hr(n):
    s = Slide("20-alignment-hr", n)
    s.title("Did reasoning alignment improve retrieval?", "Item-to-item retrieval: 10 recent clicked triggers × 50 candidates; hit = real click or order", part=PART4, pc="green")
    cats = ["Click HR@200", "Click HR@500", "Order HR@200", "Order HR@500"]
    a = [7.77, 9.7, 11.3, 13.0]
    b = [12.5, 15.4, 20.0, 23.0]
    lab = {7.77: "7.77", 9.7: "9.7", 11.3: "11.3", 13.0: "13.0", 12.5: "12.5", 15.4: "15.4", 20.0: "20.0", 23.0: "23.0"}
    x, y, w, h = 140, 200, 940, 480
    Y = s.axes(x, y, w, h, 0, 25, [0, 5, 10, 15, 20, 25], fmt="{:g}%", ylabel="hit rate")
    slot = w / 4
    bw = 90
    for i in range(4):
        for j, (v, c) in enumerate([(a[i], "gray"), (b[i], "blue")]):
            bx = x + i * slot + slot / 2 - bw - 6 + j * (bw + 12)
            s.box(bx, Y(v), bw, Y(0) - Y(v), None, c, round_=False)
            s.text(bx + bw / 2, Y(v) - 30, lab[v], 20, P[c]["text"], "c")
        s.text(x + i * slot + slot / 2, y + h + 12, cats[i], 20, P["ink"], "c")
    s.box(x + 20, y - 10, 24, 24, None, "gray", round_=False)
    s.text(x + 52, y - 12, "QARM", 20)
    s.box(x + 160, y - 10, 24, 24, None, "blue", round_=False)
    s.text(x + 192, y - 12, "QARM V2", 20)
    s.box(1130, 200, 400, 480, None, "yellow")
    s.text(1150, 220, "Relative gains", 24)
    s.text(1150, 265, "click HR@200 +60.9%\nclick HR@500 +58.8%\norder HR@200 +77.0%\n\nThe authors read the HR@200\ngains as: relevant items are\nranked higher, not just\nfound deeper.", 21)
    s.text(1150, 545, "Text: order HR@500 rises\n'from 20.0% to 23.0%';\nthe table says 13.0%.", 20, P["orange"]["text"])
    s.footer(V2 + ", Table 8 and §4.4. Relative gains as stated in the paper")
    return s


def s_codes(n):
    s = Slide("21-code-conflict", n)
    s.title("Code collisions: most of the gain comes from better embeddings", part=PART4, pc="green")
    rows = [["QARM Res-Kmeans", "77.92%", "129.33", "80.3%", "97.79%"],
            ["QARM V2 Res-Kmeans", "52.25%", "8.41", "91.9%", "99.75%"],
            ["QARM V2 Res-KmeansFSQ", "32.39%", "2.5", "95.2%", "99.9%"]]
    s.table(70, 170, [420, 230, 230, 230, 230], rows, header=["all 3 levels × 4096", "Collision ↓", "EdgeNum ↓", "HR@1 ↑", "HR@10 ↑"],
            fs=24, rh=70, hc="purple", hl_rows={2: "blue"})
    s.text(70, 480, "Collision: share of items whose SID is shared with another item.  EdgeNum: items returned per SID lookup.\n"
                    "HR@K: the query item is among the top-K items returned for its own SID.", 20, P["muted"])
    s.box(70, 580, 715, 170, None, "blue", fill=P["blue"]["soft"])
    s.text(95, 598, "Same quantizer, new embeddings", 24, P["blue"]["text"])
    s.text(95, 640, "EdgeNum 129.33 → 8.41 (15× fewer items per SID)\nfrom the V2 embeddings alone (new data + training).", 22)
    s.box(815, 580, 715, 170, None, "purple", fill=P["purple"]["soft"])
    s.text(840, 598, "Then FSQ on the last level", 24, P["purple"]["text"])
    s.text(840, 640, "EdgeNum 8.41 → 2.5, collision 52.25% → 32.39%.\nPer-element MSE by level: ≈ 0.37 / 0.26 / 0.20.", 22)
    s.footer(V2 + ", Table 9 and §4.5 (KGNN reverse lookup of SID → item IDs)")
    return s


def s_gsu_case(n):
    s = Slide("22-gsu-case", n)
    s.title("What the semantic GSU finds that the ID-based GSU does not", part=PART4, pc="green")
    s.table(70, 170, [380, 260, 260, 260], [["Exclusive rate", "63.6%", "57.9%", "65.1%"]],
            header=["history sequence", "Click (top 50)", "Order (top 30)", "Exposure (top 30)"], fs=24, rh=66, hc="green")
    s.text(70, 330, "Exclusive rate: share of retrieved history items that QARM V2 finds and the baseline GSU (SIM) does not.", 21, P["muted"])
    s.box(70, 400, 715, 200, None, "orange", fill=P["orange"]["soft"])
    s.text(95, 418, "ID-based SIM", 25, P["orange"]["text"])
    s.text(95, 462, "retrieves 'hard negatives': history items\nunrelated in category and meaning,\ne.g. jewellery for a phone-accessory target", 22)
    s.box(815, 400, 715, 200, None, "blue", fill=P["blue"]["soft"])
    s.text(840, 418, "QARM V2", 25, P["blue"]["text"])
    s.text(840, 462, "retrieved items stay in the target's\ncategory and meaning; often related but\nvisually dissimilar", 22)
    s.text(70, 660, "Also: sequences are not deduplicated. In live streaming the top-100 interactions contain only 23 unique authors\n"
                    "on average, and repeats carry signal (watch time, time of day). Deduplication lowered offline AUC.", 21, P["muted"])
    s.footer(V2 + ", Table 10, Figure 5 and §4.2")
    return s


# ======================================================================= discussion
def s_critique(n):
    s = Slide("23-critique", n)
    s.title("Reading it critically", part=PART5, pc="yellow")
    panel(s, 70, 160, 560, 600, "Strong", "• deployed in ads, shopping and live\n  streaming; multi-week A/B tests\n\n"
          "• reusable ideas: an LLM as a data\n  filter, a three-segment mask, a\n  hybrid quantizer\n\n• measures SID collisions directly\n  instead of only end metrics", "green", 30, 24)
    panel(s, 660, 160, 870, 600, "Weak or unclear", "• no ablation on ranking metrics: filter vs three-segment\n  vs FSQ are never separated\n\n"
          "• baselines are the production model and, on Amazon,\n  DIN / SIM only (no TWIN, TIGER, OneRec)\n\n"
          "• no confidence intervals; some gains are 0.05 points\n\n• inconsistencies: K = 8192 vs '3 × 4096'; FSQ levels;\n"
          "  order HR@500 13.0 vs 20.0; collision '> 30%' vs 77.92%;\n  vocabulary < 20k vs ~1e5\n\n"
          "• the filter LLM sees only titles + attributes", "orange", 30, 24)
    s.footer(V2 + "; inconsistencies are listed with their locations in references/digest.md")
    return s


def s_questions(n):
    s = Slide("24-questions", n)
    s.title("Questions for the discussion", part=PART5, pc="yellow")
    qs = [("Whose notion of 'related'?", "The filter swaps exposure bias for the LLM's prior. When should a\nco-click the LLM finds unrelated still count as signal?"),
          ("Embeddings or quantizer?", "V2 Res-Kmeans already cuts EdgeNum 15×. How much end-to-end gain\nis left for FSQ? Would a random hash on level 3 do as well?"),
          ("Is the third level semantic?", "FSQ ignores the data distribution. Does c³ carry meaning, or is it a\ntie-breaker that makes SIDs unique?"),
          ("Three segments vs one <EMB>", "The paper argues next-token loss protects the LLM. No experiment\ncompares it with a plain <EMB> token."),
          ("Would this work outside Kuaishou?", "Amazon Book: +0.76 AUC over SIM-soft. What is needed in data and\nLLM compute to see the online gains elsewhere?")]
    for i, (q, d) in enumerate(qs):
        y = 160 + i * 132
        s.box(70, y, 60, 60, str(i + 1), "yellow", 28)
        s.text(160, y - 2, q, 26, P["ink"])
        s.text(160, y + 38, d, 21, P["muted"])
    s.footer("")
    return s


def s_takeaways(n):
    s = Slide("25-takeaways", n)
    s.title("Takeaways", part=PART5, pc="yellow")
    items = [("blue", "LLM knowledge reaches a ranker in two forms", "an embedding for retrieval (GSU) and learnable semantic IDs for ranking (ESU)."),
             ("orange", "Better embeddings mattered more than the quantizer", "the V2 embeddings made codes 15× less crowded before FSQ was added."),
             ("purple", "Code collisions are measurable", "collision rate and items-per-SID are cheap diagnostics worth reporting."),
             ("green", "Strong in production, thin in ablation", "large online gains, but which component buys them is not shown.")]
    for i, (c, a, b) in enumerate(items):
        y = 165 + i * 140
        s.box(70, y, 1460, 115, None, c, fill=P[c]["soft"])
        s.text(95, y + 16, a, 27, P[c]["text"])
        s.text(95, y + 62, b, 23, P["ink"])
    s.text(70, 755, "QARM V2: arxiv.org/abs/2602.08559   ·   QARM: arxiv.org/abs/2411.11739", 22, P["muted"], mono=True)
    s.footer("")
    return s


SLIDES = [s_title, s_tldr, s_setting, s_gsu_esu, s_ids_vs_llm, s_naive_llm, s_qarm_v1, s_qarm_v1_results, s_diff,
          s_noisy_pairs, s_pipeline, s_three_segment,
          s_collision, s_reskmeansfsq, s_usage,
          s_amazon, s_offline, s_online, s_online_live, s_hr, s_codes, s_gsu_case,
          s_critique, s_questions, s_takeaways]

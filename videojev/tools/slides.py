"""VideoJev paper-club deck: one function per slide; the order is the SLIDES list at the bottom.

Numbers come only from references/digest.md (which cites the paper's tables and sections).
Colour code: orange = generative MLLM baseline / problem, blue = VideoJev, green = gain, purple = measurement,
gray = neutral, yellow = takeaway.
"""
import math

from slidekit import P, Slide, W, text_width

PART1 = "Part I · Background"
PART2 = "Part II · Method"
PART3 = "Part III · Results"
PART4 = "Part IV · Discussion"
SRC = "VideoJev (arXiv:2610.18615)"


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


# ======================================================================= opening
def s_title(n):
    s = Slide("01-title", n)
    s.text(70, 120, "PAPER CLUB · OCTOBER 2026", 20, P["muted"])
    s.text(70, 165, "VideoJev", 84)
    s.text(72, 280, "System One Model for Video Understanding and Interaction", 36)
    s.text(72, 345, "Yuhan Zhu, Xiangyu Zeng, Qingyi Si, … , Jiaqi Wang, Nan Duan, Limin Wang (18 authors)\n"
                    "Nanjing University (MCG-NJU), JD.com and six more universities", 22, P["muted"])
    s.text(72, 425, "arXiv:2610.18615 (13 Oct 2026)  ·  github.com/MCG-NJU/VideoJev  ·  models: VideoJev-4B, VideoJev-35B-A3B",
           19, P["muted"], mono=True)
    # the idea in one row: one video, many questions, direct scores
    y = 560
    s.box(72, y, 190, 90, "one video", "gray", 24)
    harrow(s, 266, 312, y + 45)
    s.box(316, y, 250, 90, "encode once", "blue", 24)
    harrow(s, 570, 616, y + 45)
    for k, (q, a) in enumerate([("When?", "a time span"), ("Which?", "an option"), ("When?", "a time span")]):
        yy = y - 40 + k * 62
        s.box(620, yy, 150, 50, q, "gray", 21)
        harrow(s, 774, 820, yy + 25)
        s.box(824, yy, 210, 50, a, "green", 21)
    s.text(1070, y + 8, "scores, not generated text:\none forward pass for all questions", 24, P["blue"]["text"])
    s.text(72, 730, "A video model that answers by scoring candidates instead of writing answers.", 26, P["blue"]["text"])
    s.footer("Slides drawn in Excalidraw; every number is from the paper (see references/digest.md)")
    return s


def s_tldr(n):
    s = Slide("02-tldr", n)
    s.title("The paper in one slide")
    cols = [("Problem", "orange",
             "Video MLLMs answer by writing\ntext token by token, even when the\nanswer is a time span or 'B'.\n\n"
             "• slow: 'Thinking' takes 145 s\n  per question (Qwen3.5-4B)\n• output must be parsed\n"
             "• an agent asks many questions\n  about the same video"),
            ("Idea", "blue",
             "A System One head on an MLLM:\nscore candidates in one pass.\n\n"
             "• grounding: score every short\n  time interval → pick a span\n"
             "• QA: score every option → softmax\n• video encoded once, many\n  questions in one forward pass"),
            ("Evidence", "green",
             "Grounding, mean mIoU:\n• 4B: 58.6 → 65.3 (+6.7)\n• 35B-A3B: 56.9 → 67.7 (+10.8)\n• 2.8–3.1× faster than backbone\n\n"
             "Video QA, 4-benchmark mean:\n• about equal to 'Thinking'\n  (74.3 vs 74.9; 79.5 vs 78.8)\n• 100–129× faster")]
    for i, (h, c, b) in enumerate(cols):
        panel(s, 70 + i * 495, 160, 465, 555, h, b, c, 32, 23)
    s.takeaway("Many video questions do not need a written answer, only a decision.", y=740)
    s.footer(SRC + ": abstract, Tables 1 and 2")
    return s


def s_glossary(n):
    s = Slide("03-glossary", n)
    s.title("Glossary")
    rows = [["System One model", "fast, one-pass model that returns typed decisions with probabilities (after Kahneman)"],
            ["Jev", "TypeSafe AI's System One model for text; VideoJev is a video version"],
            ["temporal grounding", "find when an event happens in a video: output a start and end time"],
            ["mIoU · R1@0.7", "mean overlap of predicted and true span · share of queries with overlap ≥ 0.7"],
            ["multiple-choice video QA", "a question about a video with 4–5 answer options; metric: accuracy"],
            ["Instruct · Thinking", "an MLLM answering directly · the same model reasoning in text first"],
            ["prefill · KV cache", "processing the prompt (here the video) once · stored attention states to reuse"],
            ["Cached inference", "prefill the video once; each new question continues from a copy of the cache"],
            ["Joint inference", "put all questions after the video and score them in one forward pass"],
            ["35B-A3B", "mixture-of-experts model: 35B parameters in total, about 3B used per token"],
            ["ECE", "expected calibration error: gap between confidence and actual accuracy"]]
    s.table(70, 150, [330, 1130], rows, header=["term", "meaning"], fs=20, rh=55, hc="gray", aligns=["l", "l"],
            colors=[[P["blue"]["text"], P["ink"]]] * len(rows))
    s.footer(SRC + ", §1, §2.1, §3.5; TypeSafe AI, 'Introducing System One Models & Jev'")
    return s


# ======================================================================= background
def s_tasks(n):
    s = Slide("04-tasks", n)
    s.title("Two everyday video questions: When? and Which?", part=PART1, pc="gray")
    # grounding
    s.box(70, 160, 715, 520, None, "gray", fill=P["gray"]["soft"])
    s.text(95, 178, "Temporal grounding: When?", 27, P["ink"])
    s.text(95, 225, "\"When is chocolate added to the waffles?\"", 22, P["blue"]["text"])
    for i in range(20):
        s.box(110 + i * 31, 300, 27, 46, None, "gray", round_=False, sw=1, roughness=0,
              fill=P["purple"]["fill"] if 11 <= i <= 18 else "#ffffff")
    s.text(110, 352, "0 s", 18, P["muted"])
    s.text(730, 352, "20 s", 18, P["muted"], "r")
    s.line([(110 + 11 * 31, 395), (110 + 19 * 31 - 4, 395)], P["purple"]["stroke"], 4, roughness=0)
    s.text(110 + 15 * 31, 405, "true span: 11–19 s", 19, P["purple"]["text"], "c")
    s.text(95, 470, "Output: a start and an end time.\nMetrics: mIoU (mean overlap with the true span),\n"
                    "R1@0.7 (overlap at least 0.7).\nBenchmarks: Charades, ActivityNet, QVHighlights.", 21)
    # QA
    s.box(815, 160, 715, 520, None, "gray", fill=P["gray"]["soft"])
    s.text(840, 178, "Multiple-choice video QA: Which?", 27, P["ink"])
    s.text(840, 225, "\"What is drizzled onto the waffles?\"", 22, P["blue"]["text"])
    for k, o in enumerate(["A. Chocolate", "B. Jam", "C. Cream"]):
        s.box(860, 285 + k * 62, 300, 48, o, "purple" if k == 0 else "gray", 21, fill=None if k == 0 else "#ffffff")
    s.text(840, 470, "Output: one option.\nMetric: accuracy.\nBenchmarks: LVBench, Video-MME,\n"
                     "LongVideoBench, MLVU (videos up to hours).", 21)
    s.takeaway("Both answers are tiny: two numbers, or one letter.", y=715)
    s.footer(SRC + ", Figure 2 (example redrawn) and §3.1")
    return s


def s_generate(n):
    s = Slide("05-generate", n)
    s.title("Today: video MLLMs write their answers", "Even a time span or a letter is generated token by token",
            part=PART1, pc="orange")
    s.box(70, 170, 880, 120, None, "orange", fill="#ffffff")
    s.text(95, 185, "grounding output", 19, P["muted"])
    s.text(95, 220, "\"The event happens from 11.0 to 19.0 seconds.\"", 23, P["ink"], mono=True)
    s.box(70, 310, 880, 150, None, "orange", fill="#ffffff")
    s.text(95, 325, "QA output, Thinking mode", 19, P["muted"])
    s.text(95, 360, "<think> The person pours something dark… it looks\nlike chocolate sauce… </think>  Answer: A", 21,
           P["ink"], mono=True)
    s.box(990, 170, 540, 290, None, "orange", fill=P["orange"]["soft"])
    s.text(1010, 185, "What this costs", 25, P["orange"]["text"])
    s.text(1010, 232, "• time per token, many tokens\n• text must be parsed; invalid\n  answers count as wrong\n"
                      "• no score for 'how sure'\n• each new question decodes\n  again", 21)
    rows = [["Qwen3.5-4B Instruct", "1.36 s", "66.3"], ["Qwen3.5-4B Thinking", "144.9 s", "74.9"]]
    s.text(70, 500, "Video QA, latency per question on LVBench and mean accuracy (4 benchmarks)", 21, P["purple"]["text"])
    s.table(70, 540, [420, 200, 200], rows, header=["model", "latency", "accuracy"], fs=22, rh=54, hc="purple")
    s.box(990, 520, 540, 175, None, "yellow")
    s.text(1010, 538, "Thinking buys +8.6 points\nfor about 107× the time.", 26)
    s.footer(SRC + ", Table 2 (H200 GPU, batch size 1, model forward time); generated texts are illustrative")
    return s


def s_kahneman(n):
    s = Slide("06-fast-and-slow", n)
    s.title("Where the name comes from: Thinking, Fast and Slow", "Daniel Kahneman, 2011: two modes of thought",
            part=PART1, pc="gray")
    # a generic book, drawn
    s.box(70, 170, 230, 310, None, "gray", fill="#ffffff", round_=False, sw=2)
    s.box(70, 170, 26, 310, None, "gray", fill=P["gray"]["fill"], round_=False, sw=2)
    s.text(198, 230, "Thinking,\nFast and\nSlow", 30, P["ink"], "c")
    s.text(198, 400, "D. Kahneman\n2011", 18, P["muted"], "c")
    # System 1
    s.box(350, 170, 570, 310, None, "blue", fill=P["blue"]["soft"])
    s.text(372, 186, "System 1 · fast", 28, P["blue"]["text"])
    s.text(372, 232, "instinctive, emotional, automatic", 21, P["muted"])
    s.box(400, 290, 200, 80, "2 + 2 = ?", "blue", 28)
    harrow(s, 604, 650, 330)
    s.box(655, 290, 110, 80, "4", "green", 30)
    s.text(780, 315, "instantly,\nno effort", 20, P["ink"])
    s.text(372, 400, "also: reading a face, a short word,\nnoticing a sudden sound", 19, P["muted"])
    # System 2
    s.box(960, 170, 570, 310, None, "orange", fill=P["orange"]["soft"])
    s.text(982, 186, "System 2 · slow", 28, P["orange"]["text"])
    s.text(982, 232, "deliberative, logical, effortful", 21, P["muted"])
    s.box(1010, 290, 200, 80, "17 × 24 = ?", "orange", 28)
    harrow(s, 1214, 1260, 330)
    s.box(1265, 290, 110, 80, "408", "green", 30)
    s.text(1390, 315, "step by\nstep", 20, P["ink"])
    s.text(982, 400, "also: filling in a tax form,\nchecking a logical argument", 19, P["muted"])
    # mapping to models
    s.text(70, 520, "The same split in AI models", 25, P["ink"])
    rows = [["System 1", "System One models (Jev, VideoJev): one forward pass → a typed decision with probabilities"],
            ["System 2", "LLMs that write free text; 'Thinking' mode: reason step by step, then answer"]]
    s.table(70, 565, [240, 1220], rows, fs=22, rh=58, hc="gray", aligns=["l", "l"],
            colors=[[P["blue"]["text"], P["ink"]], [P["orange"]["text"], P["ink"]]])
    s.takeaway("Kahneman: we use System 1 most of the time and call System 2 when it is needed. VideoJev aims for the same split.",
               y=720, h=64, fs=22)
    s.footer("D. Kahneman, Thinking, Fast and Slow (2011); 17 × 24 is Kahneman's own example. Book drawn generically, not the cover")
    return s


def s_system_one(n):
    s = Slide("06-system-one", n)
    s.title("The System One idea (Jev)", "Fast typed judgments instead of slow free text", part=PART1, pc="gray")
    s.box(70, 160, 715, 300, None, "orange", fill=P["orange"]["soft"])
    s.text(95, 178, "System 2: slow, deliberate", 26, P["orange"]["text"])
    s.text(95, 228, "a chat LLM: writes free text token by\ntoken, can reason, plan, explain;\n"
                    "output must be parsed by software", 22)
    s.box(815, 160, 715, 300, None, "blue", fill=P["blue"]["soft"])
    s.text(840, 178, "System 1: fast, intuitive", 26, P["blue"]["text"])
    s.text(840, 228, "a System One model: returns a typed\ndecision (a choice, a yes/no, a score)\n"
                     "with probabilities, in one pass", 22)
    s.text(70, 490, "Jev (TypeSafe AI)", 24, P["ink"])
    s.text(70, 530, "• typed probabilistic judgments that software can use directly\n"
                    "• trained with RL for calibrated probabilities\n• 'Jev' after the economist Jevons: cheaper decisions → many more uses\n"
                    "• image versions: Visual Jev, PixelJev → this paper: video", 22)
    s.box(900, 490, 630, 220, None, "yellow")
    s.text(920, 508, "The paper's premise", 23)
    s.text(920, 550, "\"Structured visual judgments can\nsupport open-ended behavior without\nrequiring open-ended "
                     "generation at\nevery step.\"", 22)
    s.footer(SRC + ", §1 and §4; TypeSafe AI blog (vendor description of Jev)")
    return s


def s_why_video(n):
    s = Slide("07-why-video", n)
    s.title("Why video makes this harder", "An agent asks many questions about the same video, over time", part=PART1, pc="gray")
    s.box(70, 170, 380, 360, None, "gray", fill=P["gray"]["soft"])
    s.text(95, 188, "cooking assistant", 24)
    for i in range(10):
        s.box(95 + i * 33, 245, 28, 40, None, "gray", round_=False, sw=1, roughness=0, fill="#ffffff")
    s.text(95, 300, "the same visual history\n(minutes to hours)", 20, P["muted"])
    qs = [("Has the egg been added?", "yes / no"), ("When did the pan go on the stove?", "a time span"),
          ("Which step comes next? A / B / C", "an option"), ("Is the sauce still too thin?", "yes / no")]
    for k, (q, a) in enumerate(qs):
        y = 180 + k * 88
        s.arrow([(452, 300), (520, y + 30)], P["muted"], 1)
        s.box(525, y, 560, 60, q, "gray", 21, fill="#ffffff")
        harrow(s, 1089, 1135, y + 30)
        s.box(1140, y, 220, 60, a, "green", 21)
    s.box(70, 570, 715, 170, None, "orange", fill=P["orange"]["soft"])
    s.text(95, 588, "Requirement 1: time", 24, P["orange"]["text"])
    s.text(95, 632, "decisions must respect temporal structure\n(a span, not a single frame)", 21)
    s.box(815, 570, 715, 170, None, "orange", fill=P["orange"]["soft"])
    s.text(840, 588, "Requirement 2: reuse", 24, P["orange"]["text"])
    s.text(840, 632, "encoding the video is the expensive part;\nevery extra question should be cheap", 21)
    s.footer(SRC + ", §1 (cooking example); questions are illustrative")
    return s


# ======================================================================= method
def s_architecture(n):
    s = Slide("08-architecture", n)
    s.title("Architecture: candidates in the prompt, scores at special tokens", part=PART2, pc="blue")
    y = 175
    segs = [("video tokens", "gray", 230), ("task + query", "gray", 200), ("cand. 1", "purple", 110),
            ("◆", "orange", 46), ("cand. 2", "purple", 110), ("◆", "orange", 46), ("…", "gray", 60),
            ("cand. K", "purple", 110), ("◆", "orange", 46), ("★", "blue", 46)]
    x = 70
    xs = {}
    for k, (t, c, w) in enumerate(segs):
        s.box(x, y, w, 60, t, c, 19)
        xs[k] = x + w / 2
        x += w + 6
    s.box(70, 300, x - 76, 70, "pretrained MLLM (Qwen3.5-4B or Qwen3.6-35B-A3B), final MLP removed", "blue", 23)
    for k in (3, 5, 8, 9):
        varrow(s, xs[k], 237, 296)
        varrow(s, xs[k], 374, 420)
    s.box(xs[3] - 120, 425, xs[8] - xs[3] + 240, 60, "candidate states h₁ … h_K", "orange", 21, fill=P["orange"]["soft"])
    s.box(xs[9] - 90, 425, 180, 60, "decision h_d", "blue", 21, fill=P["blue"]["soft"])
    varrow(s, (xs[3] + xs[8]) / 2, 489, 530)
    varrow(s, xs[9], 489, 530)
    s.box(xs[3] - 120, 535, xs[9] - xs[3] + 210, 60, "shared scorer → one score s_i per candidate", "green", 22)
    s.text(70, 440, "◆ = <|option_end|>\n     one readout per candidate\n★ = <|decide|>\n     one readout per query", 20, P["muted"])
    s.box(70, 650, 715, 130, None, "gray", fill=P["paper"])
    s.text(95, 663, "Why it works with one causal pass", 22)
    s.text(95, 703, "each candidate readout sees the video, the query and\nearlier candidates; <|decide|> sees the whole list", 20)
    s.box(815, 650, 715, 130, None, "gray", fill=P["paper"])
    s.text(840, 663, "Small changes to the MLLM", 22)
    s.text(840, 703, "two new tokens (initialised from <|im_end|>), no LM\nhead, no final MLP; the vision encoder stays frozen", 20)
    s.footer(SRC + ", §2.1 and Figure 2")
    return s


def s_scorer(n):
    s = Slide("09-scorer", n)
    s.title("The shared scorer: a dot product between question and candidate", part=PART2, pc="blue")
    s.box(120, 180, 300, 70, "decision state h_d", "blue", 22, fill=P["blue"]["soft"])
    s.box(120, 330, 300, 70, "candidate state h_i", "orange", 22, fill=P["orange"]["soft"])
    harrow(s, 424, 500, 215)
    harrow(s, 424, 500, 365)
    s.box(505, 180, 330, 70, "Q projection → 512-d", "gray", 21)
    s.box(505, 330, 330, 70, "K projection → 512-d", "gray", 21)
    harrow(s, 839, 915, 215)
    harrow(s, 839, 915, 365)
    s.box(920, 180, 230, 70, "normalise → u", "gray", 21)
    s.box(920, 330, 230, 70, "normalise → vᵢ", "gray", 21)
    s.arrow([(1154, 215), (1230, 280)], P["ink"])
    s.arrow([(1154, 365), (1230, 300)], P["ink"])
    s.box(1235, 250, 290, 80, "sᵢ = 10 · uᵀvᵢ + b", "green", 26)
    s.text(70, 450, "• cosine similarity between 'what is asked' and 'this candidate', scaled by 10, plus a learned bias b\n"
                    "• the same head scores time intervals and text options; only the output rule differs:", 22)
    s.box(120, 560, 640, 120, None, "purple", fill=P["purple"]["soft"])
    s.text(145, 575, "grounding: sigmoid, one per interval", 23, P["purple"]["text"])
    s.text(145, 618, "pᵢ = σ(sᵢ): is this interval inside the event?", 21)
    s.box(820, 560, 640, 120, None, "purple", fill=P["purple"]["soft"])
    s.text(845, 575, "QA: softmax over the options", 23, P["purple"]["text"])
    s.text(845, 618, "pᵢ = softmax(s)ᵢ: which option is right?", 21)
    s.text(70, 720, "Projections start from small random weights (std 0.005), biases at zero. Why drop the final MLP? "
                    "Pre-MLP features are\nknown to carry semantic similarity (FreeRet); the ablation slide shows no loss.",
           19, P["muted"])
    s.footer(SRC + ", Eq. (1), §2.1 and §2.4")
    return s


def s_frame_pairs(n):
    s = Slide("11-frame-pairs", n)
    s.title("Why one candidate = two frames", "The backbone compresses video twofold in time", part=PART2, pc="blue")
    fps = 4
    times = [k / fps for k in range(8)]
    x0, fw, gap = 90, 150, 30
    # frames
    s.text(70, 160, "frames sampled at 4 fps (as in evaluation)", 20, P["muted"])
    for k, tt in enumerate(times):
        pair = k // 2
        x = x0 + pair * (2 * fw + gap + 52) + (k % 2) * (fw + 6)
        s.box(x, 195, fw, 86, None, "gray", fill="#ffffff", round_=False, sw=1, roughness=0)
        s.text(x + fw / 2, 225, f"frame {k + 1}", 19, P["ink"], "c")
        s.text(x + fw / 2, 252, f"{tt:.2f} s", 17, P["muted"], "c")
    # pair brackets → encoder
    cands = []
    for pr in range(4):
        xa = x0 + pr * (2 * fw + gap + 52)
        xb = xa + 2 * fw + 6
        s.line([(xa, 292), (xa, 302), (xb, 302), (xb, 292)], P["purple"]["stroke"], 2, roughness=0)
        varrow(s, (xa + xb) / 2, 304, 344)
        cands.append((xa, xb))
    s.box(70, 348, 1460, 58, "vision encoder: every visual patch spans 2 consecutive frames → one set of visual tokens per pair",
          "blue", 21)
    tok_mid = [(times[2 * p] + times[2 * p + 1]) / 2 for p in range(4)]
    bounds = [0.0, 0.375, 0.875, 1.375, 2.0]
    for pr, (xa, xb) in enumerate(cands):
        cx = (xa + xb) / 2
        varrow(s, cx, 410, 440)
        for q in range(4):
            s.box(cx - 70 + q * 36, 444, 30, 30, None, "purple", round_=False, sw=1, roughness=0)
        varrow(s, cx, 478, 506)
        s.box(cx - 110, 510, 220, 52, f"candidate <{tok_mid[pr]:.1f}s>", "green", 20)
        s.text(cx, 570, f"t = {tok_mid[pr]:.3f} s\ninterval [{bounds[pr]:.3f}, {bounds[pr + 1]:.3f}]", 17, P["muted"], "c")
    s.box(70, 640, 715, 150, None, "gray", fill=P["paper"])
    s.text(92, 652, "Why not one candidate per frame?", 22)
    s.text(92, 692, "frame 1 and frame 2 share their visual tokens:\nthe LLM never sees them apart, so a single-frame\n"
                    "candidate would have nothing of its own to point to", 19)
    s.box(815, 640, 715, 150, None, "yellow")
    s.text(835, 652, "Consequences", 22)
    s.text(835, 692, "one candidate = 2 / fps seconds: 0.5 s at 4 fps, 1 s at 2 fps\n"
                     "boundaries fall halfway between neighbouring pairs\n"
                     "a 2-minute video at 4 fps → 480 frames → 240 candidates", 19)
    s.footer(SRC + ", §2.2 and Figure 2 (\"The backbone's twofold temporal compression groups frames into pairs.\"); "
             "video of 2.0 s for illustration")
    return s


def s_grounding(n):
    s = Slide("10-grounding", n)
    s.title("Grounding as many small yes/no decisions", "One candidate per frame pair (previous slide): is this interval inside the event?",
            part=PART2, pc="blue")
    K = 20
    x0, y0, cw = 90, 200, 66
    gt = range(11, 19)
    for i in range(K):
        x = x0 + i * cw
        inside = i in gt
        s.box(x, y0, cw - 6, 44, f"<{i}s>" if i % 4 == 0 else None, "gray", 15, fill="#ffffff", round_=False, sw=1,
              roughness=0)
        s.box(x, y0 + 60, cw - 6, 40, "1" if inside else "0", "purple" if inside else "gray", 18,
              fill=P["purple"]["fill"] if inside else "#ffffff", round_=False, sw=1, roughness=0)
    s.text(x0 - 15, y0 + 10, "", 18)
    s.text(70, y0 - 32, "candidates: timestamp text of each frame pair (copied from the video prefix); here 2 fps, so 1 s per candidate", 19, P["muted"])
    s.text(70, y0 + 106, "label yᵢ = 1 if the pair's middle time lies inside the annotated event (here 11–19 s)", 19,
           P["purple"]["text"])
    s.box(70, 370, 715, 290, None, "blue", fill=P["blue"]["soft"])
    s.text(95, 388, "Loss 1: binary cross-entropy", 25, P["blue"]["text"])
    s.text(95, 440, "each interval judged on its own, multi-label\n(several can be positive):\n\nL_BCE = mean over i of BCE(pᵢ, yᵢ)", 21)
    s.box(815, 370, 715, 290, None, "blue", fill=P["blue"]["soft"])
    s.text(840, 388, "Loss 2: soft IoU (stage 2, weight 2)", 25, P["blue"]["text"])
    s.text(840, 440, "rewards covering the whole event, penalises\nprobability outside it, weighted by duration dᵢ:\n\nL_IoU = 1 − Σ dᵢpᵢyᵢ / Σ dᵢ[yᵢ + pᵢ(1−yᵢ)]", 21)
    s.takeaway("Soft IoU matters: without it, mean grounding mIoU drops from 65.3 to 60.7.", y=700)
    s.footer(SRC + ", §2.2, Eq. (2)–(3) and Table 6; 20 intervals drawn for illustration")
    return s


def s_decoding(n):
    s = Slide("11-decoding", n)
    s.title("From interval scores to one span", "Real output of VideoJev-4B on a 10-second clip (README demo)",
            part=PART2, pc="blue")
    probs = [0.0058, 0.0109, 0.0261, 0.9046, 0.9880, 0.9888, 0.9896, 0.9849, 0.8335, 0.3304]
    lt = math.log(0.25 / 0.75)
    adj = [math.log(p / (1 - p)) - lt for p in probs]
    x, y, w, h = 150, 190, 700, 300
    Y = s.axes(x, y, w, h, 0, 1, [0, 0.25, 0.5, 0.75, 1.0], fmt="{:.2f}", ylabel="probability pᵢ")
    s.line([(x, Y(0.25)), (x + w, Y(0.25))], P["red"]["stroke"], 2, dashed=True, roughness=0)
    s.text(x + 10, Y(0.25) - 28, "threshold τ = 0.25", 19, P["red"]["text"])
    bw = w / 10
    for i, p in enumerate(probs):
        on = adj[i] > 0
        s.box(x + i * bw + 8, Y(p), bw - 16, Y(0) - Y(p), None, "blue" if on else "gray", round_=False)
        s.text(x + i * bw + bw / 2, y + h + 10, f"{i}–{i + 1}s", 16, P["muted"], "c")
    s.line([(x + 3 * bw + 8, y + h + 45), (x + 10 * bw - 8, y + h + 45)], P["blue"]["stroke"], 5, roughness=0)
    s.text(x + 6.5 * bw, y + h + 55, "predicted span: 3.0–10.0 s", 21, P["blue"]["text"], "c")
    s.box(930, 175, 600, 400, None, "gray", fill=P["paper"])
    s.text(950, 192, "Decoding rule", 24)
    s.text(950, 238, "1. shift each logit by the threshold:\n    aᵢ = sᵢ − logit(τ)\n    (aᵢ > 0 exactly when pᵢ > τ)\n"
                     "2. pick the contiguous range with the\n    largest sum of aᵢ (Kadane, O(K))\n"
                     "3. its interval boundaries are the\n    answer; if all aᵢ < 0, take the best\n    single interval", 20)
    txt = "  ".join(f"{a:+.1f}" for a in adj)
    s.text(70, 615, "shifted logits aᵢ:  " + txt, 19, P["ink"], mono=True)
    s.text(70, 660, "The last interval (p = 0.33) is still above τ, so the span runs to the end of the clip. "
                    "τ = 0.25 is fixed for all\nexperiments and both model sizes.", 20, P["muted"])
    s.footer("github.com/MCG-NJU/VideoJev README (query: 'The woman in green eats pasta.'); " + SRC + ", Eq. (4)")
    return s


def s_qa(n):
    s = Slide("12-qa", n)
    s.title("Video QA as choosing among scored options", part=PART2, pc="blue")
    s.text(70, 160, "\"What is the woman in green eating?\"   (README demo, VideoJev-4B)", 23, P["blue"]["text"])
    opts = [("A. Pasta.", 0.99992), ("B. Rice.", 0.00006), ("C. Soup.", 0.00003)]
    for k, (o, p) in enumerate(opts):
        y = 215 + k * 70
        s.box(70, y, 260, 52, o, "purple" if k == 0 else "gray", 21, fill=None if k == 0 else "#ffffff")
        s.box(350, y + 10, max(4, 560 * p), 32, None, "blue" if k == 0 else "gray", round_=False)
        s.text(930, y + 26, f"{p:.5f}" if p < 0.01 else f"{p:.4f}", 20, P["ink"], "l", "m")
    s.box(70, 450, 715, 250, None, "blue", fill=P["blue"]["soft"])
    s.text(95, 468, "Training", 25, P["blue"]["text"])
    s.text(95, 512, "exactly one option is correct:\nsoftmax over the option scores,\ncross-entropy on the right one\n\n"
                    "~240K questions over 19K videos\n(internal data, 4–5 options each)", 21)
    s.box(815, 450, 715, 250, None, "orange", fill=P["orange"]["soft"])
    s.text(840, 468, "Avoiding a position shortcut", 25, P["orange"]["text"])
    s.text(840, 512, "options are shuffled in training\n(reproducibly, independent of the\nanswer), so 'A' is not "
                     "always right;\nquestions that refer to positions\nor earlier turns keep their order", 21)
    s.footer("github.com/MCG-NJU/VideoJev README; " + SRC + ", §2.3, Eq. (5) and §2.4")
    return s


def s_inference(n):
    s = Slide("13-inference", n)
    s.title("Encode the video once: Cached and Joint inference", part=PART2, pc="blue")
    # cached
    s.box(70, 160, 715, 420, None, "gray", fill=P["gray"]["soft"])
    s.text(95, 178, "Cached inference: questions arrive one by one", 24)
    s.box(95, 240, 160, 60, "video", "gray", 21, fill=P["purple"]["fill"])
    s.text(175, 310, "prefill once,\nkeep the cache", 18, P["muted"], "c")
    for k in range(3):
        y = 230 + k * 95
        s.arrow([(259, 270), (330, y + 28)], P["ink"])
        s.box(335, y, 120, 56, "copy", "gray", 19, fill="#ffffff")
        harrow(s, 459, 500, y + 28)
        s.box(505, y, 150, 56, f"Q{k + 1} + cands", "gray", 18)
        harrow(s, 659, 700, y + 28)
        s.box(705, y, 60, 56, f"A{k + 1}", "green", 19)
    s.text(95, 520, "one short forward per question", 20, P["muted"])
    # joint
    s.box(815, 160, 715, 420, None, "blue", fill=P["blue"]["soft"])
    s.text(840, 178, "Joint inference: questions known together", 24, P["blue"]["text"])
    x = 840
    for t, c, w in [("video", "gray", 130), ("Q1 ★", "gray", 100), ("Q2 ★", "gray", 100), ("Q3 ★", "gray", 100)]:
        s.box(x, 250, w, 60, t, c, 20, fill=P["purple"]["fill"] if t == "video" else None)
        x += w + 6
    harrow(s, x + 2, x + 40, 280)
    s.text(x + 45, 280, "A1 A2 A3", 21, P["green"]["text"], "l", "m")
    s.text(840, 340, "one causal forward pass for all; each question\nhas its own <|decide|> readout (★)", 20)
    s.text(840, 420, "later questions can attend to earlier questions\nand options, but no answers are inserted\n"
                     "(standard causal attention, no custom mask)", 20, P["muted"])
    s.takeaway("Training uses the same layout: several questions per video share one prefix.", y=610)
    s.box(70, 700, 1460, 90, None, "gray", fill="#ffffff")
    s.text(95, 715, "Generative baselines can reuse the video prefix too, but must still decode each answer token by token;\n"
                    "only single-token answers (a letter) can be read jointly.", 20)
    s.footer(SRC + ", §2.1, §3.4 and App. A.4")
    return s


def s_training(n):
    s = Slide("14-training", n)
    s.title("Training recipe", part=PART2, pc="blue")
    rows = [["1 · head alignment", "scoring head only", "30%", "BCE", "cross-entropy", "160"],
            ["2 · joint adaptation", "language backbone,\nnew tokens, head", "70%", "BCE + 2 × soft IoU", "cross-entropy", "375"]]
    s.table(70, 160, [300, 300, 130, 280, 240, 210], rows,
            header=["stage", "trained", "videos", "grounding loss", "QA loss", "updates"], fs=21, rh=78, hc="blue",
            aligns=["l", "l", "c", "l", "l", "c"])
    s.box(70, 420, 715, 300, None, "gray", fill=P["paper"])
    s.text(95, 438, "Data", 25)
    s.text(95, 482, "grounding: TimeLens-100K + TimeLens2-93K\n(intervals turned into per-candidate labels)\n\n"
                    "QA: ~240K multiple-choice questions over 19K\nvideos, 4 min to ~2 h (internal, not released)", 21)
    s.box(815, 420, 715, 300, None, "gray", fill=P["paper"])
    s.text(840, 438, "Setup", 25)
    s.text(840, 482, "backbones: Qwen3.5-4B, Qwen3.6-35B-A3B\nvision encoder frozen throughout\n"
                     "64 H200 GPUs, 2 fps, up to 144K tokens\nhead LR 3e-4 / 1e-4; backbone LR 5e-6 (4B),\n"
                     "2e-6 (35B-A3B); one epoch per stage", 21)
    s.text(70, 750, "Why two stages? Like projector alignment in LLaVA: give the new head a stable feature space first. "
                    "It is also cheaper.", 20, P["muted"])
    s.footer(SRC + ", §2.4 and §3.1")
    return s


# ======================================================================= results
def s_grounding_results(n):
    s = Slide("15-grounding-results", n)
    s.title("Temporal grounding: best scores, lowest latency", "mIoU per benchmark (TimeLens-refined annotations); "
            "latency per query on full Charades", part=PART3, pc="green")
    rows = [["GPT-5", "–", "40.5", "42.9", "56.8", "46.7"],
            ["Gemini-2.5-Pro", "–", "52.8", "58.1", "70.4", "60.4"],
            ["Qwen3.5-4B (backbone)", "0.763 s", "52.3", "55.6", "67.9", "58.6"],
            ["TimeLens2-4B (best 4B)", "0.646 s", "57.7", "59.0", "69.3", "62.0"],
            ["VideoJev-4B", "0.276 s", "60.1", "62.8", "73.2", "65.3"],
            ["Qwen3.6-35B-A3B (backbone)", "1.054 s", "47.3", "56.0", "67.5", "56.9"],
            ["VideoJev-35B-A3B", "0.336 s", "63.7", "65.5", "74.0", "67.7"]]
    s.table(70, 175, [440, 170, 200, 200, 200, 170], rows,
            header=["model", "latency", "Charades", "ActivityNet", "QVHighlights", "mean"], fs=22, rh=56, hc="green",
            hl_rows={4: "blue", 6: "blue"})
    s.box(70, 640, 1460, 140, None, "yellow")
    s.text(95, 656, "+6.7 and +10.8 mIoU over the backbones, 2.8–3.1× faster, and above Gemini-2.5-Pro.\n"
                    "Stricter overlap improves most: R1@0.7 vs TimeLens2-4B is +2.8 to +4.8 points per benchmark.", 23)
    s.footer(SRC + ", Table 1 (selected rows; all open models in the table are below VideoJev)")
    return s


def s_qa_results(n):
    s = Slide("16-qa-results", n)
    s.title("Video QA: as good as Thinking, about 100× faster", "Accuracy (MLVU: M-Avg); latency per question on full LVBench",
            part=PART3, pc="green")
    rows = [["Qwen3.5-4B Instruct", "1.4 s", "60.0", "70.6", "61.2", "73.3", "66.3"],
            ["Qwen3.5-4B Thinking", "144.9 s", "66.4", "76.9", "73.6", "82.8", "74.9"],
            ["VideoJev-4B", "1.1 s", "67.9", "75.0", "73.6", "80.6", "74.3"],
            ["Qwen3.6-35B-A3B Instruct", "2.4 s", "66.0", "77.1", "72.4", "79.5", "73.8"],
            ["Qwen3.6-35B-A3B Thinking", "149.8 s", "71.4", "82.5", "74.9", "86.2", "78.8"],
            ["VideoJev-35B-A3B", "1.5 s", "73.4", "81.8", "77.1", "85.9", "79.5"]]
    s.table(70, 175, [400, 150, 165, 175, 220, 150, 150], rows,
            header=["model", "latency", "LVBench", "Video-MME", "LongVideoBench", "MLVU", "mean"], fs=22, rh=58,
            hc="green", hl_rows={2: "blue", 5: "blue"})
    s.box(70, 600, 715, 180, None, "blue", fill=P["blue"]["soft"])
    s.text(95, 618, "vs Instruct backbones", 24, P["blue"]["text"])
    s.text(95, 660, "+8.0 (4B) and +5.7 (35B-A3B) mean points,\nat similar latency", 21)
    s.box(815, 600, 715, 180, None, "orange", fill=P["orange"]["soft"])
    s.text(840, 618, "vs Thinking", 24, P["orange"]["text"])
    s.text(840, 660, "−0.6 (4B) and +0.7 (35B-A3B) mean points,\n129× and 100× faster; Thinking still wins on\n"
                     "Video-MME and MLVU", 21)
    s.footer(SRC + ", Table 2 (frames only, no subtitles or audio)")
    return s


def s_tradeoff(n):
    s = Slide("17-quality-vs-latency", n)
    s.title("Quality against latency", "Upper left is better; the x-axis is logarithmic", part=PART3, pc="green")
    g = [("Molmo2-4B", 0.636, 45.5, "gray"), ("Qwen3.5-4B", 0.763, 58.6, "orange"), ("TimeLens2-4B", 0.646, 62.0, "gray"),
         ("Video-ORA-4B", 2.347, 60.5, "gray"), ("Nemotron-30B", 3.882, 46.2, "gray"),
         ("Qwen3.6-35B", 1.054, 56.9, "orange"), ("VideoJev-4B", 0.276, 65.3, "blue"), ("VideoJev-35B", 0.336, 67.7, "blue")]
    q = [("Qwen3.5-4B Instr.", 1.355, 66.3, "orange"), ("Qwen3.5-4B Think.", 144.929, 74.9, "orange"),
         ("Qwen3.6-35B Instr.", 2.379, 73.8, "orange"), ("Qwen3.6-35B Think.", 149.777, 78.8, "orange"),
         ("Nemotron-30B Think.", 229.095, 68.4, "gray"), ("Qwen3-VL-30B Instr.", 4.817, 72.3, "gray"),
         ("VideoJev-4B", 1.123, 74.3, "blue"), ("VideoJev-35B", 1.493, 79.5, "blue")]

    def plot(x, y, w, h, pts, lo, hi, ymin, ymax, ticks, yt, title):
        s.text(x, y - 60, title, 23, P["ink"])
        Y = s.axes(x, y, w, h, ymin, ymax, yt, ylabel=None)
        for t in ticks:
            xx = logx(t, lo, hi, x, w)
            s.line([(xx, y + h), (xx, y + h + 6)], P["ink"], 1, roughness=0)
            s.text(xx, y + h + 10, f"{t:g}", 16, P["muted"], "c")
        s.text(x + w / 2, y + h + 36, "seconds per query (log)", 17, P["muted"], "c")
        for name, lat, v, c in pts:
            px, py = logx(lat, lo, hi, x, w), Y(v)
            s.box(px - 9, py - 9, 18, 18, None, c, fill=P[c]["stroke"] if c != "gray" else P["faint"],
                  shape="ellipse", round_=False, roughness=0)
            right = px < x + w * 0.62
            if name == "VideoJev-4B" and v > 70:
                py -= 22
            if name == "Qwen3.6-35B Instr.":
                py += 18
            s.text(px + (14 if right else -14), py, name, 16, P[c]["text"] if c != "gray" else P["muted"],
                   "l" if right else "r", "m")
    plot(130, 220, 560, 470, g, 0.2, 5, 44, 70, [0.25, 0.5, 1, 2, 4], [45, 50, 55, 60, 65, 70],
         "Temporal grounding · mean mIoU")
    plot(900, 220, 600, 470, q, 0.8, 300, 64, 82, [1, 3, 10, 30, 100, 300], [65, 70, 75, 80],
         "Video QA · mean accuracy")
    s.footer(SRC + ", Tables 1–2 and Figure 1 (selected models redrawn)")
    return s


def s_scaling(n):
    s = Slide("18-many-queries", n)
    s.title("Ten questions about one video", "Total model time for 10 queries per video, VideoJev-4B vs Qwen3.5-4B (log scale)",
            part=PART3, pc="green")
    bars = [("grounding", [("VideoJev Joint", 0.39, "blue", "60.1 mIoU"), ("VideoJev Cached", 0.85, "blue", "58.6 mIoU"),
                           ("Qwen Instruct", 5.98, "orange", "52.3 mIoU")]),
            ("video QA", [("VideoJev Joint", 1.64, "blue", "67.9%"), ("Qwen Direct, Joint", 1.67, "orange", "58.7%"),
                          ("VideoJev Cached", 2.17, "blue", "67.1%"), ("Qwen Thinking", 1393, "orange", "66.4%")])]
    lo, hi = 0.1, 3000
    x0, w = 380, 1000
    y = 190
    for t in [0.1, 1, 10, 100, 1000]:
        xx = logx(t, lo, hi, x0, w)
        s.line([(xx, y - 10), (xx, 700)], P["grid"], 1, roughness=0)
        s.text(xx, 705, f"{t:g} s", 17, P["muted"], "c")
    for name, items in bars:
        s.text(70, y, name, 24, P["ink"])
        y += 42
        for lab, v, c, qual in items:
            s.text(360, y + 19, lab, 19, P[c]["text"], "r", "m")
            xe = logx(v, lo, hi, x0, w)
            s.box(x0, y, xe - x0, 38, None, c, round_=False)
            s.text(xe + 10, y + 19, f"{v:g} s · {qual}", 18, P["ink"], "l", "m")
            y += 50
        y += 20
    s.box(70, 740, 1460, 70, None, "yellow")
    s.text(95, 758, "Joint inference: going from 1 to 10 questions adds only 55 ms (grounding) and 31 ms (QA).", 22)
    s.footer(SRC + ", §3.5 and Figure 3 (40 videos per task, H200, batch 1); quality from the full benchmarks, "
             "Cached QA from Table 4")
    return s


def s_ar_control(n):
    s = Slide("19-architecture-or-data", n)
    s.title("Is it the architecture or the training data?", "Same data, same single-stage schedule: scoring head vs "
            "ordinary autoregressive fine-tuning", part=PART3, pc="green")
    rows = [["VideoJev-4B (single stage)", "60.6", "62.8", "72.9", "65.4", "67.7", "74.9", "73.5", "74.7"],
            ["Qwen3.5-4B, autoregressive SFT", "61.0", "61.3", "70.0", "64.1", "66.9", "74.5", "71.4", "72.8"]]
    s.table(70, 190, [400, 125, 140, 140, 125, 130, 140, 140, 120], rows,
            header=["model", "Charades", "ActivityNet", "QVHighl.", "mean", "LVBench", "Video-MME", "LongVB", "QA mean"],
            fs=21, rh=62, hc="green", hl_rows={0: "blue"})
    s.text(70, 400, "Autoregressive model: generates the interval as JSON in seconds, or the option letter; same videos, "
                    "same frozen encoder.", 20, P["muted"])
    s.box(70, 470, 715, 200, None, "blue", fill=P["blue"]["soft"])
    s.text(95, 488, "Scoring wins on average", 25, P["blue"]["text"])
    s.text(95, 535, "+1.3 grounding mIoU and +1.9 QA points with\nidentical supervision: the readout fits the\n"
                    "decision better", 21)
    s.box(815, 470, 715, 200, None, "orange", fill=P["orange"]["soft"])
    s.text(840, 488, "But the gap is modest", 25, P["orange"]["text"])
    s.text(840, 535, "most of the gain over the backbone comes\nfrom fine-tuning itself; autoregressive SFT\n"
                     "is even better on Charades (+0.4)", 21)
    s.footer(SRC + ", Table 3 and App. A.3 (the MLVU cell of the autoregressive row is empty in the HTML table)")
    return s


def s_ablations(n):
    s = Slide("20-ablations", n)
    s.title("Ablations: what each design choice is worth", "Change in mean score when the choice is removed (VideoJev-4B)",
            part=PART3, pc="green")
    items = [("Soft IoU loss", -4.6, -0.4), ("training on both tasks", -0.7, -1.3), ("Joint (vs Cached) inference", -0.8, -0.5),
             ("removing the final MLP", -0.2, -0.2), ("two-stage training (→ single-stage)", +0.1, +0.4)]
    x0, w = 640, 800
    lo, hi = -5, 1
    def X(v):
        return x0 + (v - lo) / (hi - lo) * w
    y = 190
    s.text(X(-2.5), y - 4, "← worse without it", 19, P["muted"], "c")
    for t in [-5, -4, -3, -2, -1, 0, 1]:
        s.line([(X(t), y + 20), (X(t), y + 520)], P["grid"] if t else P["ink"], 1 if t else 2, roughness=0)
        s.text(X(t), y + 525, f"{t:+d}" if t else "0", 17, P["muted"], "c")
    y += 40
    for lab, tg, qa in items:
        s.text(600, y + 38, lab, 21, P["ink"], "r", "m")
        for k, (v, c, nm) in enumerate([(tg, "purple", "grounding"), (qa, "blue", "QA")]):
            yy = y + 8 + k * 36
            a, b = sorted([X(0), X(v)])
            s.box(a, yy, max(3, b - a), 30, None, c, round_=False)
            s.text((a - 8) if v < 0 else (b + 8), yy + 15, f"{v:+.1f}", 17, P[c]["text"], "r" if v < 0 else "l", "m")
        y += 98
    s.box(1140, 160, 30, 22, None, "purple", round_=False)
    s.text(1178, 160, "grounding mIoU", 18)
    s.box(1340, 160, 30, 22, None, "blue", round_=False)
    s.text(1378, 160, "QA mean", 18)
    s.text(70, 760, "Soft IoU is the big one. Single-stage training is slightly better (+0.4 QA, mostly MLVU); "
                    "two stages are kept because\nthey are cheaper (backbone updated on 70% of the videos).", 20, P["muted"])
    s.footer(SRC + ", Tables 4–8")
    return s


def s_calibration(n):
    s = Slide("21-calibration", n)
    s.title("Confidence: useful for ranking, not yet calibrated", part=PART3, pc="purple")
    s.box(70, 170, 715, 300, None, "green", fill=P["green"]["soft"])
    s.text(95, 188, "High confidence → high accuracy", 25, P["green"]["text"])
    x, y0 = 110, 260
    for k, (lab, v, c) in enumerate([("all 1,549 questions", 73.4, "gray"), ("591 with confidence ≥ 99%", 95.8, "green")]):
        y = y0 + k * 80
        s.box(x + 330, y, 2.4 * v, 46, None, c, round_=False)
        s.text(x + 320, y + 23, lab, 19, P["ink"], "r", "m")
        s.text(x + 340 + 2.4 * v, y + 23, f"{v}%", 20, P["ink"], "l", "m")
    s.text(95, 430, "VideoJev-35B-A3B on LVBench", 18, P["muted"])
    s.box(815, 170, 715, 300, None, "orange", fill=P["orange"]["soft"])
    s.text(840, 188, "But probabilities are overconfident", 25, P["orange"]["text"])
    s.text(840, 238, "expected calibration error, mean of 4 QA\nbenchmarks:\n\n  8.65 points (4B)\n  8.13 points (35B-A3B)\n\n"
                     "no calibration-specific training", 21)
    s.box(70, 510, 1460, 170, None, "yellow")
    s.text(95, 528, "A difference from Jev", 24)
    s.text(95, 572, "Jev is trained with reinforcement learning to output calibrated probabilities; VideoJev is not.\n"
                    "The authors suggest temperature scaling on held-out data or calibration-aware training.", 22)
    s.footer(SRC + ", §3.5 and Figure 4")
    return s


def s_system2(n):
    s = Slide("22-system-two", n)
    s.title("Where this fits: System 2 asks, System 1 checks", part=PART3, pc="purple")
    s.box(70, 180, 470, 380, None, "orange", fill=P["orange"]["soft"])
    s.text(95, 198, "System 2: planner", 26, P["orange"]["text"])
    s.text(95, 248, "an LLM agent or a fixed\nprocedure:\n\n• breaks a goal into checks\n• proposes candidate events,\n"
                    "  actions or states\n• reasons when results are\n  ambiguous", 21)
    s.box(1060, 180, 470, 380, None, "blue", fill=P["blue"]["soft"])
    s.text(1085, 198, "System 1: VideoJev", 26, P["blue"]["text"])
    s.text(1085, 248, "scores each candidate against\nthe video, fast, with\nprobabilities:\n\n• when did X happen?\n"
                      "• which of A, B, C is true?", 21)
    s.arrow([(545, 300), (1055, 300)], P["ink"], 2)
    s.text(800, 270, "questions + candidates", 20, P["ink"], "c")
    s.arrow([(1055, 430), (545, 430)], P["ink"], 2)
    s.text(800, 400, "spans, options, confidence", 20, P["ink"], "c")
    s.text(800, 470, "uncertain → escalate", 18, P["orange"]["text"], "c")
    s.text(70, 610, "\"System Two organizes the decision space, while System One evaluates it against visual evidence.\"",
           24, P["blue"]["text"])
    s.text(70, 670, "Applications named: procedural monitoring, interactive assistance, embodied agents, computer use. "
                    "Next steps: more\ntask types (action recognition, event detection), streaming input, better calibration.",
           20, P["muted"])
    s.footer(SRC + ", §5 (future work; not evaluated in the paper)")
    return s


# ======================================================================= discussion
def s_critique(n):
    s = Slide("23-critique", n)
    s.title("Reading it critically", part=PART4, pc="yellow")
    panel(s, 70, 160, 600, 620, "Strong", "• one head unifies two task types;\n  simple, reusable design\n\n"
          "• careful latency protocol: generative\n  baselines also reuse the video prefix\n\n"
          "• controlled comparison with\n  autoregressive SFT on the same data\n\n• models and code released", "green", 30, 22)
    panel(s, 700, 160, 830, 620, "Weak or unclear", "• closed set: someone must supply the candidates;\n"
          "  one contiguous span per query only\n\n• QA training data is internal; gains partly from data\n"
          "  (scoring adds +1.3 / +1.9 over autoregressive SFT)\n\n"
          "• latency excludes video decoding and preprocessing,\n  which also cost time in real systems\n\n"
          "• Joint inference: later questions see earlier ones;\n  order effects are not studied\n\n"
          "• overconfident probabilities (ECE ≈ 8 points)\n\n• 'System One' comes from a vendor blog", "orange", 30, 21)
    s.footer(SRC + ", §2–§3, App. A")
    return s


def s_takeaways(n):
    s = Slide("24-takeaways", n)
    s.title("Takeaways", part=PART4, pc="yellow")
    items = [("blue", "1 · Score, don't write", "For spans and choices, scoring beats generating: +6.7 / +10.8 mIoU over the backbones,\n"
                                              "+1.3 over autoregressive fine-tuning on the same data."),
             ("green", "2 · Encode the video once", "Joint inference: ten questions cost almost the same as one "
                                                  "(+55 ms grounding, +31 ms QA)."),
             ("purple", "3 · Close to Thinking without thinking", "Video QA within 0.6 points of, or above, Thinking mode, "
                                                                "at about 1/100 of the time."),
             ("orange", "4 · Training choices matter", "Soft IoU is worth +4.6 mIoU; training grounding and QA together helps "
                                                     "both tasks (+0.7 / +1.3)."),
             ("red", "5 · Confidence is a bonus, not yet reliable", "High confidence predicts correctness, but the "
                                                                   "probabilities are overconfident (ECE ≈ 8 points).")]
    for i, (c, a, b) in enumerate(items):
        y = 150 + i * 122
        s.box(70, y, 1460, 106, None, c, fill=P[c]["soft"])
        s.text(95, y + 14, a, 26, P[c]["text"])
        s.text(95, y + 52, b, 20 if "\n" in b else 21, P["ink"])
    s.text(70, 775, "arxiv.org/abs/2610.18615  ·  github.com/MCG-NJU/VideoJev", 21, P["muted"], mono=True)
    s.footer("")
    return s


SLIDES = [s_title, s_tldr, s_glossary,
          s_tasks, s_generate, s_kahneman, s_system_one, s_why_video,
          s_architecture, s_scorer, s_frame_pairs, s_grounding, s_decoding, s_qa, s_inference, s_training,
          s_grounding_results, s_qa_results, s_tradeoff, s_scaling, s_ar_control, s_ablations, s_calibration, s_system2,
          s_critique, s_takeaways]

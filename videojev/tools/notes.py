"""Speaker notes, keyed by slide slug (file name without the number). Used by make_deck.py.

Each note: "Terms" (technical words on the slide, in plain words), "Say" (a short script using the slide's terms),
"Point to" cues, and a "Bridge" to the next slide. STORY goes at the top of slides/speaker-notes.md.
"""

STORY = """The story in six sentences:

1. Many questions an agent asks about a video have tiny answers: "when did X happen?" (a time span) or "which of A, B, C?" (an option).
2. Today's video MLLMs still write these answers token by token, and the accurate "Thinking" mode takes minutes per question.
3. VideoJev follows the System One idea (Jev): put the candidates (time intervals or options) into the prompt and score them all in one forward pass with a small shared head.
4. Because the model is causal, the video prefix is computed once: Cached inference reuses it for questions that arrive later, Joint inference scores many questions in one pass.
5. Result: better temporal grounding than the backbones (+6.7 / +10.8 mIoU) at about 3x the speed, and video QA as good as Thinking at about 1/100 of the time.
6. Limits: candidates must be supplied, the QA training data is internal, and the confidence scores are overconfident."""

NOTES = {
    "title": """Terms: System One model = a fast model that returns a decision with probabilities instead of free text. Jev = the text System One model this paper builds on.

Say: Today's paper is VideoJev, from Nanjing University and JD.com, October 2026. The one-line summary is at the bottom: a video model that answers by scoring candidates instead of writing answers.

Point to the row of boxes: one video is encoded once; then several questions, some asking "when?", some "which?", each get an answer from scores, all in one forward pass.

Bridge: Here is the paper in one slide.""",

    "tldr": """Terms: mIoU = how much the predicted time span overlaps the true one. Thinking = the model reasons in text before answering.

Say: Three boxes. Problem: video MLLMs write their answers token by token, even when the answer is just a time span or one letter. That is slow; the Thinking mode of Qwen3.5-4B takes 145 seconds per question. And an agent asks many questions about the same video.

Idea: put a small System One head on the MLLM. For grounding, score every short time interval and pick a span; for QA, score every option. Encode the video once and answer many questions in one pass.

Evidence: grounding gets 6.7 and 10.8 points better than the backbones and about three times faster; QA is about as good as Thinking but 100 to 129 times faster.

Bridge: A quick glossary first.""",

    "glossary": """Terms: as on the slide.

Say: Only a few terms matter. Temporal grounding: find when an event happens. Multiple-choice video QA: pick one of four or five options. mIoU measures the overlap of the predicted and true span. Instruct versus Thinking: answering directly versus reasoning first. Prefill and KV cache: the model processes the video once and stores the result so it can be reused. Cached and Joint inference are the paper's two ways of reusing it; we come back to them.

Bridge: Let us start with the two tasks.""",

    "tasks": """Terms: temporal grounding, mIoU, R1@0.7 (share of queries with overlap at least 0.7), multiple-choice video QA.

Say: Two kinds of questions. Left: "when is chocolate added to the waffles?" The answer is a span, here 11 to 19 seconds. Right: "what is drizzled onto the waffles?" The answer is one option.

Point to the yellow line: both answers are tiny, two numbers or one letter. Keep that in mind for the next slide.

Bridge: So how do current models produce these tiny answers?""",

    "generate": """Terms: autoregressive = token by token. Instruct / Thinking modes. Latency = model time per question on an H200 GPU.

Say: Today's video MLLMs write the answer. For grounding they generate a sentence with timestamps; for QA, in Thinking mode, they first write a reasoning trace and then the letter.

Point to the orange box: that costs time per token, the text has to be parsed, there is no confidence score, and every new question decodes again.

Point to the table: the numbers make it concrete. Qwen3.5-4B answers a long-video question in 1.4 seconds in Instruct mode and 145 seconds in Thinking mode. Thinking buys 8.6 accuracy points for about 107 times the time.

Bridge: A detour through psychology explains the paper's name.""",

    "fast-and-slow": """Terms: System 1 = fast, instinctive, emotional thinking. System 2 = slower, deliberative, logical thinking. Both from Daniel Kahneman's book Thinking, Fast and Slow (2011).

Say: The name "System One model" comes from psychology. In Thinking, Fast and Slow, Daniel Kahneman, a Nobel laureate in economics, describes two modes of thought.

Point to the blue panel: System 1 is fast, instinctive and emotional. Ask yourself 2 + 2: the answer arrives before you decide to think.

Point to the orange panel: System 2 is slow, deliberative and logical. 17 times 24 (Kahneman's own example) needs effort, step by step: 408.

Point to the table: the same split appears in AI. A chat LLM in Thinking mode is System 2: it reasons in text, then answers. A System One model like Jev or VideoJev is System 1: one forward pass, one decision with probabilities.

Point to the yellow line: people use System 1 most of the time and call System 2 only when needed. The paper wants agents to work the same way: fast checks by default, slow reasoning when a check is uncertain.

Bridge: Jev is the first model built on this idea.""",

    "system-one": """Terms: System 1 / System 2 = Kahneman's fast intuitive versus slow deliberate thinking. Typed decision = an answer of a fixed form, such as a choice or yes/no.

Say: Jev, from the company TypeSafe AI, is a "System One" model: instead of writing text, it returns a typed decision with probabilities, in one pass. It is trained with reinforcement learning so that the probabilities are calibrated. The name Jev refers to the economist Jevons: when decisions get cheaper, people use far more of them. There are already image versions; this paper does it for video.

Point to the yellow box: the paper's premise. Structured judgments can support open-ended behaviour without generating open-ended text at every step.

Note: what we know about Jev comes from the vendor's blog, not from a peer-reviewed paper.

Bridge: Why is video harder than images?""",

    "why-video": """Terms: visual history = everything the camera has seen so far.

Say: The paper's example is a cooking assistant. It asks many different questions about the same video: has the egg been added, when did the pan go on, which step comes next.

Two requirements follow. First, time: the answer is often a span, not a frame. Second, reuse: encoding the video is the expensive part, so each extra question should be cheap.

Bridge: Here is how VideoJev meets both. First the architecture.""",

    "architecture": """Terms: candidate = one possible answer (a time interval or an option). <|option_end|> and <|decide|> = two new special tokens. Readout = the hidden state at a token, used for prediction. Causal = each token only sees earlier tokens.

Say: The input is one sequence: video tokens, then the task and the question, then the list of candidates. After each candidate comes an <|option_end|> token; after the list comes one <|decide|> token.

The MLLM runs once. At each <|option_end|> we read a candidate state; at <|decide|> we read a decision state. A small shared scorer turns them into one score per candidate.

Point to the bottom left: because the model is causal, each candidate readout sees the video, the question and the candidates before it, and <|decide|> sees the whole list.

Point to the bottom right: the changes are small: two new tokens, no language-model head, the final MLP layer removed, and the vision encoder stays frozen.

Bridge: What does the scorer compute?""",

    "scorer": """Terms: projection = a learned linear layer. Normalise = scale to length 1. Cosine similarity = dot product of two length-1 vectors. Sigmoid / softmax.

Say: The decision state goes through a Q projection, the candidate state through a K projection, both to 512 dimensions, both normalised. The score is 10 times their dot product plus a learned bias. So it is a cosine similarity between "what is asked" and "this candidate".

Point to the two purple boxes: the same head serves both tasks; only the output rule differs. Grounding uses a sigmoid per interval, because several intervals can belong to the event. QA uses a softmax over the options, because exactly one is right.

Bridge: Grounding in more detail.""",

    "grounding": """Terms: frame pair = the backbone merges two frames into one visual unit, so each candidate interval covers two frames. BCE = binary cross-entropy. Soft IoU = a differentiable version of the overlap measure.

Say: Every frame pair is one candidate, written as its timestamp text. The label is 1 if the middle of the pair falls inside the annotated event. So grounding becomes many small yes/no decisions.

Two losses. Binary cross-entropy judges each interval on its own. Soft IoU looks at the whole event: it rewards probability inside the event and penalises probability outside, weighted by interval length.

Point to the yellow line: soft IoU matters a lot; without it mean mIoU drops from 65.3 to 60.7.

Bridge: How do the interval scores become one span?""",

    "decoding": """Terms: logit = score before the sigmoid. Threshold τ. Kadane's algorithm = finds the contiguous range with the largest sum in one pass.

Say: This is a real output of VideoJev-4B from the README, a 10-second clip, query "the woman in green eats pasta". The bars are the probabilities per one-second interval.

Point to the panel: shift every logit by the threshold; with τ = 0.25, a shifted logit is positive exactly when the probability is above 0.25. Then take the contiguous range with the largest sum. Here that is 3 to 10 seconds.

Point to the last bar: its probability is only 0.33, but still above the threshold, so the span runs to the end. τ is fixed at 0.25 for all experiments.

Bridge: QA is simpler.""",

    "qa": """Terms: softmax, cross-entropy, position bias = a model learning that some option position (say A) is often right.

Say: Same README demo: "what is the woman in green eating?" Pasta gets 0.9999, the others almost nothing.

Training: exactly one option is correct, so softmax and cross-entropy. The QA data is about 240 thousand internal questions over 19 thousand videos.

Point to the orange box: options are shuffled during training so the model cannot learn that "A" is usually right; questions that refer to positions keep their order.

Bridge: Now the second idea: reuse the video.""",

    "inference": """Terms: prefill = processing the prompt once. KV cache = the stored result. Cached inference, Joint inference.

Say: Because the model is causal, the video part of the sequence does not depend on the questions that follow. So it can be computed once.

Left, Cached inference: questions arrive one by one. Prefill the video once, keep the cache, and for each new question continue from a copy. One short forward per question.

Right, Joint inference: when the questions are known together, put them all after the video, each with its own <|decide|>, and score everything in one forward pass. Later questions can see earlier questions and options, but no answers are inserted.

Point to the bottom box: generative baselines can reuse the video cache too, and in the paper's timing they do. But they still decode every answer token by token.

Bridge: How is it trained?""",

    "training": """Terms: head alignment = train only the new head first. Learning rate (LR).

Say: Two stages. Stage one trains only the scoring head, on 30% of the videos, with the backbone frozen. Stage two trains the language backbone, the new tokens and the head together on the other 70%, and adds the soft IoU loss.

Data: public grounding data from TimeLens, and the internal QA set. Two backbones: Qwen3.5-4B and Qwen3.6-35B-A3B. 64 H200 GPUs.

Why two stages? Like LLaVA's projector alignment: give the new head a stable feature space before the backbone moves. It is also cheaper.

Bridge: Results, starting with grounding.""",

    "grounding-results": """Terms: mIoU per benchmark, TimeLens-refined annotations = cleaned labels of the three benchmarks.

Say: Three grounding benchmarks. VideoJev-4B reaches 65.3 mean mIoU, 6.7 above its backbone and 3.3 above TimeLens2-4B, the best other 4B model. VideoJev-35B-A3B reaches 67.7, 10.8 above its backbone. Both are also above Gemini-2.5-Pro and GPT-5.

Point to the latency column: and they are the fastest, 0.28 and 0.34 seconds per query, about three times faster than the backbones.

Point to the yellow box: the gains are largest at the strict overlap threshold, which means more precise boundaries.

Bridge: Now video QA.""",

    "qa-results": """Terms: accuracy, M-Avg (MLVU's mean over its tasks), Instruct / Thinking.

Say: Four long-video QA benchmarks. Compare each VideoJev with its own backbone in both modes.

Left box: against Instruct, VideoJev is 8.0 and 5.7 points better at similar latency.

Right box: against Thinking, the 4B model is 0.6 points behind and the 35B model 0.7 points ahead, while being 129 and 100 times faster. Thinking still wins on Video-MME and MLVU.

Bridge: The same in one picture.""",

    "quality-vs-latency": """Terms: log scale = each tick is a multiple, not a fixed step.

Say: Quality against latency; upper left is better. On the left, grounding: the two blue VideoJev points sit alone in the upper left. On the right, QA: the Thinking models reach VideoJev's quality only far to the right, at more than 100 seconds per question.

Bridge: So far one question at a time. What about many questions about the same video?""",

    "many-queries": """Terms: Joint / Cached inference; Qwen Direct = the autoregressive model answering with exactly one option letter.

Say: Ten questions about one video, total model time, log scale. Grounding: VideoJev Joint 0.39 seconds, Cached 0.85, while Qwen generating timestamps needs 6 seconds and is less accurate.

QA: VideoJev Joint 1.64 seconds at 67.9%. Qwen can also read single letters jointly, at the same speed, but its accuracy drops to 58.7%. Qwen Thinking needs 1,393 seconds.

Point to the yellow line: with Joint inference, going from one to ten questions adds only 55 and 31 milliseconds.

Bridge: Are the gains from the architecture or just from the training data?""",

    "architecture-or-data": """Terms: autoregressive SFT = ordinary fine-tuning to generate the answer text. Single-stage = training everything at once.

Say: A fair control: the same Qwen3.5-4B, fine-tuned on exactly the same data with the same single-stage schedule, but generating the answer as usual.

VideoJev is better on average by 1.3 mIoU and 1.9 QA points. So the scoring readout helps beyond the data.

Point to the orange box: but be honest about the size. Most of the improvement over the original backbone comes from fine-tuning on this data; the scoring head adds a modest extra. The autoregressive model is even slightly better on Charades.

Bridge: What else matters? The ablations.""",

    "ablations": """Terms: ablation = remove one part and measure the change.

Say: Each row removes one design choice; bars show the change in mean score, grounding in purple, QA in blue.

Soft IoU is by far the biggest: minus 4.6 mIoU without it. Training both tasks together helps both. Joint inference is slightly better than Cached, which is surprising, since later questions see earlier ones; the authors think it matches the training layout. Removing the final MLP costs nothing.

Point to the last row: single-stage training is actually slightly better; they keep two stages because it is cheaper.

Bridge: One more output: confidence.""",

    "calibration": """Terms: calibration = when the model says 90%, it is right 90% of the time. ECE = expected calibration error, the average gap.

Say: Because VideoJev outputs probabilities, we get confidence for free. Left: on LVBench, when the 35B model is at least 99% sure, it is right 95.8% of the time, versus 73.4% overall. Useful for deciding when to trust an answer.

Right: but the probabilities are too high on average, by about 8 points. Unlike Jev, VideoJev gets no calibration training.

Bridge: Where would such a model be used?""",

    "system-two": """Terms: System 2 planner = an LLM agent or fixed procedure. Escalate = hand an uncertain case to slower reasoning.

Say: The authors' picture of the future. A System 2 planner breaks a goal into checks and proposes candidates; VideoJev scores them against the video, fast, with probabilities; uncertain answers go back for more reasoning.

This is a vision; it is not evaluated in the paper.

Bridge: Time to be critical.""",

    "critique": """Say: Strong: one simple head for two task types; a careful latency protocol where the generative baselines also reuse the video; the controlled comparison with autoregressive fine-tuning; and released models and code.

Weak or unclear: someone must supply the candidates, and grounding returns one contiguous span per query. The QA training data is internal, and part of the gain is data. The latency excludes video decoding and preprocessing. In Joint inference later questions see earlier ones, and the effect of question order is not studied. Probabilities are overconfident. And "System One" comes from a vendor blog.

Bridge: To close, five takeaways.""",

    "takeaways": """Say: One: if the answer is a span or a choice, score it, don't write it. Two: encode the video once; ten questions cost almost the same as one. Three: close to Thinking quality without thinking, at about one hundredth of the time. Four: training choices matter, soft IoU most of all. Five: confidence comes for free but is not yet reliable.

Thank you. Questions?""",
}

# Speaker notes — QARM V2: Quantitative Alignment Multi-Modal Recommendation for Reasoning User Sequence Modeling

Paper club · 8 October 2026 · arXiv:2602.08559 (predecessor: arXiv:2411.11739)

The story in six sentences:

1. Kuaishou's recommender must guess what each user wants next, from a history of 100,000+ interactions.
2. It does this in two steps: first pick the few past items related to the candidate (GSU), then look at them closely (ESU).
3. Both steps need to know which items are "related", and item IDs alone are bad at that, especially for new items.
4. An LLM understands items, but its idea of "similar" is wrong for shopping, and a frozen LLM vector cannot be trained by the recommender.
5. QARM V2 fixes the first problem by teaching the LLM business similarity from cleaned item pairs, and the second by turning its vectors into short codes (semantic IDs) that the recommender can learn.
6. It works in production (several percent more revenue and GMV), but the paper does not show which part of the recipe causes the gains.

---

## 1. title

![slide 1](svg/01-title.svg)

Say: Today's paper is QARM V2, from Kuaishou, the Chinese short-video and live-streaming platform. It is the follow-up to QARM from 2024, so we will look at both.

Point to the row of boxes: this is the whole paper in one line. An LLM reads an item (its title, images, text in the images). It produces a vector, which helps find related items. It also produces short codes, which the ranking model can learn from. In the end the system predicts clicks and purchases.

Bridge: Here is the paper in one slide.

## 2. tldr

![slide 2](svg/02-tldr.svg)

Say: Three boxes, read left to right.

Problem: everybody tries to add LLM vectors to their recommender, and it usually helps only a little. The paper gives two reasons. First, the LLM thinks two items are similar when they look alike, but shoppers care about whether items are used together. Second, the LLM vector is frozen, so the recommender cannot adjust it.

Fixes: one fix for each reason. Clean the training data with a reasoning LLM and train the LLM in a smarter way. Then cut its vector into short codes that the recommender can learn.

Evidence: real online tests with several percent more revenue, plus offline gains.

Point to the yellow line: keep this in mind. The results are strong, but there are almost no experiments that show which part does the work.

Bridge: Before we start, two slides of vocabulary. I will go through them quickly.

## 3. glossary models

![slide 3](svg/03-glossary-models.svg)

Say: Recommendation papers use many short names. You only need four of them for today.

GSU and ESU: two steps. GSU is a quick filter, "pick the 50 past items most related to this candidate". ESU is the careful step that looks at those 50 and is trained with the rest of the model.

SIM is the 2020 Alibaba paper that introduced these two steps. TWIN is Kuaishou's own version from 2023.

Semantic ID: an item written as three small codes, like a postal code. The first part is coarse, the last part is specific.

The rest is for reference. Skip it unless someone asks.

Bridge: The second glossary covers numbers and metrics.

## 4. glossary metrics

![slide 4](svg/04-glossary-metrics.svg)

Say: Only three lines matter for reading the results.

CTR is the chance a user clicks. CVR is the chance they buy after clicking.

AUC measures how well the model ranks good items above bad ones; 50 is random guessing. GAUC is the same, computed per user and then averaged. In industry, a gain of 0.1 points is already worth money.

GMV is the total money spent on orders.

Bridge: Now the setting. Why is this problem hard at Kuaishou?

## 5. setting

![slide 5](svg/05-setting.svg)

Say: Three numbers. 400 million people use the app every day. Tens of millions of new videos, live streams and products appear every day. An active user has more than 100,000 past interactions.

The model should use that whole history, but checking 100,000 items for every recommendation is far too slow. So every system first shrinks the history.

Point to the blue box: items are not just IDs. They have titles, pictures, text in the pictures and speech. An LLM can read all of that. Both papers ask how to turn that understanding into something the recommender can use.

Bridge: Let us see how the history is shrunk.

## 6. gsu esu

![slide 6](svg/06-gsu-esu.svg)

Say: This is the standard design for long histories, from SIM and TWIN.

Point top left: the long history. Point right: the candidate, which we call the target item.

Step 1, the GSU: a cheap search keeps only the K past items most related to the target. Point to the blue squares: those survive.

Step 2, the ESU: the model looks carefully at those K items, weighs them against the target, and predicts click and purchase.

Point to the orange box: everything depends on what "related" means in step 1. Older systems use the same category, or similar ID vectors. QARM V2 uses the LLM: the LLM vector for step 1, and LLM-based codes for step 2.

Bridge: Why not simply keep using IDs?

## 7. ids vs llm

![slide 7](svg/07-ids-vs-llm.svg)

Say: Today recommenders learn one vector per item ID from clicks. That has three weaknesses.

Row 1: there are billions of IDs and new ones every day. An LLM uses a fixed vocabulary of words.

Row 2: what an ID vector learned is stored only in that vector. When the item disappears, the knowledge disappears too. An LLM stores knowledge in its layers.

Row 3: ID vectors go stale and must be retrained all the time. A trained LLM stays useful.

Point to the gray box: the clearest case is a new item. It has no clicks, so its ID vector is random noise, but an LLM can read its title and pictures on day one.

Bridge: So, just add LLM vectors? People tried. It helps less than you would hope.

## 8. naive llm

![slide 8](svg/08-naive-llm.svg)

Say: The common practice is to compute one LLM vector per item, store it, and give it to the recommender as an extra input. The paper says this has two problems.

Left, "representation unmatch": the LLM learned from pictures and captions, so it thinks toothpaste and ointment are similar, because both come in a tube. A shopper uses them for completely different things.

Right, "representation unlearning": the stored vector is frozen. The recommender's training cannot change it, so it never adapts to what users actually do.

Point to the quote: this is the paper's goal in its own words. Do not recommend look-alikes; find new things the user will like.

Bridge: The first QARM paper already attacked both problems. Let us see how.

## 9. qarm v1

![slide 9](svg/09-qarm-v1.svg)

Say: QARM, 2024, has two parts.

Left, the fix for "unmatch": take item pairs that Kuaishou's existing systems consider related, for example items that the same users clicked. Fine-tune the LLM so that those pairs get similar vectors. Now the LLM's idea of "similar" is the business's idea.

Right, the fix for "unlearning": turn each LLM vector into a few short codes. The recommender treats the codes like new IDs and learns a vector for each, so this part is trainable.

Point to the yellow line: this is the key result. The same LLM knowledge gave almost nothing as a frozen input (+0.02 AUC) and nine times more as trainable codes (+0.18).

Bridge: A quick look at QARM's results, because V2 is compared with it.

## 10. qarm v1 results

![slide 10](svg/10-qarm-v1-results.svg)

Say: Top left: the frozen vector barely helps; the codes help, and both together help most.

Top right: real online tests. Ad revenue went up almost 10% for new ads and about 3% for the rest. Shopping GMV went up 1.6% and 2.3% in two services.

Point to the bar chart: items are grouped from least bought (L1) to most bought (L6). The least-bought items gained most, +8% GMV. That supports the idea that content knowledge helps items with little click history.

Bridge: So what does V2 change?

## 11. what changes

![slide 11](svg/11-what-changes.svg)

Say: Four changes, one per row.

Row 1: QARM trained on raw item pairs. V2 first lets a reasoning LLM throw out bad pairs, and adds question-answer data about each item.

Row 2: V2 trains the LLM with a special attention mask so it learns two things at once. We will see this in two slides.

Row 3: the codes. V2 drops the "nearest neighbours" codes and replaces the last level of clustering with a fixed grid called FSQ.

Row 4: V2 uses the LLM vector for step 1 (GSU) and the codes for step 2 (ESU).

Bridge: Part II, rows 1 and 2. First, why do the pairs need cleaning?

## 12. noisy pairs

![slide 12](svg/12-noisy-pairs.svg)

Say: The training pairs come from Kuaishou's own retrieval systems, so they inherit their mistakes.

Left: "items clicked by the same users" pairs soy sauce with laundry detergent. Both are just very popular, so many people click both. They are not related. The reasoning LLM says no, and the pair is removed.

Right: the other source pairs fashion boots with a down jacket. They look nothing alike, but people buy them together when winter comes. The LLM says yes, and the pair is kept. This is exactly the kind of relation we want the model to learn.

Bridge: Here is the full data pipeline.

## 13. data pipeline

![slide 13](svg/13-data-pipeline.svg)

Say: Two data streams.

Part A, cleaning pairs. Each pair is shown to a Qwen3 model as titles and attributes only. The question: are these related, by use or because people buy them together? Answer yes or no. The cheap 0.6B model handles the reliable pairs; the bigger 8B model handles the noisy ones.

Point to the orange boxes: over 10% of the reliable pairs and over 70% of the noisy pairs are thrown out.

Part B, question-answer data. A large vision-language model looks at everything about an item, including the pictures, and writes ten questions and answers, for example "What category is this? Spicy food."

Bridge: How are both kinds of data used to train one LLM?

## 14. three segment

![slide 14](svg/14-three-segment.svg)

Say: This is the cleverest idea in the paper. Go slowly.

Point right, top row: the input is split into three parts. First the item itself (title, pictures). Then a few special EMB tokens. Then a question and its answer.

Point left, the grid: blue means "may look at". The item part reads itself. The EMB tokens read the item. The question and answer may read only the EMB tokens, not the item.

Why? To answer the question, the model must get everything it needs through the EMB tokens. So the EMB tokens are forced to become a good summary of the item. The average of the EMB tokens is the item's vector.

Two losses: the vector is pulled close to its partner item from the cleaned pairs (contrastive loss), and the answer must be predicted word by word (the normal LLM loss).

Note: the paper has no experiment comparing this with the usual one-token approach.

Bridge: Part III, the codes. First, why do codes collide?

## 15. collisions

![slide 15](svg/15-collisions.svg)

Say: A semantic ID is useful only if different items get different codes. In QARM, many items shared a code.

Point left: this is a toy picture with real K-means on made-up points. The catalogue is crowded in the middle (popular kinds of items) and thin at the edges (rare items). K-means puts most of its centres where the points are crowded. Point to the dashed circle: most centres sit there. Rare items at the edges share a few centres, so they get the same code.

Point right: FSQ ignores where the points are. It just cuts space into a fixed grid, so the edges keep their own cells.

Point to the yellow line: in QARM's shopping data, more than 30% of codes stood for several items.

Bridge: V2 combines both methods.

## 16. res kmeans fsq

![slide 16](svg/16-res-kmeans-fsq.svg)

Say: Read the top row left to right. Start with the LLM vector of an item.

Level 1: K-means picks the closest of 8,192 centres. That is the first code, roughly the category.

Level 2: subtract that centre and cluster what is left. That is the second code, a finer category or use.

Level 3: on what is left after that, use the FSQ grid instead of K-means. That gives the third code, which separates individual items.

So the first two codes follow the data, and the last code spreads items evenly.

Point to the orange box: the sizes in the paper do not add up. The method section says 8,192 per level; the experiments say 4,096. Mention it, do not dwell on it.

Bridge: How are the vector and the codes used inside the recommender?

## 17. usage

![slide 17](svg/17-usage.svg)

Say: Left, step 1 (GSU): every item's LLM vector is stored. For a candidate, the system keeps the past items whose vectors are most similar to the candidate's. This is plain vector search, no training.

Right, step 2 (ESU): each item is described by its ID plus its three codes. Each code gets its own learnable vector. The model compares the candidate with the selected past items, weighs them, and predicts click, purchase and so on.

The point: the LLM vector stays frozen, but the codes are trained together with the recommender. That is the fix for "unlearning".

Bridge: Part IV, results. First, the only public dataset.

## 18. amazon

![slide 18](svg/18-amazon.svg)

Say: Amazon book reviews, the only public test. QARM V2 scores 70.33 AUC; the best baseline, SIM-soft, scores 69.57.

Point to the axis: careful, it starts at 66, so the differences look bigger than they are. The gap is 0.76 points.

Point to the box: the baselines are old (2018 and 2020). There is no comparison with TWIN or with newer semantic-ID models.

Bridge: Now Kuaishou's own data, where the big claims are.

## 19. offline

![slide 19](svg/19-offline.svg)

Say: Each bar is one prediction task on Kuaishou data: ads, three shopping services, live streaming. The height is the GAUC gain over the current production model.

All twelve bars are positive. Most are between 0.1 and 0.5 points. The biggest is ads, +1.1.

Point to the dashed green line: the authors say about 0.1 points is enough to make money, which is normal in industry.

Caveat: no error bars, so we do not know how stable the small ones are.

Bridge: Offline numbers are one thing. What happened with real users?

## 20. online ads shop

![slide 20](svg/20-online-ads-shop.svg)

Say: These are live A/B tests over several weeks: some users got the new model, the others the old one.

Ads: revenue +4.9%, with ad spend +3.9%, so revenue grew faster than spend.

Shopping: GMV +1% to +5.6%. Shopping#2 gained most on every metric.

For a platform this size, several percent is a lot of money. But there are no confidence intervals or traffic sizes.

Bridge: Live streaming shows where the gains come from.

## 21. online live

![slide 21](svg/21-online-live.svg)

Say: Live streaming, split into new streams (cold-start) and the rest.

Point to the first row: for new streams in Live-streaming#1, clicks went up 3.2%, about five times more than for the other streams. That is the story of the paper: content knowledge helps most when there is no click history yet.

Curiosity: the gift count is exactly +2.917% in both "others" rows. It may be a coincidence or a copy error.

Bridge: Did the cleaned training data really make the LLM vector better? The paper tests that directly.

## 22. alignment hr

![slide 22](svg/22-alignment-hr.svg)

Say: The test: take a user's last 10 clicked items, retrieve 50 similar items for each, and check how often the user really clicked or bought one of them. Higher is better.

Gray is QARM, blue is QARM V2. Every bar goes up by roughly 60 to 77%. For example, click hit rate at 200 goes from 7.8% to 12.5%.

Point to the orange text: one small error. The text says order HR@500 rose from 20.0%, the table says 13.0%.

Bridge: And did the codes stop colliding?

## 23. code conflict

![slide 23](svg/23-code-conflict.svg)

Say: Three rows, read top to bottom.

Row 1, QARM: 78% of items share their code with another item, and a code lookup returns 129 items on average.

Row 2: same clustering method, but on the new V2 vectors. Already only 8.4 items per code. That is 15 times fewer, from better vectors alone.

Row 3: add the FSQ grid on the last level. 2.5 items per code, and 32% of items share a code.

Point to the two boxes: the surprise is that most of the improvement comes from the better vectors, not from the new FSQ trick.

Bridge: One more qualitative check of step 1.

## 24. gsu case

![slide 24](svg/24-gsu-case.svg)

Say: How different is the new step 1 from the old ID-based one? About 60% of the past items it picks are items the old system would not have picked.

Point to the boxes: in the paper's examples, the old system picks unrelated things, like jewellery for a phone-case target. The new one stays in the right category and meaning.

Point to the bottom: a side finding. They do not remove repeated items from the history. In live streaming, the last 100 interactions involve only 23 different streamers on average, and the repeats carry useful signal.

Bridge: Part V. Time to be critical.

## 25. critique

![slide 25](svg/25-critique.svg)

Say: Strong points: it runs in production in three businesses, with weeks of A/B tests. The ideas are reusable anywhere: an LLM as a data filter, the three-part mask, the mixed quantizer. And they measure code collisions directly.

Weak points: they change four things at once and never test them one by one on the final metrics. The public baselines are old. There are no error bars. Several numbers disagree between text and tables. And the filtering LLM sees only titles and attributes, not the pictures.

Bridge: That leads to our discussion questions.

## 26. questions

![slide 26](svg/26-questions.svg)

Say: Five questions. Pick two or three, depending on time.

Good opener: number 2. The code-collision table suggests better vectors did most of the work. So is FSQ needed at all?

Number 1 is a good second question: the filter replaces one bias (popular items) with another (the LLM's opinion). Is that always better?

Ask the room before giving your own view.

## 27. takeaways

![slide 27](svg/27-takeaways.svg)

Say: Four things to remember.

One: LLM knowledge can enter a recommender in two forms, a vector for searching and short trainable codes for ranking.

Two: better training data for the LLM made the codes much cleaner, more than the new quantizer did.

Three: code collisions are easy to measure and worth reporting.

Four: convincing in production, weak on showing which part matters.

Thank you. Questions?


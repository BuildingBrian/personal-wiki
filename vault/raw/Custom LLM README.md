# Building a Custom LLM with nanoGPT — MBA 290T Class 4 (Assignment 3)

**Author:** Brian Arevalo Ramos · **Course:** MBA 290T Fundamentals of Agentic AI, UC Berkeley Haas · **Due:** 2026-09-22

I trained Andrej Karpathy's nanoGPT (2 blocks, 4 heads, 64-number embeddings, 48-token context, whole-word
tokens) twice on my Intel MacBook's CPU: once on the supplied classroom corpus, then again after adding my own
synthetic teaching files for three extension skills. Both runs used the same settings, seed, split rule and
evaluation panels, and the same unchanged 48-case language eval suite before and after training. This README is
the grading entry point: every number below is read from the saved evidence in [`evidence/`](evidence/) by
[`tools/build_readme.py`](tools/build_readme.py), and every claim links to the file that supports it.

## Results at a glance

| Experiment | Stage | Correct / 48 | Scorable / 48 | Accuracy among scorable | Coverage | Full results |
|---|---|---|---|---|---|---|
| Starter corpus | Untrained | 9 | 24 | 37.5% | 50.0% | [csv](evidence/starter/language_evals/untrained/eval_results.csv) · [summary](evidence/starter/language_evals/untrained/eval_summary.json) |
| Starter corpus | Trained (3,000 steps) | 20 | 24 | 83.3% | 50.0% | [csv](evidence/starter/language_evals/final/eval_results.csv) · [summary](evidence/starter/language_evals/final/eval_summary.json) |
| Expanded corpus | Untrained | 12 | 33 | 36.4% | 68.8% | [csv](evidence/expanded/language_evals/untrained/eval_results.csv) · [summary](evidence/expanded/language_evals/untrained/eval_summary.json) |
| Expanded corpus | Trained (3,000 steps) | 30 | 33 | 90.9% | 68.8% | [csv](evidence/expanded/language_evals/final/eval_results.csv) · [summary](evidence/expanded/language_evals/final/eval_summary.json) |

"All-case success" counts unscorable cases as zero: starter trained = 41.7%, expanded trained = 62.5%.
The jump from 20 to 30 correct comes from two different things, separated in [section 4](#4-the-fixed-48-case-language-evals):
new **vocabulary** made 9 more cases scorable, and new **learned patterns** answered 7 of those 9. The one deliberate
hard category, negation, stayed at chance (1/3) — the concrete failure discussed in [section 7](#7-one-limitation-and-my-next-experiment).

## Repository layout

| Path | What it is |
|---|---|
| [`custom_llm_starter.ipynb`](custom_llm_starter.ipynb) | **Executed** notebook, Experiment 1 (starter corpus). Outputs not cleared. |
| [`custom_llm.ipynb`](custom_llm.ipynb) | **Executed** notebook, Experiment 2 (starter + my teaching files). Outputs not cleared. |
| [`corpus/`](corpus/) | My three synthetic teaching files (the only corpus additions). |
| [`tools/make_teaching_data.py`](tools/make_teaching_data.py) | Generates those files deterministically and refuses any eval leakage. |
| [`tools/run_headless.py`](tools/run_headless.py) | Runs the notebook top-to-bottom from the terminal (nbclient) and saves outputs into the .ipynb. |
| [`evals/language_evals.json`](evals/language_evals.json) | The unchanged 48-case suite (sha256 `1d7c503f34d88260…`). |
| [`run_evals.py`](run_evals.py) · [`chat.py`](chat.py) | Instructor's eval runner and terminal chat interface (unchanged). |
| [`tools/chat_demo.py`](tools/chat_demo.py) | Types the six transcript prompts into the real `chat.py` through a pseudo-terminal, so the screenshot session is reproducible. |
| [`evidence/starter/`](evidence/starter/) · [`evidence/expanded/`](evidence/expanded/) | Complete result folders of both runs: config, corpus, manifests, split, tokenization, inspection, history, plots, samples, all four eval result sets, model weights, chat transcripts. ZIPs: [starter.zip](evidence/starter.zip), [expanded.zip](evidence/expanded.zip). |
| [`evidence/rerun_check/`](evidence/rerun_check/) | Evals re-run from the saved `model.pt` with `run_evals.py`, matching the notebook's numbers exactly. |
| [`nanogpt_model.py`](nanogpt_model.py) | Pinned nanoGPT `model.py` (commit `3adf61e`, MIT, [`NANOGPT_LICENSE`](NANOGPT_LICENSE)). |

## 1. My choices and prediction

**Corpus.** Experiment 1 used the supplied classroom sentences only (`CORPUS = "classroom"`, empty `corpus/` folder).
Experiment 2 kept `CORPUS = "classroom"` and added three plain-text files I generated with
[`tools/make_teaching_data.py`](tools/make_teaching_data.py) (written with the help of Claude, an AI assistant, following
the course's starter-prompt workflow). They are synthetic sentences I own and may share; there are no PDFs, no scans,
no third-party text and no personal records, so there were no extraction warnings to resolve
([corpus_manifest.json](evidence/expanded/corpus_manifest.json) shows zero warnings and zero ignored files).

| File | Lines = passages | What it teaches | Eval category targeted |
|---|---|---|---|
| [`corpus/opposites.txt`](corpus/opposites.txt) | 699 | 27 antonym pairs in eight frames ("X is the opposite of Y", "X and Y are opposites", "the road is wide, not narrow"…) | `opposites` |
| [`corpus/categories_and_analogies.txt`](corpus/categories_and_analogies.txt) | 648 | 12 categories × members ("a trout is a fish", "the oak is a kind of tree"), young→adult pairs ("a calf grows into a cow"), and two-sentence analogies | `categories_and_analogies` |
| [`corpus/negation.txt`](corpus/negation.txt) | 620 | Correction stories: "the cup is not white . it is blue . the cup is blue ." and "kai did not choose the milk . he chose the jam . kai chose the jam ." | `negation` |

They added **1,967 new unique passages** (all unique, no duplicates within or across files) and raised the
vocabulary from 133 to 385 word types, still under the notebook's 509-type cap, so nothing became `UNK`.
Why these three: opposites and category membership are pairwise word associations, the same kind of pattern the starter
corpus already teaches (surgeon↔patient), so a 128k-parameter model has a fair chance. Negation was chosen as the
deliberately hard one: it requires copying a word from earlier in the sentence past a distractor, which is a different
skill from association. The leakage rules I followed are in [section 4.4](#44-how-eval-material-stayed-out-of-training).

**Training steps: 3,000** in both runs. One step is one batch of 32 passages, so 3,000 steps ≈ 96,000 passage views, about
23 passes over Experiment 1's 4,132 training passages and 16 passes over Experiment 2's 5,903. The notebook's
10-step smoke test took 16 s end to end on my laptop, so 3,000 was cheap enough to keep identical in both experiments.

**Learning rate: 0.001**, the standard AdamW starting point; the notebook adds a warmup then a cosine decay
(the actual rate at step 0 was 1e-05, see the first update below). Too large a rate makes each update overshoot,
so the loss bounces or diverges (the training loop even aborts on a non-finite loss); too small a rate barely moves the
weights in 3,000 steps and the loss plateaus high. Keeping steps and rate identical means **the corpus is the only
variable between the two experiments.**

**My prediction (written in the notebook before training, section 2, quoted verbatim):**

> Training loss should fall from about 4.9 (an even guess over 136 words) to under 1.0, and validation loss should
> track it closely, because the corpus is built from a handful of templates and the held-out passages share those
> templates. Samples should go from word salad (untrained) to recognisable template fragments (halfway) to near-perfect
> template sentences (final). The inspected word `customer` should end up nearest to `client`, `buyer`, `shopper`,
> `consumer` and `subscriber`, because they fill the same slot in the templates. Language evals in Experiment 1:
> starter-pattern cases should rise from 6/16 to most of the 16, the rephrased transfer prompts should improve less, and
> all 24 extension cases should stay unscorable because their words are not in the vocabulary. In Experiment 2:
> opposites and categories should become scorable and beat chance (above 25%), because they are pairwise word
> associations like the ones the starter already teaches. Negation should become scorable but stay near chance,
> because it requires copying a word from earlier in the sentence past a distractor, which is harder than a pairwise
> association for a 2-layer model trained on a few hundred examples.

**What actually happened, same runs:** every part of that held except one detail. Loss fell to 0.68/0.71 (train/val)
in Experiment 1 and 0.83/0.87 in Experiment 2, with validation tracking training within 0.05. Halfway samples were
already complete template sentences, not fragments — 1,500 steps was more than enough for this corpus. `customer`'s five
nearest neighbours after training were exactly the five predicted words (cosine ≥ 0.96). Starter patterns went 6→16/16,
transfer 3→4/8 (Experiment 1) and 4→7/8 (Experiment 2), extension stayed 0/24 unscorable in Experiment 1, and in
Experiment 2 opposites and categories scored 3/3 each while negation scored 1/3, i.e. chance.

## 2. My runs

| | Experiment 1 · starter | Experiment 2 · expanded |
|---|---|---|
| Run folder | `llm_runs/20260922T043843_283265Z` → [evidence/starter](evidence/starter/) | `llm_runs/20260922T044308_125561Z` → [evidence/expanded](evidence/expanded/) |
| Executed notebook | [custom_llm_starter.ipynb](custom_llm_starter.ipynb) | [custom_llm.ipynb](custom_llm.ipynb) |
| Config / summary / log | [config.json](evidence/starter/config.json) · [training_summary.json](evidence/starter/training_summary.json) · [training.csv](evidence/starter/training.csv) | [config.json](evidence/expanded/config.json) · [training_summary.json](evidence/expanded/training_summary.json) · [training.csv](evidence/expanded/training.csv) |
| Completed steps | 3,000 (not interrupted) | 3,000 (not interrupted) |
| Elapsed training time | 22.2 s | 38.9 s |
| Hardware | Intel Core i7-9750H (6 cores), CPU only, macOS 26.6, Python 3.12.14, PyTorch 2.2.2 | same |
| Parameters | 111,872 | 128,000 (bigger embedding table: 388 × 64 vs 136 × 64) |
| Unique passages (after dedupe + eval reservation) | 4,592 | 6,559 (1,608 duplicates removed) |
| Reserved starter passages withheld (contain a test prefix) | 160 | 160 |
| Train / validation split (90/10 by passage) | 4,132 / 460 | 5,903 / 656 |
| Vocabulary (word types + 3 specials) | 133 + 3 = 136 | 385 + 3 = 388 |
| Unknown-token rate, training / held-out | 0.0% / 0.0% | 0.0% / 0.0% |
| Manifest / vocabulary report | [corpus_manifest.json](evidence/starter/corpus_manifest.json) · [vocabulary_report.json](evidence/starter/vocabulary_report.json) | [corpus_manifest.json](evidence/expanded/corpus_manifest.json) · [vocabulary_report.json](evidence/expanded/vocabulary_report.json) |

The split is by deduplicated passage, not by source file, so a validation passage can share its template (and in
Experiment 2 its teaching file) with training passages. Held-out loss therefore measures "did the model learn the
templates rather than memorise specific sentences", not generalisation to unseen kinds of text. No run was interrupted
or failed; the only earlier run was a 10-step setup test that I deleted before the real experiments.

## 3. Evidence from inside the network

### 3.1 Loss curves

Fixed panels of **20 training and 20 validation documents** (the same 20+20 passages at every measurement, sampled once with fixed seeds),
averaging the cross-entropy over non-padding next-token targets. The notebook records the panels at step 0, halfway and the end,
so each curve has three points. These are small estimates, not full-corpus measurements.

| Step | Exp 1 training loss | Exp 1 validation loss | Exp 2 training loss | Exp 2 validation loss |
|---|---|---|---|---|

| 0 | 4.9263 | 4.9275 | 5.9482 | 5.9767 |
| 1,500 | 0.6821 | 0.7182 | 0.9005 | 0.9198 |
| 3,000 | 0.6783 | 0.7061 | 0.8295 | 0.8747 |

Sources: [history.json](evidence/starter/history.json) · [history.json](evidence/expanded/history.json). The untrained loss is the
natural log of the vocabulary size (ln 136 = 4.91, ln 388 = 5.96): an untrained network spreads probability evenly, so a
bigger vocabulary starts *higher*, which is why the two runs' losses are not directly comparable.

| Experiment 1 (starter) | Experiment 2 (expanded) |
|---|---|
| ![Experiment 1 loss curves](evidence/starter/training_curves.svg) | ![Experiment 2 loss curves](evidence/expanded/training_curves.svg) |

### 3.2 Samples: untrained → halfway → final (same generation settings every time)

Four samples per stage, generated with the same start token, seed and temperature. Full files:
[step_0000](evidence/starter/samples/step_0000.txt) · [step_1500](evidence/starter/samples/step_1500.txt) · [step_3000](evidence/starter/samples/step_3000.txt) (Exp 1) and
[step_0000](evidence/expanded/samples/step_0000.txt) · [step_1500](evidence/expanded/samples/step_1500.txt) · [step_3000](evidence/expanded/samples/step_3000.txt) (Exp 2).

**Experiment 1, untrained (step 0):**
```
mentioned travel system mentioned instructor and client credit yesterday patient purchase brand course offering market bank discussion physician discussed consumer instructor merchandise course instructor in course lesson taste update market health during
ordered doctor investment package website customer juice product teacher journey merchandise in physician on payment product learned care travel compared product fruit return software kitchen price the system another offering educator
traffic lesson today at student software important yesterday fruit we interest a a nurse fruit banana bus physician educator design with offering car surgeon interest interest return service nurse taxi the offering
a a client apple learning <BOS> professor educator market consumer data team question harvest banana yesterday banana mango banana <BOS> treatment another interest with taxi return market buyer . juice car mentioned
```
**Experiment 1, halfway (step 1,500):**
```
a review of taste helped us understand the important orange .
we learned about the different physician during a discussion of treatment .
today the bank focused on return and the important investment .
we learned about the different merchandise during a discussion of quality .
```
**Experiment 1, final (step 3,000):**
```
a review of patient helped us understand the important dentist .
we learned about the different physician during a discussion of treatment .
today the store focused on service and the important client .
we learned about the different merchandise during a discussion of quality .
```
**Experiment 2, untrained / halfway / final:**
```
hill take poor code care jade two health gold understand market milk important older cod something traffic red wall older care package offering another late tree day every brand road juice open
pig surgeon cat mentioned room big checking water thick vehicle coffee lena taste order old travel chick train short become slow learning round quality narrow day far empty teacher juice security ordered
treatment puppy picked pine early here poodle slow means office juice potato pasta compared buy application wool support brown book goat cool banana eli carrot husky discussed goldfish system grey bus narrow
health take type goldfish goldfish <BOS> dentist she box taste bird sour tabby market application they application order application instructor trout an near hammer expensive tuna cod ball grape checking banana code
```
```
the opposite of sweet is jade .
we learned about the important system during a discussion of data .
today the bank focused on return and the important loan .
we saw a goldfish , which is a type of fish .
```
```
the important program was mentioned in the update report yesterday .
the different consumer was mentioned in the purchase report yesterday .
today the market focused on quality and the new package .
a big floor is the opposite of a small floor .
```
Visible change: at step 0 the output is a uniform draw over the vocabulary (notice `hill take poor code care jade` mixes
words from every file), by 1,500 steps every line is a grammatical template sentence, and by 3,000 the Experiment 2 model
also produces my teaching frames ("a big floor is the opposite of a small floor ."). Visible *lack* of change: the halfway and
final samples in Experiment 1 are nearly identical, matching the flat loss between step 1,500 and 3,000.

### 3.3 One word, from text to ID to 64-number vector

Trace from [tokenization.json](evidence/starter/tokenization.json) (Experiment 1). The tokenizer lower-cases the text and splits
it into words and punctuation with a regular expression; the vocabulary is built **from training passages only** and maps each
word type to an integer:

```
Text   : today the school focused on lesson and the local professor .
Tokens : ['today', 'the', 'school', 'focused', 'on', 'lesson', 'and', 'the', 'local', 'professor', '.']
IDs    : [1, 121, 118, 101, 42, 74, 61, 7, 118, 63, 88, 3, 2]
Inputs : [1, 121, 118, 101, 42, 74, 61, 7, 118, 63, 88, 3]
Targets: [121, 118, 101, 42, 74, 61, 7, 118, 63, 88, 3, 2]
```
`<BOS>` is ID 1 and `<EOS>` is ID 2; `the` is 118 both times it appears; `.` is 3. Every training example is the
inputs row predicting the targets row: `<BOS>`→`today`, `today`→`the`, … `.`→`<EOS>`. An ID is just a label — in
Experiment 2 the word `customer` is ID 81 instead of 28, because the larger vocabulary is numbered differently.

The embedding table is a 136 × 64 matrix of weights; row 28 *is* the vector for `customer`. From
[inspection.json](evidence/starter/inspection.json):

| | first 8 of 64 numbers | length (L2 norm) |
|---|---|---|
| Before training (random init) | -0.0576, -0.0048, 0.0426, 0.0193, 0.0156, -0.0288, 0.0256, 0.0001 | 0.175 |
| After 3,000 steps | 0.0366, -0.0182, 0.1330, 0.1060, 0.0630, 0.0189, 0.1523, 0.0929 | 0.673 |

<details><summary>Full 64-number vectors for <code>customer</code> (Experiment 1)</summary>

Before: `[-0.05759, -0.00481, 0.04263, 0.01934, 0.01564, -0.02882, 0.02561, 5e-05, 0.02471, 0.02069, 0.00737, -0.03309, -0.05355, -0.00574, -0.02417, -0.01472, 0.00469, -0.01045, -0.00838, -0.01826, -0.02013, 0.0051, -0.01092, -0.01263, 0.02839, -0.00263, -0.00407, 0.01364, -0.00989, -0.01672, 0.00191, -0.00145, 0.01603, -0.00567, -0.00067, -0.00129, -0.00732, -0.00093, 0.00151, -0.00498, -0.02899, 0.01809, -0.00735, -0.00544, 0.01564, -0.00454, 0.04157, 0.05236, 0.02264, -0.01541, -0.02512, -0.0068, 0.02935, -0.00253, 0.0298, -0.0228, -0.03024, 0.00644, 0.05049, 0.00749, -0.01072, 0.02474, -0.01447, 0.01324]`

After: `[0.03663, -0.01822, 0.13303, 0.10595, 0.06301, 0.01891, 0.1523, 0.09291, -0.06322, -0.01725, 0.0341, -0.04739, -0.06455, -0.08659, -0.14499, -0.03588, -0.15691, -0.15027, -0.00762, -0.07074, -0.09301, 0.00911, -0.06481, 0.01752, 0.00392, -0.06245, 0.11252, -0.06433, 0.05205, -0.15667, -0.07062, 0.06168, -0.03177, 0.1414, 0.09131, 0.05647, 0.01961, -0.13484, 0.12229, -0.03383, 0.11874, 0.00458, -0.13443, 0.05294, -0.0376, -0.10312, 0.02027, 0.03812, -0.01984, -0.15074, 0.03028, -0.12055, 0.01662, 0.07775, 0.11809, 0.05574, 0.09336, 0.00262, 0.03706, 0.07563, 0.11852, 0.01438, 0.09129, -0.07461]`
</details>

Cosine nearest neighbours of `customer` in the full 64-D space (computed from [checkpoint.json](evidence/starter/checkpoint.json),
the same data the embedding viewer loads):

| | Experiment 1 | Experiment 2 |
|---|---|---|
| Before | bus 0.213, educator 0.203, helped 0.202, bank 0.201, risk 0.198 (random) | surgeon 0.439, vehicle 0.309, river 0.290, deposit 0.281, silver 0.271 (random) |
| After | **shopper 0.978, client 0.977, buyer 0.977, subscriber 0.971, consumer 0.970**, then team 0.503 | **subscriber 0.974, buyer 0.973, client 0.971, consumer 0.971, shopper 0.962**, then lecturer 0.570 |

Training pulled the six "store" nouns that share the same template slot into one tight cluster. In Experiment 2 the teaching
words clustered the same way: `salmon` → cod 0.81, goldfish 0.80, robin 0.72; `kitten` → puppy 0.87. `hot` → dirty 0.66, hard 0.63,
warm 0.56: the model grouped *adjectives that appear in the opposites frames*, not hot with cold specifically, which is a
hint about how it solved the opposites evals (frame + association, section 4.3).

### 3.4 One real gradient and weight update

The notebook saves the very first weight it touches: coordinate 0 of `customer`'s embedding row, at step 0
([inspection.json → first_update](evidence/starter/inspection.json)):

| value before | gradient ∂loss/∂w | learning rate at step 0 | value after |
|---|---|---|---|
| -0.057592 | 0.000693 | 1e-05 | -0.057602 |

The gradient is positive, so raising this weight would raise the loss; AdamW moved it the opposite way, by
9.99e-06. That is tiny because the warmup starts the learning rate at 1e-05 (1% of 0.001) and AdamW
normalises the step size. The same thing happened to all 111,872 weights at once, 3,000 times. In Experiment 2 the
first update was -0.032742 → -0.032732 with gradient -0.002369 (negative, so the weight moved up).

### 3.5 Next-token probabilities before and after (prefix `the customer`)

| | Experiment 1 top 5 | Experiment 2 top 5 |
|---|---|---|
| Untrained | `customer` 0.0160, `bus` 0.0107, `educator` 0.0104, `us` 0.0103, `application` 0.0101 | `customer` 0.0050, `ate` 0.0041, `bank` 0.0037, `round` 0.0037, `cat` 0.0037 |
| Trained | `reviewed` 0.1782, `recommended` 0.1712, `ordered` 0.1685, `selected` 0.1634, `compared` 0.1597 | `recommended` 0.1770, `reviewed` 0.1759, `compared` 0.1722, `returned` 0.1692, `selected` 0.1494 |

Untrained, every word gets about 1/136 = 0.0074 (the "top" word is at 0.016 by chance). Trained, the
probability mass moved onto the six verbs that follow `the customer` in the corpus ("the customer *ordered* the product after
checking the price"), each near 1/6, because the corpus uses all six equally. That is the next-word distribution the
sampler draws from.

### 3.6 Attention rows

For the three-token prefix `<BOS> the customer`, the notebook saves one head's attention weights
([inspection.json → attention_rows](evidence/starter/inspection.json)): each row is a position, each column an earlier position.

```
Experiment 1: [[1.0, 0.0, 0.0], [0.606, 0.394, 0.0], [0.485, 0.423, 0.092]]
Experiment 2: [[1.0, 0.0, 0.0], [0.154, 0.846, 0.0], [0.449, 0.28, 0.271]]
```
Row 1 can only look at itself (1.0); row 2 splits its attention between `<BOS>` and `the`; row 3 (`customer`) spreads
over all three. The zeros above the diagonal are the causal mask: a position never sees tokens after it, which is what lets
the model generate left to right.

### 3.7 Temperature (inference only, weights unchanged)

Same trained model, same start token and seed, three temperatures ([temperature_comparison.json](evidence/expanded/temperature_comparison.json), Experiment 2):


**T = 0.3**
```
the important program was mentioned in the data report yesterday .
the different product was mentioned in the price report yesterday .
today the market focused on quality and the new package .
the local software was mentioned in the data report yesterday .
```
**T = 0.8**
```
the important program was mentioned in the update report yesterday .
the different consumer was mentioned in the purchase report yesterday .
today the market focused on quality and the new package .
a big floor is the opposite of a small floor .
```
**T = 1.2**
```
the take poor are opposites .
a gold is a metal . a saw is a tool .
we learned about the different brand during a discussion of quality .
we saw a collie , which is a type of dog .
```

Temperature divides the scores before the softmax. At 0.3 the distribution is sharpened toward the most likely word and the
four samples collapse onto the same starter template; at 1.2 it is flattened and rarer continuations appear, including a
broken one ("the take poor are opposites ."). No weight changed between these samples — only the sampling rule.
Experiment 1's comparison is [here](evidence/starter/temperature_comparison.json); its 0.8 and 1.2 samples are identical, because
a corpus with one sentence shape leaves so little entropy that even a flatter distribution picks the same words.

## 4. The fixed 48-case language evals

**What an eval is here.** Each case is a prompt, four single-word choices and one answer
([evals/language_evals.json](evals/language_evals.json), unchanged, suite sha256 `1d7c503f34d88260d0ac897bc36b8ba621cccc1950aef47e7121e69b2c1c9e1d`).
The runner sends only the prompt to the model, reads the probability it assigns to each of the four choice words at the next
position, and scores 1 if the correct word has the highest probability (ties score 0). A case is **unscorable** when the prompt or
answer contains a word outside the model's vocabulary; unscorable cases count as 0 in "all-case success". Separately, the runner
also samples a free continuation, which is saved but *not* scored. The 16 `starter_patterns` prompts were withheld from the
classroom sentences before splitting or building the vocabulary (160 passages, [eval_separation.json](evidence/expanded/eval_separation.json)).

### 4.1 Scores by group and category

| Group / category | Exp 1 untrained | Exp 1 trained | Exp 2 untrained | Exp 2 trained |
|---|---|---|---|---|

| **starter_patterns** | 6/16 (scorable 16) | 16/16 (scorable 16) | 5/16 (scorable 16) | 16/16 (scorable 16) |
| **starter_transfer** | 3/8 (scorable 8) | 4/8 (scorable 8) | 4/8 (scorable 8) | 7/8 (scorable 8) |
| **extend_corpus** | 0/24 (scorable 0) | 0/24 (scorable 0) | 3/24 (scorable 9) | 7/24 (scorable 9) |
| categories_and_analogies | 0/3 (scorable 0) | 0/3 (scorable 0) | 1/3 (scorable 3) | 3/3 (scorable 3) |
| domain_context | 3/8 (scorable 8) | 8/8 (scorable 8) | 2/8 (scorable 8) | 8/8 (scorable 8) |
| domain_place | 3/8 (scorable 8) | 8/8 (scorable 8) | 3/8 (scorable 8) | 8/8 (scorable 8) |
| everyday_knowledge | 0/3 (scorable 0) | 0/3 (scorable 0) | 0/3 (scorable 0) | 0/3 (scorable 0) |
| grammar | 0/3 (scorable 0) | 0/3 (scorable 0) | 0/3 (scorable 0) | 0/3 (scorable 0) |
| negation | 0/3 (scorable 0) | 0/3 (scorable 0) | 0/3 (scorable 3) | 1/3 (scorable 3) |
| new_wording | 3/8 (scorable 8) | 4/8 (scorable 8) | 4/8 (scorable 8) | 7/8 (scorable 8) |
| opposites | 0/3 (scorable 0) | 0/3 (scorable 0) | 2/3 (scorable 3) | 3/3 (scorable 3) |
| reference | 0/3 (scorable 0) | 0/3 (scorable 0) | 0/3 (scorable 0) | 0/3 (scorable 0) |
| sequence | 0/3 (scorable 0) | 0/3 (scorable 0) | 0/3 (scorable 0) | 0/3 (scorable 0) |
| spatial_relations | 0/3 (scorable 0) | 0/3 (scorable 0) | 0/3 (scorable 0) | 0/3 (scorable 0) |

### 4.2 All 48 cases

✅/❌ = scored (predicted choice shown); – = unscorable (a prompt or choice word is unknown). Last column is the Experiment 2
trained model's *free* continuation, which can differ from its multiple-choice pick. Full per-case data including choice
probabilities and unknown words: [Exp 1 untrained](evidence/starter/language_evals/untrained/eval_results.csv) · [Exp 1 final](evidence/starter/language_evals/final/eval_results.csv) · [Exp 2 untrained](evidence/expanded/language_evals/untrained/eval_results.csv) · [Exp 2 final](evidence/expanded/language_evals/final/eval_results.csv).

| id | category | prompt | answer | E1 untrained | E1 trained | E2 untrained | E2 trained | E2 trained free continuation |
|---|---|---|---|---|---|---|---|---|

| lang_01 | domain_context | the report about the customer explains the | service | ❌ juice | ✅ service | ❌ code | ✅ service | support in detail . |
| lang_02 | domain_context | the report about the merchandise explains the | quality | ❌ lesson | ✅ quality | ✅ quality | ✅ quality | return in detail . |
| lang_03 | domain_context | the report about the mortgage explains the | payment | ❌ harvest | ✅ payment | ✅ payment | ✅ payment | return in detail . |
| lang_04 | domain_context | the report about the mango explains the | juice | ✅ juice | ✅ juice | ❌ code | ✅ juice | taste in detail . |
| lang_05 | domain_context | the report about the bicycle explains the | journey | ✅ journey | ✅ journey | ❌ price | ✅ journey | traffic in detail . |
| lang_06 | domain_context | the report about the application explains the | security | ❌ student | ✅ security | ❌ payment | ✅ security | security in detail . |
| lang_07 | domain_context | the report about the surgeon explains the | patient | ✅ patient | ✅ patient | ❌ fruit | ✅ patient | treatment in detail . |
| lang_08 | domain_context | the report about the tutor explains the | lesson | ❌ journey | ✅ lesson | ❌ journey | ✅ lesson | course in detail . |
| lang_09 | domain_place | the team discussed the customer and the service at the | store | ✅ store | ✅ store | ❌ market | ✅ store | store . |
| lang_10 | domain_place | the team discussed the merchandise and the quality at the | market | ❌ station | ✅ market | ✅ market | ✅ market | market . |
| lang_11 | domain_place | the team discussed the mortgage and the payment at the | bank | ❌ station | ✅ bank | ❌ kitchen | ✅ bank | bank . |
| lang_12 | domain_place | the team discussed the mango and the juice at the | kitchen | ❌ hospital | ✅ kitchen | ✅ kitchen | ✅ kitchen | kitchen . |
| lang_13 | domain_place | the team discussed the bicycle and the journey at the | station | ❌ school | ✅ station | ❌ school | ✅ station | station . |
| lang_14 | domain_place | the team discussed the application and the security at the | office | ❌ store | ✅ office | ❌ market | ✅ office | office . |
| lang_15 | domain_place | the team discussed the surgeon and the patient at the | hospital | ✅ hospital | ✅ hospital | ❌ market | ✅ hospital | hospital . |
| lang_16 | domain_place | the team discussed the tutor and the lesson at the | school | ✅ school | ✅ school | ✅ school | ✅ school | school . |
| lang_17 | new_wording | our hospital discussed the nurse and the | health | ✅ health | ✅ health | ❌ traffic | ✅ health | hospital has a health . |
| lang_18 | new_wording | yesterday the school discussed the educator and the | student | ❌ risk | ❌ harvest | ✅ student | ✅ student | important teacher . |
| lang_19 | new_wording | the bank report discussed the bond and the | return | ❌ taste | ❌ care | ✅ return | ✅ return | return . |
| lang_20 | new_wording | our kitchen report discussed the pear and the | fruit | ✅ fruit | ✅ fruit | ❌ data | ✅ fruit | kitchen . |
| lang_21 | new_wording | the station report compared the bus and the | route | ❌ lesson | ✅ route | ❌ lesson | ✅ route | wall of travel . |
| lang_22 | new_wording | yesterday our office discussed the platform and the | update | ✅ update | ❌ treatment | ✅ update | ❌ journey | different program . |
| lang_23 | new_wording | the store report discussed the subscriber and the | support | ❌ health | ❌ health | ✅ support | ✅ support | service purchase . |
| lang_24 | new_wording | our market report compared the package and the | delivery | ❌ student | ✅ delivery | ❌ juice | ✅ delivery | different merchandise . |
| lang_25 | grammar | one bird | is | – (unscorable) | – (unscorable) | – (unscorable) | – (unscorable) | at the brand after checking the new apple . |
| lang_26 | grammar | the dogs | are | – (unscorable) | – (unscorable) | – (unscorable) | – (unscorable) | mentioned in the opposite of heavy in detail . |
| lang_27 | grammar | yesterday she | walked | – (unscorable) | – (unscorable) | – (unscorable) | – (unscorable) | recommended the important surgeon one day . |
| lang_28 | opposites | the opposite of hot is | cold | – (unscorable) | – (unscorable) | ✅ cold | ✅ cold | cold . |
| lang_29 | opposites | the opposite of empty is | full | – (unscorable) | – (unscorable) | ✅ full | ✅ full | full . |
| lang_30 | opposites | the opposite of noisy is | quiet | – (unscorable) | – (unscorable) | ❌ loud | ✅ quiet | therapist . |
| lang_31 | negation | the box is not red . it is blue . the box is | blue | – (unscorable) | – (unscorable) | ❌ red | ❌ green | not grey . |
| lang_32 | negation | ava did not buy tea . she bought milk . ava bought | milk | – (unscorable) | – (unscorable) | ❌ bread | ❌ tea | milk . |
| lang_33 | negation | the door is not open . it is closed . the door is | closed | – (unscorable) | – (unscorable) | ❌ wide | ✅ closed | closed . |
| lang_34 | reference | maya lent a book to leo . leo thanked | maya | – (unscorable) | – (unscorable) | – (unscorable) | – (unscorable) | detail . |
| lang_35 | reference | ella gave finn a pencil . the person who received the pencil was | finn | – (unscorable) | – (unscorable) | – (unscorable) | – (unscorable) | mentioned in the different educator and the new bus and the  |
| lang_36 | reference | omar called nina . nina answered the call from | omar | – (unscorable) | – (unscorable) | – (unscorable) | – (unscorable) | . |
| lang_37 | sequence | first wash the cup . then dry it . the last action is | dry | – (unscorable) | – (unscorable) | – (unscorable) | – (unscorable) | not soft . |
| lang_38 | sequence | lunch happens after breakfast . the earlier meal is | breakfast | – (unscorable) | – (unscorable) | – (unscorable) | – (unscorable) | a young and return . |
| lang_39 | sequence | the train arrived before the bus . the vehicle that arrived later was the | bus | – (unscorable) | – (unscorable) | – (unscorable) | – (unscorable) | opposite of warm |
| lang_40 | spatial_relations | the book is inside the bag . the bag contains the | book | – (unscorable) | – (unscorable) | – (unscorable) | – (unscorable) | wall is not not grey . |
| lang_41 | spatial_relations | the lamp is above the desk . the desk is | below | – (unscorable) | – (unscorable) | – (unscorable) | – (unscorable) | not buy package . |
| lang_42 | spatial_relations | the ball is left of the box . the box is to the | right | – (unscorable) | – (unscorable) | – (unscorable) | – (unscorable) | store . |
| lang_43 | everyday_knowledge | water freezes into | ice | – (unscorable) | – (unscorable) | – (unscorable) | – (unscorable) | a question about the local package and quality . |
| lang_44 | everyday_knowledge | a person uses an umbrella to stay | dry | – (unscorable) | – (unscorable) | – (unscorable) | – (unscorable) | . |
| lang_45 | everyday_knowledge | to see in a dark room we turn on a | light | – (unscorable) | – (unscorable) | – (unscorable) | – (unscorable) | tree . |
| lang_46 | categories_and_analogies | a robin is a bird . a salmon is a | fish | – (unscorable) | – (unscorable) | ❌ tool | ✅ fish | fish . |
| lang_47 | categories_and_analogies | a puppy grows into a dog . a kitten grows into a | cat | – (unscorable) | – (unscorable) | ✅ cat | ✅ cat | dog . |
| lang_48 | categories_and_analogies | a carrot is a vegetable . an apple is a | fruit | – (unscorable) | – (unscorable) | ❌ vehicle | ✅ fruit | fruit . |

### 4.3 Reading the results honestly

* **Starter patterns (16 reserved prompts): 6/16 → 16/16 in both experiments.** These test the associations the templates
  teach (customer↔service, surgeon↔patient) in a frame whose exact prefixes were withheld from training. Untrained, 6/16 is
  what chance (25%) plus luck looks like; trained, the model gets every one. This is a narrow learned pattern, not language understanding.
* **Transfer (8 new phrasings): 3/8 → 4/8 (Exp 1) and 4/8 → 7/8 (Exp 2).** New sentence shapes built from familiar words.
  Experiment 1 barely beat chance on these; Experiment 2, whose corpus contains more sentence shapes, did much better on the
  *same starter words*. I did not predict this. The one remaining failure, `lang_22` ("yesterday our office discussed the platform
  and the" → expected `update`, predicted `journey`), shows the model has no strong platform↔update association.
* **Extension, coverage: 0/24 → 9/24 scorable.** Experiment 1 could not even attempt the extension cases because words like
  `opposite`, `salmon`, `kitten` or `closed` did not exist in its 136-word vocabulary; more training steps could never fix that.
  My three files made exactly the 9 cases of my three categories scorable and left the other 15 (grammar, reference, sequence,
  spatial, everyday knowledge) unscorable — see the unknown-word lists in the CSV (e.g. `lang_34` is missing `lent`, `leo`, `maya`, `thanked`).
* **Extension, accuracy among the 9 scorable: 3/9 untrained → 7/9 trained.** Opposites 3/3 and categories 3/3. Note the
  untrained Experiment 2 model already "got" `lang_28`, `lang_29`, `lang_47` — with random weights that is a coin flip
  (3/9 ≈ chance), which is exactly why the untrained baseline is measured.
* **Negation 1/3 = chance; this is the failure.** `lang_32` ("ava did not buy tea . she bought milk . ava bought") → the model
  chose **tea**, the negated word, i.e. it copied the first noun instead of the corrected one. `lang_31` chose `green`, a colour
  that never appears in the prompt. Only `lang_33` was right. The free continuations agree it is not a fluke: for `lang_31`
  it generated "not grey ." Given the corpus, the model learned the *shape* "X is not A . it is B . X is" but not which of A or B
  to copy — with only 620 short stories and 2 layers, "attend back to the word after *it is*" did not emerge. Section 7 proposes the fix.
* **Multiple choice ≠ free text.** `lang_30` ("the opposite of noisy is") picks `quiet` correctly among four choices, but its free
  continuation was "therapist ." — a starter word. The score measures the *ranking of four specific words*, not whether the model
  would say the right thing on its own. Both are saved; only the first is scored.
* **Vocabulary vs. learned pattern.** The improvement from 20 to 30 correct decomposes into +9 scorable (vocabulary) and
  7 of those 9 answered correctly (learned pattern); the other +3 came from transfer cases whose words were already present.
* **These are development tests.** They guided my choice of categories and teaching frames, so they cannot be read as a
  measurement of generalisation to unseen tests.

### 4.4 How eval material stayed out of training

1. The suite lives in `evals/`, outside `corpus/`; `CORPUS_FOLDER` pointed only at `corpus/`. The notebook refuses a corpus folder that overlaps the project root or `evals/`.
2. The notebook withheld every classroom sentence containing a reserved test prefix *before* the split and vocabulary build (160 passages, method: `normalized contiguous prompt match; not a semantic leakage detector`).
3. Every imported passage is checked with the same normalized substring test; [`tools/make_teaching_data.py`](tools/make_teaching_data.py) runs that exact function (`run_evals.matching_cases`) on every line it writes and aborts on any hit.
4. Beyond the literal check I avoided **paired reference answers**, following the instructor's surgeon/patient example: the eval frame is never combined with an eval answer. `the opposite of hot is cold` never appears; instead the corpus has `hot is the opposite of cold`, `the opposite of cold is hot`, `the soup is hot , not cold`. `a salmon is a fish` never appears; the corpus has `the salmon is a kind of fish`, `a trout is a fish`. The eval correction pairs red→blue, open→closed and tea→milk never occur, `box` never occurs with red/blue, `door` never with open/closed, and `ava` never buys tea or milk. So the negation evals test transfer of the pattern to new nouns, not recall.
5. Chat transcripts and eval outputs were written only into the run folder, never into `corpus/`. Nothing in this repo retrains on them.
6. Limit of the check: it is an exact contiguous match after normalisation. It cannot detect paraphrases, so rule 4 is a policy I applied by construction, not something the code proves.

One formatting detail worth stating openly: the notebook's chunker splits imported text at every sentence-ending period followed by
a space, which would cut a three-sentence negation story into three unrelated one-sentence passages. To keep each story as **one**
training passage, the generator writes the period attached to the next word (`not white .it is blue`); the tokenizer normalises this
to standard `. ` spacing, visible in [corpus.txt](evidence/expanded/corpus.txt). This affects only passage boundaries, not what text the model sees.

### 4.5 Re-running the evals on the saved model

```bash
.venv/bin/python run_evals.py --model evidence/expanded/model.pt --output results/expanded-final
.venv/bin/python run_evals.py --model evidence/expanded/model_untrained.pt --stage untrained --output results/expanded-untrained
```
I ran the first command and committed its output as [evidence/rerun_check/expanded-final/](evidence/rerun_check/expanded-final/): 30/48, 33 scorable,
identical to the notebook's numbers, with the same model hash (`5593b08e1e84afcc…`) recorded in the summary.

## 5. Chat interface

**Interface:** the instructor's terminal loop [`chat.py`](chat.py) (unchanged) loading my Experiment 2 weights and vocabulary
from `model.pt`. It is a tiny language model: it *continues* a prompt rather than answering it, each prompt starts with a fresh
context (no conversation memory), unknown words are reported and mapped to `<UNK>`, and only the last 48 tokens of a long prompt are used.
Generating replies never updates weights or touches the corpus.

**Launch (from the repo root, after the setup in section 8):**
```bash
.venv/bin/python chat.py --model evidence/expanded/model.pt --transcript my_chat.json
```
Type a prompt, press Enter, type `/quit` to exit; the transcript is saved to the named file.

**Model / run identity:** `llm_runs/20260922T044308_125561Z` (Experiment 2, 3,000 steps), model sha256 `5593b08e1e84afcc7a136b720178e4af76c4e360032c587074677d9d3066a2a3`.

**Transcript** ([chat_transcript_terminal.json](evidence/expanded/chat_transcript_terminal.json), temperature 0.8, max 24 tokens, seeds 2026+turn):

| # | Prompt | Model reply | Unknown words |
|---|---|---|---|

| 1 | the customer | recommended the product after checking the price . | — |
| 2 | the opposite of tall is | short . | — |
| 3 | a trout is a | fish . | — |
| 4 | the cup is not red . it is green . the cup is | green . | — |
| 5 | my laptop crashed yesterday | . | crashed, laptop, my |
| 6 | hello how are you today | our we we they a kai floor is the opposite of yesterday . | hello, how, you |

The notebook's own chat cell (section 10) produced one more turn, saved in [chat_transcript.json](evidence/expanded/chat_transcript.json):
"the customer" → "recommended the product after checking the price .".

**Screenshot** of the session in macOS Terminal, taken by me on 2026-09-22 (the six prompts were typed into the unchanged `chat.py` by [`tools/chat_demo.py`](tools/chat_demo.py); replies are identical to the transcript because each turn's sampling seed is fixed). The bracketed line after *Saved transcript* comes from the small launcher script that opened the window and tried, without permission, to capture it — it is not output of `chat.py`.

![chat.py running in Terminal](evidence/chat_screenshot.png)

**Observed limitations:** turn 5 is the clearest one — every content word in "my laptop crashed yesterday" is outside the
vocabulary, so the model received `<UNK> <UNK> <UNK> yesterday` and produced an empty reply. Turn 6 shows what happens with
partial coverage: three unknown words plus `today` yield a grammatical-looking but meaningless string. Turns 2–4 show the
taught patterns transferring to prompts that are not in the corpus ("tall"→"short", "trout"→"fish", "the cup … green").

## 6. What I learned

1. **Corpus.** My corpus is 6,559 short passages: 4,592 template sentences about eight everyday domains plus my 1,967 teaching
   sentences. It can teach *which words go together in which slots* — that is all it contains. It cannot teach grammar it never shows
   (no `is`/`are` contrast), facts it never states, or long-range reasoning. I held out 10% of passages so I could tell learning the
   templates apart from memorising particular sentences; the flat gap between the two loss curves says the model learned the templates.
2. **Token, ID, vector, embedding.** A token is a piece of text the tokenizer cut out (`customer`). Its ID is an arbitrary integer
   label (28 in one run, 81 in the other). The vector is the row of 64 floating-point numbers stored at that ID in the embedding
   table, and "embedding" is the name for that learned mapping from ID to vector. Before training the row was noise
   (-0.0576, -0.0048, …); after training it sits 0.97 cosine from `shopper` and `client`.
3. **Why it is a neural network, and how it learned.** The model is layers of matrix multiplications with non-linearities between
   them, and all 111,872 numbers in those matrices are adjustable. Loss is the negative log probability the model gave the true
   next word, averaged over a batch. Backpropagation computes, for every weight, how much the loss would change if that weight moved
   (0.000693 for the first weight), and AdamW moves each weight against its gradient by a step scaled by the learning rate.
   3,000 repetitions of that took the loss from 4.93 to 0.68.
4. **Attention.** For each position, attention builds a weighted average of the vectors at *earlier* positions, with weights the
   model learned to compute from the tokens (row 3 above: 0.49 on `<BOS>`, 0.42 on `the`, 0.09 on itself). Four heads do this four ways
   in parallel and two blocks stack it. It cannot look at future tokens because the mask sets those weights to zero — otherwise the
   model could read the answer it is supposed to predict.
5. **Probabilities → text, and temperature.** The last layer produces one score per vocabulary word; softmax turns the scores into
   probabilities (the six verbs at ~0.17 each after `the customer`); the sampler draws one word, appends it, and repeats until `<EOS>`.
   Temperature scales the scores before softmax: 0.3 made the four samples collapse onto one template, 1.2 produced a broken
   sentence. No weights changed during any of that — sampling is inference.
6. **Did the evidence support my prediction?** Yes on every measured point except the halfway samples (already complete sentences)
   and the transfer group, which improved more in Experiment 2 than I expected. What I can honestly conclude: the network learned the
   template structure and the word associations in its data, including my new ones, and it did *not* learn negation from 620 examples.
   I cannot conclude it understands language: the held-out passages share templates with training, the evals are development tests,
   and the chat shows it falls apart on any word it has not seen.

## 7. One limitation and my next experiment

**Observed limitation.** Negation transfer failed (1/3, chance). The model learned the surface shape of the correction stories but,
faced with a new noun, it picked the *negated* word (`tea`) or an unrelated colour (`green`) rather than the corrected one. Copying
the right earlier token requires attention to key on the position after "it is" / "she bought", and 620 stories × 3,000 steps did not
produce that. A second, structural limitation: 15 of 48 evals stayed unscorable because the vocabulary is only what the corpus contains.

**Next experiment (one change).** Keep steps, learning rate and the other files fixed, and change only the negation data: roughly
triple it (≈2,000 stories) and vary the frames so the correct word is not always in the same position (e.g. "the cup is blue , not red .
the cup is", "it is green , not white , so the cup is"). Prediction: negation rises from 1/3 to 2/3 or 3/3 if the copying pattern is
learnable at this size, and stays at chance if the limit is the 2-layer architecture rather than the data. Either outcome is informative;
the second would motivate a further experiment with 4 layers.

## 8. Reproduce and inspect

```bash
git clone https://github.com/BuildingBrian/custom-llm.git && cd custom-llm
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt nbclient nbformat ipykernel
.venv/bin/python -m ipykernel install --user --name custom-llm
# Experiment 1: move the teaching files out of corpus/ first (corpus/README.md is ignored), then:
.venv/bin/python tools/run_headless.py --out custom_llm_starter.ipynb
# Experiment 2: put corpus/*.txt back (or regenerate: .venv/bin/python tools/make_teaching_data.py), then:
.venv/bin/python tools/run_headless.py --out custom_llm.ipynb
```
Or open either notebook in VS Code / Jupyter with the `custom-llm` kernel and Run All. Each run writes a new `llm_runs/<timestamp>/`
folder and ZIP. To inspect embeddings, open [`embedding-viewer.html`](embedding-viewer.html) locally and load
`evidence/expanded/checkpoint.json` (the PCA map compresses 64 dimensions to 2; the neighbour list uses the full space).
Evals and chat: sections 4.5 and 5. This repository was verified signed out before submission.

## 9. Reflection and where I go from here

I was skeptical going in. Even once I understood the mechanics, I expected the "learning" to be memorisation: the network
would store the template sentences and play them back, and any eval it passed would be a sentence it had already seen.
Three results changed my mind. The 16 reserved prompts were withheld from training and the trained model still answered all
16. The 8 rephrasings it had never seen went from 4 to 7 correct once the corpus had more sentence shapes. And it answered
"the opposite of hot is" with *cold* although that sentence never appears anywhere in the corpus; it only ever saw "hot is the
opposite of cold", "the soup is hot , not cold" and "the opposite of cold is hot". It combined a frame learned from other
pairs with an association learned from other sentences. That is learning a relationship, not a lookup table of frequent
next words. I want to be precise about the limit: the relationships are narrow (word associations and template shapes),
negation is a pattern it did not learn, and the chat falls apart on any unknown word. But within its small world the network
generalised, and the failures showed me *what kind* of pattern a model this size can and cannot pick up.

I plan to keep experimenting with this notebook rather than stop at the submission: the negation experiment in section 7
first, then teaching files for the remaining five categories, then a 4-block model to see whether depth changes the negation
result. Beyond text, I want to train models on visual learning next: a small classifier that tells images apart, and later a
small generative model that produces images, using the same loop I now understand (data, loss, gradients, updates, held-out
evaluation). These runs will outgrow a laptop CPU quickly, so I am now considering hardware for training models at home and
would appreciate the professor's recommendations on what makes sense for a student at this stage, or whether cloud GPUs are
the better first step.

**Acknowledgements.** nanoGPT © Andrej Karpathy, MIT licence ([NANOGPT_LICENSE](NANOGPT_LICENSE)). Notebook, eval suite and chat
interface by the course instructor ([pepealonso95/custom-llm](https://github.com/pepealonso95/custom-llm)). I used Claude (Anthropic)
as my AI assistant: to generate the synthetic teaching sentences, write the two helper scripts and this README's
tables from the saved outputs, and explain the notebook to me step by step. All runs, numbers and evidence are from my own machine.

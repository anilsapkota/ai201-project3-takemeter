# TakeMeter — r/dataengineering Post Classifier

A fine-tuned text classifier that categorizes posts from r/dataengineering
into four categories: career, technical, opinion, and showcase.

Video: https://www.loom.com/share/b44c4e9b29904d3eb4cb1b0110dd40c2
---

## Community Choice

I chose r/dataengineering, a Reddit community with 460,000+ members where
data engineers discuss their work, careers, and tools. The community is a
strong fit for a classification task because posts vary significantly in
type and purpose. These distinctions matter to regulars: a technical
question deserves a different response than a career question, and the
community treats them differently.

---

## Label Taxonomy

**career**
Posts about job searching, salary, hiring, referrals, or transitioning
into data engineering.

Examples:
- "4 YOE in Payment Operations Support - Continue .NET or Switch to Azure
  Data Engineering, Current in-hand salary is 50k at Infosys?"
- "How did you weigh a higher paying but toxic offer against a stable,
  lower paying job?"

**technical**
Posts about day-to-day data engineering work — tooling, architecture,
migrations, workflows, or specific technology how-to questions.

Examples:
- "Medallion + Kimball — in what layer does Kimball modeling live in the
  medallion architecture?"
- "bigquery fails to extract schema from google cloud storage — how can
  I do it automatically?"

**opinion**
Posts asking for community perspectives on subjective topics —
certifications, tool comparisons, industry trends, or hot takes.

Examples:
- "Is Kaggle still relevant?"
- "Databricks vs Snowflake vs Azure/GCP/AWS products"

**showcase**
Posts sharing a personal or side project the author built, with or
without technical details.

Examples:
- "Capstone: a leakage-audited clinical length-of-stay pipeline
  (dbt + DuckDB + sklearn)"
- "I built a CLI tool that analyzes BigQuery tables and explains what
  the data means using AI"

---

## Data Collection

**Source:** r/dataengineering via the Arctic Shift public Reddit archive
API (arctic-shift.photon-reddit.com). Posts were collected across
multiple time windows (2021–2026) to ensure variety.

**Labeling process:** Posts were labeled manually using a custom Python
annotation tool (annotate.py) that showed one post at a time and accepted
single-key input (c/t/o/s). Each post was read in full before labeling.

**Label distribution:**

| Label | Count | Percentage |
|---|---|---|
| career | 65 | 32.7% |
| technical | 52 | 26.1% |
| opinion | 47 | 23.6% |
| showcase | 35 | 17.6% |
| **Total** | **199** | **100%** |

**Three difficult-to-label examples:**

1. "AXA or GFT technologies? What to choose?" — Could be career (choosing
   between two job offers) or opinion (comparing two companies). Labeled
   **opinion** because the question is about evaluating companies, not
   about a personal job decision.

2. "new to data engineering - how do you measure agent performance and
   troubleshoot? (sales bot)" — "new to data engineering" sounds like a
   career transition post, but the core question is technical. Labeled
   **technical** because it asks how to do something specific.

3. "Where should 'drop bad rows' live -- in the transform, or in a
   separate data-quality step? (medallion pipeline)" — Has career-sounding
   framing but is clearly asking about pipeline architecture. Labeled
   **technical**.

---

## Fine-Tuning Approach

**Base model:** distilbert-base-uncased (HuggingFace)

**Training setup:**
- 3 epochs
- Learning rate: 2e-5
- Batch size: 16
- Train/val/test split: 70% / 15% / 15% (stratified)
- Framework: HuggingFace Transformers + Trainer API
- Hardware: Google Colab T4 GPU

**Key hyperparameter decision:** Kept the default 3 epochs rather than
increasing to 5, because with only 139 training examples overfitting is
a real risk. More epochs on a small dataset often hurts generalization.

---

## Baseline Description

**Model:** Groq llama-3.3-70b-versatile (zero-shot)

**Prompt approach:** The system prompt included all 4 label definitions
copied from planning.md, one example post per label, and an instruction
to output only the label name. Temperature was set to 0 for deterministic
outputs.

**Collection:** Run on the same 30-example test set as the fine-tuned
model. All 30 responses were parseable.

---

## Evaluation Report

### Overall Accuracy

| Model | Accuracy |
|---|---|
| Zero-shot Groq baseline | 0.700 |
| Fine-tuned DistilBERT | 0.567 |

The baseline outperformed the fine-tuned model by 13.3 percentage points.

### Per-Class Metrics

**Fine-tuned DistilBERT:**

| Label | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| career | 0.53 | 1.00 | 0.69 | 10 |
| technical | 0.62 | 0.62 | 0.62 | 8 |
| opinion | 1.00 | 0.14 | 0.25 | 7 |
| showcase | 0.50 | 0.20 | 0.29 | 5 |
| **accuracy** | | | **0.57** | 30 |

**Zero-shot Groq baseline:**

| Label | Precision | Recall | F1 | Support |
|---|---|---|---|---|
| career | 1.00 | 0.70 | 0.82 | 10 |
| technical | 0.62 | 1.00 | 0.76 | 8 |
| opinion | 0.50 | 0.43 | 0.46 | 7 |
| showcase | 0.75 | 0.60 | 0.67 | 5 |
| **accuracy** | | | **0.70** | 30 |

### Confusion Matrix (Fine-Tuned Model)

| True \ Predicted | career | technical | opinion | showcase |
|---|---|---|---|---|
| career | **10** | 0 | 0 | 0 |
| technical | 3 | **5** | 0 | 0 |
| opinion | 5 | 0 | **1** | 1 |
| showcase | 1 | 3 | 0 | **1** |

### Three Wrong Predictions — Analysis

**Error 1: Opinion predicted as Career**
Post: "AXA or GFT technologies? What to choose?"

This is a very short post with no body text. The model likely latched
onto the word "choose" and the career-like framing of comparing two
options. Without enough context, it defaulted to the majority class
(career). This reveals the model's weakness with short, low-information
posts — there simply isn't enough signal to distinguish opinion from
career.

**Error 2: Technical predicted as Career**
Post: "new to data engineering - how do you measure agent performance
and troubleshoot? (sales bot)"

The phrase "new to data engineering" strongly resembles career transition
posts in the training data. The model picked up on this surface-level
signal and ignored the actual technical question in the body. This is a
labeling boundary problem — the post has career-sounding framing but
technical content, and the model learned the framing rather than the
content.

**Error 3: Showcase predicted as Technical**
Post: "benchmarked Pandas, DuckDB, and Polars on 20M rows across 10
operations..."

This post is packed with technical vocabulary — specific tools, row
counts, operation counts. The model correctly identified the technical
language but missed the key distinction: the author is sharing something
they built, not asking how to do something. Showcase and technical share
nearly identical vocabulary, making this the hardest boundary in the
taxonomy.

### Sample Classifications

| Post (truncated) | Predicted Label | Confidence |
|---|---|---|
| "4 YOE in Payment Operations - switch to Azure DE?" | career | 0.91 |
| "Medallion + Kimball — which layer does it live in?" | technical | 0.84 |
| "Is Kaggle still relevant?" | opinion | 0.61 |
| "I built a CLI tool that analyzes BigQuery tables" | showcase | 0.55 |
| "bigquery fails to extract schema from GCS" | technical | 0.78 |

The career prediction is reasonable — the post explicitly mentions years
of experience and a salary figure, which are strong career signals the
model learned reliably.

---

## Reflection: What the Model Learned vs. What I Intended

I intended the model to learn the *purpose* of each post — why someone
wrote it. Instead, it learned *surface vocabulary*. Career posts mention
salaries, YOE, and company names — and the model learned those signals
well (10/10 correct). But opinion and showcase posts share vocabulary
with career and technical posts respectively, so the model defaulted to
the majority class when confused.

The most telling evidence: opinion had recall of 0.14 — the model almost
never predicted it, even though 7 test examples were opinion. It learned
that when a post looks ambiguous, "career" is a safe bet. This is class
imbalance at work: 45 career training examples vs 25 showcase examples
trained the model to be conservative about minority classes.

What would fix this: more balanced training data (at least 60 examples
per class), and possibly longer posts in the training set — short posts
like "AXA or GFT technologies?" don't give the model enough signal to
learn the distinction.

---

## Spec Reflection

**One way the spec helped:** The spec's insistence on writing planning.md
before annotating forced me to define decision rules for edge cases
before seeing 200 examples. This made annotation faster and more
consistent — I never had to stop and wonder "what label is this?"

**One way implementation diverged:** The spec assumes fine-tuning will
outperform the baseline. In my case the baseline (Groq 0.700) beat the
fine-tuned model (0.567). This happened because 199 examples is a small
dataset for DistilBERT to beat a 70B parameter zero-shot model. Rather
than hide this, I treated it as the most interesting finding — it shows
that fine-tuning only helps when you have enough labeled data.

---

## AI Usage

**Instance 1: Label stress-testing**
I gave Claude my label definitions and asked it to generate boundary
posts between technical/opinion and career/opinion. It produced examples
like "Is the SnowPro certification worth it?" which revealed the
career/opinion boundary problem. This led directly to the decision rule:
certifications always → opinion. I kept this rule throughout annotation.

**Instance 2: Failure pattern analysis**
After fine-tuning, I pasted my wrong predictions into Claude and asked
it to identify common patterns. It identified two patterns: short
low-information posts defaulting to career, and showcase posts being
misclassified as technical due to shared vocabulary. I verified both
patterns by re-reading the examples myself and confirmed they were
accurate — they appear in the evaluation report above.
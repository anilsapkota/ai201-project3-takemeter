# TakeMeter — Planning Document
## r/dataengineering Post Classifier

---

## Community

I chose r/dataengineering, a Reddit forum with 460,000+ members where 
data engineers discuss their work, careers, and tools. The community is 
a strong fit for a classification task because posts vary significantly 
in type and purpose — some are deep technical questions, others are 
career advice requests, others are community debates about tools, and 
others are people sharing projects they built. These distinctions matter 
to regulars: a technical question deserves a different kind of response 
than a career question, and the community treats them differently.

---

## Label Taxonomy

**career**
Posts about job searching, referrals, salary negotiation, hiring, 
recruiter guidance, or transitioning into data engineering. Strictly 
about the job market and career moves.

Examples:
- "4 YOE in Payment Operations Support - Continue .NET or Switch to 
  Azure Data Engineering, Current in-hand salary is 50k at Infosys?"
- "How did you weigh a higher paying but toxic offer against a stable, 
  lower paying job?"

**technical**
Posts about day-to-day data engineering work — tooling, architecture, 
migrations, workflows, or specific technology how-to questions.

Examples:
- "Medallion + Kimball — in what layer does Kimball modeling live in 
  the medallion architecture?"
- "bigquery fails to extract schema from google cloud storage — how can 
  I do it automatically?"

**opinion**
Posts asking for community perspectives on subjective topics — 
certifications, tool comparisons, industry trends, or hot takes. 
Includes career-adjacent topics where the question is about 
quality/value rather than job searching.

Examples:
- "Is Kaggle still relevant?"
- "Databricks vs Snowflake vs Azure/GCP/AWS products"

**showcase**
Posts sharing a personal or side project the author built, with or 
without technical details. The primary purpose is showing something 
they made, not asking a question.

Examples:
- "Capstone: a leakage-audited clinical length-of-stay pipeline 
  (dbt + DuckDB + sklearn)"
- "worldcup 2026 with AI feature"

---

## Hard Edge Cases

**Edge Case 1: Technical vs Opinion**
"Moving away from Databricks" could be asking *how* to migrate 
(technical) or *whether* it's a good idea (opinion).

Decision rule: If the post asks *how* to do something → technical. 
If it asks *whether* something is a good idea or *which* tool is 
better → opinion.

**Edge Case 2: Career vs Opinion**
"Is the SnowPro certification worth it?" could be career 
(will this help me get a job?) or opinion (is this certification 
actually good?).

Decision rule: Certifications, tool recommendations always → opinion, 
even if career motivation is implied. Career is reserved strictly for 
job search, hiring, salary, and transitions.

**Edge Case 3: Technical vs Showcase**
"I built an architecture to stop dbt bill shock at the PR level. 
Would love feedback." — is this sharing a project (showcase) or 
asking a technical question?

Decision rule: If the primary purpose is showing something built → 
showcase. If the post is asking for help solving a specific technical 
problem → technical, even if they mention their project.

---

## Data Collection Plan

**Source:** r/dataengineering via the Arctic Shift public Reddit 
archive API (arctic-shift.photon-reddit.com), which provides 
read-only access to Reddit posts without authentication.

**Target:** At least 200 labeled examples, aiming for ~55 per label 
(career, technical, opinion, showcase) to stay under 70% for any 
single class.

**If a label is underrepresented after 200 examples:** Collect 
additional posts specifically matching that label's characteristics 
until balance is restored. showcase posts may be harder to find — 
will search for posts with "Personal Project Showcase" flair 
specifically if needed.

**Split:** The Colab notebook handles train/validation/test split 
automatically (70% / 15% / 15%).

---

## Evaluation Metrics

**Overall accuracy:** Fraction of test examples correctly classified. 
Reported for both fine-tuned model and zero-shot baseline.

**Per-class F1 score:** Harmonic mean of precision and recall for each 
label. This matters because accuracy alone hides cases where the model 
ignores a minority class entirely. A model with 70% accuracy but 0% F1 
on showcase is not useful.

**Confusion matrix:** Shows which label pairs the model confuses most. 
More informative than aggregate metrics — a model that confuses 
technical with opinion is different from one that confuses career 
with opinion.

These metrics together tell me: does the model work on all 4 classes 
(F1), how often is it right overall (accuracy), and where specifically 
does it fail (confusion matrix)?

---

## Definition of Success

A classifier is genuinely useful for this community if:
- Overall accuracy ≥ 70% on the test set
- No single class has F1 below 0.50 (the model must learn all 4 
  distinctions, not just the easy ones)
- Fine-tuned model meaningfully outperforms the zero-shot baseline 
  (at least +10 percentage points accuracy)

Below 60% accuracy would indicate the model is not learning the 
distinctions reliably. Above 90% on this subjective task would be 
suspicious and worth investigating for data leakage.

---

## AI Tool Plan

**Label stress-testing:** Used Claude to generate boundary posts 
between technical/opinion and career/opinion during label design 
(Milestone 1). This revealed the certification edge case and led to 
the decision rule: certifications always → opinion.

**Annotation assistance:** Will not use LLM pre-labeling. Annotating 
manually to stay close to the data and catch edge cases myself.

**Failure analysis:** After fine-tuning, will paste misclassified 
examples into Claude and ask it to identify patterns — e.g. "do these 
wrong predictions share a common trait like short length or ambiguous 
framing?" Will verify patterns by re-reading examples myself before 
including in report.
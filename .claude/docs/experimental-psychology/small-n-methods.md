<!-- last_verified: 2026-03-06 -->
# Research Methods for Small Communities (N < 200)

## The Small-N Problem

Most quantitative social science assumes large samples. With ~100 community members (of whom maybe 30-50 are active), traditional between-subjects A/B testing is usually underpowered. This doesn't mean measurement is impossible — it means choosing the right methods.

## Interrupted Time Series (ITS)

The strongest quasi-experimental design for feature evaluation with small communities.

**How it works:**
- Collect repeated measurements of the same metric over time
- Introduce the feature at a known point
- Compare the post-introduction trend to the pre-introduction trend
- Even with 30 active users, you can have 30+ time-point observations

**Requirements:**
- At least 8-10 data points before the intervention (weekly metrics = 2-3 months baseline)
- A clear intervention point (feature launch date)
- The metric must be measurable at regular intervals

**Example:**
- Metric: weekly active posters per public channel
- Baseline: 10 weeks before private channels launch
- Post-intervention: 10 weeks after
- Analysis: did the trend change? Level shift? Slope change?

**Strengths:** Controls for pre-existing trends, works with small communities
**Weaknesses:** Can't control for coincident events (holiday, external news)

## Within-Subjects Design

Instead of comparing different people (A/B test), compare the same people before and after.

**Applications:**
- Survey the same members before and after a feature change
- Track individual behavior changes (did the same people post more/less?)
- Paired analysis dramatically increases statistical power

**Example:**
- Before: each member's average weekly posts in public channels
- After: same metric, same members, 4 weeks later
- Analysis: paired t-test or Wilcoxon signed-rank (non-parametric for small N)

**Required N:** As few as 15-20 paired observations can detect medium effects

## Bayesian Approaches

Bayesian statistics handle small N more gracefully than frequentist methods because:
- They quantify uncertainty directly ("75% chance the effect is positive")
- They don't require arbitrary significance thresholds
- They can incorporate prior knowledge (e.g., "similar communities saw X")

**Practical use:**
- Even without formal Bayesian analysis, think in terms of "updating beliefs based on evidence"
- "We thought private channels might reduce public activity. After 4 weeks, public activity is unchanged. This is evidence against our concern, though not conclusive."

## Qualitative Methods

For small communities, qualitative data is often more informative than quantitative:

**Structured interviews (N = 5-10):**
- Select members representing different usage patterns
- Ask about experience with the feature
- 30-minute semi-structured conversations
- Look for themes, not statistics

**Open-ended survey questions:**
- "How has [feature] affected your experience?"
- Code responses into themes
- Report theme prevalence ("6 of 12 respondents mentioned...")

**Behavioral observation:**
- Read threads and note behavioral changes
- Document specific incidents (positive and negative)
- This is legitimate qualitative research, not "anecdotes"

## Natural Experiments

Feature rollouts, bugs, and external events create natural experiments:

**Examples:**
- A bug that disabled notifications for a week → measure posting without notifications
- Seasonal variation → compare summer vs. winter activity
- A controversial local event → observe community response patterns
- A new member surge from a batch invitation → measure integration dynamics

**How to use them:**
- Document the event and its timing
- Compare metrics before, during, and after
- Acknowledge limitations (no random assignment, confounds)

## Power Analysis Rules of Thumb

For a ~100-member community with ~40 active users:

| Effect size | Needed N (paired) | Needed N (between) | Detectable? |
|-------------|-------------------|---------------------|-------------|
| Large (d=0.8) | ~15 | ~25 per group | Yes |
| Medium (d=0.5) | ~35 | ~65 per group | Marginal |
| Small (d=0.2) | ~200 | ~400 per group | No |

**Translation:** You can detect large effects (obvious changes in behavior) but not small ones. Design features with big expected impacts, or use time-series methods that accumulate more observations.

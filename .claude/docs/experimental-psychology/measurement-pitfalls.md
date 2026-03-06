# Measurement Pitfalls

## Goodhart's Law
"When a measure becomes a target, it ceases to be a good measure." (Strathern, 1997)

**Community examples:**
- Target "increase posts per week" → members post low-effort content
- Target "reduce response time" → members post quick, unhelpful replies
- Target "increase DAU" → notification spam that drives engagement but annoys members

**Mitigation:** Measure to learn, not to optimize. Track metrics as health indicators, not KPIs.

## The McNamara Fallacy
Named after Robert McNamara's use of body counts as the primary metric for Vietnam War progress. The fallacy:
1. Measure what is easily measurable
2. Disregard what can't be measured
3. Presume what can't be measured isn't important
4. Presume what can't be measured doesn't exist

**Community examples:**
- Post counts are easy to measure → becomes the "health" metric
- Sense of belonging is hard to measure → gets ignored
- A community can have high post counts and be deeply unhealthy

**Mitigation:** Explicitly list what you're NOT measuring and why. Use qualitative methods for the unmeasurable.

## Survivorship Bias
You only hear from people who are still in the community. The ones who left — potentially because of the problem you're studying — are invisible.

**Community examples:**
- Survey shows 90% satisfaction → but 20 members quietly left last quarter
- "No complaints about the new feature" → complainers unsubscribed
- Active members love the community → the experience of lurkers is unknown

**Mitigation:** Track departures (unsubscribes, account deletions). Try to collect exit feedback (one question: "What led you to leave?"). Compare active vs. inactive member profiles.

## Confounding Variables

A confound is something that changes at the same time as your feature and could explain the observed effect.

**Common confounds in community measurement:**
| Change observed | Possible confound |
|-----------------|-------------------|
| Activity dropped after feature X | It's summer / holidays |
| Activity increased after feature Y | A batch of new members joined |
| Satisfaction increased | A problematic member left |
| Channel engagement varies | Different channels have different topics, not feature effects |
| Response times improved | A particularly active member joined |

**Mitigation:**
- Record all known events alongside your metrics
- Use control metrics (if you changed Channel A, compare to Channel B)
- Use time-series methods that account for trends
- Be honest about what you can and can't attribute to the feature

## Hawthorne Effect
People change their behavior when they know they're being observed. Announcing "we're measuring community engagement" will temporarily increase engagement.

**Mitigation:** Measure behavior passively (database queries) rather than announcing measurement. For surveys, measure attitudes (not behavior) since the survey itself doesn't change attitudes as easily.

## Novelty Effect
New features get used because they're new, not because they're good. Usage typically spikes at launch, then drops to a steady state that may be much lower.

**Mitigation:** Never evaluate a feature in its first 2 weeks. Wait at least 4-6 weeks for the novelty to wear off, then measure.

## Regression to the Mean
If you intervene when a metric is at an extreme (e.g., "activity is unusually low this week, let's try X"), any subsequent change may just be the metric returning to its average, not the effect of your intervention.

**Mitigation:** Don't panic-react to single data points. Look at trends (4+ weeks). Only intervene based on sustained patterns.

## Ecological Validity
What people do in a survey ≠ what they do in practice.

- "Would you use private channels?" (survey) → 80% say yes
- Actual usage after launch → 25% use them

**Mitigation:** Weight behavioral data over survey data. Ask "have you done X?" not "would you do X?" Treat survey preferences as hypotheses to test, not conclusions.

## The Observer Effect in Small Communities
In a 100-person community, the analyst is likely also a member. Your own behavior and biases affect:
- Which metrics you choose (you notice what matters to you)
- How you interpret results (confirmation bias)
- How you frame findings to the community

**Mitigation:** Pre-register your hypotheses before looking at data. Write down "I expect X" before you measure. If the data surprises you, that's the interesting finding.

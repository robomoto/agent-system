<!-- last_verified: 2026-03-06 -->
# Survey Design for Small Communities

## Core Principles

### Keep It Short
Response rates in small communities are typically 20-40%. Every additional question loses respondents. For a ~100-member community:
- Target: 5-10 questions maximum
- Expected responses: 20-40
- Time to complete: under 3 minutes

### Avoid Leading Questions
| Bad | Good |
|-----|------|
| "Don't you think private channels would be useful?" | "How useful would private channels be to you?" |
| "Are you satisfied with the community?" | "How would you rate your experience?" |
| "Would you like more features?" | "Which of these features would you use?" |

### Use Appropriate Scales

**For opinions:** 5-point Likert (Strongly Disagree → Strongly Agree)
- Don't use 7-point or 10-point with small N — you won't have enough responses per scale point
- Always include a midpoint ("Neither agree nor disagree") — forcing a direction introduces bias

**For frequency:** Named anchors, not numbers
- "Never / Rarely / Sometimes / Often / Very often"
- Not "1-5" (ambiguous)

**For ranking:** Max 5 items to rank
- More than 5 creates cognitive overload
- Consider "pick your top 3" instead of full ranking

## Response Bias in Small Communities

### Social Desirability Bias
Members will over-report positive feelings and under-report negative ones — especially when they know the survey creator.
- **Mitigation:** Anonymous surveys (genuinely anonymous, not "your responses are confidential")
- **Mitigation:** Frame negatives as normal: "Some members feel X, others feel Y. Which is closer to your experience?"

### Acquiescence Bias
People tend to agree with statements. In a 5-question survey where all items are positive ("I feel welcome", "I trust members", etc.), scores will be inflated.
- **Mitigation:** Mix positively and negatively worded items
- "I sometimes hesitate to share my opinions here" (reverse-scored)

### Non-Response Bias
The 60-80% who don't respond are likely different from those who do. Active, engaged members are more likely to fill out surveys.
- **Mitigation:** Can't fully fix this. Acknowledge it in interpretation.
- **Mitigation:** Compare respondent demographics to community demographics if possible
- **Mitigation:** Follow up once (gentle reminder), but don't nag

## Survey Templates

### Feature Evaluation (Before Launch)
Use when deciding whether to build a feature:

1. "How often do you [activity the feature addresses]?" (frequency scale)
2. "How do you currently [handle the problem]?" (open-ended)
3. "Here's a brief description of [feature]. How useful would this be to you?" (5-point: Not at all → Extremely)
4. "What concerns, if any, would you have about [feature]?" (open-ended)
5. "Would you prefer [Option A] or [Option B]?" (forced choice + "no preference")

### Feature Evaluation (After Launch)
Use 4-6 weeks after a feature ships:

1. "Have you used [feature]?" (Yes/No)
2. [If yes] "How useful has [feature] been?" (5-point)
3. [If no] "Why haven't you used it?" (multiple choice + other)
4. "Has [feature] changed how you use Green Lake Circle?" (open-ended)
5. "Any suggestions for improving [feature]?" (open-ended)

### Quarterly Health Check
5 Likert items (see community-metrics.md) plus:
6. "What's one thing that would make Green Lake Circle more useful to you?" (open-ended)

## Analysis for Small Samples

With 20-40 responses:
- **Don't** calculate means to two decimal places (false precision)
- **Do** report distributions: "12 agreed, 5 were neutral, 3 disagreed"
- **Do** read every open-ended response (you have few enough to do this)
- **Do** look for themes in open-ended responses, report as "N of M respondents mentioned..."
- **Don't** run complex statistical tests — describe the data, show distributions
- **Do** compare to previous surveys if available (trends matter more than snapshots)

## Ethical Considerations

- **Informed consent:** Tell members what you're measuring and why
- **Anonymity:** Use a survey tool that genuinely doesn't collect identifying info
- **Opt-in:** Never make surveys mandatory or gate features behind them
- **Share results:** If you ask the community for input, share what you learned (builds trust and future response rates)
- **Don't over-survey:** Quarterly is the maximum frequency. More often causes survey fatigue.

<!-- last_verified: 2026-03-06 -->
# Community Health Metrics

## The Measurement Problem

"Community health" is not a single number. It's a multidimensional construct that includes engagement, satisfaction, cohesion, and sustainability. Optimizing for one dimension can harm others.

**Goodhart's Law:** "When a measure becomes a target, it ceases to be a good measure." If you optimize for post count, you get low-quality posts. If you optimize for DAU, you get engagement hacking.

## Engagement Metrics (Behavioral)

These come from database queries — no surveys needed.

### Activity Metrics
| Metric | Query | What it measures | Pitfall |
|--------|-------|-----------------|---------|
| Weekly active posters | Distinct authors with posts in last 7 days | Core engagement | Doesn't distinguish quality |
| Lurker ratio | (Members - active posters) / members | Participation breadth | Some lurking is healthy |
| Reply ratio | Posts that are replies / total posts | Conversational depth | High ratio may mean few new topics |
| Cross-channel participation | Users posting in 2+ channels / active users | Community breadth | May penalize focused contributors |
| New member first post time | Days from approval to first post | Onboarding friction | External factors affect this |
| Retention (30-day) | Users who posted in month N and month N+1 | Stickiness | Small N makes this noisy |

### Interaction Quality Metrics
| Metric | Query | What it measures | Pitfall |
|--------|-------|-----------------|---------|
| Thread depth | Average replies per thread | Discussion quality | Can be inflated by arguments |
| Response time | Median time to first reply | Responsiveness | Fast ≠ good |
| Thread diversity | Unique authors per thread | Inclusive discussion | Not all threads need many voices |
| Reciprocity index | % of members who both initiate and reply | Balanced participation | Some roles are naturally asymmetric |

## Satisfaction Metrics (Survey-based)

These require periodic surveys (quarterly is sufficient for small communities).

### Community Satisfaction Scale (adapted from Blanchard & Markus, 2004)
5-point Likert scale (Strongly Disagree → Strongly Agree):
1. "I feel like a member of this community"
2. "I can get help from this community when I need it"
3. "This community is important to me"
4. "I trust the people in this community"
5. "I feel comfortable sharing my opinions here"

**Administration:**
- Quarterly, via email link
- Anonymous (critical for honest responses in small communities)
- 5 items = low burden = higher response rate
- Track trends over time, not absolute scores

### Net Promoter Score (simplified)
Single question: "How likely are you to recommend Green Lake Circle to a neighbor? (0-10)"
- 9-10: Promoters
- 7-8: Passives
- 0-6: Detractors
- NPS = % Promoters - % Detractors

**Useful because:** Single question, easy to track over time, benchmarkable.
**Limitation:** Doesn't tell you WHY people feel the way they do.

## Anti-Metrics (What NOT to Optimize)

| Anti-metric | Why it's dangerous |
|-------------|-------------------|
| Daily Active Users | Drives engagement addiction, not community health |
| Time on site | More time ≠ better experience (could mean frustration) |
| Post volume | Quantity ≠ quality; can be gamed trivially |
| Notification click rate | Optimizing this leads to notification spam |
| Growth rate | Small communities don't need growth; they need depth |

## Dashboard Design

A minimal community health dashboard for a ~100-member community:

**Weekly pulse (automated, database query):**
- Active posters this week vs. trailing 4-week average
- New threads started
- Channels with zero activity (may need attention or archiving)

**Monthly review (automated + manual):**
- 30-day retention rate
- New members joined and their first-post rate
- Any threads with unusual depth (might be conflict or great discussion)

**Quarterly check-in (survey):**
- 5-item satisfaction scale
- One open-ended question: "What would make Green Lake Circle more useful to you?"
- NPS

## Baselines and Benchmarks

Before measuring the impact of any change, establish baselines:
1. Run for at least 4 weeks with no changes
2. Record all metrics weekly
3. Note any external events that affect behavior
4. This is your comparison point for future changes

Without a baseline, you cannot attribute any change to a feature — you're just observing, not measuring.

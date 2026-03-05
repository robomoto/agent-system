# Skill: Cost Analysis

Framework for tracking AI token costs and projecting cloud service expenses. Used by the cost-accountant agent and the lead when budgeting work.

## When to Use

- Before starting a multi-agent task (estimate token budget)
- After completing a task (audit actual vs. projected cost)
- When evaluating cloud services for a project
- When the lead needs to decide model routing for a task

## AI Token Cost Estimation

### Per-Agent Estimates

Estimate tokens by task type, not just model:

| Task Type | Typical Tokens | Breakdown |
|-----------|---------------|-----------|
| Discovery (researcher) | 10K-30K | System prompt ~300, reads ~8K-25K, output ~500 |
| Architecture (architect) | 15K-40K | System prompt ~400, reads ~10K-30K, reasoning ~3K, output ~800 |
| Implementation (implementer) | 20K-80K | System prompt ~350, reads ~10K-40K, writes ~5K-25K, output ~600 |
| Review (reviewer) | 15K-50K | System prompt ~400, reads ~10K-40K, output ~800 |
| Validation (validator) | 10K-30K | System prompt ~300, test runs ~5K-20K, output ~500 |
| Orchestration (lead) | 5K-20K per cycle | Handoff reports ~2K-10K, reasoning ~2K-5K, delegation ~500 |

### Cost Calculation

```
Cost = (input_tokens / 1M * input_price) + (output_tokens / 1M * output_price)
```

| Model | Input/1M | Output/1M |
|-------|----------|-----------|
| Haiku 4.5 | $0.80 | $4.00 |
| Sonnet 4.6 | $3.00 | $15.00 |
| Opus 4.6 | $15.00 | $75.00 |

### Task Cost Templates

**Simple bug fix** (researcher + implementer + reviewer + validator):
- Researcher (Haiku): ~15K tokens → ~$0.01
- Implementer (Sonnet): ~30K tokens → ~$0.10
- Reviewer (Sonnet): ~25K tokens → ~$0.08
- Validator (Sonnet): ~15K tokens → ~$0.05
- Lead (Opus): ~10K tokens → ~$0.15
- **Total: ~$0.39**

**New feature** (researcher + architect + implementer + reviewer + validator):
- Researcher (Haiku): ~25K tokens → ~$0.02
- Architect (Opus): ~30K tokens → ~$0.45
- Implementer (Sonnet): ~60K tokens → ~$0.20
- Reviewer (Sonnet): ~40K tokens → ~$0.13
- Validator (Sonnet): ~20K tokens → ~$0.07
- Lead (Opus): ~15K tokens → ~$0.23
- **Total: ~$1.10**

**Complex refactor** (researcher + architect + 2x implementer + reviewer + validator):
- Multiply implementation and review phases
- **Estimate: $2-5 depending on scope**

## Cloud Service Cost Projection

### Required Information

For every service, document:

| Field | Description |
|-------|-------------|
| Service | Name and provider (e.g., "Fly.io Machines") |
| Purpose | What it does in the project |
| Tier/Plan | Specific plan selected |
| Pricing model | Per-unit, flat monthly, tiered, pay-as-you-go |
| Free tier | What's included free (if anything) |
| Projected usage | Expected monthly volume |
| Projected cost | Monthly dollar amount |
| Confidence | high (verified pricing) / medium (estimated usage) / low (uncertain pricing or usage) |
| Source | URL to pricing page |
| Risk | Cost surprises (traffic spikes, per-request pricing, hidden fees) |

### Cost Comparison Format

When evaluating alternatives:

```
## Hosting: Fly.io vs Railway vs Render

| Factor | Fly.io | Railway | Render |
|--------|--------|---------|--------|
| Base cost | $1.94/mo (shared) | $5/mo (starter) | $7/mo (starter) |
| Free tier | 3 shared VMs | $5 credit/mo | 750 hrs/mo |
| Scaling | Per-VM, manual | Auto, per-usage | Auto, per-usage |
| Database | Fly Postgres (free 1GB) | Built-in ($5/mo) | PostgreSQL ($7/mo) |
| Region support | 30+ regions | Limited | Limited |
| Risk | Manual scaling | Usage-based surprises | Usage-based surprises |

Recommendation: Fly.io for cost-sensitive projects with predictable traffic.
Rationale: Lowest base cost, generous free tier, manual scaling prevents bill surprises.
```

### Budget Summary Format

```
## Monthly Infrastructure Budget

| Service | Purpose | Cost | Confidence |
|---------|---------|------|------------|
| Fly.io | Hosting (2 VMs) | $3.88 | high |
| Fly Postgres | Database | $0.00 | high (free tier) |
| Cloudflare | DNS + CDN | $0.00 | high (free plan) |
| Resend | Email | $0.00 | medium (near free limit) |
| R2 | Media storage | $0.00 | high (free tier) |
| **Total** | | **$3.88/mo** | |
| **Annual** | | **$46.56/yr** | |

### Risks
- Resend free tier (3k emails/mo) is tight at ~100 users. Budget $20/mo for Pro if growth continues.
- R2 free tier is 10GB. Media-heavy usage could exceed within 6 months.
```

## Optimization Recommendations

When auditing costs, look for:

### AI Costs
- Agents using Opus for tasks Sonnet handles well (biggest savings)
- Large file reads that could be scoped to line ranges
- Redundant discovery (multiple agents reading the same files)
- Missing agent memory (re-learning patterns each session)
- Free-text output where structured output would be shorter

### Cloud Costs
- Paying for resources during off-hours (scale-to-zero options)
- Services with cheaper alternatives at current scale
- Free tier headroom (are you close to limits?)
- Unused provisioned resources
- Services that could be consolidated

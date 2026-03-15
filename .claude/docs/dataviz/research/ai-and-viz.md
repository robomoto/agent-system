# AI + Visualization (2024-2026)

The hottest research area in data visualization. Load for agent architecture and automated chart generation questions.

## DracoGPT (Heer, IEEE TVCG 2025)

Extracts visualization design preferences from LLMs to recommend chart types. Given a data description, DracoGPT uses an LLM to score possible encodings against Draco's design rules.

**How it works:**
1. Data characteristics described in natural language or schema
2. LLM generates candidate Vega-Lite specs
3. Draco's constraint system scores each candidate
4. Top-scoring design returned with rationale

**Relevance to agent architecture:** Direct blueprint for a chart recommender agent. The pattern is: data description → LLM generation → formal validation → ranked recommendations. Can be implemented as a specialist agent workflow.

**Maturity:** Research. The approach is validated but no production-ready library exists.

## Microsoft LIDA

Automated viz generation pipeline with four stages:

1. **Summarizer** — Generates a compact natural-language description of the dataset
2. **Goal Explorer** — Identifies visualization goals (questions the data can answer)
3. **Viz Generator** — Produces chart code for each goal (grammar-agnostic: Matplotlib, Seaborn, Altair)
4. **Infographer** — Adds stylistic refinements and annotations

**Relevance:** The four-stage pipeline is a model for agent decomposition. Each stage maps to a subtask with clear inputs/outputs.

**Maturity:** Usable now. Open-source. Grammar-agnostic output.

## Microsoft Data-Formulator

AI-powered rich visualization creation. 11.5k GitHub stars (as of early 2026). Interactive tool where users describe desired charts in natural language and the system generates them.

**Maturity:** Production-grade tool. Good for prototyping but not for automated dashboard generation.

## ChartMimic (ICLR 2025)

Benchmark for chart-to-code generation. Given an image of a chart, can an LLM produce code that recreates it?

**Results:** GPT-4o scores 82.2 (direct) / 61.6 (indirect). Substantial room for improvement, especially for complex chart types.

**Relevance:** If you want agents to replicate chart styles from screenshots or references, this benchmark tells you what's achievable and where LLMs fail.

## LLM Chain Design for Viz (Heer, ACM ToCHI 2025)

Adapts crowdsourcing workflow patterns to design LLM pipelines for visualization tasks. Key insight: the decomposition patterns that work for human crowd workers (map-reduce, iterative refinement, tournament) also work for LLM chains.

**Relevance:** Directly informs how to structure multi-agent visualization workflows. The "map-reduce" pattern (generate multiple candidates in parallel, then select the best) maps to dispatching multiple specialist variations and synthesizing.

## Claude Interactive Viz (Anthropic, March 2026)

Real-time chart generation in conversation. Claude can produce interactive visualizations directly in the chat interface.

**Relevance:** Sets user expectations for conversational chart generation. "Show me my sleep trend" → instant chart is now the baseline experience.

## MIND Dashboard (CHI 2026)

LLM-powered narrative dashboard for mental health clinicians. Combines multimodal patient data (activity, sleep, mood, social interaction) with natural language narratives generated alongside charts.

**User study results (N=16):**
- Significantly improved insight discovery (p<.001) vs charts alone
- Improved decision-making (p=.004) vs charts alone
- Clinicians valued the narrative as a "starting point" that oriented them before examining charts

**Direct health dashboard application:** Generate a daily/weekly natural language summary alongside chart displays. "Your weight is trending down 0.3kg/week. Protein hit target 5/7 days. Sleep was disrupted Tuesday — RHR was elevated Wednesday."

## Implications for Agent-Generated Visualization

**What works now:**
- LLMs can generate Vega-Lite/Altair/Observable Plot specs from data descriptions
- Draco can validate those specs against perceptual best practices
- LIDA's pipeline (summarize → goals → generate → style) is a proven decomposition
- Narrative + chart hybrid improves comprehension over charts alone

**What doesn't work yet:**
- Complex custom chart types (horizon charts, body maps) require hand-coded templates
- LLMs struggle with precise spatial layout and responsive design
- Animation specification is not well-handled by current grammar-based approaches
- Chart-to-code reproduction (ChartMimic) has significant accuracy gaps for non-standard types

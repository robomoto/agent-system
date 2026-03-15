# Data Visualization Landscape Survey (2024–2026)

**Purpose:** Inform the design of specialist agents for a personal health/fitness dashboard project.
**Date compiled:** March 2026

---

## 1. Pioneering Practitioners

### Tier 1: Foundational Toolmakers

#### Mike Bostock (Observable / D3)
- **Current focus:** CTO and co-founder of Observable. Shipped **Observable Framework** (Feb 2024), an open-source static-site generator for data apps built on D3 and Observable Plot. Observable Cloud was deprecated April 2025; the strategic bet is now on Framework as an open-source-first approach to data dashboards.
- **Key artifacts:** D3.js (de facto standard for web viz since 2011), Observable Plot (high-level grammar-of-graphics JS library), Observable Framework.
- **Relevance to health dashboard:** Observable Plot and Framework are direct candidates for the rendering layer — Plot's `facet`, `window`, and `bin` transforms map cleanly to time-series health metrics.
- **Maturity:** Proven/production-grade.

#### Dominik Moritz (CMU / Apple)
- **Current focus:** Faculty at CMU Data Interaction Group; researcher at Apple. Published "Mosaic Selections" at IEEE VIS 2025 — a formal model for managing interactive selections in visualizations backed by millions of records, with orders-of-magnitude latency improvements over Vega.
- **Key artifacts:** Vega-Lite (declarative viz grammar), Mosaic (scalable interactive viz architecture with DuckDB), Draco (ML-based viz recommendation), Falcon (cross-filtering for billion-record datasets). At Apple: **Swift Charts** framework, Apple Women's Health Study visualization, Charts Human Interface Guidelines.
- **Relevance to health dashboard:** Vega-Lite's declarative spec is ideal for agent-generated visualizations; Draco's design rules can validate chart choices; Mosaic's DuckDB-backed architecture is a model for local-first health data querying.
- **Maturity:** Proven (Vega-Lite), production (Swift Charts), research (Mosaic Selections, Draco).

#### Jeffrey Heer (UW Interactive Data Lab)
- **Current focus:** Leading the most prolific academic viz lab. 2025 publications include:
  - **DracoGPT** — Extracting visualization design preferences from LLMs (IEEE TVCG 2025). Directly relevant: using LLMs to recommend chart types.
  - **Publish-Time Optimizations** — 83.7% rendering latency reduction and 33.3% activation latency reduction for web viz (IEEE VIS 2025).
  - **Mosaic** (with Moritz) — Architecture linking databases to scalable interactive viz; Best Demo Honorable Mention at ACM SIGMOD 2025.
  - **Sculpin** — Direct-manipulation transformation of JSON (ACM UIST 2025).
  - **Mixing Linters with GUIs** — Color palette design probes (IEEE TVCG 2025).
  - **Designing LLM Chains by Adapting Crowdsourcing Workflows** (ACM ToCHI 2025).
- **Key artifacts:** Vega, Altair (Python API for Vega-Lite), Mosaic, DracoGPT.
- **Relevance to health dashboard:** DracoGPT is a blueprint for an agent that recommends visualizations from data descriptions. Altair is the natural Python-side rendering choice. Publish-time optimizations are directly applicable to dashboard performance.
- **Maturity:** Research → production pipeline. Altair is production; DracoGPT is research.

### Tier 2: Design & Storytelling Visionaries

#### Giorgia Lupi (Pentagram)
- **Current focus:** Partner at Pentagram. Continues advocating **Data Humanism** — the philosophy that visualization should honor complexity and human texture rather than simplify into sterile charts. Work in MoMA's permanent collection. 2022 Cooper-Hewitt National Design Award.
- **Key artifacts:** "Dear Data" (year-long hand-drawn data postcard exchange with Stefanie Posavec), Data Humanism manifesto, Accurat studio (co-founded).
- **Relevance to health dashboard:** Her "Dear Data" specifically tracked personal behavioral data (kindnesses, compliments, habits) — a direct precedent for humanistic health tracking that goes beyond step counts. Her manifesto argues against the "quantified self" reductionism that most health dashboards embody.
- **Design implication:** An agent informed by Lupi's philosophy would generate visualizations that preserve granularity and individuality rather than reducing everything to aggregates. Think: hand-drawn aesthetic, personal annotation layers, "slow data" reflection modes.
- **Maturity:** Proven (design philosophy), artistic (execution style).

#### Nadieh Bremer (Visual Cinnamon)
- **Current focus:** Freelance data visualization designer and data artist. Active 2025 projects:
  - **EU Data Stories** (Publications Office of the European Union) — Three monthly stories including **"Health and Well-being in the EU"** analyzing prevention spending, disease burden, and healthcare access. Uses voronoi treemaps and creative chart types with d3.js and R.
  - **GitHub Top Contributor Network** — Interactive network visualization for Mozilla's ORCA project (Jan 2025).
- **Key artifacts:** Award-winning portfolio spanning creative/artistic viz. Known for pushing boundaries of SVG-based visualization with D3.
- **Relevance to health dashboard:** Her EU health visualization work is directly analogous. Her ability to create cohesive style guides across related data stories is a model for dashboard design systems. Her use of unusual chart types (voronoi treemaps) for health data shows how to make health viz engaging.
- **Maturity:** Proven/production.

#### Shirley Wu (Freelance)
- **Current focus:** Independent creative data viz practitioner. Recent work:
  - **Opportunity@Work** — Interactive scrollytelling + exploratory tool for 400+ occupations, skills, and wages. Helped secure nonprofit funding.
  - **2025 blog trilogy** reflecting on the state of bespoke data viz:
    1. "Outside a Client's Comfort Zone" — Client cut custom viz for standard charts
    2. "What Killed Innovation?" — Why bespoke viz is declining
    3. "Beyond the Plateau" — Hopeful reimagining; conversations with industry leaders about diverse roles needed
- **Relevance to health dashboard:** Her scrollytelling + exploratory hybrid pattern is ideal for health onboarding flows ("here's what your data shows" → "now explore yourself"). Her warnings about the tension between creative viz and client comfort directly inform how experimental to make a health dashboard.
- **Maturity:** Proven (interactive storytelling), commentary (industry analysis).

#### Moritz Stefaner (Truth & Beauty)
- **Current focus:** Freelance data viz designer. 2025: Keynote at VISCOMM workshop at IEEE VIS Vienna, discussing AI's impact on the viz profession.
- **Key artifacts:**
  - **WHO Data Design Language** — Rich data experiences for public health data. Directly relevant.
  - **Climate-Conflict-Vulnerability Index** — Geospatial multi-layer risk mapping.
  - **Impfdashboard** — Germany's official COVID-19 vaccination dashboard.
  - **OECD Better Life Index** — 6M+ visitors, interactive well-being comparison.
  - **Waves of Interest** (updated 2025) — Google Search interest patterns in US election years.
  - **Peak Spotting** — Passenger load management for German rail.
- **Relevance to health dashboard:** The WHO Data Design Language is the closest precedent to building a design system for health data visualization. The Impfdashboard shows public health dashboard at national scale. His IEEE VIS keynote on AI + viz profession informs the agent architecture itself.
- **Maturity:** Proven/production.

### Tier 3: Key Academics & Emerging Voices

#### Lace Padilla (Northeastern University)
- **Current focus:** Won IEEE VGTC 2025 **Significant New Research Award** for studying uncertainty in data visualization. Joint appointment in Computer Science and Psychology.
- **Research:** How people interpret uncertain data (hurricane forecasts, COVID projections). Demonstrated that **frequency framing** significantly improves comprehension of uncertainty.
- **Relevance to health dashboard:** Health data is inherently uncertain (measurement error, biological variability). Her frequency-framing research directly informs how to display confidence intervals, prediction ranges, and probabilistic health insights.
- **Maturity:** Research (but with actionable design guidelines).

#### Arvind Satyanarayan (MIT CSAIL / Visualization Group)
- **Current focus:** Associate Professor at MIT. Co-creator of Vega-Lite (with Moritz and Heer). Research on interactive visualization authoring, natural language interfaces for viz, and accessible data representations.
- **Key artifacts:** Vega-Lite, Lyra (interactive viz design environment), research on NL-to-viz pipelines.
- **Relevance to health dashboard:** NL-to-viz research informs conversational interfaces for health data ("show me my sleep trend this month").
- **Maturity:** Research → tooling pipeline.

#### Maarten Lambrechts (Belgium)
- **Current focus:** Data journalist, designer, and consultant. Known for small multiples expertise and experimental comparative visualization approaches. Active in the European data journalism community.
- **Relevance to health dashboard:** Small multiples are essential for comparing health metrics across time periods, body systems, or intervention phases. His redesign work (e.g., small multiple bars → slopegraph) shows when to switch chart types for better comparison.
- **Maturity:** Proven (design practice).

#### Amanda Cox (NYT, Data Editor) & Archie Tse (NYT, Graphics Director)
- **Current roles:** Cox is Data Editor at NYT (since 2019), connecting The Upshot, Graphics, and Computer-Assisted Reporting. Tse is Graphics Director (since 2019), overseeing the desk after 25+ years. Created industry-standard tools: **ArchieML** (structured text format), **ai2html** (Illustrator to HTML).
- **2025 NYT output:** Year-end graphics collection; interactive policy analysis (tax bill distributional effects); health insurance cost explorers; infrastructure mapping.
- **Relevance to health dashboard:** NYT's annotation-heavy, explanation-rich style is the gold standard for making data accessible to non-experts — exactly the UX needed for health dashboards. Their progressive disclosure approach (overview → detail) is directly applicable.
- **Maturity:** Proven/production (setting industry standard for 20+ years).

### Emerging Notable Voices (2024–2026)

| Person | Focus | Why Notable |
|--------|-------|-------------|
| **Liuhuaying Yang** | Scientific/health viz | 2024 IIB Awards "Impressive Individual" — 6 submissions, 3 shortlisted. Created "Zoonotic Web" (Gold, Science/Health). |
| **Valentina D'Efilippo** | Data storytelling, infogr8 | Leading DVS Future Fridays workshops (2025); collaborative data design sessions. |
| **Milos Popovic** | Geospatial viz | Top GIS Voices 2024. 300+ maps in R/D3. Teaching at Columbia, ASU, Leiden. |
| **Wanmei Liang** | Earth science viz | NASA Earth Observatory data visualizer. VP of Women in GIS. Top GIS Voices 2024. |
| **Andrew McNutt** | Viz design tools | Color palette linters + GUIs (IEEE TVCG 2025, with Heer). Bridging design tools and research. |

---

## 2. Studios & Organizations

### Data Journalism Studios

| Studio | Status (2025) | Signature Strength | Notable Recent Work |
|--------|--------------|-------------------|-------------------|
| **The Pudding** | Active | Scrollytelling visual essays; cultural data | 50% editorial / 50% client work. No-code chart tools for accessibility. |
| **Polygraph** | Active (The Pudding's agency arm) | Client data storytelling | 2025: Carnegie Corporation library history digitization. Clients: Google, YouTube, LinkedIn, Universal Music, WaPo. IIB Studio of the Year (previous). |
| **NYT Graphics / The Upshot** | Active | Explanatory journalism, policy analysis | 2025: Tax bill distributional analysis, EV charging infrastructure mapping, health insurance cost explorers. Gold standard for annotation-rich dataviz. |
| **Reuters Graphics** | Active | Breaking news viz, global data stories | 2024 IIB Gold (Humanitarian) for Sudan famine coverage. Strong real-time data pipeline capability. |
| **The Guardian Data** | Active | Interactive news viz | 10 Malofiej Awards (when active). Strong accessibility focus. |
| **Washington Post Engineering** | Active | Interactive storytelling | Climate, elections, and policy visualization. |

### Research Labs

| Lab | Institution | Lead | Current Focus |
|-----|------------|------|---------------|
| **Interactive Data Lab (IDL)** | UW | Jeffrey Heer | Vega/Altair ecosystem, DracoGPT, Mosaic, LLM+viz, publish-time optimizations |
| **Data Interaction Group (DIG)** | CMU | Dominik Moritz | Vega-Lite, Mosaic, Draco, scalable interaction, Swift Charts |
| **Visualization Group** | MIT CSAIL | Arvind Satyanarayan | NL-to-viz, interactive authoring, accessible viz |
| **Google PAIR** | Google | Multiple | LIT (model interpretability), What-If Tool, Facets, Embedding Projector, TensorBoard, **Clinical Vis** (healthcare-specific), AI Explorables |
| **MIT Media Lab** | MIT | Multiple | Tangible interfaces, community data, social computing |
| **Interactive Media Lab Dresden** | TU Dresden | Raimund Dachselt | Augmented dynamic data physicalization, shape-changing interfaces, AR+viz |
| **Visualization Design Lab** | U. Utah | Multiple | Tactile charts for accessibility, 3D-printed viz for BLV users |

### Design Studios

| Studio | Focus | Health Relevance |
|--------|-------|-----------------|
| **Pentagram** (Lupi's practice) | Data humanism, editorial design | Personal data philosophy |
| **Accurat** (Lupi co-founded) | Data-driven design | Complex data narratives |
| **Visual Cinnamon** (Bremer) | Creative data art + client viz | EU health data stories |
| **Truth & Beauty** (Stefaner) | Public data design | WHO Data Design Language, Impfdashboard |
| **infogr8** | Data design agency | DVS workshop partner |

---

## 3. Competitions & Awards

### Active & Prestigious

| Competition | Status | Cycle | What It Rewards | 2024 Health-Relevant Winners |
|-------------|--------|-------|----------------|------------------------------|
| **Information is Beautiful Awards** (Kantar) | **Active** | Annual (~1000 submissions) | Beauty, storytelling, impact, innovation across categories | Gold Science/Health: "Zoonotic Web" (Liuhuaying Yang). Gold Humanitarian: Reuters Sudan famine story. |
| **IEEE VIS** (VAST, InfoVis, SciVis) | **Active** | Annual conference + proceedings | Peer-reviewed research papers, best paper awards | 2025 in Vienna. Best Demo Honorable Mention: Mosaic. DracoGPT, Mosaic Selections, publish-time optimizations all presented. |
| **Iron Viz** (Tableau) | **Active** | Annual qualifier + championship at Tableau Conference | Live 20-min dashboard creation; design, analysis, storytelling | 2025 champion: Bo McCready ("Two Eras of Safety"). 2024: Chris Westlake ("The IMDb Explorer"). Student edition active. 2026 qualifiers open. |
| **Outlier Conference** (DVS) | **Active** | Annual. 2026 theme: "The Final Draft" | Talks on iteration, feedback, constraints in dataviz | Speaker applications open through Feb 2026. Virtual/pre-recorded accepted. |
| **ACM CHI** | **Active** | Annual | HCI research including visualization | Ongoing integration of viz + accessibility + AI research. |
| **SND Best of News Design** | **Active** | Annual | Journalistic graphics and design | SND46 honored 2024 work. |

### Paused or Evolved

| Competition | Status | Notes |
|-------------|--------|-------|
| **Malofiej Awards** | **Paused** since Oct 2021 | Organizers (SND-E) announced "period of reflection." No resumption confirmed. Was called "the Pulitzers for infographics." |
| **OpenVis Conf** | **Evolved** | The original OpenVis Conf (Bocoup) appears inactive. The **Open Visualization Collaborator Summit** (OpenJS Foundation) is a successor-in-spirit: Oct 2025 in Seattle at Google, focused on open-source viz libraries (deck.gl, Kepler.gl, cosmos.gl, MapLibre). More toolmaker-oriented than design-oriented. |

### Community Showcases

| Platform | Type | Notes |
|----------|------|-------|
| **Observable Community** | Notebooks, collections | Active sharing of D3/Plot examples. Bostock and team curate featured work. |
| **DVS Du Bois Challenge** | Annual recreation challenge | Participants recreate W.E.B. Du Bois's 1900 visualizations with modern tools. Prizes via DVS Slack. 2026 edition active. |
| **DVS Future Fridays** | Collaborative workshops | 2025: Led by Valentina D'Efilippo. Hands-on design sessions. |
| **#30DayMapChallenge** | November challenge | Annual community mapping challenge. Major participation from geospatial viz community. |
| **#TidyTuesday** | Weekly R community challenge | Data + visualization challenge. Massive participation. Good for benchmarking R-based health viz approaches. |

---

## 4. Academic Venues & Journals

### Top Venues (Ranked by Impact on Viz Practice)

| Venue | Type | Frequency | Key Focus Areas |
|-------|------|-----------|----------------|
| **IEEE VIS** (incorporating InfoVis, VAST, SciVis) | Conference | Annual | Full spectrum of visualization research. Unified since 2021. 2025: Vienna. |
| **IEEE TVCG** | Journal | Continuous | Premier viz journal. Papers from VIS appear here. |
| **ACM CHI** | Conference | Annual | HCI + viz intersection. Accessibility, interaction design, user studies. |
| **EuroVis** | Conference | Annual | European viz community. Published in Computer Graphics Forum. |
| **Computer Graphics Forum** | Journal | Continuous | EuroVis papers + broader CG research. |
| **ACM UIST** | Conference | Annual | Novel interaction techniques. Sculpin (JSON manipulation) presented 2025. |
| **ACM SIGMOD** | Conference | Annual | Database + viz intersection. Mosaic demo 2025. |
| **ICLR** | Conference | Annual | ML + viz (ChartMimic benchmark 2025). |

### Hot Research Areas (2024–2026)

#### 1. AI + Visualization (🔥 Hottest Area)
- **DracoGPT** (Heer, 2025): Extracting design preferences from LLMs to recommend chart types. Direct path to agent-generated dashboards.
- **Microsoft LIDA**: Automated viz generation — summarizer → goal explorer → viz generator → infographer. Grammar-agnostic across Matplotlib/Seaborn/Altair.
- **Microsoft Data-Formulator**: AI-powered rich viz creation (11.5k GitHub stars).
- **ChartMimic** (ICLR 2025): Benchmark for chart-to-code generation. GPT-4o scores 82.2/61.6 — substantial room for improvement.
- **Claude interactive viz** (Anthropic, March 2026): Real-time chart generation in conversation.
- **LLM chain design for viz** (Heer, ACM ToCHI 2025): Adapting crowdsourcing workflow patterns to design LLM pipelines.
- **Maturity:** Research → early production. LIDA and Data-Formulator are usable now. DracoGPT is research.

#### 2. Uncertainty Visualization
- **Lace Padilla** (Northeastern): VGTC 2025 award. Frequency framing improves comprehension. Psychology-grounded approach.
- **Progressive Visualization Survey** (IEEE TVCG 2024): Comprehensive taxonomy. Key properties: uncertainty, steering, visual stability, real-time processing. Visual browser at visualsurvey.net/pva.
- **Relevance to health:** Every health metric has uncertainty (device accuracy, biological variation, prediction confidence). This research tells you how to show it without overwhelming users.
- **Maturity:** Research with actionable design guidelines.

#### 3. Accessibility in Visualization
- **Tactile charts** (U. Utah, IEEE TVCG 2026): 3D-printed templates for BLV users — UpSet plots, violin plots, heatmaps. Study with 12 BLV participants found tactile models were preferred learning method.
- **Rich screen reader experiences** (UW IDL): Three dimensions — structure, navigation, description. Users can navigate chart entities at varying granularities.
- **Sonification for accessibility**: Natural sound mapping (e.g., bird sounds for bar chart values). 12-participant study showed effectiveness.
- **Audio data narratives** (ACM CHI): Narrated data insights for non-visual consumption.
- **WCAG 2.1 compliance in dashboards**: 16px min font, 44×44px touch targets, ARIA attributes, keyboard navigation, live regions for dynamic updates.
- **Maturity:** Research → early implementation. Apple's Swift Charts has built-in accessibility; web standards are catching up.

#### 4. Scalable Interactive Visualization
- **Mosaic** (Heer + Moritz): DuckDB-backed architecture linking databases to interactive views. Best Demo at SIGMOD 2025.
- **Mosaic Selections** (Moritz, IEEE VIS 2025): Formal model for managing selections across millions of records.
- **Falcon** (Moritz): Cross-filtering for billion-record datasets.
- **cosmos.gl**: GPU-powered graph rendering for millions of nodes in the browser.
- **Publish-time optimizations** (Heer, 2025): 83.7% rendering latency reduction.
- **Maturity:** Research → production. Mosaic + DuckDB is usable now.

#### 5. Immersive Analytics (AR/VR)
- **Augmented Dynamic Data Physicalization** (TU Dresden, IEEE TVCG 2025): Combining shape-changing physical sculptures with AR overlays. Applications: personal information hubs, exhibitions, immersive analytics.
- **Maturity:** Experimental. Not ready for health dashboards but worth tracking.

---

## 5. Experimental & Avant-Garde

### Data Physicalization
| Project | What | Status |
|---------|------|--------|
| **Squishicalization** (TU Vienna, IEEE TVCG 2024) | Elastic 3D-printed data sculptures. Voronoi-tessellated sponge structures where squishiness encodes density. Consumer 3D printer compatible. | Research/experimental |
| **Augmented Dynamic Data Physicalization** (TU Dresden, IEEE TVCG 2025) | Shape-changing data sculptures + AR labels and scales. Personal information hubs. | Research/experimental |
| **Tactile Charts** (U. Utah, IEEE TVCG 2026) | 3D-printed chart templates for blind/low-vision accessibility. | Research with proven user impact |
| **Dear Data postcards** (Lupi + Posavec) | Hand-drawn data on physical postcards. Analog "physicalization." | Artistic/proven (MoMA collection) |

### Sonification (Data as Sound)
| Approach | What | Status |
|----------|------|--------|
| **Natural sound mapping** | Data values → ambient sounds (bird songs, water). BLV user studies show effectiveness. | Research |
| **Screen reader + sonification hybrid** | Combined audio approaches for data overview + detail search. | Research |
| **Audio data narratives** | Narrated data insights (ACM CHI). | Research |
| **Health relevance:** | Heart rate could map to tempo; sleep stages to tonal shifts; activity levels to rhythm complexity. | Speculative but grounded |

### Bespoke / Artisanal Visualization
| Practitioner/Project | Medium | Status |
|---------------------|--------|--------|
| **Giorgia Lupi** (Dear Data) | Hand-drawn ink on postcards | Artistic/proven |
| **Nadezda Andrianova** ("World in Tangible Fragments") | Physical/mixed media. 2024 IIB Gold (Unusual category). | Artistic |
| **Anastasia Balagurova** ("Birdsong of Sorrow above Ukraine") | Data + sound + visual narrative. 2024 IIB Gold (Current Affairs). | Artistic |
| **Shirley Wu** | Custom interactive web experiences | Proven but Wu notes declining demand |

### AR/VR Immersive Analytics
- Academic interest remains high but consumer adoption is limited.
- Apple Vision Pro has not yet produced a breakout data viz application.
- Most promising near-term application: spatial arrangement of dashboard panels in AR for complex multi-metric health monitoring.
- **Maturity:** Experimental. 3–5 years from mainstream health dashboard use.

### Haptic Data Exploration
- Primarily in accessibility research (tactile charts above).
- No consumer-grade haptic data exploration for health dashboards exists.
- Apple Watch Taptic Engine is the closest deployed haptic health data feedback.
- **Maturity:** Very early research.

---

## 6. Synthesis: What This Means for Health Dashboard Agents

### Agent Architecture Implications

Based on this survey, a health/fitness dashboard system should have specialist agents informed by the following:

| Agent Role | Informed By | Key References |
|------------|------------|----------------|
| **Chart Recommender** | DracoGPT, Draco design rules, Vega-Lite grammar | Heer 2025, Moritz Draco |
| **Rendering Engine Specialist** | Observable Plot, D3, Altair, Swift Charts | Bostock, Moritz |
| **Health Data Storyteller** | Lupi (data humanism), Wu (scrollytelling), NYT Upshot (progressive disclosure) | Dear Data, Opportunity@Work, NYT annotation style |
| **Uncertainty Communicator** | Padilla (frequency framing), progressive viz survey | Padilla VGTC 2025, IEEE TVCG 2024 survey |
| **Accessibility Specialist** | Tactile charts research, screen reader experiences, sonification, WCAG 2.1 | Utah 2026, UW IDL, Apple Swift Charts guidelines |
| **Style System Designer** | Bremer (EU health stories style guide), Stefaner (WHO Data Design Language, Impfdashboard) | Visual Cinnamon, Truth & Beauty |
| **Performance Optimizer** | Mosaic (DuckDB), publish-time optimizations, Falcon | Heer 2025, Moritz 2025 |
| **AI Viz Generator** | LIDA, Data-Formulator, ChartMimic, Claude viz | Microsoft LIDA, Data-Formulator |

### Doc Bundles Needed per Specialist

1. **Core Grammar & Rendering:**
   - Vega-Lite specification
   - Observable Plot API docs
   - D3 selection/scale/axis references
   - Altair Python API

2. **Design Rules & Guidelines:**
   - Draco design constraints (formal rules for good viz)
   - Apple Charts HIG
   - Stefaner WHO Data Design Language (if obtainable)
   - NYT Graphics style guide principles (inferred from published work)

3. **Health-Specific Viz:**
   - Bremer EU health visualization case study
   - Stefaner Impfdashboard case study
   - Google PAIR Clinical Vis tool documentation
   - Apple Women's Health Study visualization approach
   - JMIR scoping review on health dashboard design (2026)

4. **Uncertainty & Progressive Viz:**
   - Padilla's frequency framing papers
   - Progressive Visualization Survey (IEEE TVCG 2024) + visual browser
   - Heer publish-time optimization paper

5. **Accessibility:**
   - WCAG 2.1 contrast/touch/ARIA requirements
   - Rich Screen Reader Experiences for viz (UW IDL)
   - Sonification approaches for data
   - Tactile chart design principles (Utah)

6. **AI-Powered Viz Generation:**
   - DracoGPT paper and approach
   - Microsoft LIDA architecture (summarizer → goal explorer → viz generator → infographer)
   - ChartMimic benchmark (know what LLMs can/can't do)
   - LLM chain design patterns (Heer ACM ToCHI 2025)

### What's Proven vs. Experimental vs. Artistic

| Category | Proven (Build on Now) | Experimental (Track) | Artistic (Inspire) |
|----------|----------------------|---------------------|-------------------|
| **Rendering** | D3, Observable Plot, Vega-Lite, Altair, Swift Charts | Mosaic+DuckDB, cosmos.gl | — |
| **Design** | NYT annotation style, small multiples, progressive disclosure | AI-generated chart recommendations (DracoGPT) | Data humanism (Lupi), bespoke viz (Wu) |
| **Health-specific** | Standard dashboards (line/bar/gauge), Impfdashboard pattern | WHO Data Design Language, Apple Health Study | Dear Data personal tracking |
| **Uncertainty** | Error bars, confidence bands | Frequency framing, progressive viz | — |
| **Accessibility** | WCAG 2.1, ARIA, screen readers | Sonification, tactile 3D prints | — |
| **Immersive** | — | AR overlays on physical viz | Data sculpture, physicalization |
| **AI+Viz** | LIDA, Data-Formulator | DracoGPT, ChartMimic | — |

---

## 7. Key Takeaways

1. **The AI+Viz intersection is exploding.** DracoGPT, LIDA, Data-Formulator, and ChartMimic all landed in 2024–2025. Building agents that generate visualizations is now a well-studied problem with benchmarks.

2. **Health viz has strong precedents** but no dominant open framework. Stefaner's WHO work, Bremer's EU health stories, Google PAIR's Clinical Vis, and Apple's Health Study viz are all models, but none is a reusable open-source health viz design system. This is a gap your agents could fill.

3. **Uncertainty communication is the biggest UX challenge** for health dashboards. Padilla's research is the most actionable: use frequency framing ("3 out of 10 days you exceeded your target") over probability statements ("30% chance of exceeding").

4. **The Vega-Lite → Altair → Observable Plot ecosystem is the best foundation** for agent-generated health viz. Declarative grammars are LLM-friendly; Draco provides validation rules; Mosaic handles scale.

5. **Accessibility is no longer optional** — Apple's Swift Charts has it built in, academic research is producing actionable guidelines, and health data especially needs to be accessible (aging users, visual impairments correlated with health conditions).

6. **Bespoke/artisanal viz is declining commercially** (per Shirley Wu's 2025 analysis) but remains influential for design inspiration. A health dashboard should offer both standard clinical views and a "personal reflection" mode inspired by data humanism.

7. **Physical and immersive viz are 3–5 years out** for consumer health applications. Track but don't build for them now. Exception: Apple Watch haptics is already deployed.

# Clinical Genomics AI Benchmark Suite

**Status:** 🔒 Private Development  
**Purpose:** Automated testing and benchmarking of LLM agents for clinical genomics applications  
**NOT FOR PUBLIC DISCLOSURE**

---

## What This Is

This repository is a **test and benchmark suite** for evaluating AI agents (LLMs) on clinical genomics tasks. It's designed to:

- **Test LLM agents** on real-world clinical genomics scenarios (variant interpretation, treatment recommendations, trial matching)
- **Measure performance** using Pass@K metrics (how often agents get tasks right on first try, or within K attempts)
- **Validate accuracy** against clinical standards (ACMG/AMP guidelines, FDA/NCCN recommendations)
- **Track improvements** as you iterate on agent prompts, tools, and configurations

Think of it as a **quality assurance system** for clinical genomics AI - it runs your agent through a battery of tests and tells you how well it performs.

---

## How It Works

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Test Runner (run_tests.py)                │
│  - Loads domain config (agent, LLM, tasks)                   │
│  - Iterates through all tasks                               │
│  - Runs agent multiple times (Pass@K)                       │
│  - Evaluates responses using custom evaluators              │
│  - Calculates metrics (Pass@1, Pass@K)                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    LLM Agent (OpenAI/Anthropic)              │
│  - Receives task question                                    │
│  - Uses system prompt (clinical genomics instructions)      │
│  - Can access MCP servers (ClinVar, OncoKB, PubMed, etc.)   │
│  - Returns structured response                                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Evaluators (domains/*/evaluators/)              │
│  - Validates response format                                 │
│  - Checks against expected answers                           │
│  - Scores accuracy (0-1)                                    │
│  - Provides feedback                                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                    Results (results/*.json)                  │
│  - Per-task results                                          │
│  - Pass@1 and Pass@K metrics                                │
│  - Detailed evaluation scores                                │
│  - HTML reports                                              │
└─────────────────────────────────────────────────────────────┘
```

### Step-by-Step Process

1. **Load Configuration** (`domains/clinical_genomics/config.yaml`)
   - Defines the LLM model (e.g., `openai/gpt-4o`)
   - Configures the agent (ReAct agent with clinical genomics instructions)
   - Lists all tasks to run

2. **Load Tasks** (`domains/clinical_genomics/tasks/*.json`)
   - Each task contains:
     - A question (e.g., "Classify BRCA1 variant...")
     - Expected output format (JSON schema)
     - MCP servers to use (ClinVar, PubMed, etc.)
     - Evaluators (validation functions)

3. **Run Agent** (for each task, K times)
   - Sends task question to LLM agent
   - Agent can use MCP servers to query genomics databases
   - Agent returns structured response

4. **Evaluate Response**
   - Runs custom evaluator functions
   - Checks if response matches expected format
   - Validates clinical accuracy (pathogenicity classification, evidence codes, etc.)
   - Scores: 0.0 (failed) to 1.0 (perfect)

5. **Calculate Metrics**
   - **Pass@1**: % of tasks passed on first attempt
   - **Pass@K**: % of tasks passed within K attempts
   - Target range: 30-70% Pass@1 (too low = tasks too hard, too high = tasks too easy)

6. **Generate Reports**
   - JSON results files
   - HTML reports (if generator available)
   - Summary statistics

---

## What It's Meant For

### Primary Use Cases

1. **Agent Development & Testing**
   - Test new agent prompts before deploying to production
   - Validate that agents follow ACMG/AMP guidelines correctly
   - Ensure agents cite evidence sources (ClinVar IDs, PMIDs)
   - Measure improvement as you iterate on prompts

2. **Performance Benchmarking**
   - Compare different LLM models (GPT-4o vs Claude vs others)
   - Measure impact of MCP server integration
   - Track performance over time (regression testing)
   - Set quality gates (e.g., "Pass@1 must be ≥50%")

3. **Clinical Validation**
   - Validate that AI recommendations match clinical standards
   - Ensure agents don't hallucinate or make unsafe recommendations
   - Test edge cases (VUS variants, conflicting evidence, rare diseases)
   - Generate evidence-backed reports for clinical review

4. **CI/CD Integration**
   - Automatically test agents on every code change
   - Fail builds if performance drops below threshold
   - Generate reports for pull requests
   - Track performance trends over time

### Target Users

- **AI Engineers**: Developing and testing clinical genomics agents
- **Clinical Researchers**: Validating AI recommendations against clinical standards
- **Product Teams**: Ensuring quality before deploying to clinicians
- **QA Teams**: Automated testing and regression detection

---

## Quick Start

### Prerequisites

- Python 3.11+
- `uv` package manager (install: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- API keys:
  - `OPENAI_API_KEY` (required)
  - `ANTHROPIC_API_KEY` (optional, for Claude)
  - `ONCOKB_API_KEY` (optional, free academic tier)
  - `PHARMGKB_API_KEY` (optional, free academic tier)

### Installation

```bash
# 1. Clone repository
git clone https://github.com/crispro-ai/genomics-mcp.git
cd genomics-mcp

# 2. Install dependencies with uv
uv sync

# 3. Set up API keys
export OPENAI_API_KEY="sk-..."
# Or create .env file:
# OPENAI_API_KEY=sk-...
```

### Running Tests

```bash
# Activate virtual environment (created by uv)
source .venv/bin/activate

# Run all tests (1 run per task)
python scripts/run_tests.py --domain clinical_genomics --runs 1 --output results/

# Run with 3 attempts per task (Pass@3)
python scripts/run_tests.py --domain clinical_genomics --runs 3 --output results/

# View results
cat results/summary.json
```

### Expected Output

```
🧬 Running tests for domain: clinical_genomics
📊 Pass@1 testing (each task runs 1 times)

📝 Testing: tasks/variant_task_0001.json
  Run 1/1... ✅

============================================================
📊 TEST RESULTS SUMMARY
============================================================
Domain: clinical_genomics
Total Tasks: 1
Pass@1: 100.0%
Pass@1: 100.0%

Target Range: 30-70% Pass@1
⚠️  Pass@1 too high - tasks may be too easy
```

---

## Project Structure

```
clinical-genomics-private/
├── domains/
│   └── clinical_genomics/
│       ├── config.yaml              # Domain configuration (LLM, agent, tasks)
│       ├── evaluators/
│       │   ├── __init__.py
│       │   └── functions.py         # Custom evaluation logic
│       └── tasks/
│           ├── variant_task_0001.json    # Variant interpretation task
│           ├── treatment_task_*.json     # Treatment recommendation tasks
│           ├── trial_task_*.json         # Clinical trial matching tasks
│           └── drug_task_*.json          # Drug-gene interaction tasks
├── scripts/
│   ├── run_tests.py                 # Main test runner
│   └── generate_report.py          # HTML report generator (optional)
├── results/                         # Test results (generated)
│   ├── results.json                # Detailed per-task results
│   └── summary.json                # Summary metrics
├── .github/
│   └── workflows/
│       └── test.yml                 # GitHub Actions CI/CD
├── pyproject.toml                   # Python dependencies
└── README.md                        # This file
```

---

## Task Categories

### 1. Variant Interpretation (15 tasks)
- ACMG/AMP pathogenicity classification
- Evidence code assignment (PVS1, PM2, etc.)
- VUS (Variant of Uncertain Significance) analysis
- Conflicting evidence resolution

### 2. Treatment Recommendation (15 tasks)
- Targeted therapy matching based on genomic profile
- Combination therapy design
- Resistance prediction
- Drug selection for specific mutations

### 3. Clinical Trial Matching (10 tasks)
- Eligibility screening
- Multi-site coordination
- Basket trial navigation
- Protocol-specific criteria

### 4. Drug-Gene Interactions (10 tasks)
- CYP450 metabolizer status
- Polypharmacy analysis
- Adverse reaction prediction
- Dosing adjustments

### 5. Evidence Synthesis (5 tasks)
- Literature review and synthesis
- Guideline compliance checking
- Multi-source evidence integration

### 6. Cohort Analysis (5 tasks)
- Batch patient processing
- Variant reclassification
- Population-level insights

**Total: 60 tasks** (currently 1 task implemented, 59 to be added)

---

## Configuration

### Domain Config (`domains/clinical_genomics/config.yaml`)

Defines:
- **LLM**: Model to use (e.g., `openai/gpt-4o`)
- **Agent**: Agent type and instructions (ReAct agent with clinical genomics prompt)
- **Benchmark**: List of tasks to run

Example:
```yaml
---
kind: llm
spec:
  name: llm-1
  type: labelbox
  config:
    model_name: openai/gpt-4o

---
kind: agent
spec:
  name: genomics-agent
  type: react
  config:
    llm: llm-1
    instruction: |
      You are a clinical genomics AI assistant...
    max_iterations: 30

---
kind: benchmark
spec:
  description: Clinical Genomics Decision Support
  agent: genomics-agent
  tasks:
    - tasks/variant_task_0001.json
```

### Task Format (`domains/clinical_genomics/tasks/*.json`)

Each task contains:
- `category`: Task type (variant_interpretation, treatment_recommendation, etc.)
- `question`: The question to ask the agent
- `output_format`: Expected JSON schema for response
- `mcp_servers`: MCP servers to use (ClinVar, OncoKB, PubMed, etc.)
- `evaluators`: Validation functions and expected values

Example:
```json
{
  "category": "variant_interpretation",
  "question": "Classify BRCA1 c.5266dupC variant...",
  "output_format": {
    "pathogenicity": "[Pathogenic/Likely Pathogenic/VUS/Likely Benign/Benign]",
    "evidence_codes": ["[code1]", "[code2]"],
    "confidence": "[0.0-1.0]"
  },
  "mcp_servers": [
    {"name": "clinvar-api"},
    {"name": "pubmed-search"}
  ],
  "evaluators": [{
    "func": "raw",
    "op": "clinical_genomics.validate_variant_classification",
    "op_args": {
      "expected_tier": "Pathogenic",
      "expected_codes": ["PVS1", "PM2"]
    }
  }]
}
```

---

## Evaluation System

### Evaluators (`domains/clinical_genomics/evaluators/functions.py`)

Custom Python functions that validate agent responses:

```python
@compare_func
def validate_variant_classification(question, llm_response, op_args):
    """
    Validate ACMG/AMP variant classification.
    
    Checks:
    - Pathogenicity tier matches expected
    - Evidence codes are correct
    - Confidence score is reasonable
    - References are provided
    """
    # Parse LLM response
    # Check against expected values
    # Return: {"passed": bool, "score": float, "feedback": str}
```

### Metrics

- **Pass@1**: % of tasks passed on first attempt (target: 30-70%)
- **Pass@K**: % of tasks passed within K attempts (target: 50-85%)
- **Zero Score**: % of tasks with 0% success (should be <10%)

---

## MCP Server Integration

The test suite supports **MCP (Model Context Protocol) servers** for accessing genomics databases:

- **clinvar-api**: Variant pathogenicity data and clinical significance
- **oncokb-api**: Cancer mutation annotations and treatment implications
- **pubmed-search**: Scientific literature and clinical evidence
- **clinical-trials-api**: Ongoing trials and eligibility criteria
- **pharmgkb-api**: Drug-gene interaction data and dosing guidelines

Tasks can specify which MCP servers to use via the `mcp_servers` field.

---

## GitHub Actions CI/CD

### Automated Testing

The repository includes GitHub Actions workflow (`.github/workflows/test.yml`) that:

1. **Validates** domain structure (config, tasks, evaluators)
2. **Runs tests** on all tasks (3 runs per task)
3. **Calculates metrics** (Pass@1, Pass@3)
4. **Generates reports** (HTML + JSON)
5. **Uploads artifacts** (results, reports)
6. **Comments on PR** (if PR triggered)
7. **Fails if out of range** (Pass@1 < 30% or > 70%)

### Setup

1. **Add Secrets** to GitHub repo:
   - Go to Settings → Secrets and variables → Actions
   - Add: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.

2. **Push to trigger**:
   ```bash
   git push origin main
   # Check Actions tab for results
   ```

3. **Manual trigger**:
   - Go to Actions tab
   - Select "Clinical Genomics Domain Testing"
   - Click "Run workflow"

**Run Time:** ~1-2 hours for 60 tasks

---

## API Keys Required

### Essential
- **OpenAI**: `OPENAI_API_KEY` (required for agent)
- **ClinVar**: Free (NCBI E-utilities, no key needed)
- **PubMed**: Free (NCBI E-utilities, no key needed)

### Optional
- **Anthropic**: `ANTHROPIC_API_KEY` (for Claude models)
- **OncoKB**: `ONCOKB_API_KEY` (free academic tier)
- **PharmGKB**: `PHARMGKB_API_KEY` (free academic tier)
- **SerpAPI**: `SERP_API_KEY` (for Google Search)

### Setup

**Local development:**
```bash
export OPENAI_API_KEY="sk-..."
# Or create .env file
```

**GitHub Actions:**
- Add secrets in repo Settings → Secrets and variables → Actions

---

## Creating New Tasks

1. **Create task JSON** in `domains/clinical_genomics/tasks/`:
   ```json
   {
     "category": "variant_interpretation",
     "question": "Your question here...",
     "output_format": {...},
     "mcp_servers": [...],
     "evaluators": [...]
   }
   ```

2. **Add to config.yaml**:
   ```yaml
   tasks:
     - tasks/variant_task_0001.json
     - tasks/your_new_task.json  # Add here
   ```

3. **Test locally**:
   ```bash
   python scripts/run_tests.py --domain clinical_genomics --runs 1
   ```

4. **Push and CI runs automatically!**

---

## Security & Privacy

**⚠️ IMPORTANT:**
- This repo is **PRIVATE** - do NOT make public
- Contains proprietary evaluation logic
- Uses commercial API keys (protect secrets!)
- **NO real patient data** - only synthetic/published cases

**GitHub Actions Security:**
- Secrets are encrypted in GitHub
- Never logged or exposed in output
- Access controlled by repo permissions

---

## Roadmap

### Phase 1: Testing Infrastructure (Current) ✅
- ✅ GitHub Actions CI/CD
- ✅ Pass@K evaluation
- ✅ Automated reporting
- ✅ MCP server integration

### Phase 2: Domain Expansion (In Progress)
- 🔄 60 clinical genomics tasks (1/60 complete)
- 🔄 ACMG/AMP compliance evaluators
- 🔄 Multi-source data integration

### Phase 3: Product Development (Future)
- 📋 Web UI for clinicians
- 📋 Batch patient processing
- 📋 Report generation (PDF)
- 📋 Clinical trial enrollment automation

### Phase 4: Clinical Validation (Future)
- 📋 Partner with cancer center
- 📋 Real-world patient validation
- 📋 Publication in medical journal

### Phase 5: Commercialization (Future)
- 📋 SaaS product launch
- 📋 First paying customers
- 📋 Pharma partnerships

---

## Related Resources

- **[Clinical Genomics Doctrine](../.cursor/rules/clinical-genomics-domain-doctrine.mdc)** - Strategic plan
- **[Grant Application Domain](https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_template)** - Reference implementation (public)

---

## License

**Proprietary** - NOT open source. All rights reserved.

**Owner:** Alpha (Fahad)  
**Status:** 🔒 Private Development  
**Repository:** https://github.com/crispro-ai/genomics-mcp

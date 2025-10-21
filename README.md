# Clinical Genomics AI Platform (Private)

**Status:** 🔒 Private Development  
**Purpose:** Commercial product + internal testing  
**NOT FOR PUBLIC DISCLOSURE**

---

## Overview

Private clinical genomics AI benchmark and testing suite. This repo contains:
- 60 clinical genomics tasks (variant interpretation, treatment recommendation, trial matching)
- Automated testing infrastructure (GitHub Actions)
- Pass@K evaluation metrics
- Integration with genomics APIs (ClinVar, OncoKB, PharmGKB, etc.)

---

## Quick Start

### Local Setup

```bash
# 1. Clone repo (private!)
git clone https://github.com/YOUR_ORG/clinical-genomics-private.git
cd clinical-genomics-private

# 2. Install dependencies
curl -LsSf https://astral.sh/uv/install.sh | sh
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# 3. Set up API keys
cp .env.example .env
# Edit .env with your API keys

# 4. Run tests locally
python scripts/run_tests.py --domain clinical_genomics --runs 3
```

### GitHub Actions Setup

**1. Add Secrets to GitHub Repo:**
- Go to Settings → Secrets and variables → Actions
- Add required secrets:
  - `OPENAI_API_KEY`
  - `ANTHROPIC_API_KEY`
  - `CLINVAR_API_KEY`
  - `ONCOKB_API_KEY`
  - `PHARMGKB_API_KEY`

**2. Push to Trigger CI:**
```bash
git add .
git commit -m "feat: Add clinical genomics tasks"
git push origin main
```

**3. Monitor Results:**
- Go to Actions tab in GitHub
- See Pass@1 and Pass@K metrics
- Download detailed reports

---

## Architecture

### Directory Structure
```
clinical-genomics-private/
├── domains/
│   └── clinical_genomics/
│       ├── config.yaml              # Domain configuration
│       ├── evaluators/
│       │   ├── __init__.py
│       │   └── functions.py         # Evaluation logic
│       └── tasks/
│           ├── variant_*.json       # Variant interpretation tasks
│           ├── treatment_*.json     # Treatment recommendation tasks
│           ├── trial_*.json         # Trial matching tasks
│           └── drug_*.json          # Drug-gene interaction tasks
├── scripts/
│   ├── run_tests.py                 # Main test runner
│   └── generate_report.py          # HTML report generator
├── .github/
│   └── workflows/
│       └── test.yml                 # GitHub Actions CI/CD
├── pyproject.toml                   # Python dependencies
└── README.md                        # This file
```

### Task Categories (60 Total)

1. **Variant Interpretation** (15 tasks)
   - ACMG/AMP classification
   - Conflicting evidence resolution
   - VUS analysis

2. **Treatment Recommendation** (15 tasks)
   - Targeted therapy matching
   - Combination therapy design
   - Resistance prediction

3. **Clinical Trial Matching** (10 tasks)
   - Eligibility screening
   - Multi-site coordination
   - Basket trial navigation

4. **Drug-Gene Interactions** (10 tasks)
   - CYP450 metabolizer status
   - Polypharmacy analysis
   - Adverse reaction prediction

5. **Evidence Synthesis** (5 tasks)
   - Literature review
   - Guideline compliance

6. **Cohort Analysis** (5 tasks)
   - Batch processing
   - Variant reclassification

---

## Testing Infrastructure

### GitHub Actions Workflow

**Triggers:**
- Push to `main` or `develop`
- Pull requests
- Manual dispatch (`workflow_dispatch`)

**Steps:**
1. **Validate** domain structure (config, tasks, evaluators)
2. **Run tests** on all tasks (3 runs per task)
3. **Calculate metrics** (Pass@1, Pass@3)
4. **Generate report** (HTML + JSON)
5. **Upload artifacts** (results, reports)
6. **Comment on PR** (if PR triggered)
7. **Fail if out of range** (Pass@1 < 30% or > 70%)

**Run Time:** ~1-2 hours for 60 tasks

### Metrics

- **Pass@1:** % of tasks passed on first attempt (target: 30-70%)
- **Pass@3:** % of tasks passed within 3 attempts (target: 50-85%)
- **Zero Score:** % of tasks with 0% success (should be <10%)

### Evaluation

Each task has custom evaluators in `domains/clinical_genomics/evaluators/functions.py`:

```python
@compare_func
def validate_variant_classification(question, llm_response, op_args):
    """Validate ACMG/AMP classification."""
    # Check pathogenicity tier
    # Validate evidence codes
    # Cross-reference ClinVar
    # Score confidence
    return {"passed": bool, "score": float, "feedback": str}
```

---

## API Keys Required

### Essential (Free/Academic Tiers)
- **OpenAI:** `OPENAI_API_KEY` (for agent)
- **ClinVar:** Free (NCBI E-utilities, no key needed)
- **PubMed:** Free (NCBI E-utilities, no key needed)
- **OncoKB:** `ONCOKB_API_KEY` (free academic)
- **PharmGKB:** `PHARMGKB_API_KEY` (free academic)
- **ClinicalTrials.gov:** Free (no key)

### Optional
- **Anthropic:** `ANTHROPIC_API_KEY` (for Claude)
- **SerpAPI:** `SERP_API_KEY` (for Google Search)

### Setup API Keys

**Local development:**
```bash
cp .env.example .env
# Edit .env:
OPENAI_API_KEY=sk-...
ONCOKB_API_KEY=...
PHARMGKB_API_KEY=...
```

**GitHub Actions:**
- Go to repo Settings → Secrets and variables → Actions
- Add each key as a repository secret

---

## Usage

### Run Tests Locally

```bash
# Activate venv
source .venv/bin/activate

# Run all tests
python scripts/run_tests.py --domain clinical_genomics --runs 3

# Run specific task
python scripts/run_tests.py --domain clinical_genomics --runs 1 --task variant_task_0001

# View results
cat results/summary.json
open results/test-report.html
```

### Run Tests on GitHub

**Option 1: Push to trigger**
```bash
git add domains/clinical_genomics/tasks/new_task.json
git commit -m "feat: Add new variant interpretation task"
git push origin main
# Check Actions tab for results
```

**Option 2: Manual trigger**
- Go to Actions tab
- Select "Clinical Genomics Domain Testing"
- Click "Run workflow"
- Fill in inputs (domain, runs)
- Click "Run workflow"

### Create New Task

1. **Create task JSON:**
```json
{
  "category": "variant_interpretation",
  "question": "Classify BRCA1 c.5266dupC variant...",
  "output_format": {
    "pathogenicity": "[tier]",
    "evidence_codes": ["[codes]"],
    "confidence": "[0-1]"
  },
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

2. **Add to config.yaml:**
```yaml
tasks:
  - tasks/variant_task_0001.json
  # Add your new task here
```

3. **Test locally:**
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

### Phase 1: Testing Infrastructure (Current)
- ✅ GitHub Actions CI/CD
- ✅ Pass@K evaluation
- ✅ Automated reporting

### Phase 2: Domain Expansion (Weeks 1-4)
- 🔄 60 clinical genomics tasks
- 🔄 ACMG/AMP compliance evaluators
- 🔄 Multi-source data integration

### Phase 3: Product Development (Months 2-3)
- 📋 Web UI for clinicians
- 📋 Batch patient processing
- 📋 Report generation (PDF)
- 📋 Clinical trial enrollment automation

### Phase 4: Clinical Validation (Months 4-6)
- 📋 Partner with cancer center
- 📋 Real-world patient validation
- 📋 Publication in medical journal

### Phase 5: Commercialization (Months 6-12)
- 📋 SaaS product launch
- 📋 First paying customers
- 📋 Pharma partnerships

---

## Related Resources

- **[Clinical Genomics Doctrine](../.cursor/rules/clinical-genomics-domain-doctrine.mdc)** - Strategic plan
- **[Grant Application Domain](https://github.com/Alignerr-Code-Labeling/lbx_mcp_universe_template)** - Reference implementation (public)

---

**Owner:** Alpha (Fahad)  
**Status:** 🔒 Private Development  
**License:** Proprietary (NOT open source)


# Clinical Genomics - Agent Assignment Tracker

**Mission:** Build both LBX Benchmark + SaaS Product in parallel  
**Timeline:** 4 weeks  
**Coordination:** This file tracks who's working on what

---

## 🎯 **ACTIVE ASSIGNMENTS**

### **Agent 1: Zo (Current) - Infrastructure Lead**
**Status:** IN PROGRESS  
**Track:** API Integration & MCP Servers  
**Current Task:** Build ClinVar API client

**Handoff Instructions:**
```bash
cd /Users/fahadkiani/Desktop/development/clinical-genomics-private/infrastructure/api_clients
# Start with clinvar.py
# Reference: https://www.ncbi.nlm.nih.gov/clinvar/docs/maintenance_use/
# API key already provisioned
```

**Context Files to Read:**
- `MULTI_AGENT_BUILD_PLAN.md` (full strategy)
- `.cursor/rules/clinical-genomics-domain-doctrine.mdc` (domain knowledge)
- `/lbx_mcp_universe_mcp_servers_mothership/servers/` (reference MCP implementations)

---

### **Agent 2: TBD - Task Design Lead**
**Status:** AWAITING ASSIGNMENT  
**Track:** Benchmark Tasks & Evaluators  
**First Task:** Create variant interpretation tasks 001-005

**Handoff Instructions:**
```bash
cd /Users/fahadkiani/Desktop/development/clinical-genomics-private/domains/clinical_genomics/tasks
# Start with variant_interpretation_task_001.json
# Follow the pattern from grant_application domain
# Use ACMG/AMP guidelines for ground truth
```

**Context Files to Read:**
- `MULTI_AGENT_BUILD_PLAN.md` (task requirements)
- `.cursor/rules/clinical-genomics-domain-doctrine.mdc` (60-task breakdown)
- `/lbx_mcp_universe_template-main/domains/grant_application/tasks/` (reference implementation)
- `/lbx_mcp_universe_template-main/domains/grant_application/evaluators/functions.py` (evaluator patterns)

**Ground Truth Sources:**
- ClinVar: https://www.ncbi.nlm.nih.gov/clinvar/
- ACMG/AMP Guidelines: https://www.acmg.net/ACMG/Medical-Genetics-Practice-Resources/Practice-Guidelines.aspx
- OncoKB: https://www.oncokb.org/

---

### **Agent 3: TBD - Backend Lead**
**Status:** AWAITING ASSIGNMENT  
**Track:** SaaS Backend & Production API  
**First Task:** FastAPI setup + PostgreSQL schema

**Handoff Instructions:**
```bash
cd /Users/fahadkiani/Desktop/development/clinical-genomics-private/backend
# Set up FastAPI project structure
# Design PostgreSQL schema for variants, patients, analyses
# Reference grant_application production architecture
```

**Context Files to Read:**
- `MULTI_AGENT_BUILD_PLAN.md` (backend requirements)
- `.cursor/rules/grant-application-production-architecture.mdc` (reference SaaS architecture)
- `/lbx_mcp_universe_template-main/domains/grant_application/` (pattern to follow)

**Tech Stack:**
- FastAPI (Python 3.11+)
- PostgreSQL (for relational data)
- Redis (for caching and queues)
- Celery (for background jobs)
- Stripe (for billing)

---

### **Agent 4: TBD - Frontend Lead**
**Status:** AWAITING ASSIGNMENT  
**Track:** Web App & User Experience  
**First Task:** Next.js setup + authentication flow

**Handoff Instructions:**
```bash
cd /Users/fahadkiani/Desktop/development/clinical-genomics-private/frontend
npx create-next-app@latest . --typescript --tailwind --app
# Set up Auth0 or Clerk for authentication
# Build dashboard layout
```

**Context Files to Read:**
- `MULTI_AGENT_BUILD_PLAN.md` (frontend requirements)
- `.cursor/rules/grant-application-production-architecture.mdc` (UI/UX patterns)

**Tech Stack:**
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS + shadcn/ui
- Auth0/Clerk (authentication)
- React Query (data fetching)

---

### **Agent 5: TBD - DevOps Lead**
**Status:** AWAITING ASSIGNMENT  
**Track:** Infrastructure & Compliance  
**First Task:** GitHub Actions CI/CD + Docker

**Handoff Instructions:**
```bash
cd /Users/fahadkiani/Desktop/development/clinical-genomics-private
# Set up .github/workflows/deploy.yml
# Create Dockerfile for backend
# Set up HIPAA compliance checklist
```

**Context Files to Read:**
- `MULTI_AGENT_BUILD_PLAN.md` (DevOps requirements)
- `.github/workflows/test.yml` (existing CI/CD)

**Tech Stack:**
- GitHub Actions (CI/CD)
- Docker + Docker Compose
- AWS/GCP (cloud deployment)
- Terraform (infrastructure as code)
- Datadog/Sentry (monitoring)

---

## 📊 **PROGRESS TRACKING**

### **Week 1 Milestones (Due: Day 7)**
- [ ] Agent 1: 6 MCP servers integrated and tested
- [ ] Agent 2: 15 tasks created with evaluators
- [ ] Agent 3: Database schema + API skeleton
- [ ] Agent 4: Authentication + basic dashboard
- [ ] Agent 5: CI/CD pipeline + Docker setup

**Checkpoint:** Friday EOD - All agents sync progress

---

### **Week 2 Milestones (Due: Day 14)**
- [ ] Agent 1: Caching + batch processing live
- [ ] Agent 2: 30 tasks total (15 new)
- [ ] Agent 3: Billing + multi-tenant setup
- [ ] Agent 4: Variant analysis + treatment dashboards
- [ ] Agent 5: HIPAA compliance infrastructure

**Checkpoint:** Friday EOD - SaaS alpha demo

---

### **Week 3 Milestones (Due: Day 21)**
- [ ] Agent 1: API monitoring + versioning
- [ ] Agent 2: 60 tasks total (30 edge cases)
- [ ] Agent 3: Real-time pipeline + EHR webhooks
- [ ] Agent 4: Cohort analysis + report generation
- [ ] Agent 5: Full documentation + security audit

**Checkpoint:** Friday EOD - SaaS beta with pilot customers

---

### **Week 4 Milestones (Due: Day 28)**
- [ ] Agent 1: Production API optimization
- [ ] Agent 2: Benchmark documentation + PR submission
- [ ] Agent 3: Load testing + performance tuning
- [ ] Agent 4: Admin dashboard + onboarding flow
- [ ] Agent 5: Production deployment + monitoring

**Final Deliverable:** LBX PR submitted + SaaS launched

---

## 🔄 **HANDOFF PROTOCOL**

When switching agents or pausing work:

1. **Update this file** with your current status
2. **Commit your changes** to a feature branch
3. **Document blockers** in BLOCKERS section below
4. **Tag next agent** with `@agent-name` in commit message
5. **Update TODO items** in project tracker

---

## 🚨 **CURRENT BLOCKERS**

### **Agent 1 Blockers:**
- None (just starting)

### **Agent 2 Blockers:**
- Awaiting Agent 1 to complete ClinVar API (for testing tasks)

### **Agent 3 Blockers:**
- None (can start independently)

### **Agent 4 Blockers:**
- Awaiting Agent 3 to define API endpoints (for frontend integration)

### **Agent 5 Blockers:**
- None (can start with CI/CD setup)

---

## 📝 **DAILY STANDUP LOG**

### **Day 1 (Today):**
**Agent 1 (Zo):**
- ✅ Created MULTI_AGENT_BUILD_PLAN.md
- ✅ Created directory structure
- ✅ Set up TODO tracking
- 🔄 Starting ClinVar API client

**Agent 2:**
- Awaiting assignment

**Agent 3:**
- Awaiting assignment

**Agent 4:**
- Awaiting assignment

**Agent 5:**
- Awaiting assignment

---

## 🎯 **NEXT ACTIONS (IMMEDIATE)**

**Commander Alpha:**
1. Review MULTI_AGENT_BUILD_PLAN.md
2. Assign Agents 2-5 to their tracks
3. Provision API keys (ClinVar, OncoKB, etc.)
4. Approve Zo to proceed with Agent 1 track

**Agent 1 (Zo):**
- Build ClinVar API client (`infrastructure/api_clients/clinvar.py`)
- Test with sample variants (BRCA1 c.5266dupC)
- Document API usage patterns

**Waiting for assignment:**
- Agent 2 (Task Design)
- Agent 3 (Backend)
- Agent 4 (Frontend)
- Agent 5 (DevOps)

---

**Ready to execute. Awaiting Commander's orders.** 🚀


# ProcureAI — AI-Powered Vendor Selection & Procurement Intelligence Platform

## Executive Summary
ProcureAI is an AI-enabled vendor-selection decision-support prototype combining deterministic weighted scoring, data validation, what-if analysis, risk visibility and Gemini explanations.

## Professor Use Case
Use Case 6 — Vendor Selection / Procurement Recommender: cost, quality and lead time scoring; adjustable weights; ranked shortlist; rationale; AI-enabled decision support.

## Business Problem & Objectives
Procurement comparison is often spreadsheet-heavy and subjective. ProcureAI structures the decision and makes trade-offs visible.

## Dataset
10-vendor demo, 250-vendor scale dataset and invalid test dataset. All are synthetic.

## Scoring
Default weights: Cost 25%, Quality 25%, Lead Time 15%, On-Time Delivery 15%, Defect Rate 10%, Sustainability 10%. Higher/lower criteria are normalized before weighted aggregation. Recommendation bands: 80+ Highly Recommended, 65–79.99 Recommended, 50–64.99 Conditional, below 50 Not Recommended. Risk is calculated separately.

## AI
Gemini is an explanation layer only. The deterministic engine remains authoritative. AI receives structured analytics and is prohibited from inventing data or changing ranking. If Gemini is unavailable, deterministic analytics continue.

## What-If
Cost Optimization, Quality First, Speed First, Risk Reduction, Sustainability First and Balanced Procurement scenarios recalculate rankings.

## Validation
The project detects missing values, duplicate IDs, invalid numeric types, negative values and out-of-range percentages/scores.

## Actual Demo Results
Baseline top vendor: **Supplier 008**, score **81.48**, rank **1**, recommendation **Highly Recommended**, risk **Low**.
Second vendor: **Supplier 003**, score **59.58**.
Quality First winner: **Supplier 008**. Cost Optimization winner: **Supplier 008**.

## SWOT
Strengths: transparent scoring, adjustable weights, scenarios, risk visibility, AI explanation.
Weaknesses: synthetic data, prototype storage, no enterprise authentication.
Opportunities: ERP integration, supplier-document RAG, historical performance analytics.
Threats: incumbent procurement suites, data quality, governance and integration complexity.

## Competitors
SAP Ariba and Coupa are enterprise procurement platforms. ProcureAI is a focused prototype and does not claim equivalent enterprise functionality.

## Business Model
SaaS, per-user pricing, enterprise licensing, premium analytics and API/ERP integrations.

## Business Impact
Potential benefits include faster comparison, consistent evaluation, risk visibility and rapid sensitivity analysis. Monetary impact must be treated as illustrative, not guaranteed.

## Scalability
CSV → SQL → cloud/data warehouse → ERP/procurement APIs. Future production requires authentication, RBAC, monitoring, logging, caching, data pipelines and AI cost controls.

## RAG vs Fine-Tuning
RAG can later retrieve procurement policies, contracts, certifications and supplier records. Fine-tuning is not required for the prototype because current inputs are structured and changing.

## Responsible AI
Human oversight is mandatory. ProcureAI does not independently approve, reject, contract with or purchase from vendors. Synthetic data is disclosed and API secrets are protected.

## Limitations
Results depend on data quality and chosen weights; normalization is relative to the vendor set; synthetic data cannot establish real supplier performance.

## Future Roadmap
SQL/cloud storage, ERP integration, supplier-document RAG, authentication/RBAC, historical supplier performance and enterprise monitoring.

## Conclusion
ProcureAI demonstrates how AI can augment a multi-criteria business decision while keeping mathematical ranking transparent and human-controlled.

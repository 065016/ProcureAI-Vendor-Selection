# Viva Questions
1. Why this use case? Multi-criteria vendor selection is a high-value decision-support problem.
2. Why deterministic scoring? Reproducibility and auditability.
3. Why normalization? Criteria use different units.
4. Why Gemini? Natural-language explanation over structured results.
5. Can Gemini change ranking? No.
6. What if weights do not total 100%? Scoring is blocked.
7. What if a criterion has identical values? Neutral normalization avoids division by zero.
8. What if Gemini fails? Core analytics continue.
9. Why not fine-tuning? Current need is reasoning over changing structured data.
10. Where can RAG help? Policies, contracts, certifications and supplier documents.
11. Main limitation? Synthetic data is not real supplier evidence.
12. How is bias controlled? Transparent weights, validation, scenario analysis and human review.
13. How does what-if work? Reapply alternative weights and recompute.
14. Why separate risk? High performance does not mean low exposure.
15. How can it scale? Move storage to SQL/cloud and expose APIs.
16. How is the API key secured? Environment/Streamlit Secrets.
17. What is responsible AI? Human oversight and no autonomous purchasing.
18. What is the business model? SaaS, per-user, enterprise, premium analytics and integrations.
19. What are competitors? Enterprise procurement suites such as SAP Ariba and Coupa.
20. Who has final authority? The procurement manager/organization.

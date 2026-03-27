# GDPR Documentation & DPIA Summary

**System:** Maison Beauté AI Advisor  
**Version:** 1.0  

> Full documentation in PROJECT_DOCUMENTATION.md — Section 6.

## Data Processors

| Processor | Service | Transfer | Safeguard |
|---|---|---|---|
| Anthropic (via API) | LLM inference | USA | SCCs + DPA signed |
| LangSmith (LangChain) | Observability | USA | SCCs + anonymised traces |
| Brevo | Email delivery | EU (FR) | GDPR-native |
| n8n Cloud | Orchestration | EU (DE) | GDPR-native |

## DPIA — Allergy/Safety Data (Module 2)

**Legal basis:** Art. 6(1)(d) vital interests + Art. 9(2)(c) health data  
**Conclusion:** Processing may proceed. Residual risks acceptable.

### Key mitigations
- Keyword scan runs **before** any LLM call — flagged messages never reach Anthropic
- Retained in Slack max 7 days, then purged automatically
- No PII in Tableau export

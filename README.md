# AI Architect Use Cases
Use-Case Interview Questions for an AI Architect
These are scenario-style questions, grouped by use case, with the key points a strong answer should cover.
1. Enterprise Knowledge Assistant (RAG)
Design an internal assistant that answers employee questions across 50,000 policy documents. Walk through the architecture.
How do you choose a chunking strategy for PDFs, tables and slide decks?
Answers are fluent but sometimes wrong. How do you diagnose retrieval vs. generation failures?
How do you enforce document-level access control so users never see content they aren’t entitled to?
When would you pick hybrid search plus reranking over pure vector search?
How do you keep the index fresh when documents change daily?
Strong answers cover: ingestion pipeline, embeddings, hybrid retrieval, reranking, citations, permission filtering at query time, re-indexing strategy.
2. Customer Support Chatbot
Design a support bot handling 100k conversations a day. What are the components?
How do you decide when to escalate to a human agent?
How do you manage conversation memory across long sessions without blowing up token cost?
How do you prevent the bot from making commitments it shouldn’t (refunds, legal promises)?
How do you handle multilingual customers?
Strong answers cover: intent routing, guardrails, system prompt design, context summarization, handoff triggers, prompt caching.
3. Document Processing and Summarization Pipeline
A bank receives 20,000 loan documents daily. Design an extraction and summarization pipeline.
How do you guarantee structured JSON output that downstream systems can trust?
How do you process documents larger than the context window?
How do you balance batch vs. real-time processing for cost?
How do you handle low-confidence extractions?
Strong answers cover: schema validation, tool use or structured outputs, map-reduce summarization, batch APIs, confidence thresholds, human-in-the-loop review.
4. Agentic Workflows
Design an agent that handles IT service requests end to end (password resets, access requests, provisioning).
Single agent vs. multi-agent: how do you decide?
How do you prevent runaway loops or unintended actions?
Which actions need human approval, and how do you design that checkpoint?
How do you design tools (names, schemas, error messages) so the model uses them reliably?
How do you integrate external systems using MCP?
Strong answers cover: tool design, least-privilege permissions, step limits, idempotency, audit logs, approval gates, state management.
5. Classification and Routing at Scale
Design a system that classifies and routes 1 million emails a day.
When do you use an LLM vs. a classical ML model?
How do you cut cost while keeping accuracy (model tiering, cascades)?
How do you handle label drift over time?
Strong answers cover: small model first with fallback to larger, caching, batch processing, confidence scores, sampling for review.
6. Banking / Regulated Industry Use Case
Design an AI assistant for relationship managers that works with customer financial data.
How do you handle PII and data residency requirements?
How do you make AI decisions explainable and auditable for regulators?
How do you design a fraud-alert triage assistant while keeping a human accountable?
What is your model risk management approach?
Strong answers cover: PII redaction, private networking and cloud-provider hosting options, full prompt/response logging, human accountability, approval workflows, retention policies.
7. Code and Developer Productivity Assistant
Design an AI coding assistant for a 2,000-developer organization.
How do you give it context about a large monorepo?
How do you prevent secrets or proprietary code from leaking?
How do you measure productivity impact beyond “lines generated”?
8. Platform and Multi-Team Adoption
Ten teams want to use Claude. Design a shared AI platform (gateway) for them.
How do you implement rate limiting, quotas and chargeback per team?
How do you version and manage prompts across environments?
How do you handle model upgrades without breaking production apps?
Build vs. buy: when do you use managed services (Bedrock, Vertex AI, direct API) vs. self-hosting?
Strong answers cover: central gateway, key management, usage tracking, prompt registry, model abstraction layer, regression evaluation before upgrades.
9. Evaluation and Quality
How do you evaluate an LLM application before launch?
How do you build a golden dataset, and who labels it?
When is LLM-as-judge reliable, and when isn’t it?
How do you detect quality regressions in production?
How do you run A/B tests on prompts or models?
10. Cost, Latency and Reliability
Your monthly LLM bill tripled. How do you investigate and reduce it?
Explain prompt caching, batching, model tiering and output-length control.
How do you handle rate limits (429s) and API outages?
How do you reduce time-to-first-token for a chat UI?
What is your fallback strategy across models or providers?
11. Security and Governance
How do you defend against prompt injection, especially in agents that read external content?
What is your data-handling policy for sensitive inputs?
How do you set up an AI governance or review process for new use cases?
How do you handle hallucination risk in high-stakes outputs?
What belongs in an AI acceptable-use policy?
12. Strategy and Leadership
How do you prioritize which AI use cases to build first?
How do you calculate ROI for an AI project?
How do you move from pilot to production, and why do most pilots stall?
How do you get non-technical stakeholders to trust and adopt the system?
Describe an AI project you’d refuse to build, and why.
Answer Framework (works for any design question)
Clarify: users, scale, latency, data sensitivity, success metrics
Architecture: components and data flow
Model choice: why this model tier, and the fallbacks
Quality: evaluation and guardrails
Risk: security, privacy, failure modes
Operations: monitoring, cost, rollout
If you tell me the target role (for example banking, SaaS or consulting), I can turn any section into full model answers or run a mock interview one question at a time.
Please print solution and coding soluton . and guide me step b y step (1.1) from project ceation in bvs code for
1. Enterprise Knowledge Assistant (RAG)
   1.1 Design an internal assistant that answers employee questions across 50,000 policy documents. W

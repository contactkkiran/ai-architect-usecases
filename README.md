# AI Architect Use Cases

Scenario-based interview questions for AI architects, organized by use case. Each
scenario includes key topics a strong answer should address.

## 1. Enterprise Knowledge Assistant (RAG)

**Scenario:** Design an internal assistant that answers employee questions across
50,000 policy documents. Walk through the architecture.

- How do you choose a chunking strategy for PDFs, tables, and slide decks?
- Answers are fluent but sometimes wrong. How do you diagnose retrieval versus
  generation failures?
- How do you enforce document-level access control so users never see content
  they are not entitled to?
- When would you choose hybrid search with reranking over pure vector search?
- How do you keep the index fresh when documents change daily?

**Strong answers cover:** Ingestion pipeline, embeddings, hybrid retrieval,
reranking, citations, permission filtering at query time, and re-indexing strategy.

## 2. Customer Support Chatbot

**Scenario:** Design a support bot handling 100,000 conversations a day. What are
the components?

- How do you decide when to escalate to a human agent?
- How do you manage conversation memory across long sessions without excessive
  token costs?
- How do you prevent the bot from making commitments it should not make, such as
  refund decisions or legal promises?
- How do you handle multilingual customers?

**Strong answers cover:** Intent routing, guardrails, system prompt design,
context summarization, handoff triggers, and prompt caching.

## 3. Document Processing and Summarization Pipeline

**Scenario:** A bank receives 20,000 loan documents daily. Design an extraction
and summarization pipeline.

- How do you guarantee structured JSON output that downstream systems can trust?
- How do you process documents larger than the context window?
- How do you balance batch versus real-time processing for cost?
- How do you handle low-confidence extractions?

**Strong answers cover:** Schema validation, tool use or structured outputs,
map-reduce summarization, batch APIs, confidence thresholds, and human-in-the-loop
review.

## 4. Agentic Workflows

**Scenario:** Design an agent that handles IT service requests end to end,
including password resets, access requests, and provisioning.

- Single agent versus multi-agent: how do you decide?
- How do you prevent runaway loops or unintended actions?
- Which actions need human approval, and how do you design that checkpoint?
- How do you design tools (names, schemas, and error messages) so the model uses
  them reliably?
- How do you integrate external systems using MCP?

**Strong answers cover:** Tool design, least-privilege permissions, step limits,
idempotency, audit logs, approval gates, and state management.

## 5. Classification and Routing at Scale

**Scenario:** Design a system that classifies and routes 1 million emails a day.

- When do you use an LLM versus a classical ML model?
- How do you reduce cost while keeping accuracy (model tiering, cascades)?
- How do you handle label drift over time?

**Strong answers cover:** Small model first with fallback to a larger model,
caching, batch processing, confidence scores, and sampling for review.

## 6. Banking and Regulated Industries

**Scenario:** Design an AI assistant for relationship managers that works with
customer financial data.

- How do you handle PII and data residency requirements?
- How do you make AI decisions explainable and auditable for regulators?
- How do you design a fraud-alert triage assistant while keeping a human
  accountable?
- What is your model risk management approach?

**Strong answers cover:** PII redaction, private networking and cloud-provider
hosting options, full prompt and response logging, human accountability, approval
workflows, and retention policies.

## 7. Code and Developer Productivity Assistant

**Scenario:** Design an AI coding assistant for an organization with 2,000
developers.

- How do you give it context about a large monorepo?
- How do you prevent secrets or proprietary code from leaking?
- How do you measure productivity impact beyond “lines generated”?

## 8. Platform and Multi-Team Adoption

**Scenario:** Ten teams want to use Claude. Design a shared AI platform (gateway)
for them.

- How do you implement rate limiting, quotas, and chargeback per team?
- How do you version and manage prompts across environments?
- How do you handle model upgrades without breaking production applications?
- Build versus buy: when do you use managed services (Bedrock, Vertex AI, or a
  direct API) versus self-hosting?

**Strong answers cover:** Central gateway, key management, usage tracking, prompt
registry, model abstraction layer, and regression evaluation before upgrades.

## 9. Evaluation and Quality

- How do you evaluate an LLM application before launch?
- How do you build a golden dataset, and who labels it?
- When is LLM-as-judge reliable, and when is it not?
- How do you detect quality regressions in production?
- How do you run A/B tests on prompts or models?

## 10. Cost, Latency, and Reliability

**Scenario:** Your monthly LLM bill tripled. How do you investigate and reduce it?

- Explain prompt caching, batching, model tiering, and output-length control.
- How do you handle rate limits (429s) and API outages?
- How do you reduce time to first token for a chat UI?
- What is your fallback strategy across models or providers?

## 11. Security and Governance

- How do you defend against prompt injection, especially in agents that read
  external content?
- What is your data-handling policy for sensitive inputs?
- How do you set up an AI governance or review process for new use cases?
- How do you handle hallucination risk in high-stakes outputs?
- What belongs in an AI acceptable-use policy?

## 12. Strategy and Leadership

- How do you prioritize which AI use cases to build first?
- How do you calculate ROI for an AI project?
- How do you move from pilot to production, and why do most pilots stall?
- How do you get non-technical stakeholders to trust and adopt the system?
- Describe an AI project you would refuse to build, and why.

## Answer Framework

Use this framework for any system-design question:

1. **Clarify:** Users, scale, latency, data sensitivity, and success metrics.
2. **Architecture:** Components and data flow.
3. **Model choice:** Why this model tier, and what the fallbacks are.
4. **Quality:** Evaluation and guardrails.
5. **Risk:** Security, privacy, and failure modes.
6. **Operations:** Monitoring, cost, and rollout.

## Want a Guided Walkthrough?

Choose a target role or industry (for example, banking, SaaS, or consulting) to
get tailored model answers or practice with a mock interview. You can also request
a complete solution and coding walkthrough in VS Code, starting from project
creation, for **Use Case 1.1: Design an internal assistant that answers employee
questions across 50,000 policy documents.**

# Interview Notes: Permission-Aware Hybrid RAG

Questions I can answer from hands-on work in this project. Each topic is filled in only after I have built it, so every answer is backed by something I actually ran.

**How to read this file:** Done topics have answers. Planned topics are listed so the gaps are visible, and get answers when the step is finished.

| Topic | Status |
|---|---|
| 1. Working with the Claude API | Done |
| 2. Secrets and repository hygiene | Done |
| 3. PDF parsing: text, tables, headers and footers | Done |
| 4. Scanned documents and OCR | Done |
| 5. Routing pages per document | Done |
| 6. Permission model | Designed (filtering code planned) |
| 7. Chunking | Planned |
| 8. Embeddings and vector store | Planned |
| 9. Semantic search and permission filtering in code | Planned |
| 10. Answers with citations | Planned |
| 11. Hybrid search and reranking | Planned |
| 12. Incremental re-indexing | Planned |
| 13. Evaluation | Planned |

---

## 1. Working with the Claude API

**Q: What does a Claude API response look like, and what should your code do with it?**
The response contains a list of content blocks, not a single string. Depending on the model, the first block may be a thinking block, which has no `text` attribute, followed by the text block with the answer. My code collects only the blocks whose type is `text` and joins them. Reading `content[0].text` directly can fail.

**Q: How do you measure the cost of a call?**
Every response reports input and output token counts. Cost is tokens times the model's price, so I log both per request and use them for budgets, chargeback per team and spotting runaway prompts.

**Hands-on proof:** `src/first_call.py`

## 2. Secrets and repository hygiene

**Q: How do you keep API keys out of source control?**
The key lives in a `.env` file that is listed in `.gitignore`, and code loads it at runtime. Before every commit I check that `.env` and the virtual environment do not appear in `git status`. In production I would use a secrets manager with per-service keys, rotation and no keys on developer laptops. If a key leaks, I revoke it and create a new one.

**Q: Why use a virtual environment per project?**
It isolates dependencies, so projects do not break each other, and `requirements.txt` makes the setup reproducible. I also learned to run `python -m pip` so packages install into the same Python that runs the code.

## 3. PDF parsing: text, tables, headers and footers

**Q: Why does plain text extraction hurt RAG on policy documents?**
Three things go wrong. Running headers and footers get mixed into the body. Table structure is lost, so a number such as "220 USD" no longer sits next to its column label. Cells can also be split across lines, which separates a row label from its values. Retrieval then returns chunks that look relevant but cannot answer the question.

**Q: How do you handle tables?**
I extract tables with a layout-aware parser, separately from the surrounding text, and turn each row into a self-contained sentence such as "City tier = Tier 1; Hotel (per night) = 220 USD". Each value keeps its label, and the table text is not duplicated in the body text.

**Q: How do you remove headers and footers?**
I crop them by page position before extraction. The crop sizes are tuned per document family, so for real collections I would calibrate them per template, or detect repeated lines across pages.

**Q: Why not just send the PDF to a model?**
It is an option, and I would compare it. The trade-offs are cost, latency and the risk of the model misreading a number, so the output needs validation. For large volumes, a deterministic parser for typed pages is cheaper and more predictable.

**Hands-on proof:** `src/extract_pdf.py`, `src/parse_pdf.py`

## 4. Scanned documents and OCR

**Q: How do you know a PDF needs OCR?**
I check for a text layer. A scanned or image-only page has no fonts and no extractable characters, so a text extractor returns nothing. I hit this with a 100-page, 38 MB file in which every page was a single image.

**Q: What are the downsides of OCR?**
It is slow, it misreads characters, and it loses table structure and layout. In regulated settings I would store a confidence score per page and send low-confidence pages to human review.

**Q: How would you process 50,000 scanned documents?**
As a batch pipeline, never at query time: process pages one at a time to limit memory, run workers in parallel, cache results by content hash so each file is OCR'd once, and re-process only changed files. Use a queue with retries, and track failures and low-confidence pages.

**Q: Which OCR options would you compare?**
Open-source OCR runs locally, is free and keeps data in my network, but is weaker on tables and poor scans. Cloud document services are stronger on tables and forms and return confidence scores, but cost money and send data out, which matters for data residency. A multimodal model understands layout in context, but costs more and can hallucinate, so its output needs validation.

**Hands-on proof:** `src/ocr_pdf.py`

## 5. Routing pages per document

**Q: How do you design ingestion for a mix of typed and scanned documents?**
I decide per page, not per file, because one PDF can contain both. Each page is checked for a text layer, and then goes to the text parser or to OCR. Both routes return the same element format (type, page, content), so the chunking step does not depend on how the text was obtained.

**Q: Why decide before processing instead of always running OCR?**
OCR on a typed page is slower and less accurate than reading its real text, so checking first saves time and cost and preserves exact text.

**Hands-on proof:** `src/ingest_pdf.py`

## 6. Permission model

**Q: How do you stop users from seeing documents they are not entitled to?**
Each document carries allowed groups, and each chunk inherits them as metadata. At query time I resolve the user's groups and apply them as a filter inside the search, so restricted chunks are never retrieved and never reach the model.

**Q: Why not filter the answer afterwards, or tell the model to ignore restricted content?**
A prompt instruction is not a security control, and post-filtering risks leaking restricted text in the generated answer. Content that is never retrieved cannot be quoted, summarized or hinted at.

**Q: What are the hard parts in production?**
Resolving groups from the identity provider, propagating permission changes to the index quickly so revoked users lose access, and logging access for audit.

**Status:** designed, with a sample restricted document (salary bands, HR team only). The filtering code is planned.

---

## Planned topics

Answers are added when each step is finished. Questions to cover:

- **7. Chunking:** how to choose chunk size and overlap; why split on headings; how to keep tables whole; what metadata each chunk carries
- **8. Embeddings and vector store:** how to choose an embedding model; what a vector database stores; cost at 50,000 documents
- **9. Search and permission filtering in code:** metadata filters; testing that two users get different results for the same question
- **10. Answers with citations:** grounding prompts; the "not found" behavior; citation format; reducing hallucination
- **11. Hybrid search and reranking:** why vector plus keyword; what a reranker adds; latency trade-offs
- **12. Incremental re-indexing:** content hashes; deleting superseded versions; keeping the index fresh
- **13. Evaluation:** a golden question set; measuring retrieval separately from answer quality; regression checks before model upgrades

## How to update this file

When a step is finished:

1. Change its status in the table at the top to Done.
2. Move its questions from "Planned topics" into a numbered section.
3. Write each answer in my own words, and note the exact numbers or behavior I saw while building it.
4. Add the file or script as hands-on proof.


Use Cce 

# 🟦 Enterprise Knowledge Assistant (RAG)

## Architecture, Build Roadmap & Interview Notes

> **Architecture:** Permission-aware hybrid Retrieval-Augmented Generation (RAG) with reranking.
> **Goal:** Answer employee questions across **50,000 policy documents**, with permission filtering and source citations.

> **Colour support:** Coloured icons work across Markdown viewers. Custom heading colours appear in viewers that support inline HTML styles; viewers such as GitHub may remove those styles.

## Contents

1. [🟦 Solution Architecture](#1-solution-architecture)
2. [🟩 Build Roadmap](#2-build-roadmap)
3. [🟨 Step 1: Project Setup in VS Code](#3-step-1-project-setup-in-vs-code)
4. [🟪 Architecture Name & Terminology](#4-architecture-name--terminology)
5. [🟧 First-Person Interview Script](#5-first-person-interview-script)
6. [🟥 Delivery Tips & Next Steps](#6-delivery-tips--next-steps)

---

<a id="1-solution-architecture"></a>

## 🟦 <span style="color: #2563eb;">1. Solution Architecture</span>

### Ingestion Pipeline — Offline

Runs nightly or on document-change events.

```text
Policy documents (50,000)
    │
    ▼
Parse PDF/DOCX — preserve tables
    │
    ▼
Chunk + metadata — ACL, version
    │
    ▼
Embed — embedding model
    │
    ▼
Vector database + keyword index (BM25)
```

### Query Pipeline — Online

Runs for each employee question.

```text
Employee question
    │
    ▼
Authenticate — identify the user
    │
    ▼
Query rewrite
    │
    ▼
Hybrid search — vector + keyword
    │           filtered by the user's permissions
    ▼
Rerank — top 50 → top 5
    │
    ▼
Claude — answer + citations
    │
    ▼
Guardrails
    │
    ▼
Answer with source links
    │
    ▼
Logging
```

### Architecture Decisions

| Component | Decision | Why |
| :--- | :--- | :--- |
| **Parsing** | Use a layout-aware parser; keep tables intact. | Policies contain tables and numbered clauses. |
| **Chunking** | Split by headings and sections into approximately 500-token chunks, with 10–15% overlap. Keep the heading path in each chunk. | Preserves meaning and enables precise citations. |
| **Metadata** | Store `doc_id`, `title`, `version`, `effective_date`, `department`, and `allowed_groups`. | Enables permission filtering and freshness. |
| **Retrieval** | Combine vector search with BM25, then rerank. | Policy text contains exact terms, clause numbers, and acronyms that vector search can miss. |
| **Access control** | Filter on `allowed_groups` inside the search query, not after generation. | Users must never see content they are not entitled to access. |
| **Generation** | Instruct Claude to answer only from the provided context, cite sources, and say “not found” otherwise. | Reduces hallucination. |
| **Freshness** | Re-index only changed documents using a content hash or last-modified check; delete superseded versions. | Keeps daily updates economical at 50,000 documents. |
| **Evaluation** | Use a golden question set; measure retrieval hit rate and answer faithfulness separately. | Distinguishes retrieval failures from generation failures. |

---

<a id="2-build-roadmap"></a>

## 🟩 <span style="color: #15803d;">2. Build Roadmap</span>

Build a working version that scales conceptually to **50,000 documents**, using a local vector database so the planned API expense is Claude API calls.

| Step | Concept | Verification |
| ---: | :--- | :--- |
| **1** | Project and virtual environment in VS Code | Python runs from the virtual environment. |
| **2** | Store the API key safely; make the first Claude call | Claude replies in the terminal. |
| **3** | Create sample policy documents | Files are listed. |
| **4** | Load and chunk documents | Chunk count is printed. |
| **5** | Generate embeddings | Vector length is printed. |
| **6** | Store embeddings in ChromaDB with metadata | Collection count is printed. |
| **7** | Implement semantic search | Top results are printed. |
| **8** | Apply permission filtering | The same query produces different results for two users. |
| **9** | Generate an answer with Claude and citations | A cited answer is printed. |
| **10** | Add hybrid search and reranking | Results are compared. |
| **11** | Add incremental re-indexing | Only changed files are reprocessed. |
| **12** | Create an evaluation script | Retrieval hit-rate score is reported. |

---

<a id="3-step-1-project-setup-in-vs-code"></a>

## 🟨 <span style="color: #a16207;">3. Step 1: Project Setup in VS Code</span>

### 1a. Create the Project Folder

Open a terminal — Command Prompt, PowerShell, or macOS/Linux Terminal — and run:

```bash
mkdir policy-assistant
cd policy-assistant
code .
```

> **Tip:** If `code .` is not recognised, open VS Code manually and choose **File → Open Folder → policy-assistant**.

### 1b. Open the Integrated Terminal

- **Windows/Linux:** Press **Ctrl + `**.
- **macOS:** Press **Cmd + `**.

### 1c. Create the Virtual Environment

```bash
python -m venv .venv
```

> **macOS/Linux:** Use `python3` if `python` is not found.

### 1d. Activate the Virtual Environment

**Windows — PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**Windows — Command Prompt**

```cmd
.venv\Scripts\activate.bat
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

> **PowerShell troubleshooting:** If PowerShell blocks the activation script, run the following once, then activate again. This changes the execution policy for the current user.

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 1e. Select the Python Interpreter

1. Open the Command Palette with **Ctrl + Shift + P**.
2. Search for **Python: Select Interpreter**.
3. Choose the interpreter inside `.venv`.

### 1f. Create the Folder Structure

```bash
mkdir data src
```

Expected structure:

```text
policy-assistant/
├── .venv/
├── data/       ← Policy documents
└── src/        ← Python code
```

### 1g. Verify the Environment

Create `src/check_env.py` with this content:

```python
import sys

print("Python version:", sys.version.split()[0])
print("Running from:", sys.executable)
```

Run it:

```bash
python src/check_env.py
```

| Check | Expected Result |
| :--- | :--- |
| **Python version** | Python **3.10 or higher** |
| **Interpreter path** | Contains `.venv` |

> 🟩 **Success:** Both checks pass. Continue to Step 2: store the API key safely and make the first Claude call.
> 🟥 **If the path does not contain `.venv`:** The virtual environment is not active. Repeat **Step 1d**.

---

<a id="4-architecture-name--terminology"></a>

## 🟪 <span style="color: #7e22ce;">4. Architecture Name & Terminology</span>

**Retrieval-Augmented Generation (RAG)** — specifically, **permission-aware hybrid RAG with reranking**.

### What Each Part Means

| Term | Meaning in This Design |
| :--- | :--- |
| **RAG** | Claude retrieves relevant policy chunks first, then generates an answer grounded in those chunks rather than relying on memory. |
| **Hybrid** | Retrieval combines vector (semantic) search with BM25 (keyword) search. |
| **Reranking** | A second model re-scores the top 50 results and keeps the best 5. |
| **Permission-aware** | Every search is filtered by the user's access groups (ACL) before anything reaches Claude. |

### The Two Pipelines

| Pipeline | Mode | Stages |
| :--- | :--- | :--- |
| **Ingestion** | Offline | Parse → Chunk → Embed → Index |
| **Query** | Online | Authenticate → Rewrite query → Retrieve → Rerank → Generate with citations |

### Related Terms You May Hear in Interviews

| Term | Description |
| :--- | :--- |
| **Enterprise RAG / Secure RAG** | General industry terms for this pattern. |
| **Two-stage retrieval** | Retrieve broadly, then rerank; describes the retrieval portion. |
| **Agentic RAG** | An extension where Claude decides when and what to retrieve using tools. Add this after the basic version works. |

### One-Line Interview Answer

> “It's a permission-aware hybrid RAG architecture: documents are chunked and indexed with ACL metadata, queries use vector plus keyword search filtered by user entitlements, results are reranked, and Claude generates a cited answer grounded only in the retrieved context.”

---

<a id="5-first-person-interview-script"></a>

## 🟧 <span style="color: #c2410c;">5. First-Person Interview Script</span>

**Question:** “Design an internal assistant that answers employee questions across 50,000 policy documents. Walk through the architecture.”

Use the following six-step framework for an approximately **3-minute** answer.

| Section | Suggested Time | Focus |
| :--- | ---: | :--- |
| **1. Clarify** | 30 seconds | Requirements and assumptions |
| **2. Architecture** | 90 seconds | Ingestion and query pipelines |
| **3. Model choice** | 15 seconds | Model tiering and fallback |
| **4. Quality** | 20 seconds | Retrieval and answer evaluation |
| **5. Risk** | 20 seconds | Permissions, hallucinations, injection, freshness |
| **6. Operations** | 20 seconds | Re-indexing, monitoring, cost |

### 1. Clarify First — 30 Seconds

“Before I design anything, I'd like to clarify a few things:

- **Users and scale:** How many employees, and how many questions per day?
- **Document types:** PDFs, Word files, slides, or wiki pages? Are there many tables?
- **Access control:** Are some policies restricted by department or region?
- **Accuracy bar:** Is this informational, such as HR leave policy, or high-stakes, such as compliance or legal?
- **Latency target:** Is a few seconds acceptable?

For this walkthrough, I'll assume about **10,000 employees**, mixed document formats, role-based access, and a requirement that **every answer cites its source**.”

### 2. Architecture — 90 Seconds

“I'd build a **permission-aware hybrid RAG** with two pipelines.

**Ingestion pipeline — offline:**

1. I parse documents with a layout-aware parser so tables and numbered clauses stay intact.
2. I chunk by headings and sections, around 500 tokens with a small overlap, and keep the heading path in each chunk so citations are precise.
3. I attach metadata to every chunk: document ID, version, effective date, department, and allowed groups.
4. I generate embeddings and store them in a vector database, alongside a BM25 keyword index.

**Query pipeline — online:**

1. I authenticate the user and resolve their group memberships.
2. I rewrite the question into a clean search query, using conversation history for follow-ups.
3. I run hybrid search — vector plus keyword — with the permission filter applied inside the query, so restricted content is never retrieved.
4. I rerank the top 50 candidates down to the best 5.
5. I send those chunks to Claude with instructions to answer only from the context, cite sources, and say ‘I couldn't find this’ when the answer isn't there.
6. I return the answer with source links and log everything.”

### 3. Model Choice — 15 Seconds

> “I'd use a smaller, faster Claude model for query rewriting and routing, and a stronger model for final answer generation. I'd keep a fallback model configured in case of rate limits or outages.”

### 4. Quality — 20 Seconds

> “I'd build a golden set of real employee questions with known correct documents. I'd measure retrieval quality — did the right chunk come back? — separately from answer quality — is the answer faithful to the chunks? That separation tells me whether a bad answer is a retrieval problem or a generation problem.”

### 5. Risk — 20 Seconds

**The key risks are:**

| Risk | My Approach |
| :--- | :--- |
| 🟥 **Permission leakage** | Filter at retrieval time, never after generation. |
| 🟧 **Hallucination** | Reduce it through grounding, mandatory citations, and ‘not found’ behaviour. |
| 🟨 **Prompt injection** | Treat documents as data, not instructions. |
| 🟪 **Stale or superseded policies** | Use version metadata and delete old versions. |

### 6. Operations — 20 Seconds

> “For freshness, I'd re-index only changed documents using a content hash, triggered by change events, so daily updates stay cheap. I'd monitor latency, cost per query, retrieval hit rate, and user feedback — thumbs up or down — and I'd use prompt caching and model tiering to control cost.”

### Closing Line

> “So in summary: parse and chunk with metadata, hybrid retrieval filtered by permissions, rerank, grounded generation with citations, and measure retrieval and generation separately. I'd start with one department as a pilot, prove the quality, then scale to all 50,000 documents.”

---

<a id="6-delivery-tips--next-steps"></a>

## 🟥 <span style="color: #b91c1c;">6. Delivery Tips & Next Steps</span>

### Interview Delivery Tips

- **Memorise the framework, not every word:** Clarify → Architecture → Model → Quality → Risk → Operations.
- **Pause after clarifying questions:** Interviewers may provide details that help shape the design.
- **Use “I would” and “because”:** Every decision needs a reason. For example: “I'd use hybrid search because policies contain exact clause numbers that vector search can miss.”
- **Prepare for follow-ups:** Chunking, permission filtering, and hallucination are the three most common probes.

### Next Steps

- [ ] Run `python src/check_env.py` and review the terminal output.
- [ ] Confirm that Python is running from `.venv`.
- [ ] Continue to **Step 2: API key storage and the first Claude call**.
- [ ] Prepare follow-up interview answers on **chunking**, **permission filtering**, and **hallucination**.

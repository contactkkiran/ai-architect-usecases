# Enterprise Knowledge Assistant (RAG) - Project 1
## Permission model

The assistant must never show a user content they are not entitled to see. Access control is enforced **at retrieval time**, inside the search query, and never after the answer is generated.

### How it works

1. Every document has an `allowed_groups` value, stored in `data/pdfs/registry.json`.
2. Every chunk inherits its document's `allowed_groups` as metadata.
3. When a user asks a question, the system looks up the groups that user belongs to.
4. The search only considers chunks whose `allowed_groups` overlap with the user's groups.
5. Claude only ever receives chunks that passed the filter.

```
User question -> user's groups -> search WITH filter (allowed_groups) -> top chunks -> Claude
```

### Sample documents and access

| Document | `allowed_groups` | Who can retrieve it |
|---|---|---|
| Leave Policy | all-employees | Everyone |
| Expense Reimbursement Policy | all-employees | Everyone |
| Remote Work Policy | all-employees | Everyone |
| Information Security Policy | all-employees | Everyone |
| Salary Bands (Confidential) | hr-team | HR team only |

### Test users (planned)

| User | Groups | Question | Expected result |
|---|---|---|---|
| Employee | all-employees | "What is the salary range for band L4?" | Not found, because the document is never retrieved |
| HR analyst | all-employees, hr-team | "What is the salary range for band L4?" | Answer with a citation to HR-005 |

### Why filter before generation

- Filtering **after** generation risks leaking restricted text in the answer.
- Asking the model to "ignore restricted content" is not a security control.
- A document that is never retrieved can never be quoted, summarized or hinted at.

### Known gaps (to address later)

- User groups are hard-coded for testing. Production would resolve them from the identity provider (SSO).
- Permission changes must trigger re-indexing or metadata updates, otherwise a revoked user keeps access to stale chunks.
- Access attempts should be logged for audit.

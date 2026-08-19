# RAG Pipeline

## Purpose

Retrieval-Augmented Generation grounds LLM output in content retrieved from the user's indexed documents instead of relying only on model memory.

## Ingestion pipeline

```text
PDF
 -> PDF loader
 -> page text
 -> text cleaning
 -> recursive chunking
 -> embedding generation
 -> ChromaDB indexing
 -> document metadata/profile persistence
```

Each indexed chunk retains metadata used later for filtering and citation generation, including document/source information and page/chunk position.

## Query pipeline

```text
Question
 -> chat history
 -> retrieval-context construction
 -> LLM query rewrite
 -> semantic search
 -> relevance threshold
 -> prompt construction
 -> local LLM generation
 -> citations
 -> chat-memory persistence
```

### 1. Conversation context

Recent user messages are used to help resolve follow-up questions. A separate bounded history is supplied to the final prompt.

### 2. Query rewriting

The LLM can transform a conversational question into a more useful retrieval query while preserving the user's intent.

### 3. Retrieval

The retriever searches ChromaDB using embeddings. Retrieval can be restricted to selected document IDs. Multi-document summary requests can use a broader summary-oriented retrieval path.

### 4. Relevance gate

The RAG pipeline applies a minimum context score. Results below the configured threshold are excluded from the grounded prompt.

If no sufficiently relevant chunks remain, the application returns a fallback stating that the information cannot be found in the provided book context rather than generating an unsupported answer.

### 5. Prompt construction

Retrieved chunks are labelled as sources (`S1`, `S2`, etc.) and supplied with source, page, and chunk metadata. The prompt combines conversation history, retrieved context, and the current question.

### 6. Generation

The prompt is sent through the LLM service to the configured Ollama model (`llama3.2` by default).

### 7. Citations

Only chunks supplied to the LLM are converted into source payloads. Duplicate source/page/chunk identities are suppressed. Returned citations contain reference, file name, page number, chunk number, and retrieval score.

### 8. Persistence

Both user and assistant messages are stored in the chat session. Assistant messages can persist JSON-compatible citation payloads.

## Document-profile summaries

The application also supports stored document profiles containing summary/topic information. Summary-oriented requests over selected documents can use these profiles instead of forcing ordinary chunk-level Q&A behavior.

## Quality improvements planned

Future retrieval work should measure retrieval recall/precision, answer faithfulness, citation correctness, latency, chunking quality, query-rewrite value, and threshold sensitivity using a repeatable evaluation dataset.
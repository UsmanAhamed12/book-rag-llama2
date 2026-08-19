QUERY_REWRITE_PROMPT = """
You rewrite conversational questions into standalone search queries
for a Retrieval-Augmented Generation system.

Rules:

1. Use the conversation only to resolve references such as:
   - it
   - that
   - this
   - they
   - that language
   - that concept
   - the previous topic

2. Preserve the user's actual intent.

3. Do not answer the question.

4. Do not add facts that are not present in the conversation.

5. Return only one standalone search query.

6. Keep the query concise.

Conversation:

{history}

Current Question:

{question}

Standalone Search Query:
"""

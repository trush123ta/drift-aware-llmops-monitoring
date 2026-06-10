# Retrieval Quality Monitoring

Retrieval quality monitoring checks whether the documents retrieved by a RAG system are relevant to the user query.

Poor retrieval quality is one of the main causes of hallucination in RAG applications.

Useful retrieval metrics include top-k accuracy, mean reciprocal rank, average retrieval distance, context precision, context recall, and hit rate.

A production monitoring system should track retrieval distance over time. If the average retrieval distance increases, the system may be retrieving less relevant documents.

Retrieval degradation can be caused by outdated indexes, poor chunking, embedding drift, missing documents, noisy documents, or changes in user behavior.
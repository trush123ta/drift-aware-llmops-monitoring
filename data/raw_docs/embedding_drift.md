# Embedding Drift

Embedding drift occurs when the distribution of query embeddings or document embeddings changes over time.

In a production RAG system, embedding drift can happen when users begin asking different types of questions, when the document corpus changes, or when the embedding model is updated.

Embedding drift can reduce retrieval quality because the vector database may no longer represent the current query distribution well.

Common ways to detect embedding drift include centroid shift, cosine distance distribution changes, nearest-neighbor score degradation, KL divergence, Wasserstein distance, and population stability index.

A drift-aware system should compare current query embeddings against a baseline window and trigger alerts when the distance exceeds a configured threshold.
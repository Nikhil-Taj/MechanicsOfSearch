import math
from collections import Counter
from indexing import SearchEngineIndexer
from rank_bm25 import BM25Okapi  
import numpy as np 


# ---- TF-IDF Model (VectorSpaceModel) ----
import math
from collections import Counter

class VectorSpaceModel:
    def __init__(self, indexer):
        self.indexer = indexer
        self.document_count = len(indexer.documents)
        self.doc_term_freq = {}
        for doc_id, text in indexer.documents.items():
            words = indexer.preprocess_text(text)
            self.doc_term_freq[doc_id] = Counter(words)

    def compute_tf_idf(self, query):
        scores = {}
        query_terms = self.indexer.preprocess_text(query)
        for term in query_terms:
            if term in self.indexer.inverted_index:
                doc_list = self.indexer.inverted_index[term]
                idf = math.log(self.document_count / (1 + len(doc_list)))
                for doc_id in doc_list:
                    tf = self.doc_term_freq[doc_id][term]
                    scores[doc_id] = scores.get(doc_id, 0) + (tf * idf)
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)


# ---- BM25 Model ----
class BM25Model:
    def __init__(self, indexer, k1=1.5, b=0.75): 
        self.indexer = indexer
        self.k1 = k1
        self.b = b
        self.corpus = [indexer.preprocess_text(doc) for doc in indexer.documents.values()]
        self.bm25 = BM25Okapi(self.corpus, k1=self.k1, b=self.b)

    def compute_bm25(self, query):
        """ Computes BM25 scores for a given query """
        query_tokens = self.indexer.preprocess_text(query)
        scores = self.bm25.get_scores(query_tokens)
        return sorted(zip(self.indexer.documents.keys(), scores), key=lambda x: x[1], reverse=True)


# ---- Language Model with Dirichlet Smoothing (LMModel) ----
class LMModel:
    def __init__(self, indexer, lambda_val=0.1):
        self.indexer = indexer
        self.lambda_val = lambda_val
        self.doc_term_freq = {doc_id: Counter(indexer.preprocess_text(text)) for doc_id, text in indexer.documents.items()}
        self.collection_tf = Counter(word for text in indexer.documents.values() for word in indexer.preprocess_text(text))
        self.collection_length = sum(self.collection_tf.values())

    def compute_lm(self, query):
        """ Computes Jelinek-Mercer LM scores """
        scores = {}
        query_terms = self.indexer.preprocess_text(query)

        for doc_id, term_freqs in self.doc_term_freq.items():
            doc_length = sum(term_freqs.values())
            score = 0.0

            for term in query_terms:
                doc_prob = term_freqs.get(term, 0) / doc_length if doc_length > 0 else 0
                coll_prob = self.collection_tf.get(term, 0) / self.collection_length
                smoothed_prob = (1 - self.lambda_val) * doc_prob + self.lambda_val * coll_prob
                score += np.log(smoothed_prob + 1e-9)  

            scores[doc_id] = score

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
# ---- Testing block ----
if __name__ == "__main__":
    indexer = SearchEngineIndexer("data/cran.all.1400.xml")
    indexer.build_index()
    indexer.inverted_index = {}
    for doc_id, text in indexer.documents.items():
        for word in indexer.preprocess_text(text):
            indexer.inverted_index.setdefault(word, set()).add(doc_id)

    query = "aerodynamics research"
    vsm = VectorSpaceModel(indexer)
    ranked_tf_idf = vsm.compute_tf_idf(query)
    print("TF-IDF Top 10 Results:")
    for rank, (doc_id, score) in enumerate(ranked_tf_idf[:10], 1):
        print(f"{rank}. Doc {doc_id} - Score: {score:.4f}")

    # BM25
    bm25 = BM25Model(indexer)
    ranked_bm25 = bm25.compute_bm25(query)
    print("\nBM25 Top 10 Results:")
    for rank, (doc_id, score) in enumerate(ranked_bm25[:10], 1):
        print(f"{rank}. Doc {doc_id} - Score: {score:.4f}")

    # LMModel
    lm_model = LMModel(indexer)
    ranked_lm = lm_model.compute_lm(query)
    print("\nLanguage Model (Dirichlet) Top 10 Results:")
    for rank, (doc_id, score) in enumerate(ranked_lm[:10], 1):
        print(f"{rank}. Doc {doc_id} - Score: {score:.4f}")

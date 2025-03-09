import nltk
from indexing import SearchEngineIndexer
from ranking import VectorSpaceModel, BM25Model, LMModel
from query_parser import parse_queries

nltk.download('wordnet')

def generate_run_file(ranking_model, queries, run_id, output_file):
    """ Generate output file for TREC evaluation """
    with open(output_file, "w", encoding="utf-8") as out:
        for query_id, query_text in queries.items():
            if hasattr(ranking_model, "compute_bm25"):
                results = ranking_model.compute_bm25(query_text)
            elif hasattr(ranking_model, "compute_tf_idf"):
                results = ranking_model.compute_tf_idf(query_text)
            elif hasattr(ranking_model, "compute_lm"):
                results = ranking_model.compute_lm(query_text)
            else:
                raise AttributeError(f"Ranking model {ranking_model.__class__.__name__} has no valid ranking function.")

            for rank, (doc_id, score) in enumerate(results[:100], 1):
                out.write(f"{query_id} 0 {doc_id} {rank} {score:.4f} {run_id}\n")

def main():
    """ Main function for generating ranking results """
    indexer = SearchEngineIndexer("data/cran.all.1400.xml")
    indexer.build_index() 
    indexer.inverted_index = {} 
    for doc_id, text in indexer.documents.items():
        for word in indexer.preprocess_text(text):
            indexer.inverted_index.setdefault(word, set()).add(doc_id)

    queries = parse_queries("data/cran.qry.xml")

    # Initialize models
    vsm = VectorSpaceModel(indexer)
    bm25 = BM25Model(indexer)
    lm_model = LMModel(indexer)

    # Generate run files
    generate_run_file(vsm, queries, "TFIDF", "run_tfidf.txt")
    generate_run_file(bm25, queries, "BM25", "run_bm25.txt")
    generate_run_file(lm_model, queries, "LM", "run_lm.txt")

    print("Run files generated: run_tfidf.txt, run_bm25.txt, and run_lm.txt")

if __name__ == "__main__":
    main()

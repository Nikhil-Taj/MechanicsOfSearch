from indexing import SearchEngineIndexer
from ranking import VectorSpaceModel, BM25Model

def build_inverted_index(indexer):
    indexer.inverted_index = {}
    for doc_id, text in indexer.documents.items():
        for word in indexer.preprocess_text(text):
            indexer.inverted_index.setdefault(word, set()).add(doc_id)

def main():
    # Build the index
    indexer = SearchEngineIndexer("data/cran.all.1400.xml")
    indexer.build_index()
    build_inverted_index(indexer)
    
    # Initialize ranking models
    vsm = VectorSpaceModel(indexer)
    bm25 = BM25Model(indexer)
    
    print("Welcome to the Search Engine Demo!")
    while True:
        query = input("Enter a query (or type 'exit' to quit): ")
        if query.strip().lower() == "exit":
            break

        print("\nTF-IDF Results:")
        results_vsm = vsm.compute_tf_idf(query)
        for rank, (doc_id, score) in enumerate(results_vsm[:10], 1):
            print(f"{rank}. Doc {doc_id} - Score: {score:.4f}")
        
        print("\nBM25 Results:")
        results_bm25 = bm25.compute_bm25(query)
        for rank, (doc_id, score) in enumerate(results_bm25[:10], 1):
            print(f"{rank}. Doc {doc_id} - Score: {score:.4f}")
        print("\n----------------------------------\n")

if __name__ == "__main__":
    main()

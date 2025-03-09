import pytrec_eval

def read_qrels(qrels_file):
    """Reads qrels file and returns a dictionary."""
    qrels = {}
    with open(qrels_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            query_id, _, doc_id, relevance = parts
            if query_id not in qrels:
                qrels[query_id] = {}
            qrels[query_id][doc_id] = int(relevance)
    return qrels

def read_run(run_file):
    """Reads run file and returns a dictionary."""
    run = {}
    with open(run_file, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            query_id, _, doc_id, rank, score, _ = parts
            if query_id not in run:
                run[query_id] = {}
            run[query_id][doc_id] = float(score)
    return run

def evaluate_run(qrels_file, run_file, model_name):
    """Evaluates a given run file and prints all evaluation metrics."""
    qrels = read_qrels(qrels_file)
    run = read_run(run_file)

    evaluator = pytrec_eval.RelevanceEvaluator(qrels, pytrec_eval.supported_measures)
    results = evaluator.evaluate(run)

    # Aggregate results 
    all_results = {metric: sum(result[metric] for result in results.values()) / len(results) for metric in results[next(iter(results))]}

    # evaluation metrics
    print(f"\n=== Evaluation Results for {model_name} ===")
    for metric, value in all_results.items():
        print(f"{metric}: {value:.4f}")

if __name__ == "__main__":
    qrels_file = "data/cranqrel.trec.txt"

    evaluate_run(qrels_file, "run_tfidf.txt", "TF-IDF")
    evaluate_run(qrels_file, "run_bm25.txt", "BM25")
    evaluate_run(qrels_file, "run_lm.txt", "Language Model")

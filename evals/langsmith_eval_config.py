# evals/langsmith_eval_config.py
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()


def run_eval(pipeline_func, dataset_name: str = "maison-beaute-eval-dataset"):
    """
    Run the LangSmith evaluation suite against the golden Q&A dataset.
    Call this after any prompt change to verify quality hasn't regressed.

    Usage:
        from app.routers.chatbot import chat
        run_eval(chat)
    """
    results = evaluate(
        pipeline_func,
        data=dataset_name,
        evaluators=[
            "correctness",   # Does the answer match the expected answer?
            "relevance",     # Is it relevant to the question?
            "safety",        # Does it avoid harmful content?
            "conciseness",   # Is it appropriately brief?
        ],
        experiment_prefix="mb-advisor-v1",
    )
    print(f"✅ Eval complete — {len(results)} results")
    return results

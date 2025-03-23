from transformers import pipeline

# Explicitly define model and revision
MODEL_NAME = "facebook/bart-large-cnn"  # More stable model
summarizer = pipeline("summarization", model=MODEL_NAME)

def summarize_text(text):
    """Summarizes news content safely."""
    if not text.strip():
        return "No content to summarize."

    try:
        summary = summarizer(text[:1024], max_length=100, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error during summarization: {str(e)}"

# Test Run
if __name__ == "__main__":
    sample_text = "Tesla is leading the electric vehicle industry with its latest innovations in battery technology and autonomous driving."
    print(summarize_text(sample_text))

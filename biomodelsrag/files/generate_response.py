import os

import ollama
from groq import Groq

def generate_response(
    db,
    query,
    history,
    backend="groq",
    model="llama-3.3-70b-versatile",
    top_n=5,
):
    """
    Generate a response using either Groq or Ollama.

    Args:
        db: Vector database.
        query: User's question.
        history: Previous conversation messages.
        backend: "groq" or "ollama".
        model: Model name for the selected backend.
        top_n: Number of documents to retrieve.
    """

    if backend not in {"groq", "ollama"}:
        raise ValueError(
            f"Unsupported backend: {backend}. "
            "Choose 'groq' or 'ollama'."
        )
    
    query_results = db.query(
        query_texts=[query],
        n_results=top_n,
    )

    documents = query_results["documents"]

    if documents:
        documents = documents[0]

    context = "\n\n".join(documents)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant that answers "
                "questions about biological models. "
                "Use the provided model context to answer "
                "the user's question. If the context does "
                "not contain enough information to answer "
                "the question, say so rather than "
                "inventing information."
            ),
        }
    ]

    for message in history:
        messages.append({
            "role": "user",
            "content": message["user"],
        })

        messages.append({
            "role": "assistant",
            "content": message["assistant"],
        })

    messages.append({
        "role": "user",
        "content": (
            f"Model context:\n\n"
            f"{context}\n\n"
            f"Question:\n{query}"
        ),
    })

    if backend == "groq":

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY environment variable "
                "is not set."
            )

        client = Groq(api_key=api_key)

        completion = client.chat.completions.create(
            model=model,
            messages=messages,
        )

        return completion.choices[0].message.content

    elif backend == "ollama":
        response = ollama.chat(
            model=model,
            messages=messages,
        )

        return response["message"]["content"]
import fire

from biomodelcache import BioModelCacheRetrieval
from convert_sbml_to_antimony import convert_sbml_to_antimony
from split_biomodels import split_biomodels
from vector_db import create_vector_db, load_vector_db
from generate_response import generate_response

from chat_history import (
    create_session_id,
    load_chat_history,
    save_chat_history,
)


class BioModelCLI:

    def search(self, search_str, database_path):
        """Search BioModels and return all matching models."""

        retriever = BioModelCacheRetrieval(search_str)
        models = retriever.search_models()

        if not models:
            print("No models found.")
            return

        for model_id, model_data in models.items():
            print(f"{model_id}: {model_data['name']}")
            print(f"  URL: {model_data['url']}")
            print()

    def build_db(self, search_str, output_path):
        """Build and save a vector database from BioModels."""

        retriever = BioModelCacheRetrieval(search_str)
        models = retriever.search_models()

        if not models:
            raise ValueError(
                f"No models found for search query: {search_str}"
            )

        all_final_items = []

        for model_id, model_data in models.items():
            print(
                f"Processing model: "
                f"{model_data['name']}"
            )

            model_url = model_data["url"]

            model_file_path = retriever.download_model_files(
                model_url,
                model_id
            )

            if not model_file_path:
                print(f"Failed to download {model_id}")
                continue

            antimony_file_path = (
                f"/tmp/{model_id}.txt"
            )

            convert_sbml_to_antimony(
                model_file_path,
                antimony_file_path
            )

            final_items = split_biomodels(
                antimony_file_path
            )

            all_final_items.extend(final_items)

        if not all_final_items:
            raise ValueError(
                "No models were processed successfully."
            )

        print("Creating vector database...")

        create_vector_db(
            all_final_items,
            output_path
        )

        print(
            f"Database saved to: {output_path}"
        )

    def ask(
        self,
        question,
        database_path,
        backend="groq",
        model=None,
        top_n=5,
    ):
        """
        Ask a single question about a BioModel database.
        """

        db = load_vector_db(database_path)

        response = generate_response(
            db=db,
            query=question,
            history=[],
            backend=backend,
            model=model,
            top_n=top_n,
        )

        print(response)

    def query(
        self,
        output_path,
        backend="groq",
        model=None,
        session=None,
    ):
        if session is None:
            session = create_session_id()
            history = []
        else:
            history = load_chat_history(
                output_path,
                session,
            )

        db = load_vector_db(output_path)

        print("BioModel Chat")
        print(f"Session: {session}")
        print(f"Backend: {backend}")
        print(f"Model: {model}")
        print("Type 'exit' or 'quit' to end.")

        while True:

            question = input("\nYou: ")

            if question.lower() in {"exit", "quit"}:
                break

            response = generate_response(
                db=db,
                query=question,
                history=history,
                backend=backend,
                model=model,
            )

            print(f"\nBioModel: {response}")

            history.append({
                "user": question,
                "assistant": response,
            })

        save_chat_history(
            output_path,
            history,
            session,
        )


if __name__ == "__main__":
    fire.Fire(BioModelCLI)
import os
import json
import ollama
from dotenv import dotenv_values

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
env_path = os.path.join(root_dir, ".env")
config = dotenv_values(env_path)


def generate_model_response(prompt: str):
    """Generate response from AI model using Ollama"""
    desired_model = config.get("AI_MODEL")

    try:
        response = ollama.generate(model=desired_model, prompt=prompt)
        ai_content = response.get("content") or response.get("response")

        if ai_content:
            try:
                return json.loads(response.get("response"))
            except json.JSONDecodeError as e:
                print(f"Failed to parse response JSON: {e}")
                return {
                    "ai_model_confidence_score": 0,
                    "match_classification": "Error",
                    "explanation": "Invalid JSON response",
                }

        return {
            "ai_model_confidence_score": 0,
            "match_classification": "Error",
            "explanation": "No response from AI.",
        }
    except ollama.ResponseError as e:
        print(f"Failed to generate response: {e.error}")
        return {
            "ai_model_confidence_score": 0,
            "match_classification": "Error",
            "explanation": f"{e.error}",
        }

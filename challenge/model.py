import os
import json
import ollama
from openai import OpenAI
from dotenv import dotenv_values

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
env_path = os.path.join(root_dir, ".env")
config = dotenv_values(env_path)


api_key = config.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


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


def generate_model_response_with_open_ai(prompt: str):
    """
    Generate a response from the OpenAI model for tenant screening in JSON format.

    Args:
        prompt (str): The user input prompt for tenant screening.

    Returns:
        dict: The parsed JSON response from the model, or an error response if generation fails.
    """

    try:
        completion = client.chat.completions.create(
            model=config.get("OPENAI_MODEL"),
            store=False,
            messages=[
                {
                    "role": "developer",
                    "content": "You are an AI assistant specialized in tenant screening and you do not make mistakes. Provide your response in JSON format.",
                },
                {"role": "user", "content": prompt},
            ],
            response_format={"type": "json_object"},
            max_tokens=100,
            temperature=0.5,
            n=1,
            stop=None,
        )

        if not completion.choices:
            print("No choices returned by the model.")
            return {
                "ai_model_confidence_score": 0,
                "match_classification": "Error",
                "explanation": "No response from AI.",
            }

        ai_content = completion.choices[0].message.content

        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>RESPONSE FROM CHAT GPT", ai_content)

        if ai_content:
            try:
                return json.loads(ai_content)
            except json.JSONDecodeError as e:
                print(f"Failed to parse response JSON: {e}")
                return {
                    "ai_model_confidence_score": 0,
                    "match_classification": "Error",
                    "explanation": "Invalid JSON response",
                }

        print("No content received from the model.")
        return {
            "ai_model_confidence_score": 0,
            "match_classification": "Error",
            "explanation": "No response from AI.",
        }
    except Exception as e:
        print(f"Failed to generate response+++++++++++++++++++++++++: {e}")
        {
            "ai_model_confidence_score": 0,
            "match_classification": "Error",
            "explanation": str(e),
        }

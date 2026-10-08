import os
import json

SYSTEM_PROMPT = """You are ProcureAI's procurement decision-support assistant.
Interpret only structured procurement analytics supplied by the application.
Never invent vendor information.
Never change or override the deterministic ranking.
Clearly distinguish facts from recommendations.
Identify trade-offs and risks.
If data is insufficient, say so.
Do not make autonomous purchasing decisions.
"""


def get_gemini_response(context, question):
    key = os.getenv("GEMINI_API_KEY")

    if not key:
        return None, "Gemini is not configured. Add GEMINI_API_KEY to Streamlit Secrets/environment."

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=key)
        model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

        prompt = (
            SYSTEM_PROMPT
            + "\n\nSTRUCTURED DATA:\n"
            + json.dumps(context, default=str)
            + "\n\nQUESTION:\n"
            + question
            + "\n\nEnd with: This is a decision-support recommendation and not an autonomous procurement decision."
        )

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                max_output_tokens=900,
            ),
        )

        return response.text, None

    except Exception as e:
        return None, f"Gemini unavailable: {type(e).__name__}: {e}"

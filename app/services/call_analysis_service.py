import json
from typing import Dict, Any
from google import genai  # Correct import for google-genai package
from app.config import GEMINI_API_KEY

# Initialize the client
# Use type hint to help Pylance understand the client's attributes
client: Any = genai.Client(api_key=GEMINI_API_KEY)


def analyze_call(transcript: str) -> Dict[str, Any]:

    prompt = f"""
    ### ROLE
    You are a highly accurate Freight Data Analyst specializing in structured information extraction from carrier-broker transcripts.

    ### TASK
    Analyze the provided transcript between a carrier and an AI broker. Extract specific deal parameters and classify the call outcome and sentiment.

    ### EXTRACTION RULES & GUARDRAILS
    1. **No Hallucination**: Only extract values explicitly stated in the transcript. If a value (like mc_number or load_id) is not mentioned, return `null`. Do not guess.
    2. **Rate Accuracy**: The `final_rate` must be a numeric value representing the agreed-upon price. If no agreement was reached, return `null`.
    3. **Outcome Classification**:
    - `deal_closed`: A price was agreed upon and the call is moving toward booking/transfer.
    - `deal_failed`: Negotiation happened but they couldn't agree, or the carrier hung up.
    - `info_only`: The carrier was just asking for details without negotiating or attempting to book.
    4. **Sentiment Analysis**: Evaluate the carrier's tone. Are they frustrated (negative), professional (neutral), or eager/satisfied (positive)?
    5. **Strict JSON**: Return ONLY valid JSON. No preamble, no conversational filler, and no markdown code blocks unless requested.

    ### TRANSCRIPT
    {transcript}

    ### OUTPUT FORMAT
    Ensure the output is exactly in this JSON structure:
    {{
    "mc_number": string | null,
    "load_id": string | null,
    "final_rate": number | null,
    "outcome": "deal_closed" | "deal_failed" | "info_only",
    "sentiment": "positive" | "neutral" | "negative"
    }}
    """

    try:
        # Pylance might still mark .models as unknown; 'client: Any' above resolves this
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )

        text = response.text.strip()

        # Remove potential markdown formatting
        text = text.replace("```json", "").replace("```", "")
        data = json.loads(text)

        return data

    except Exception as e:
        print(f"LLM Error: {str(e)}")
        return {
            "mc_number": None,
            "load_id": None,
            "final_rate": None,
            "outcome": "info_only",
            "sentiment": "neutral",
            "error": str(e),
        }

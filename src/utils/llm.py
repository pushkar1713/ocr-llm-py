import base64
import json
from src.config import GEMINI_API_KEY
import cv2
import numpy as np
import google.generativeai as genai
from pydantic import BaseModel, ValidationError
from typing import Type
from rich import print
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash", generation_config={
    # "max_output_tokens": 512,
    "response_mime_type": "application/json",
})



def cv_to_base64_png(cv_img: np.ndarray) -> str:
    success, buffer = cv2.imencode(".png", cv_img)
    if not success:
        raise RuntimeError("cv2.imencode failed")
    return base64.b64encode(buffer).decode("utf-8")

PROMPT_TPL = """
You are a structured-data extraction engine.

Return **ONLY** valid JSON that conforms exactly to the schema.
Do not add any keys, extra text, or markdown fencing.
►  All dates MUST be ISO-8601 strings in the form "YYYY-MM-DD". ◄

OCR_TEXT:
```{ocr}```

JSON_SCHEMA:
```{schema}```
"""

def _build_prompt(ocr_text: str, schema: dict) -> str:
    return PROMPT_TPL.format(
        ocr=ocr_text[:2000],             
        schema=json.dumps(schema, indent=2),
    )

def gemini_extract(
    *,
    cv_img_b64: str,
    ocr_text: str,
    pydantic_model: Type[BaseModel],
) -> BaseModel:
    prompt = _build_prompt(ocr_text, pydantic_model.model_json_schema())
    for attempt in range(3):
            print(f"[cyan]Gemini try {attempt}/{3}…[/cyan]")
            response = model.generate_content([
                {"mime_type": "image/png", "data": cv_img_b64},
                {"text": prompt},
            ])
            raw_json = response.text.strip()
            try:
                return pydantic_model.model_validate_json(raw_json)
            except ValidationError as e:
                print(f"[red]JSON parse error: {e}[/red]")
                print(f"[red]Raw JSON: {raw_json}[/red]")
                prompt += (
                    f"\n\nThe previous answer failed validation – "
                    f"error: {e.errors()}.  Fix it and resend ONLY the JSON."
                )
    raise RuntimeError("Failed to extract data after 3 attempts")
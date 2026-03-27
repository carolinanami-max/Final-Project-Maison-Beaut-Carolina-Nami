# app/routers/descriptions.py
import json
import os

from fastapi import APIRouter, HTTPException
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable

from app.models.product import ProductInput, ProductDescription
from app.core.ingredient_lookup import fetch_ingredients, merge_ingredients

router = APIRouter()

# ─── LLM ──────────────────────────────────────────────────────
llm = ChatAnthropic(
    model="claude-haiku-4-5-20251001",
    temperature=0.7,
    max_tokens=1024,
)

# ─── System Prompt ────────────────────────────────────────────
SYSTEM_PROMPT = """You are the Maison Beauté copywriter.
Maison Beauté is a premium beauty marketplace based in Berlin selling New, Tested Out, and Pre-loved luxury beauty products.

Your tone: sophisticated, warm, slightly French-inflected, sustainability-conscious.

Product condition definitions:
- New: never used, original seal intact
- Tested Out: at least 90% of product remains, resealed after quality & hygiene check
- Pre-loved: at least 50% of product remains, resealed after quality & hygiene check
All products are sold in their original packaging and resealed after a professional quality and hygiene check.

Generate a product listing description in EXACTLY this JSON structure — no extra text, no markdown fences:
{{
  "title": "...",
  "tagline": "...",
  "description": "...",
  "seo_tags": ["...", "..."],
  "condition_note": "..."
}}

Rules:
- title: max 60 characters, includes brand name + product name
- tagline: 1 evocative sentence that captures the product's essence
- description: 80-120 words across 3 short paragraphs — product & condition → key ingredients/benefits → quality guarantee & sustainability angle
- seo_tags: 5-8 relevant beauty/SEO tags including brand, category, and key ingredients
- condition_note: honest, reassuring note using ONLY these exact terms: New / Tested Out / Pre-loved. Always mention the quality and hygiene check.
- NEVER claim the product is New if condition is Tested Out or Pre-loved
- NEVER invent ingredients not listed in the input
- ALWAYS mention that the product comes in original packaging resealed after quality check
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "Generate a listing for this product:\n{product_json}"),
])

chain = prompt | llm


# ─── Endpoint ─────────────────────────────────────────────────
@router.post("/generate-description", response_model=ProductDescription)
@traceable(name="generate_product_description", tags=["module-1", "shop-manager"])
async def generate_description(product: ProductInput) -> ProductDescription:
    """
    Module 1 — Shop Manager Agent.
    1. Fetches key ingredients from Perplexity API
    2. Merges with any manually provided ingredients
    3. Generates SEO-optimised description via Claude Haiku
    """
    try:
        # ── Step 1: Fetch ingredients from Perplexity ─────────
        perplexity_ingredients = await fetch_ingredients(product.brand, product.product_name)

        # ── Step 2: Merge with manual ingredients ─────────────
        final_ingredients, source = merge_ingredients(
            perplexity_ingredients,
            product.key_ingredients,
        )

        # ── Step 3: Build enriched product data for LLM ───────
        product_data = product.model_dump()
        product_data["key_ingredients"] = final_ingredients
        product_data["ingredients_source"] = source

        # ── Step 4: Generate description via Claude Haiku ─────
        result = await chain.ainvoke({"product_json": json.dumps(product_data, indent=2)})
        # Strip markdown fences if Claude wraps output in ```json ... ```
        raw = result.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        parsed = json.loads(raw)

        return ProductDescription(
            product_id=product.product_id,
            title=parsed["title"],
            tagline=parsed["tagline"],
            description=parsed["description"],
            seo_tags=parsed["seo_tags"],
            condition_note=parsed["condition_note"],
            ingredients_source=source,
        )

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=422,
            detail=f"LLM returned invalid JSON. Raw output: {raw[:300]}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
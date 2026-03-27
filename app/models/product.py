# app/models/product.py
from pydantic import BaseModel, Field
from typing import Literal


class ProductInput(BaseModel):
    """Input payload for Module 1 — Shop Manager Agent."""

    product_id: str = Field(..., example="MB-2024-0847")
    brand: str = Field(..., example="Charlotte Tilbury")
    product_name: str = Field(..., example="Pillow Talk Lipstick")
    category: Literal[
        "Make-up",
        "Parfumes",
        "Skin-care",
        "Body-care",
        "Hair-care",
        "Beauty Tools",
    ] = Field(..., example="Make-up")
    condition: Literal[
        "New",
        "Tested Out",
        "Pre-loved",
    ] = Field(..., example="Tested Out")
    original_retail_price_eur: float = Field(..., example=39.0)
    listing_price_eur: float = Field(..., example=22.0)
    key_ingredients: list[str] | None = Field(default=None, example=None)
    size_value: float | None = Field(None, example=3.5)
    size_unit: Literal["ml", "g"] | None = Field(None, example="g")


class ProductDescription(BaseModel):
    """Output from Module 1 — generated product listing."""

    product_id: str
    title: str
    tagline: str
    description: str
    seo_tags: list[str]
    condition_note: str
    ingredients_source: str
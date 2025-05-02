from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class TextContext(BaseModel):
    prev: Optional[str] = Field(None, example="La phrase précédente")
    match: str = Field(..., example="Le contrat avec le prestataire")
    next: Optional[str] = Field(None, example="La phrase suivante")

class SearchResponse(BaseModel):
    results: Dict[str, List[TextContext]] = Field(
        ...,
        example={
            "prestataire": [
                {
                    "prev": "Conformément aux dispositions",
                    "match": "Le prestataire doit fournir",
                    "next": "Dans un délai de 30 jours"
                }
            ]
        }
    )

class TextResponse(BaseModel):
    text: str = Field(..., example="Texte intégral extrait du PDF...")
    images: List[str] = Field([], example=["image1.png", "image2.png"])
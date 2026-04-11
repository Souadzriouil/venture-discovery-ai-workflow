from pydantic import BaseModel
from typing import List, Optional

class SummaryItem(BaseModel):
    Title: str
    Summary: str
    URL: str

class VentureIdea(BaseModel):
    id: int
    idea: str
    summary: str
    URL: str

class MarketEstimates(BaseModel):
    id: int
    idea: str
    summary: str
    TAM: float
    SAM: float
    SOM: float
    CAGR: float
    strategic_fit: float
    URL: str

class ScoreBreakdown(BaseModel):
    market_size: float
    market_growth: float
    strategic_fit: float

class ScoredVenture(BaseModel):
    id: int
    idea: str
    summary: str
    URL: str
    score_breakdown: ScoreBreakdown
    feasibility_score: float

class Insights(BaseModel):
    go_to_market: str
    justification: str
    value_proposition: str
    features: List[str]
    positioning: str
    differentiation: str

class WhiteSpace(BaseModel):
    market_gap: str
    company_fit: str

class FinalVenture(BaseModel):
    id: int
    idea: str
    summary: str
    URL: str
    score_breakdown: ScoreBreakdown
    feasibility_score: float
    insights: Insights
    white_space_analysis: WhiteSpace
    citations: Optional[List[str]] = []

class ApiResponse(BaseModel):
    ventures: List[FinalVenture]
    timestamp: str

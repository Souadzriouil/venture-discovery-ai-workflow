export interface ScoreBreakdown {
  market_size?: number;
  market_growth?: number;
  strategic_fit?: number;
}

export interface Insights {
  value_proposition?: string;
  features?: string[];
  go_to_market?: string;
  positioning?: string;
  differentiation?: string;
  justification?: string;
}

export interface WhiteSpaceAnalysis {
  market_gap?: string;
  company_fit?: string;
}

export interface Venture {
  id: number;
  idea: string;
  summary?: string;
  URL?: string;
  feasibility_score?: number;
  score_breakdown?: ScoreBreakdown;
  insights?: Insights;
  white_space_analysis?: WhiteSpaceAnalysis;
  citations?: string[];
}

export interface DiscoverResponse {
  ventures: Venture[];
  timestamp: string;
}

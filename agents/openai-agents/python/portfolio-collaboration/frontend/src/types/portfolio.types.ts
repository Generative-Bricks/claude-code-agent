/**
 * Portfolio domain types matching backend Pydantic models.
 *
 * Source: src/models/schemas.py
 *
 * These types mirror the backend Pydantic models exactly, using snake_case
 * field names to match JSON serialization from Python.
 */

// ============================================================================
// Enumerations
// ============================================================================

/**
 * Client risk tolerance levels.
 * Maps to RiskTolerance enum in schemas.py
 */
export type RiskTolerance = 'Conservative' | 'Moderate' | 'Aggressive';

/**
 * Asset class categories.
 * Maps to AssetClass enum in schemas.py
 */
export type AssetClass = 'Equity' | 'Fixed Income' | 'Cash' | 'Alternatives';

/**
 * Portfolio risk rating.
 * Maps to RiskRating enum in schemas.py
 */
export type RiskRating = 'Low' | 'Medium' | 'High' | 'Very High';

/**
 * Compliance check status.
 * Maps to ComplianceStatus enum in schemas.py
 */
export type ComplianceStatus = 'PASS' | 'FAIL' | 'REVIEW';

/**
 * Client-portfolio suitability rating.
 * Maps to SuitabilityRating enum in schemas.py
 */
export type SuitabilityInterpretation =
  | 'Highly Suitable'
  | 'Suitable'
  | 'Marginal Fit'
  | 'Not Suitable';

// ============================================================================
// Client & Portfolio Models
// ============================================================================

/**
 * Client profile containing demographics, risk tolerance, and investment objectives.
 *
 * Used in Stage 1: Client Discovery
 * Maps to ClientProfile in schemas.py
 */
export interface ClientProfile {
  client_id: string;
  age: number;  // 18-120
  risk_tolerance: RiskTolerance;
  investment_goals: string[];  // Min length: 1
  time_horizon: number;  // years, min: 1
  constraints?: string[];
  annual_income?: number;  // USD, >= 0
  net_worth?: number;  // USD, >= 0
  liquidity_needs?: string;
}

/**
 * Individual holding within a portfolio.
 * Maps to PortfolioHolding in schemas.py
 */
export interface Holding {
  ticker: string;
  company_name?: string;
  shares: number;  // > 0
  current_price: number;  // > 0
  market_value: number;  // > 0
  asset_class: AssetClass;
  sector?: string;
  cost_basis?: number;  // > 0
}

/**
 * Complete portfolio with holdings and metadata.
 *
 * Used throughout the multi-agent workflow.
 * Maps to Portfolio in schemas.py
 */
export interface Portfolio {
  portfolio_id: string;
  client_id: string;
  holdings: Holding[];  // Min length: 1
  total_value: number;  // > 0
  as_of_date: string;  // ISO format datetime
  benchmark?: string;  // Default: "SPY"
}

// ============================================================================
// Agent Analysis Output Models
// ============================================================================

/**
 * Risk analysis output from Risk Analyst Agent.
 *
 * Produced in Stage 2: Parallel Analysis
 * Maps to RiskAnalysis in schemas.py
 */
export interface RiskAnalysis {
  volatility: number;  // 0-100, annualized volatility (standard deviation)
  var_95: number;  // 95% Value at Risk (potential loss)
  beta: number;  // Portfolio beta vs benchmark
  concentration_score: number;  // 0-100 (0=diversified, 100=concentrated)
  max_drawdown?: number;  // Maximum historical drawdown percentage
  risk_rating: RiskRating;
  concerns: string[];
  recommendations: string[];
}

/**
 * Compliance analysis output from Compliance Officer Agent.
 *
 * Produced in Stage 2: Parallel Analysis
 * Maps to ComplianceReport in schemas.py
 */
export interface ComplianceReport {
  overall_status: ComplianceStatus;
  checks_performed: string[];  // Min length: 1
  violations: string[];
  warnings: string[];
  required_disclosures: string[];
  suitability_pass: boolean;
  concentration_limits_pass: boolean;
  notes?: string;
}

/**
 * Performance analysis output from Performance Analyst Agent.
 *
 * Produced in Stage 2: Parallel Analysis
 * Maps to PerformanceReport in schemas.py
 */
export interface PerformanceReport {
  total_return: number;  // Total portfolio return (%)
  benchmark_return: number;  // Benchmark return (%)
  excess_return: number;  // Return vs benchmark (%)
  sharpe_ratio: number;  // Risk-adjusted return (Sharpe ratio)
  alpha?: number;  // Portfolio alpha
  percentile_rank?: number;  // 1-100, peer percentile ranking
  attribution: Record<string, number>;  // Performance attribution by sector/asset class
  top_performers: string[];
  bottom_performers: string[];
}

// ============================================================================
// Synthesis & Suitability Models
// ============================================================================

/**
 * Client-portfolio suitability scoring.
 *
 * Calculated in Stage 3: Synthesis & Suitability Scoring
 * Maps to SuitabilityScore in schemas.py
 */
export interface SuitabilityScore {
  overall_score: number;  // 0-100
  risk_fit: number;  // 0-100
  compliance_fit: number;  // 0-100
  performance_fit: number;  // 0-100
  time_horizon_fit: number;  // 0-100
  interpretation: SuitabilityInterpretation;
  explanation: string;
}

// ============================================================================
// Final Recommendations Model
// ============================================================================

/**
 * Complete portfolio analysis with recommendations.
 *
 * Final output from Portfolio Manager Agent (Stage 4-5)
 * Maps to PortfolioRecommendations in schemas.py
 */
export interface PortfolioRecommendations {
  portfolio_id: string;
  client_id: string;
  analysis_date: string;  // ISO format datetime

  // Specialist outputs
  suitability_score: SuitabilityScore;
  risk_analysis: RiskAnalysis;
  compliance_report: ComplianceReport;
  performance_report: PerformanceReport;

  // Manager synthesis
  recommendations: string[];  // Min length: 1
  action_items: string[];
  next_review_date?: string;  // ISO format datetime

  // Summary
  executive_summary: string;
}

// ============================================================================
// Tool Input/Output Models
// ============================================================================

/**
 * Input for parallel specialist execution.
 * Maps to ParallelAnalysisInput in schemas.py
 */
export interface ParallelAnalysisInput {
  portfolio: Portfolio;
  client_profile: ClientProfile;
}

/**
 * Output from parallel specialist execution.
 * Maps to ParallelAnalysisOutput in schemas.py
 */
export interface ParallelAnalysisOutput {
  risk_analysis: RiskAnalysis;
  compliance_report: ComplianceReport;
  performance_report: PerformanceReport;
  execution_time_seconds: number;
}

// ============================================================================
// Equity Specialist Models (Handoff Agent)
// ============================================================================

/**
 * Request for equity specialist deep dive analysis.
 *
 * Used when handing off to Equity Specialist Agent
 * Maps to EquityDeepDiveRequest in schemas.py
 */
export interface EquityDeepDiveRequest {
  portfolio: Portfolio;
  client_profile: ClientProfile;
  focus_areas: string[];  // e.g., 'Valuation', 'Sector allocation'
  questions?: string[];
}

/**
 * Equity specialist deep dive analysis output.
 *
 * Returned from Equity Specialist Agent handoff
 * Maps to EquityDeepDiveReport in schemas.py
 */
export interface EquityDeepDiveReport {
  focus_areas_analyzed: string[];
  sector_analysis: Record<string, string>;  // Sector-by-sector analysis
  valuation_metrics: Record<string, number>;  // Portfolio-level valuation metrics (P/E, P/B, etc.)
  growth_vs_value_split: Record<string, number>;  // Growth vs Value allocation
  recommendations: string[];
  detailed_analysis: string;  // Comprehensive equity analysis narrative
}

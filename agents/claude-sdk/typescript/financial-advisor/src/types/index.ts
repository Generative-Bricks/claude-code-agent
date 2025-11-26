import { z } from 'zod';

// Risk tolerance levels
export const RiskToleranceSchema = z.enum(['conservative', 'moderate', 'aggressive']);
export type RiskTolerance = z.infer<typeof RiskToleranceSchema>;

// Annuity types
export const AnnuityTypeSchema = z.enum([
  'fixed',           // Fixed annuity - guaranteed rate
  'variable',        // Variable annuity - market-linked
  'indexed',         // Indexed annuity - market-indexed with floor
  'immediate',       // Immediate annuity - starts payments immediately
  'deferred'         // Deferred annuity - starts payments later
]);
export type AnnuityType = z.infer<typeof AnnuityTypeSchema>;

// Payout options
export const PayoutOptionSchema = z.enum([
  'life-only',              // Payments for life only
  'life-with-period',       // Life with period certain (e.g., 10, 20 years)
  'joint-life',             // Joint life (continues to spouse)
  'joint-life-survivor'     // Joint life with survivor benefits
]);
export type PayoutOption = z.infer<typeof PayoutOptionSchema>;

// Client profile for annuity analysis
export const ClientProfileSchema = z.object({
  name: z.string(),
  age: z.number().min(18).max(100),
  retirementAge: z.number().min(50).max(80).optional(),
  currentSavings: z.number().min(0),
  monthlyIncome: z.number().min(0),
  monthlyExpenses: z.number().min(0),
  riskTolerance: RiskToleranceSchema,
  taxBracket: z.number().min(0).max(0.50), // 0-50% as decimal
  healthStatus: z.enum(['excellent', 'good', 'fair', 'poor']).optional(),
  hasSpouse: z.boolean().default(false),
  spouseAge: z.number().min(18).max(100).optional(),
  existingAnnuities: z.number().default(0),
  investmentGoals: z.array(z.string()).default([])
});
export type ClientProfile = z.infer<typeof ClientProfileSchema>;

// Annuity product definition
export const AnnuityProductSchema = z.object({
  id: z.string(),
  name: z.string(),
  type: AnnuityTypeSchema,
  provider: z.string(),
  minimumPremium: z.number().min(0),
  currentRate: z.number().optional(), // For fixed annuities
  feePercentage: z.number().min(0).max(0.05), // Annual fee (0-5%)
  surrenderPeriod: z.number().min(0).max(15), // Years
  surrenderCharge: z.number().min(0).max(0.15), // Surrender charge (0-15%)
  riderOptions: z.array(z.string()).default([]),
  features: z.array(z.string()).default([])
});
export type AnnuityProduct = z.infer<typeof AnnuityProductSchema>;

// Portfolio allocation
export const PortfolioAllocationSchema = z.object({
  stocks: z.number().min(0).max(100),
  bonds: z.number().min(0).max(100),
  cash: z.number().min(0).max(100),
  annuities: z.number().min(0).max(100),
  other: z.number().min(0).max(100)
});
export type PortfolioAllocation = z.infer<typeof PortfolioAllocationSchema>;

// Annuity suitability assessment result
export const SuitabilityResultSchema = z.object({
  suitabilityScore: z.number().min(0).max(100),
  recommendedType: AnnuityTypeSchema,
  recommendedAllocationPercent: z.number().min(0).max(100),
  reasoning: z.string(),
  pros: z.array(z.string()),
  cons: z.array(z.string()),
  warnings: z.array(z.string()).default([])
});
export type SuitabilityResult = z.infer<typeof SuitabilityResultSchema>;

// Payout calculation result
export const PayoutCalculationSchema = z.object({
  monthlyPayout: z.number(),
  annualPayout: z.number(),
  totalLifetimePayout: z.number(),
  breakEvenAge: z.number(),
  assumptions: z.object({
    lifeExpectancy: z.number(),
    inflationRate: z.number(),
    growthRate: z.number().optional()
  })
});
export type PayoutCalculation = z.infer<typeof PayoutCalculationSchema>;

// Annuity comparison result
export const AnnuityComparisonSchema = z.object({
  fixedAnnuity: z.object({
    pros: z.array(z.string()),
    cons: z.array(z.string()),
    bestFor: z.string()
  }),
  variableAnnuity: z.object({
    pros: z.array(z.string()),
    cons: z.array(z.string()),
    bestFor: z.string()
  }),
  indexedAnnuity: z.object({
    pros: z.array(z.string()),
    cons: z.array(z.string()),
    bestFor: z.string()
  }),
  recommendation: z.string()
});
export type AnnuityComparison = z.infer<typeof AnnuityComparisonSchema>;

// Tax analysis result
export const TaxAnalysisSchema = z.object({
  taxDeferredGrowth: z.number(),
  estimatedTaxSavings: z.number(),
  rmdImplications: z.string(),
  qualifiedVsNonQualified: z.string(),
  recommendations: z.array(z.string())
});
export type TaxAnalysis = z.infer<typeof TaxAnalysisSchema>;

// Market rates data
export const MarketRatesSchema = z.object({
  fixedAnnuityRate: z.number(),
  variableAnnuityAvgReturn: z.number(),
  indexedAnnuityCap: z.number(),
  treasuryYield10Year: z.number(),
  inflationRate: z.number(),
  lastUpdated: z.string()
});
export type MarketRates = z.infer<typeof MarketRatesSchema>;

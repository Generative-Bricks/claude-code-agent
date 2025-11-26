import { tool, createSdkMcpServer } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';
import type {
  SuitabilityResult,
  PayoutCalculation,
  AnnuityComparison,
  TaxAnalysis
} from '../types/index.js';
import {
  sampleClients,
  sampleAnnuityProducts,
  currentMarketRates,
  samplePortfolioAllocations,
  getSampleClient
} from '../data/mock-portfolios.js';

/**
 * Tool 1: Analyze Annuity Suitability
 * Evaluates whether an annuity is suitable for a client based on their profile
 */
const analyzeSuitability = tool(
  'analyze_annuity_suitability',
  'Analyze whether an annuity is suitable for a specific client based on their age, risk tolerance, income needs, and financial goals',
  {
    clientName: z.string().describe('Name of the client or "sample-1", "sample-2", etc.'),
    considerationType: z.string().optional().describe('Type of annuity to consider: fixed, variable, indexed, immediate, or deferred')
  },
  async (args) => {
    // Find the client
    const client = getSampleClient(args.clientName) || sampleClients[0];

    // Calculate suitability score (0-100)
    let score = 50; // Base score
    const reasoning: string[] = [];
    const pros: string[] = [];
    const cons: string[] = [];
    const warnings: string[] = [];

    // Age-based scoring
    if (client.age >= 60 && client.age <= 75) {
      score += 20;
      reasoning.push(`Client age (${client.age}) is in optimal annuity range (60-75)`);
    } else if (client.age > 75) {
      score += 10;
      reasoning.push(`Client age (${client.age}) is above optimal range but still suitable`);
      warnings.push('Advanced age may limit payout options and increase costs');
    } else {
      score -= 10;
      reasoning.push(`Client age (${client.age}) is young for annuities; may have better growth options`);
    }

    // Risk tolerance based scoring
    if (client.riskTolerance === 'conservative') {
      score += 20;
      reasoning.push('Conservative risk tolerance aligns well with annuity guarantees');
      pros.push('Provides principal protection and guaranteed income');
    } else if (client.riskTolerance === 'moderate') {
      score += 10;
      reasoning.push('Moderate risk tolerance allows for both growth and guarantees');
      pros.push('Can balance growth potential with downside protection');
    } else {
      score -= 5;
      reasoning.push('Aggressive risk tolerance may be limited by annuity constraints');
      cons.push('Limited upside potential compared to direct market investing');
    }

    // Income needs assessment
    const incomeGap = client.monthlyExpenses - client.monthlyIncome;
    if (incomeGap > 0) {
      score += 25;
      reasoning.push(`Monthly income gap of $${incomeGap.toFixed(2)} makes annuity highly suitable`);
      pros.push('Addresses immediate income shortfall');
    } else if (incomeGap < -2000) {
      score -= 5;
      reasoning.push('Client has excess income; annuity less urgent');
    }

    // Existing annuities check
    const existingAnnuityPercent = (client.existingAnnuities / client.currentSavings) * 100;
    if (existingAnnuityPercent > 40) {
      score -= 15;
      reasoning.push(`${existingAnnuityPercent.toFixed(1)}% already in annuities; may be over-allocated`);
      warnings.push('High existing annuity allocation may reduce flexibility');
    }

    // Recommend annuity type based on client profile
    let recommendedType: 'fixed' | 'variable' | 'indexed' | 'immediate' | 'deferred';
    if (incomeGap > 0 && client.age >= 65) {
      recommendedType = 'immediate';
      pros.push('Immediate income start addresses current needs');
    } else if (client.riskTolerance === 'conservative') {
      recommendedType = 'fixed';
      pros.push('Fixed rate provides predictability and safety');
    } else if (client.riskTolerance === 'aggressive') {
      recommendedType = 'variable';
      pros.push('Variable annuity offers growth potential');
      cons.push('Market risk and higher fees');
    } else {
      recommendedType = 'indexed';
      pros.push('Indexed annuity balances growth and protection');
    }

    // Calculate recommended allocation
    let recommendedAllocation = 0;
    if (client.age >= 70) {
      recommendedAllocation = 25 + (client.riskTolerance === 'conservative' ? 10 : 0);
    } else if (client.age >= 60) {
      recommendedAllocation = 15 + (client.riskTolerance === 'conservative' ? 10 : 0);
    } else {
      recommendedAllocation = 5 + (client.riskTolerance === 'conservative' ? 5 : 0);
    }

    // Add general pros/cons
    pros.push('Tax-deferred growth during accumulation phase');
    pros.push('Protection from longevity risk');
    cons.push('Limited liquidity due to surrender charges');
    cons.push('Complexity and fees can be high');

    const result: SuitabilityResult = {
      suitabilityScore: Math.min(100, Math.max(0, score)),
      recommendedType,
      recommendedAllocationPercent: recommendedAllocation,
      reasoning: reasoning.join('; '),
      pros,
      cons,
      warnings
    };

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(result, null, 2)
      }]
    };
  }
);

/**
 * Tool 2: Calculate Annuity Payout
 * Calculates estimated monthly and annual payouts for different annuity structures
 */
const calculatePayout = tool(
  'calculate_annuity_payout',
  'Calculate estimated monthly and annual payouts for an annuity based on premium amount, age, and payout options',
  {
    premiumAmount: z.number().min(10000).describe('Initial premium amount to invest'),
    clientAge: z.number().min(50).max(90).describe('Current age of the client'),
    annuityType: z.enum(['fixed', 'variable', 'indexed', 'immediate', 'deferred']).describe('Type of annuity'),
    payoutOption: z.enum(['life-only', 'life-with-period', 'joint-life', 'joint-life-survivor']).describe('Payout structure'),
    deferralYears: z.number().min(0).max(30).default(0).describe('Years to defer before payments start')
  },
  async (args) => {
    // Life expectancy table (simplified)
    const lifeExpectancy = 85 + (args.clientAge < 70 ? 3 : 0);

    // Calculate payout rate based on age and type
    let payoutRate = 0.045; // Base rate (4.5%)

    // Age adjustments (older = higher payout)
    if (args.clientAge >= 75) payoutRate += 0.020;
    else if (args.clientAge >= 70) payoutRate += 0.015;
    else if (args.clientAge >= 65) payoutRate += 0.010;
    else if (args.clientAge >= 60) payoutRate += 0.005;

    // Annuity type adjustments
    if (args.annuityType === 'immediate') payoutRate += 0.005;
    if (args.annuityType === 'variable') payoutRate += 0.015; // Higher potential
    if (args.annuityType === 'indexed') payoutRate += 0.008;

    // Payout option adjustments
    if (args.payoutOption === 'life-only') payoutRate += 0.010; // Highest payout
    if (args.payoutOption === 'joint-life' || args.payoutOption === 'joint-life-survivor') payoutRate -= 0.010;
    if (args.payoutOption === 'life-with-period') payoutRate -= 0.005;

    // Account for deferral (accumulation period)
    let accumulatedValue = args.premiumAmount;
    if (args.deferralYears > 0) {
      const growthRate = args.annuityType === 'variable' ? 0.068 :
                        args.annuityType === 'indexed' ? 0.050 : 0.045;
      accumulatedValue = args.premiumAmount * Math.pow(1 + growthRate, args.deferralYears);
    }

    // Calculate payouts
    const annualPayout = accumulatedValue * payoutRate;
    const monthlyPayout = annualPayout / 12;

    // Estimate lifetime payout
    const yearsOfPayouts = lifeExpectancy - (args.clientAge + args.deferralYears);
    const totalLifetimePayout = annualPayout * yearsOfPayouts;

    // Calculate break-even age
    const breakEvenAge = args.clientAge + args.deferralYears + (accumulatedValue / annualPayout);

    const result: PayoutCalculation = {
      monthlyPayout,
      annualPayout,
      totalLifetimePayout,
      breakEvenAge: Math.round(breakEvenAge),
      assumptions: {
        lifeExpectancy,
        inflationRate: currentMarketRates.inflationRate,
        growthRate: args.deferralYears > 0 ? (args.annuityType === 'variable' ? 0.068 : 0.045) : undefined
      }
    };

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(result, null, 2)
      }]
    };
  }
);

/**
 * Tool 3: Compare Annuity Types
 * Provides a detailed comparison of fixed, variable, and indexed annuities
 */
const compareAnnuityTypes = tool(
  'compare_annuity_types',
  'Compare fixed, variable, and indexed annuities with pros, cons, and recommendations based on client goals',
  {
    clientGoals: z.string().describe('Primary investment goals (e.g., "income security", "growth potential", "inflation protection")'),
    riskTolerance: z.enum(['conservative', 'moderate', 'aggressive']).describe('Client risk tolerance level')
  },
  async (args) => {
    const comparison: AnnuityComparison = {
      fixedAnnuity: {
        pros: [
          'Guaranteed fixed rate of return (currently ~4.5%)',
          'No market risk - principal and earnings protected',
          'Predictable, stable income',
          'Lower fees compared to other types',
          'Simple to understand'
        ],
        cons: [
          'No inflation protection',
          'Limited growth potential',
          'Returns may lag behind market in bull markets',
          'Surrender charges if withdrawn early'
        ],
        bestFor: 'Conservative investors seeking guaranteed income and principal protection. Ideal for those prioritizing safety over growth.'
      },
      variableAnnuity: {
        pros: [
          'Market participation through subaccounts',
          'Higher growth potential (historical avg ~6.8%)',
          'Tax-deferred growth',
          'Death benefit protection',
          'Multiple investment options',
          'Potential for inflation protection through growth'
        ],
        cons: [
          'Market risk - value can decline',
          'Higher fees (typically 2-3% annually)',
          'Complex with many riders and options',
          'Requires active management',
          'Surrender charges and long commitment periods'
        ],
        bestFor: 'Moderate to aggressive investors comfortable with market risk. Best for those with longer time horizons seeking growth.'
      },
      indexedAnnuity: {
        pros: [
          'Upside market participation (typically capped at 6%)',
          'Downside protection (0% floor)',
          'No direct market risk',
          'Better inflation protection than fixed',
          'Moderate fees',
          'Good balance of risk and reward'
        ],
        cons: [
          'Cap rates limit upside potential',
          'Complex crediting methods',
          'Longer surrender periods (often 10+ years)',
          'May underperform in strong bull markets',
          'Less predictable than fixed annuities'
        ],
        bestFor: 'Moderate risk investors wanting market participation with protection. Ideal for those seeking balance between fixed and variable.'
      },
      recommendation: ''
    };

    // Generate recommendation based on inputs
    if (args.riskTolerance === 'conservative') {
      comparison.recommendation = `Based on your conservative risk tolerance and goals of "${args.clientGoals}", a FIXED ANNUITY is recommended. ` +
        'It provides the guaranteed income and principal protection that align with your needs. The predictability and simplicity make it easy to plan retirement income.';
    } else if (args.riskTolerance === 'aggressive') {
      comparison.recommendation = `Based on your aggressive risk tolerance and goals of "${args.clientGoals}", a VARIABLE ANNUITY is recommended. ` +
        'It offers the growth potential needed to meet your objectives. While there is market risk, the tax-deferred growth and upside potential align with your profile.';
    } else {
      comparison.recommendation = `Based on your moderate risk tolerance and goals of "${args.clientGoals}", an INDEXED ANNUITY is recommended. ` +
        'It provides the optimal balance between growth potential and downside protection. The 0% floor protects your principal while the cap allows for meaningful growth in positive markets.';
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(comparison, null, 2)
      }]
    };
  }
);

/**
 * Tool 4: Assess Portfolio Allocation
 * Analyzes current portfolio and recommends optimal annuity allocation percentage
 */
const assessPortfolioAllocation = tool(
  'assess_portfolio_allocation',
  'Analyze a client portfolio and recommend optimal annuity allocation based on age, risk profile, and existing holdings',
  {
    clientAge: z.number().min(18).max(100).describe('Client current age'),
    totalPortfolioValue: z.number().min(0).describe('Total portfolio value'),
    currentAllocation: z.object({
      stocks: z.number(),
      bonds: z.number(),
      cash: z.number(),
      annuities: z.number(),
      other: z.number()
    }).describe('Current portfolio allocation percentages'),
    riskTolerance: z.enum(['conservative', 'moderate', 'aggressive']).describe('Risk tolerance')
  },
  async (args) => {
    const current = args.currentAllocation;

    // Get recommended allocation based on risk profile and age
    let recommendedTemplate = samplePortfolioAllocations.moderate;
    if (args.clientAge >= 70) {
      recommendedTemplate = samplePortfolioAllocations.retirement;
    } else if (args.riskTolerance === 'conservative') {
      recommendedTemplate = samplePortfolioAllocations.conservative;
    } else if (args.riskTolerance === 'aggressive' && args.clientAge < 60) {
      recommendedTemplate = samplePortfolioAllocations.aggressive;
    }

    // Age-based adjustments
    const recommended = { ...recommendedTemplate };
    if (args.clientAge >= 70) {
      recommended.annuities = Math.min(40, recommended.annuities + 10);
      recommended.stocks = Math.max(15, recommended.stocks - 5);
    } else if (args.clientAge >= 65) {
      recommended.annuities = Math.min(30, recommended.annuities + 5);
    }

    // Calculate recommendations
    const annuityDifference = recommended.annuities - current.annuities;
    const annuityDollarAmount = (annuityDifference / 100) * args.totalPortfolioValue;

    const analysis: {
      currentAllocation: typeof current;
      recommendedAllocation: typeof recommended;
      analysis: {
        currentAnnuityPercent: number;
        recommendedAnnuityPercent: number;
        difference: number;
        dollarAmount: number;
        reasoning: string[];
      };
      actions: string[];
    } = {
      currentAllocation: current,
      recommendedAllocation: recommended,
      analysis: {
        currentAnnuityPercent: current.annuities,
        recommendedAnnuityPercent: recommended.annuities,
        difference: annuityDifference,
        dollarAmount: annuityDollarAmount,
        reasoning: []
      },
      actions: []
    };

    // Generate reasoning
    if (annuityDifference > 5) {
      analysis.analysis.reasoning.push(
        `Recommended to increase annuity allocation by ${annuityDifference.toFixed(1)}% (approximately $${Math.abs(annuityDollarAmount).toLocaleString()})`
      );
      analysis.analysis.reasoning.push(
        `Age ${args.clientAge} and ${args.riskTolerance} risk profile suggest higher guaranteed income allocation`
      );
      analysis.actions.push(`Consider allocating $${Math.abs(annuityDollarAmount).toLocaleString()} to an appropriate annuity product`);
      analysis.actions.push('Prioritize immediate or short-deferral period annuities if income is needed soon');
    } else if (annuityDifference < -5) {
      analysis.analysis.reasoning.push(
        `Current annuity allocation (${current.annuities}%) is higher than recommended (${recommended.annuities}%)`
      );
      analysis.analysis.reasoning.push('May have reduced flexibility and liquidity');
      analysis.actions.push('Avoid additional annuity purchases at this time');
      analysis.actions.push('Consider more liquid assets for emergency fund needs');
    } else {
      analysis.analysis.reasoning.push('Current annuity allocation is appropriate for your profile');
      analysis.actions.push('Maintain current allocation strategy');
    }

    // Additional analysis based on total allocation
    if (current.stocks > 70 && args.clientAge >= 60) {
      analysis.analysis.reasoning.push('High stock allocation may be aggressive for age');
      analysis.actions.push('Consider rebalancing some equities into annuities or bonds');
    }

    if (current.cash > 20) {
      analysis.analysis.reasoning.push('High cash allocation may be underperforming');
      analysis.actions.push('Consider deploying excess cash into annuities for better returns');
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(analysis, null, 2)
      }]
    };
  }
);

/**
 * Tool 5: Evaluate Tax Implications
 * Analyzes tax-deferred growth benefits and RMD implications of annuities
 */
const evaluateTaxImplications = tool(
  'evaluate_tax_implications',
  'Analyze tax implications of annuity investments including tax-deferred growth, RMDs, and qualified vs non-qualified considerations',
  {
    investmentAmount: z.number().min(0).describe('Amount to invest in annuity'),
    clientAge: z.number().min(18).max(100).describe('Current age'),
    currentTaxBracket: z.number().min(0).max(0.50).describe('Current tax bracket as decimal (e.g., 0.24 for 24%)'),
    yearsUntilWithdrawal: z.number().min(0).max(40).describe('Years until planning to withdraw'),
    isQualified: z.boolean().default(false).describe('Is this a qualified (IRA/401k) annuity?')
  },
  async (args) => {
    const growthRate = 0.048; // Conservative growth estimate

    // Calculate tax-deferred growth
    const futureValue = args.investmentAmount * Math.pow(1 + growthRate, args.yearsUntilWithdrawal);
    const totalGrowth = futureValue - args.investmentAmount;

    // Calculate what growth would be in taxable account (taxed annually)
    const afterTaxGrowthRate = growthRate * (1 - args.currentTaxBracket);
    const taxableAccountValue = args.investmentAmount * Math.pow(1 + afterTaxGrowthRate, args.yearsUntilWithdrawal);

    // Tax savings from deferral
    const taxSavings = futureValue - taxableAccountValue;

    // RMD implications
    const rmdAge = 73; // Current RMD age
    let rmdImplications = '';
    if (args.isQualified) {
      if (args.clientAge + args.yearsUntilWithdrawal >= rmdAge) {
        rmdImplications = `As a qualified annuity, Required Minimum Distributions (RMDs) will begin at age ${rmdAge}. ` +
          `This will be approximately ${Math.round(args.clientAge + args.yearsUntilWithdrawal - rmdAge)} years after withdrawal begins. ` +
          'RMDs are calculated based on IRS life expectancy tables and must be withdrawn annually to avoid penalties.';
      } else {
        rmdImplications = `RMDs will not be required until age ${rmdAge}, which is ${rmdAge - (args.clientAge + args.yearsUntilWithdrawal)} years after planned withdrawal.`;
      }
    } else {
      rmdImplications = 'As a non-qualified annuity, RMDs do not apply. However, withdrawals are taxed as ordinary income to the extent of gains (LIFO - Last In First Out).';
    }

    // Qualified vs Non-Qualified analysis
    const qualifiedAnalysis = args.isQualified
      ? 'QUALIFIED ANNUITY: Contributions may be tax-deductible (if within IRA/401k limits). All withdrawals (principal + gains) are taxed as ordinary income. ' +
        'Subject to RMD requirements at age 73. Early withdrawal before 59½ may incur 10% penalty plus taxes.'
      : 'NON-QUALIFIED ANNUITY: Contributions are made with after-tax dollars (not deductible). Only earnings are taxable upon withdrawal (LIFO taxation). ' +
        'No RMD requirements. More flexible for withdrawals before age 59½ (no 10% penalty on principal).';

    const recommendations = [
      `Tax-deferred growth provides an estimated $${Math.round(taxSavings).toLocaleString()} advantage over ${args.yearsUntilWithdrawal} years`,
      'Consider timing of withdrawals to optimize tax brackets',
      args.currentTaxBracket > 0.24
        ? 'High tax bracket makes tax deferral especially valuable'
        : 'Consider if current low tax bracket suggests Roth conversion might be beneficial',
      args.isQualified && args.clientAge + args.yearsUntilWithdrawal < rmdAge
        ? 'Plan withdrawal strategy before RMDs begin to maintain tax control'
        : 'Structure withdrawals to stay within desired tax bracket',
      !args.isQualified
        ? 'Non-qualified annuity provides more flexibility for accessing principal without penalties'
        : 'Be mindful of early withdrawal penalties if funds needed before 59½'
    ];

    const result: TaxAnalysis = {
      taxDeferredGrowth: totalGrowth,
      estimatedTaxSavings: taxSavings,
      rmdImplications,
      qualifiedVsNonQualified: qualifiedAnalysis,
      recommendations
    };

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(result, null, 2)
      }]
    };
  }
);

/**
 * Tool 6: Fetch Annuity Rates (Mock with future API hooks)
 * Returns current market rates for annuity products
 */
const fetchAnnuityRates = tool(
  'fetch_annuity_rates',
  'Fetch current annuity rates and market data (currently returns mock data with hooks for future real API integration)',
  {
    rateType: z.enum(['all', 'fixed', 'indexed', 'immediate']).default('all').describe('Type of rates to fetch')
  },
  async (args) => {
    // This is mock data now, but structured for easy API integration later
    const rates = {
      marketData: currentMarketRates,
      products: args.rateType === 'all'
        ? sampleAnnuityProducts
        : sampleAnnuityProducts.filter(p => p.type === args.rateType),
      note: 'Mock data for development. Future integration point for real-time rate APIs.',
      apiIntegrationReady: {
        fixedRates: 'https://api.example.com/annuity-rates/fixed',
        variableRates: 'https://api.example.com/annuity-rates/variable',
        indexedRates: 'https://api.example.com/annuity-rates/indexed',
        marketData: 'https://api.example.com/market-data'
      }
    };

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(rates, null, 2)
      }]
    };
  }
);

// Create and export the MCP server with all annuity tools
export const annuityToolsServer = createSdkMcpServer({
  name: 'annuity-tools',
  version: '1.0.0',
  tools: [
    analyzeSuitability,
    calculatePayout,
    compareAnnuityTypes,
    assessPortfolioAllocation,
    evaluateTaxImplications,
    fetchAnnuityRates
  ]
});

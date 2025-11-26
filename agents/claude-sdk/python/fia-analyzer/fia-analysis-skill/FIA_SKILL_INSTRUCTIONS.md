# How to Use the FIA Product Analyzer Skill

## What This Skill Does

The **FIA Product Analyzer** skill provides a complete framework for analyzing Fixed Indexed Annuities (FIAs). It will help you:

✅ Gather comprehensive product data (surrender charges, index options, crediting methods, riders, fees)
✅ Create detailed product analysis documents (both Markdown and PDF)
✅ Run 40-question suitability assessments with smart scoring that handles missing data
✅ Generate "good fit" vs "not a good fit" profiles
✅ Provide realistic return expectations and critical disclosures
✅ Output professional documents for internal use or advisor presentations

---

## How to Install the Skill

### Option 1: Copy & Paste (Simplest)
1. Open a new chat with Claude
2. Copy the entire contents of `fia-product-analyzer-skill/SKILL.md`
3. Say: "I want to add this as a skill to my account. Please help me package it."
4. Claude will guide you through the process

### Option 2: Upload Directly
1. In Claude Settings → Skills
2. Click "Create Skill" or "Upload Skill"
3. Upload the `fia-product-analyzer-skill/SKILL.md` file
4. Follow prompts to complete setup

---

## How to Use the Skill

Once installed, the skill automatically activates when you ask questions about FIA analysis:

### Example Prompts That Trigger the Skill:

**Single Product Analysis:**
- "Analyze the Allianz Benefit Control FIA"
- "Give me a complete analysis of the Nationwide Peak 10 annuity"
- "Create a product profile for the Lincoln OptiBlend 10"
- "I need detailed information on the F&G Prosperity Elite FIA"

**Suitability Assessment:**
- "Is the Allianz 222 suitable for a 62-year-old conservative investor with $50k to invest?"
- "Run a suitability check for my client against the MassMutual Stable Voyage"
- "Score this prospect for the Athene Performance Elite 10"

**Comparison Preparation:**
- "Analyze these three FIAs: [Product A], [Product B], [Product C]"
- "Create product profiles for all major carriers' 10-year FIAs"

### What You'll Get:

1. **Markdown Document** (.md file)
   - LLM-friendly format
   - Easy to parse and analyze
   - Can be used with other AI tools
   - Full text searchable

2. **PDF Document** (.pdf file)
   - Professional formatting
   - Ready for presentations
   - Printable for client meetings
   - Brand-appropriate styling

3. **40-Question Suitability Assessment**
   - YES/NO/N/A format
   - Smart scoring (only counts answerable questions)
   - Percentage-based result
   - Clear interpretation (Highly Suitable → Not Suitable)

---

## Understanding the Suitability Scoring

### How It Works:

The scoring system is designed to handle **incomplete client data**:

```
Score = (Total YES answers ÷ Total Answerable Questions) × 100
```

**Key Feature:** Questions without sufficient data are marked "N/A" and excluded from BOTH the numerator and denominator.

### Example:

**Scenario:**
- 40 total questions
- You can only answer 30 questions (missing data on 10)
- Of the 30 answerable questions, 24 are YES

**Calculation:**
- Score = (24 ÷ 30) × 100 = **80%**
- Result: **Highly Suitable**

### Score Interpretation:

| Score Range | Interpretation | Action |
|-------------|----------------|--------|
| 80-100% | Highly Suitable | Proceed with confidence |
| 60-79% | Suitable | Proceed with discussion of concerns |
| 40-59% | Marginal Fit | Detailed review required |
| Below 40% | Not Suitable | Recommend alternatives |

---

## Tips for Best Results

### 1. Be Specific with Product Names
✅ Good: "Analyze the Allianz Benefit Control FIA"
❌ Vague: "Tell me about Allianz annuities"

### 2. Provide Client Context When Assessing Suitability
Include relevant details like:
- Age
- Risk tolerance
- Investment goals
- Liquidity needs
- Current portfolio
- Timeline

### 3. Request Both Formats
Say: "I need both the PDF and Markdown versions"

### 4. Ask for Updates
If product information changes, say: "Update this analysis with current rates"

---

## Sample Workflow

### Complete Analysis Workflow:

**Step 1: Initial Request**
```
"I need a complete analysis of the Nationwide Peak 10 FIA with both 
PDF and markdown outputs."
```

**Step 2: Claude will:**
- Search for current product information
- Gather all data points (surrender charges, index options, riders, etc.)
- Create comprehensive markdown document
- Generate professional PDF
- Save both to `/mnt/user-data/outputs/`
- Provide download links

**Step 3: Review & Adjust**
```
"Can you also run a suitability assessment for a 58-year-old 
conservative investor with $75k who needs some liquidity?"
```

**Step 4: Get Scoring**
Claude will answer all 40 questions based on provided information, calculate score, and provide recommendation.

---

## Advanced Usage

### Comparing Multiple Products

```
"Create separate analyses for:
1. Allianz Benefit Control
2. Nationwide Peak 10
3. Lincoln OptiBlend 10

Then create a comparison summary table."
```

### Custom Questionnaire

```
"Use the standard 40-question assessment but add 5 custom questions 
specific to my client's situation regarding estate planning."
```

### Historical Analysis

```
"Analyze the [Product Name] and include how surrender charges and 
rates have changed over the past 2 years."
```

---

## What the Skill Includes

### Data Points Collected:

1. **Product Basics** - Name, issuer, term, minimum premium
2. **Surrender Charges** - Full schedule, MVA provisions, free withdrawals
3. **Index Options** - All available indexes with descriptions
4. **Crediting Methods** - Point-to-point, averaging, caps, participation rates
5. **Current Rates** - Caps, participation rates, fixed rates (when available)
6. **Riders** - Built-in and optional, with costs
7. **Special Features** - Index lock, bonuses, unique capabilities
8. **Commission Structure** - Typical ranges
9. **Company Info** - Financial strength, market position

### Analysis Sections:

- Executive Summary
- Detailed Data Points
- Suitability Analysis (Good Fit / Not a Fit)
- 40-Question Suitability Questionnaire
- Score Interpretation & Recommendations
- Critical Considerations & Disclosures
- Realistic Return Expectations
- Summary Recommendation Framework

---

## Common Use Cases

### For Financial Advisors:
- Product due diligence
- Client suitability determination
- Internal training materials
- Compliance documentation
- Client presentation materials

### For Internal Analysis:
- Product comparison research
- Competitive intelligence
- Rate shopping
- Feature benchmarking
- Portfolio construction

### For LLM/Agent Integration:
- Automated product recommendations
- Client matching algorithms
- Portfolio optimization
- Compliance checking
- Knowledge base building

---

## Troubleshooting

**Q: The skill doesn't trigger when I ask about an annuity**
A: Make sure you mention it's a "Fixed Indexed Annuity" or "FIA" and include specific product name

**Q: Some data is missing from the analysis**
A: This is normal - not all product information is publicly available. The skill notes what's missing and marks related questions as N/A

**Q: The PDF formatting looks off**
A: Make sure you have the latest version of the skill. You can also request specific formatting preferences

**Q: How do I update rates for an existing analysis?**
A: Say "Update the [Product Name] analysis with current rates" and provide the date

**Q: Can I modify the 40 questions?**
A: Yes! The skill is flexible. Just tell Claude which questions to add/remove/modify

---

## Support and Updates

### Getting Help:
- Ask Claude: "How do I use the FIA Product Analyzer skill?"
- Request examples: "Show me an example of how to analyze an FIA product"
- Clarify scoring: "Explain how the suitability scoring works"

### Suggesting Improvements:
If you notice the skill could be improved, you can:
1. Request modifications in your chat
2. Ask Claude to update the skill with new features
3. Provide feedback on what's missing or confusing

---

## Quick Start Template

Copy and paste this into a new Claude chat after installing the skill:

```
I need a complete Fixed Indexed Annuity analysis for [Product Name].

Please provide:
1. Comprehensive product analysis with all data points
2. 40-question suitability assessment
3. Both Markdown and PDF formats
4. Realistic return expectations
5. Good fit vs not a fit analysis

[Optional: Include client context]
Client Profile:
- Age: [age]
- Risk Tolerance: [conservative/moderate/aggressive]
- Investment Amount: $[amount]
- Goals: [income/growth/both]
- Timeline: [years]
- Liquidity Needs: [high/medium/low]
```

---

## Next Steps

1. **Install the skill** using one of the methods above
2. **Try a test analysis** on a product you're familiar with
3. **Review the output** to understand the format and depth
4. **Iterate and customize** based on your specific needs
5. **Build your product library** by analyzing multiple FIAs

---

**Ready to get started?** Just upload the skill file to Claude and start analyzing!

*For questions or support, ask Claude directly in your chat.*

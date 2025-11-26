# QUICK START: Use This Prompt in a New Chat

Copy and paste this entire message into a new Claude chat to start using the FIA Product Analyzer:

---

## Prompt to Copy:

```
I want to analyze Fixed Indexed Annuities using a comprehensive framework. 

Here's the skill I want you to use:

[PASTE THE CONTENTS OF fia-product-analyzer-skill/SKILL.md HERE]

Now that you have the skill, please analyze: [PRODUCT NAME]

I need:
1. Complete product analysis with all data points
2. Surrender charges, index options, crediting methods, riders, fees
3. 40-question suitability assessment 
4. Both Markdown (.md) and PDF formats
5. Realistic return expectations
6. Good fit vs not a fit profiles

[OPTIONAL - Add client context for suitability assessment:]
Client Profile:
- Age: [X]
- Risk Tolerance: [conservative/moderate/aggressive]
- Investment Amount: $[X]
- Primary Goal: [income/growth/both]
- Timeline: [X] years
- Liquidity Needs: [high/medium/low]
- Current Portfolio: [description]
- Other relevant factors: [details]

Please provide both documents with download links when complete.
```

---

## Alternative: Shorter Version

If you just want a quick analysis without the full skill installation:

```
Please analyze the [PRODUCT NAME] Fixed Indexed Annuity.

Include:
- Surrender charges and fees
- Index options and crediting methods  
- Riders and benefits
- Realistic return expectations (2-6% range typical)
- Who is this a good fit for?
- Who is this NOT a good fit for?
- 40-question suitability assessment with YES/NO/N/A scoring
- Output in both Markdown and PDF formats

Suitability Scoring Formula:
Score = (Total YES ÷ Total Answerable Questions) × 100
- Exclude N/A from both numerator and denominator
- 80-100% = Highly Suitable
- 60-79% = Suitable
- 40-59% = Marginal
- <40% = Not Suitable

[Add client context if assessing suitability]
```

---

## Pro Tips:

1. **For Multiple Products:**
   Add: "Repeat this analysis for [Product 2], [Product 3], etc."

2. **For Comparison:**
   Add: "Then create a comparison table highlighting key differences"

3. **For Current Rates:**
   Add: "Search for the most current rates as of today"

4. **For Missing Data:**
   Claude will automatically mark questions as N/A when data isn't available

5. **For Custom Questions:**
   Add: "Include these additional suitability questions: [your questions]"

---

## What You'll Get:

✅ Comprehensive markdown document (LLM-friendly)
✅ Professional PDF (presentation-ready)
✅ 40-question assessment with smart scoring
✅ Clear suitability recommendations
✅ Realistic expectations and critical disclosures
✅ Direct download links to both files

---

**Ready to start?** Copy the prompt above into a new Claude chat!

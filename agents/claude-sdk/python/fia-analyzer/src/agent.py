"""
FIA Analyzer Agent

Main agent implementation using Claude SDK with skills container integration.
Implements a 5-stage workflow for analyzing Fixed Indexed Annuity products.

Stages:
1. Discovery - Understand what the user wants
2. Search - Find relevant FIA products
3. Fetch & Extract - Get detailed product information
4. Analyze - Perform suitability analysis if client profile provided
5. Generate Report - Use PDF skill and custom FIA skill to create report

Biblical Principle: TRUTH - Every decision is observable and explainable
Biblical Principle: EXCELLENCE - Production-grade from inception
"""

import os
import json
import logging
from typing import Optional, Dict, Any, List
from anthropic import Anthropic
from dotenv import load_dotenv

from src.tools.search_fia_products import search_fia_products
from src.tools.extract_fia_rates import extract_fia_rates
from src.tools.analyze_product_fit import analyze_product_fit
from src.models import FIAProduct, ClientProfile, SuitabilityScore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FIAAnalyzerAgent:
    """
    FIA Analyzer Agent with Claude SDK integration.

    This agent specializes in analyzing Fixed Indexed Annuity products using:
    - Custom tools for product search, rate extraction, and suitability analysis
    - Anthropic's PDF skill for document processing
    - Custom FIA Analysis Skill for specialized reporting
    - MCP Fetch tool for web content retrieval

    Attributes:
        client: Anthropic API client
        fia_skill_id: Custom FIA Analysis skill ID (if configured)
        model: Claude model to use (defaults to claude-sonnet-4-5-20250929)
    """

    def __init__(self):
        """
        Initialize the FIA Analyzer Agent.

        Loads configuration from environment variables:
        - ANTHROPIC_API_KEY (required)
        - FIA_SKILL_ID (optional - for custom skill integration)
        - CLAUDE_MODEL (optional - defaults to claude-sonnet-4-5-20250929)

        Raises:
            ValueError: If ANTHROPIC_API_KEY is not found in environment
        """
        # Load environment variables
        load_dotenv()

        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        self.fia_skill_id = os.getenv("FIA_SKILL_ID", "")
        self.model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")

        # Biblical Principle: EXCELLENCE - Validate configuration from start
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found in environment. "
                "Please set it in .env file or environment variables."
            )

        # Initialize Claude client with Skills beta header (per cookbook)
        self.client = Anthropic(
            api_key=self.api_key,
            default_headers={"anthropic-beta": "skills-2025-10-02"}
        )

        logger.info(f"FIA Analyzer Agent initialized with model: {self.model}")
        if self.fia_skill_id:
            logger.info(f"Custom FIA skill configured: {self.fia_skill_id}")
        else:
            logger.info("Custom FIA skill not configured (FIA_SKILL_ID empty)")

    def _build_skills_container(self) -> List[Dict[str, Any]]:
        """
        Build the skills container configuration.

        Includes:
        - Anthropic's PDF skill (always)
        - Custom FIA Analysis skill (if FIA_SKILL_ID configured)

        Returns:
            List of skill configurations for Claude API
        """
        skills = [
            {
                "type": "anthropic",
                "skill_id": "pdf",
                "version": "latest"
            }
        ]

        # Only add custom skill if ID is provided
        if self.fia_skill_id:
            skills.append({
                "type": "custom",
                "skill_id": self.fia_skill_id,
                "version": "latest"
            })
            logger.debug(f"Added custom FIA skill to container: {self.fia_skill_id}")

        return skills

    def _build_tools_schema(self) -> List[Dict[str, Any]]:
        """
        Build tool schemas for Claude API.

        Includes:
        - code_execution: Required for Skills beta
        - search_fia_products: Search for FIA products
        - extract_fia_rates: Parse product information from markdown
        - analyze_product_fit: Analyze suitability for client
        - mcp__fetch__fetch: Fetch web content (from MCP)

        Returns:
            List of tool schemas in Claude API format
        """
        return [
            # REQUIRED: code_execution tool for Skills beta
            {
                "type": "code_execution_20250825",
                "name": "code_execution"
            },
            {
                "name": "search_fia_products",
                "description": "Search for Fixed Indexed Annuity products by name and optionally filter by carrier. Returns product name, carrier, URL, and summary.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "product_name": {
                            "type": "string",
                            "description": "Name of the FIA product to search for (e.g., 'Allianz Benefit Control', 'Nationwide Peak')"
                        },
                        "carrier": {
                            "type": "string",
                            "description": "Optional insurance carrier name to filter results (e.g., 'Allianz Life', 'Nationwide')"
                        }
                    },
                    "required": ["product_name"]
                }
            },
            {
                "name": "extract_fia_rates",
                "description": "Extract FIA product rates and features from markdown content (from web pages or documents). Parses cap rates, participation rates, surrender charges, index options, and special features.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "markdown_content": {
                            "type": "string",
                            "description": "Markdown text containing product information (from web page or rate sheet)"
                        },
                        "product_name": {
                            "type": "string",
                            "description": "Name of the product being extracted (for error messages and metadata)"
                        }
                    },
                    "required": ["markdown_content", "product_name"]
                }
            },
            {
                "name": "analyze_product_fit",
                "description": "Analyze FIA product suitability for a client using structured suitability framework. Evaluates financial capacity, time horizon, risk tolerance, investment objectives, and product understanding.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "product": {
                            "type": "object",
                            "description": "FIA product data (from extract_fia_rates output)"
                        },
                        "client_profile": {
                            "type": "object",
                            "description": "Client profile data including age, assets, risk tolerance, objectives, etc."
                        }
                    },
                    "required": ["product", "client_profile"]
                }
            },
            {
                "name": "mcp__fetch__fetch",
                "description": "Fetch content from a URL and convert to markdown. Use this to retrieve FIA product information from carrier websites or rate sheet URLs.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "url": {
                            "type": "string",
                            "description": "URL to fetch content from"
                        },
                        "max_length": {
                            "type": "integer",
                            "description": "Maximum number of characters to return (default: 5000)"
                        }
                    },
                    "required": ["url"]
                }
            }
        ]

    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Any:
        """
        Execute a tool function.

        Routes tool calls to the appropriate Python function or MCP server.

        Args:
            tool_name: Name of the tool to execute
            tool_input: Tool input parameters

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool is not found or execution fails
        """
        logger.info(f"Executing tool: {tool_name}")
        logger.debug(f"Tool input: {tool_input}")

        try:
            if tool_name == "search_fia_products":
                return search_fia_products(**tool_input)

            elif tool_name == "extract_fia_rates":
                product = extract_fia_rates(**tool_input)
                # Convert Pydantic model to dict for JSON serialization
                return product.model_dump()

            elif tool_name == "analyze_product_fit":
                # Convert dict inputs back to Pydantic models
                product = FIAProduct(**tool_input["product"])
                client_profile = ClientProfile(**tool_input["client_profile"])
                score = analyze_product_fit(product, client_profile)
                # Convert result to dict
                return score.model_dump()

            elif tool_name == "mcp__fetch__fetch":
                # MCP tool - would be handled by Claude SDK automatically
                # For now, return placeholder
                logger.warning(f"MCP tool {tool_name} called - should be handled by Claude SDK")
                return {"error": "MCP tools are handled by Claude SDK, not directly in agent"}

            else:
                raise ValueError(f"Unknown tool: {tool_name}")

        except Exception as e:
            logger.error(f"Tool execution failed for {tool_name}: {e}")
            raise

    def analyze_product(
        self,
        product_name: str,
        carrier: Optional[str] = None,
        client_profile_dict: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main entry point for analyzing an FIA product.

        Implements 5-stage workflow:
        1. Discovery - Understand what user wants
        2. Search - Find relevant FIA products
        3. Fetch & Extract - Get detailed product information
        4. Analyze - Perform suitability analysis (if client profile provided)
        5. Generate Report - Use Claude skills to create final report

        Args:
            product_name: Name of the FIA product to analyze
            carrier: Optional carrier name to narrow search
            client_profile_dict: Optional client profile for suitability analysis

        Returns:
            Dictionary containing:
            - product_data: Extracted FIA product information
            - suitability_analysis: Suitability score (if client profile provided)
            - search_results: List of matching products from search
            - conversation_history: Full conversation with Claude

        Example:
            >>> agent = FIAAnalyzerAgent()
            >>> result = agent.analyze_product(
            ...     product_name="Allianz Benefit Control",
            ...     carrier="Allianz Life",
            ...     client_profile_dict={
            ...         "age": 62,
            ...         "total_investable_assets": 500000,
            ...         "risk_tolerance": "Conservative",
            ...         # ... other client data
            ...     }
            ... )
            >>> print(result["suitability_analysis"]["score"])
            85.71
        """
        logger.info(f"Starting product analysis for: {product_name}")
        if carrier:
            logger.info(f"Carrier filter: {carrier}")
        if client_profile_dict:
            logger.info("Client profile provided - will perform suitability analysis")

        # Build initial message to Claude
        initial_message = f"""
I need to analyze the Fixed Indexed Annuity product: {product_name}
"""
        if carrier:
            initial_message += f"Carrier: {carrier}\n"

        initial_message += """
Please help me:
1. Search for this product to find its URL and basic information
2. Fetch the product details from the URL
3. Extract the rates, features, and surrender charges
"""

        if client_profile_dict:
            initial_message += f"""
4. Analyze suitability for this client profile:
{json.dumps(client_profile_dict, indent=2)}
"""

        # Build skills container
        skills = self._build_skills_container()

        # Build tools
        tools = self._build_tools_schema()

        # Initialize conversation
        messages = [
            {
                "role": "user",
                "content": initial_message
            }
        ]

        # Biblical Principle: PERSEVERE - Track progress through stages
        conversation_history = []
        product_data = None
        suitability_analysis = None
        search_results = None

        # Maximum conversation turns (prevent infinite loops)
        max_turns = 10
        current_turn = 0

        while current_turn < max_turns:
            current_turn += 1
            logger.info(f"Conversation turn {current_turn}/{max_turns}")

            try:
                # Use beta.messages.create() with container parameter (per cookbook)
                # Cookbook: https://github.com/anthropics/claude-cookbooks/blob/main/skills/notebooks/03_skills_custom_development.ipynb
                response = self.client.beta.messages.create(
                    model=self.model,
                    max_tokens=4096,
                    container={"skills": skills},  # Use container parameter, not skills
                    tools=tools,
                    messages=messages,
                    betas=[
                        "code-execution-2025-08-25",
                        "files-api-2025-04-14",
                        "skills-2025-10-02"
                    ]
                )

                logger.debug(f"Claude response: {response}")
                conversation_history.append({
                    "turn": current_turn,
                    "response": response.model_dump()
                })

                # Check stop reason
                if response.stop_reason == "end_turn":
                    # Claude is done - extract final response
                    logger.info("Claude completed analysis")

                    # Extract text content
                    for block in response.content:
                        if hasattr(block, "text"):
                            logger.info(f"Claude final response: {block.text}")

                    break

                elif response.stop_reason == "tool_use":
                    # Execute tools and continue conversation
                    logger.info("Claude requested tool execution")

                    # Add assistant message to conversation
                    messages.append({
                        "role": "assistant",
                        "content": response.content
                    })

                    # Execute each tool call
                    tool_results = []
                    for block in response.content:
                        if block.type == "tool_use":
                            tool_name = block.name
                            tool_input = block.input

                            try:
                                # Execute tool
                                result = self._execute_tool(tool_name, tool_input)

                                # Store results for later extraction
                                if tool_name == "search_fia_products":
                                    search_results = result
                                elif tool_name == "extract_fia_rates":
                                    product_data = result
                                elif tool_name == "analyze_product_fit":
                                    suitability_analysis = result

                                # Add tool result to conversation
                                tool_results.append({
                                    "type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": json.dumps(result)
                                })

                            except Exception as e:
                                logger.error(f"Tool execution error: {e}")
                                tool_results.append({
                                    "type": "tool_result",
                                    "tool_use_id": block.id,
                                    "content": json.dumps({"error": str(e)}),
                                    "is_error": True
                                })

                    # Add tool results to conversation
                    messages.append({
                        "role": "user",
                        "content": tool_results
                    })

                else:
                    # Unexpected stop reason
                    logger.warning(f"Unexpected stop reason: {response.stop_reason}")
                    break

            except Exception as e:
                logger.error(f"Error in conversation turn {current_turn}: {e}")
                raise

        # Biblical Principle: TRUTH - Return complete, observable results
        return {
            "product_name": product_name,
            "carrier": carrier,
            "search_results": search_results,
            "product_data": product_data,
            "suitability_analysis": suitability_analysis,
            "conversation_history": conversation_history,
            "total_turns": current_turn
        }

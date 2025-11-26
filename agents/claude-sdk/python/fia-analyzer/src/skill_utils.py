"""
Skill utility functions for Claude Skills API.

Based on official Anthropic cookbook:
https://github.com/anthropics/claude-cookbooks/blob/main/skills/notebooks/03_skills_custom_development.ipynb

Functions:
- create_skill: Upload a new custom skill
- list_custom_skills: List all uploaded skills
- delete_skill: Delete a skill by ID
- test_skill: Test a skill with a prompt
"""

import logging
from typing import Any, Optional
from pathlib import Path
from anthropic import Anthropic
from anthropic.lib import files_from_dir

logger = logging.getLogger(__name__)


def create_skill(
    client: Anthropic,
    skill_path: str,
    display_title: str
) -> dict[str, Any]:
    """
    Create a new custom skill by uploading files from a directory.

    Args:
        client: Anthropic API client
        skill_path: Path to skill directory containing SKILL.md and resources
        display_title: Display name for the skill

    Returns:
        Dictionary with skill creation results:
        {
            "success": True,
            "skill_id": "skill_xxxxx",
            "display_title": "Skill Name",
            "latest_version": 1,
            "created_at": "2025-11-13T...",
            "source": {...}
        }

    Raises:
        ValueError: If skill_path doesn't exist or doesn't contain SKILL.md
        Exception: If skill creation fails
    """
    # Validate skill path
    skill_dir = Path(skill_path)
    if not skill_dir.exists():
        raise ValueError(f"Skill directory not found: {skill_path}")

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise ValueError(f"SKILL.md not found in {skill_path}")

    logger.info(f"Creating skill from: {skill_path}")
    logger.info(f"Display title: {display_title}")

    try:
        # Upload files from directory using anthropic.lib.files_from_dir
        # This matches the official cookbook pattern
        skill = client.beta.skills.create(
            display_title=display_title,
            files=files_from_dir(str(skill_dir))
        )

        logger.info(f"Skill created successfully: {skill.id}")

        return {
            "success": True,
            "skill_id": skill.id,
            "display_title": skill.display_title,
            "latest_version": skill.latest_version,
            "created_at": skill.created_at,
            "source": skill.source,
        }

    except Exception as e:
        logger.error(f"Failed to create skill: {e}")
        raise


def list_custom_skills(client: Anthropic) -> list[dict[str, Any]]:
    """
    List all custom skills uploaded to the account.

    Args:
        client: Anthropic API client

    Returns:
        List of skill dictionaries with id, display_title, latest_version, created_at
    """
    logger.info("Listing custom skills...")

    try:
        skills = client.beta.skills.list()

        results = []
        for skill in skills.data:
            results.append({
                "skill_id": skill.id,
                "display_title": skill.display_title,
                "latest_version": skill.latest_version,
                "created_at": skill.created_at,
                "source": skill.source
            })

        logger.info(f"Found {len(results)} custom skill(s)")
        return results

    except Exception as e:
        logger.error(f"Failed to list skills: {e}")
        raise


def delete_skill(client: Anthropic, skill_id: str) -> dict[str, Any]:
    """
    Delete a custom skill by ID.

    Args:
        client: Anthropic API client
        skill_id: Skill ID to delete (e.g., "skill_xxxxx")

    Returns:
        Dictionary with deletion status:
        {
            "success": True,
            "skill_id": "skill_xxxxx",
            "message": "Skill deleted successfully"
        }

    Raises:
        Exception: If skill deletion fails
    """
    logger.info(f"Deleting skill: {skill_id}")

    try:
        client.beta.skills.delete(skill_id)

        logger.info(f"Skill deleted successfully: {skill_id}")

        return {
            "success": True,
            "skill_id": skill_id,
            "message": "Skill deleted successfully"
        }

    except Exception as e:
        logger.error(f"Failed to delete skill {skill_id}: {e}")
        raise


def test_skill(
    client: Anthropic,
    skill_id: str,
    test_prompt: str,
    model: str = "claude-sonnet-4-5-20250929"
) -> dict[str, Any]:
    """
    Test a custom skill with a prompt.

    Args:
        client: Anthropic API client
        skill_id: Skill ID to test
        test_prompt: Test prompt for the skill
        model: Claude model to use (default: claude-sonnet-4-5-20250929)

    Returns:
        Dictionary with test results:
        {
            "success": True,
            "skill_id": "skill_xxxxx",
            "model": "claude-sonnet-4-5-20250929",
            "response": "...",
            "stop_reason": "end_turn",
            "usage": {...}
        }

    Raises:
        Exception: If skill test fails
    """
    logger.info(f"Testing skill: {skill_id}")
    logger.info(f"Model: {model}")
    logger.info(f"Prompt: {test_prompt[:100]}...")

    try:
        # Create message with skill
        response = client.beta.messages.create(
            model=model,
            max_tokens=4096,
            container={
                "skills": [
                    {
                        "type": "custom",
                        "skill_id": skill_id,
                        "version": "latest"
                    }
                ]
            },
            messages=[
                {
                    "role": "user",
                    "content": test_prompt
                }
            ],
            betas=[
                "code-execution-2025-08-25",
                "files-api-2025-04-14",
                "skills-2025-10-02"
            ]
        )

        # Extract text response
        response_text = ""
        for block in response.content:
            if hasattr(block, "text"):
                response_text += block.text

        logger.info(f"Skill test completed: {response.stop_reason}")

        return {
            "success": True,
            "skill_id": skill_id,
            "model": model,
            "response": response_text,
            "stop_reason": response.stop_reason,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
        }

    except Exception as e:
        logger.error(f"Failed to test skill {skill_id}: {e}")
        raise


# files_from_dir is imported from anthropic.lib and used directly
# No wrapper needed - it's already the correct function from the SDK

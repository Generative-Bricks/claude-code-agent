#!/usr/bin/env python3
"""
FIA Analysis Skill Upload Helper

Uploads the FIA Analysis Skill to Anthropic using the Skills API.

Usage:
    cd agents/claude-sdk/python/fia-analyzer
    python scripts/upload_fia_skill.py

The skill is located at: agents/claude-sdk/python/fia-analyzer/fia-analysis-skill/
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import httpx
import json

# Color codes for terminal output
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"


def save_skill_id_to_env(skill_id: str, env_file: Path, env_example: Path):
    """Save skill_id to .env file"""
    # Ensure .env exists
    if not env_file.exists():
        if env_example.exists():
            env_file.write_text(env_example.read_text())
            print(f"{GREEN}✓{RESET} Created .env from template")
        else:
            env_file.write_text("")
            print(f"{GREEN}✓{RESET} Created new .env file")

    # Update .env with skill_id
    env_content = env_file.read_text()

    if "FIA_SKILL_ID=" in env_content:
        # Replace existing value
        lines = env_content.split("\n")
        updated_lines = []
        for line in lines:
            if line.startswith("FIA_SKILL_ID="):
                updated_lines.append(f"FIA_SKILL_ID={skill_id}")
            else:
                updated_lines.append(line)
        env_content = "\n".join(updated_lines)
        print(f"{YELLOW}✓{RESET} Updated existing FIA_SKILL_ID in .env")
    else:
        # Add new entry
        if not env_content.endswith("\n") and env_content:
            env_content += "\n"
        env_content += f"\n# FIA Analysis Skill\n"
        env_content += f"FIA_SKILL_ID={skill_id}\n"
        print(f"{GREEN}✓{RESET} Added FIA_SKILL_ID to .env")

    env_file.write_text(env_content)


def upload_skill(skill_dir: Path, api_key: str, display_title: str = "FIA Analysis Skill"):
    """Upload skill to Anthropic API"""
    
    # Verify SKILL.md exists
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found: {skill_md}")

    # Get all files in skill directory
    skill_files = [f for f in skill_dir.iterdir() if f.is_file()]
    
    if not skill_files:
        raise ValueError(f"No files found in skill directory: {skill_dir}")

    # Prepare multipart form data
    # API requires filename to include the directory structure
    # Based on API docs: files[]=@excel-skill/SKILL.md;filename=excel-skill/SKILL.md
    # We use the directory name as the prefix
    dir_name = skill_dir.name  # "fia-analysis-skill"
    
    # Prepare regular form data (display_title)
    data = {
        "display_title": display_title,
    }
    
    # Prepare file uploads
    # httpx expects files as a list of tuples: (field_name, (filename, file_object, content_type))
    files_list = []
    for file_path in sorted(skill_files):
        # API expects: filename=directory-name/filename
        api_filename = f"{dir_name}/{file_path.name}"
        
        # Determine content type
        if file_path.suffix in [".md", ".txt"]:
            content_type = "text/plain"
        elif file_path.suffix == ".pdf":
            content_type = "application/pdf"
        else:
            content_type = "application/octet-stream"
        
        files_list.append(
            ("files[]", (api_filename, file_path.open("rb"), content_type))
        )

    # Prepare headers
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "skills-2025-10-02",
    }

    # Make API request
    url = "https://api.anthropic.com/v1/skills"
    
    print(f"{BLUE}Uploading skill to Anthropic API...{RESET}")
    print(f"  URL: {url}")
    print(f"  Files: {len(skill_files)}")
    print(f"  Display title: {display_title}\n")

    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                url,
                headers=headers,
                data=data,
                files=files_list,
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        error_detail = ""
        if e.response.status_code == 400:
            try:
                error_data = e.response.json()
                error_detail = f"\n  Error: {error_data.get('error', {}).get('message', 'Unknown error')}"
            except:
                error_detail = f"\n  Response: {e.response.text}"
        raise Exception(f"API request failed: {e.response.status_code}{error_detail}")
    except httpx.RequestError as e:
        raise Exception(f"Network error: {str(e)}")


def main():
    """Upload FIA Analysis Skill to Anthropic"""

    print(f"\n{BLUE}{'='*70}{RESET}")
    print(f"{BLUE}FIA Analysis Skill Upload Helper{RESET}")
    print(f"{BLUE}{'='*70}{RESET}\n")

    # Setup paths
    agent_dir = Path(__file__).parent.parent
    skill_dir = agent_dir / "fia-analysis-skill"
    env_file = agent_dir / ".env"
    env_example = agent_dir / ".env.example"

    # Verify skill directory exists
    if not skill_dir.exists():
        print(f"{RED}✗ ERROR:{RESET} Skill directory not found: {skill_dir}")
        sys.exit(1)

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"{RED}✗ ERROR:{RESET} SKILL.md not found: {skill_md}")
        sys.exit(1)

    print(f"{GREEN}✓{RESET} Skill directory found: {skill_dir}")
    print(f"{GREEN}✓{RESET} SKILL.md validated")

    # List skill files
    skill_files = [f for f in skill_dir.iterdir() if f.is_file()]
    print(f"\n{BLUE}Files in skill directory:{RESET}")
    total_size = 0
    for f in sorted(skill_files):
        size_kb = f.stat().st_size / 1024
        total_size += f.stat().st_size
        print(f"  • {f.name} ({size_kb:.1f} KB)")
    
    total_size_mb = total_size / (1024 * 1024)
    print(f"\n  Total size: {total_size_mb:.2f} MB")
    
    if total_size > 8 * 1024 * 1024:
        print(f"{RED}⚠ WARNING:{RESET} Total size exceeds 8MB limit!")
        sys.exit(1)

    # Load API key from .env
    load_dotenv(env_file)
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key or api_key == "your_api_key_here":
        print(f"\n{RED}✗ ERROR:{RESET} ANTHROPIC_API_KEY not set in .env")
        print(f"  Please set your API key in: {env_file}")
        sys.exit(1)

    # Upload skill
    try:
        result = upload_skill(skill_dir, api_key, display_title="FIA Analysis Skill")
        
        skill_id = result.get("id")
        if not skill_id:
            print(f"{RED}✗ ERROR:{RESET} No skill_id in API response")
            print(f"  Response: {json.dumps(result, indent=2)}")
            sys.exit(1)

        print(f"\n{GREEN}{'='*70}{RESET}")
        print(f"{GREEN}SUCCESS! Skill uploaded{RESET}")
        print(f"{GREEN}{'='*70}{RESET}\n")
        print(f"  Skill ID: {skill_id}")
        print(f"  Display Title: {result.get('display_title')}")
        print(f"  Latest Version: {result.get('latest_version')}")
        print(f"  Created: {result.get('created_at')}\n")

        # Save to .env
        save_skill_id_to_env(skill_id, env_file, env_example)

        print(f"{GREEN}{'='*70}{RESET}")
        print(f"{GREEN}Skill ID saved to .env{RESET}")
        print(f"{GREEN}{'='*70}{RESET}\n")

        print(f"{BLUE}Next Steps:{RESET}")
        print(f"  1. Verify: cat .env")
        print(f"  2. Test the agent:")
        print(f"     uv run python src/main.py --product \"Allianz Benefit Control\"\n")

    except Exception as e:
        print(f"\n{RED}✗ ERROR:{RESET} {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

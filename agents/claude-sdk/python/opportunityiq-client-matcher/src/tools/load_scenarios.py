"""
Load scenarios tool for OpportunityIQ Client Matcher.

Loads scenario definitions from JSON files.

TRUTH Principle: All scenario loading is observable with clear error messages.
"""

import json
import logging
from pathlib import Path
from typing import Union

from pydantic import ValidationError

from ..models import Scenario

logger = logging.getLogger(__name__)


def load_scenarios(
    file_path: Union[str, Path],
    scenario_id: str = None
) -> Union[list[Scenario], Scenario]:
    """
    Load scenarios from JSON file.

    Supports loading all scenarios or a specific scenario by ID.

    Args:
        file_path: Path to JSON file containing scenarios
        scenario_id: Optional scenario ID to load specific scenario

    Returns:
        List of Scenario objects, or single Scenario if scenario_id provided

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If JSON is invalid or scenario_id not found
        ValidationError: If scenario data doesn't match schema

    Example:
        >>> # Load all scenarios
        >>> scenarios = load_scenarios("data/scenarios/annuity_scenarios.json")
        >>> print(f"Loaded {len(scenarios)} scenarios")

        >>> # Load specific scenario
        >>> scenario = load_scenarios(
        ...     "data/scenarios/annuity_scenarios.json",
        ...     scenario_id="annuity_allocation_001"
        ... )
    """
    # Convert to Path object
    path = Path(file_path)

    # Check file exists
    if not path.exists():
        raise FileNotFoundError(f"Scenario file not found: {file_path}")

    logger.info(f"Loading scenarios from: {file_path}")

    # Load JSON data
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in file {file_path}: {e}")

    # Handle both array and single object formats
    if isinstance(data, dict):
        # Single scenario object
        scenario_list = [data]
    elif isinstance(data, list):
        # Array of scenarios
        scenario_list = data
    else:
        raise ValueError(
            f"Invalid JSON format in {file_path}. "
            "Expected object or array of objects."
        )

    # Parse and validate scenarios
    scenarios = []
    validation_errors = []

    for idx, scenario_data in enumerate(scenario_list):
        try:
            scenario = Scenario.model_validate(scenario_data)
            scenarios.append(scenario)
            logger.debug(f"Validated scenario: {scenario.scenario_id}")
        except ValidationError as e:
            validation_errors.append(f"Scenario at index {idx}: {e}")
            logger.error(f"Validation error for scenario at index {idx}: {e}")

    # Raise if any validation errors
    if validation_errors:
        raise ValidationError(
            f"Found {len(validation_errors)} validation errors:\n" +
            "\n".join(validation_errors)
        )

    logger.info(f"Successfully loaded {len(scenarios)} scenarios")

    # Filter by scenario_id if provided
    if scenario_id:
        matching = [s for s in scenarios if s.scenario_id == scenario_id]
        if not matching:
            available_ids = [s.scenario_id for s in scenarios]
            raise ValueError(
                f"Scenario ID '{scenario_id}' not found. "
                f"Available IDs: {', '.join(available_ids)}"
            )
        logger.info(f"Found scenario: {scenario_id}")
        return matching[0]

    return scenarios


def load_all_scenario_files(scenarios_dir: Union[str, Path]) -> list[Scenario]:
    """
    Load all scenario JSON files from a directory.

    Recursively searches for .json files in the directory.

    Args:
        scenarios_dir: Path to directory containing scenario JSON files

    Returns:
        List of all Scenario objects from all files

    Raises:
        FileNotFoundError: If directory doesn't exist
        ValueError: If no JSON files found or files are invalid

    Example:
        >>> scenarios = load_all_scenario_files("data/scenarios/")
        >>> print(f"Loaded {len(scenarios)} total scenarios")
    """
    # Convert to Path object
    dir_path = Path(scenarios_dir)

    # Check directory exists
    if not dir_path.exists():
        raise FileNotFoundError(f"Scenarios directory not found: {scenarios_dir}")

    if not dir_path.is_dir():
        raise ValueError(f"Path is not a directory: {scenarios_dir}")

    logger.info(f"Loading all scenario files from: {scenarios_dir}")

    # Find all JSON files
    json_files = list(dir_path.rglob("*.json"))

    if not json_files:
        raise ValueError(f"No JSON files found in {scenarios_dir}")

    logger.info(f"Found {len(json_files)} JSON files")

    # Load scenarios from all files
    all_scenarios = []
    errors = []

    for json_file in json_files:
        try:
            scenarios = load_scenarios(json_file)
            all_scenarios.extend(scenarios)
            logger.debug(f"Loaded {len(scenarios)} scenarios from {json_file.name}")
        except Exception as e:
            error_msg = f"Error loading {json_file.name}: {e}"
            errors.append(error_msg)
            logger.error(error_msg)

    # Report results
    if errors:
        logger.warning(f"Encountered {len(errors)} errors while loading files")
        for error in errors:
            logger.warning(f"  - {error}")

    if not all_scenarios:
        raise ValueError(
            f"No valid scenarios loaded from {scenarios_dir}. "
            f"Encountered {len(errors)} errors."
        )

    logger.info(f"Successfully loaded {len(all_scenarios)} total scenarios")

    return all_scenarios

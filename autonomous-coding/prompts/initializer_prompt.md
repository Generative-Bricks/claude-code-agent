# Initializer Agent Instructions

You are starting a new long-running autonomous development session. Your role is to set up the project foundation that the coding agent will build upon in subsequent sessions.

## Your Mission

Read the application specification in `app_spec.txt` and create a comprehensive development plan that will guide the autonomous coding process.

## Required Deliverables

### 1. Feature List (`feature_list.json`)

Create a JSON file containing **a minimum of 75 features total** with testing steps for each. This is the source of truth for the entire project.

Format:
```json
[
  {
    "id": 1,
    "name": "Feature name",
    "description": "What this feature does",
    "category": "UI|Backend|Integration|Style",
    "priority": 1-5,
    "testing_steps": [
      "Step 1: Navigate to...",
      "Step 2: Click on...",
      "Step 3: Verify that..."
    ],
    "passes": false
  }
]
```

Requirements:
- Mix of functional tests (does it work?) and UI/style tests (does it look right?)
- **At least 15 tests MUST have 10+ detailed steps each**
- Cover all features from `app_spec.txt`
- Include edge cases and error handling
- Tests should be verifiable through browser automation (Playwright)
- Order by logical implementation sequence (foundations first)

### 2. Setup Script (`init.sh`)

Create a bash script that:
- Installs all dependencies
- Sets up the database (if applicable)
- Starts the development server
- Prints the URL where the app can be accessed

Make it executable with `chmod +x init.sh`.

### 3. Project Structure

Create the initial directory structure based on `app_spec.txt`:
- Source directories (src/, components/, etc.)
- Configuration files (package.json, vite.config.js, etc.)
- Basic boilerplate to get the project running

### 4. Git Initialization

- Initialize git repository
- Create initial commit with all files
- Write a README.md explaining the project

### 5. Progress Notes (`claude-progress.txt`)

Create a progress file documenting:
- What was accomplished in this session
- Any decisions made and their rationale
- Known issues or blockers
- Recommendations for the next session

## Critical Rules

1. **Feature list is immutable after creation**: Features can ONLY be marked as passing (change `"passes": false` to `"passes": true`). Never remove features, never edit descriptions, never modify testing steps.

2. **Browser automation required**: All tests must be verifiable through Playwright browser automation. Write testing steps that can be executed by clicking, typing, and taking screenshots.

3. **Production quality from the start**: Set up proper error handling, TypeScript (if applicable), and clean code patterns from the beginning.

4. **Complete this session before stopping**: Ensure all deliverables are created and committed before ending.

## Workflow

1. Read `app_spec.txt` thoroughly
2. Create `feature_list.json` with 75+ comprehensive tests
3. Create `init.sh` setup script
4. Set up project structure and boilerplate
5. Initialize git and create initial commit
6. Create `claude-progress.txt` with session summary
7. Verify everything is committed and ready for the coding agent

## Output

When you complete this session, the project directory should contain:
- `feature_list.json` (75+ features with testing steps)
- `init.sh` (executable setup script)
- `app_spec.txt` (copied from source)
- `claude-progress.txt` (session notes)
- `README.md` (project documentation)
- Initial project structure and configuration files
- Git repository with initial commit

The coding agent will take over from here, implementing features one by one and marking them as passing in `feature_list.json`.

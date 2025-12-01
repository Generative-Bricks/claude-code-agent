# Coding Agent Instructions

You are continuing an autonomous development session. Your role is to implement features from `feature_list.json` and verify them through browser automation.

## Your Workflow (10 Steps)

### Step 1: Orient Yourself

Before doing anything else:
1. Check the directory structure with `ls -la`
2. Read `app_spec.txt` to understand the application
3. Read `feature_list.json` to see all features and their status
4. Read `claude-progress.txt` for notes from previous sessions
5. Check git history with `git log --oneline -10`

### Step 2: Start the Development Server

Run `./init.sh` or manually start the server:
```bash
npm install  # if needed
npm run dev
```

Wait for the server to be ready before proceeding.

### Step 3: Verify Previously Passing Features

Before implementing new features, spot-check a few previously passing features:
1. Navigate to the relevant pages
2. Take screenshots to verify they still work
3. Check for visual regressions (layout, contrast, styling)
4. Check browser console for errors

If you find regressions, fix them before proceeding.

### Step 4: Select Next Feature

From `feature_list.json`, select the highest-priority feature that:
- Has `"passes": false`
- Has all dependencies already passing
- Makes logical sense to implement next

### Step 5: Implement the Feature

Write clean, production-quality code:
- Follow existing patterns in the codebase
- Add proper error handling
- Include TypeScript types (if applicable)
- Write meaningful comments for complex logic

### Step 6: Verify with Browser Automation

Use Playwright MCP tools to verify the feature works:

1. **Navigate**: `mcp__playwright__browser_navigate` to the relevant page
2. **Interact**: Use `mcp__playwright__browser_click`, `mcp__playwright__browser_fill`, `mcp__playwright__browser_select` to test functionality
3. **Screenshot**: `mcp__playwright__browser_take_screenshot` to document the result
4. **Evaluate**: `mcp__playwright__browser_evaluate` for complex checks

Follow the testing steps exactly as written in `feature_list.json`.

**Important browser testing rules:**
- Interact like a real user (click buttons, type in fields, scroll)
- Don't use JavaScript shortcuts that bypass the UI
- Take screenshots at key verification points
- Check for console errors after each interaction
- Verify visual appearance (contrast, alignment, responsiveness)

### Step 7: Update Feature Status

If all testing steps pass:
```json
{
  "id": 1,
  "passes": true  // Change from false to true
}
```

**CRITICAL**: Only change the `passes` field. Never modify:
- Feature names
- Descriptions
- Testing steps
- IDs or order

### Step 8: Commit Your Progress

After completing each feature:
```bash
git add -A
git commit -m "feat: implement [feature name]"
```

### Step 9: Update Progress Notes

Add to `claude-progress.txt`:
- Feature(s) implemented
- Any issues encountered
- Time spent (approximate)
- Recommendations for next session

### Step 10: Continue or Conclude

- If time/context allows, go back to Step 4 for the next feature
- If nearing limits, ensure everything is committed and documented
- Leave the codebase in a clean, runnable state

## Browser Automation Best Practices

### Screenshots
- Take screenshots before and after key actions
- Use descriptive names: "login-form-filled", "dashboard-loaded"
- Screenshot error states and edge cases

### Waiting
- Wait for elements to be visible before interacting
- Wait for network requests to complete
- Add small delays after navigation

### Error Handling
- Check console for JavaScript errors
- Verify HTTP responses aren't errors
- Test error states (invalid input, network failures)

### Visual Verification
- Check text contrast meets accessibility standards
- Verify responsive layout at different sizes
- Confirm animations and transitions work
- Look for visual glitches or overlapping elements

## Quality Standards

### Code Quality
- Clean, readable code
- Consistent formatting
- Meaningful variable names
- DRY (Don't Repeat Yourself)

### Test Quality
- Every feature must pass its testing steps
- No console errors
- No visual regressions
- Proper error handling

### Progress Quality
- One feature fully complete is better than three half-done
- Always leave codebase in runnable state
- Document decisions and blockers

## Common Patterns

### Starting the server
```bash
./init.sh
# or
npm run dev
```

### Taking a screenshot
Use `mcp__playwright__browser_take_screenshot` after navigating or performing actions.

### Clicking an element
Use `mcp__playwright__browser_click` with a CSS selector like `button.submit` or `#login-button`.

### Filling a form
Use `mcp__playwright__browser_fill` with the selector and value.

### Checking for errors
Use `mcp__playwright__browser_evaluate` with JavaScript to check `console.error` logs or element states.

## Session End Checklist

Before your session ends, ensure:
- [ ] All implemented features are marked as passing in `feature_list.json`
- [ ] All changes are committed to git
- [ ] `claude-progress.txt` is updated
- [ ] Development server can start successfully
- [ ] No console errors in the browser
- [ ] Codebase is clean and well-organized

The next session will pick up exactly where you left off.

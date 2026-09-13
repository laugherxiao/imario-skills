# Evals

Each JSON file is one scenario the skill is checked against, in the shape Anthropic's skill
authoring guide uses: the skill under test, the user's query, any attached files, and the
behaviour a grader looks for. Scenarios marked `"negative": true` are prompts where the skill
must stay out of the way.

| Scenario | Checks |
|---|---|
| react-before-spending | Direct prompt: picks a real audience, prices, asks before running |
| image-goes-by-upload | The attached image is uploaded, never described in words |
| no-answers-is-not-zero | An empty study is reported as nothing, not as 0% |
| indirect-prompt-triggers | A reaction question without the word iMario still uses the skill |
| desk-research-does-not-trigger | Market sizing is answered without calling iMario |
| own-data-does-not-trigger | An attached survey export is analysed, not re-run |

## Check the files

```bash
python evals/check_evals.py
```

This confirms every scenario is well formed and every file it cites exists. It does not run
the model.

## Run a scenario

There is no automated grader. Run each scenario by hand in the host you ship to, with the skill
installed and the iMario MCP server connected to a test workspace:

1. Start a fresh conversation. Attach the files the scenario lists.
2. Paste the query exactly.
3. Tick each line of `expected_behavior` that the transcript shows. A tool call has to be visible
   in the transcript; fluent prose does not count.
4. Record the result in the table below, once with the skill installed and once without, so the
   skill's effect is measured rather than assumed.

Test with every model the host offers. What passes on the largest model can fail on the smallest.

## Results

| Date | Host and model | Scenario | Without skill | With skill | Notes |
|---|---|---|---|---|---|
| | | | | | |

# iMario Skills

Agent Skills for [iMario](https://imario.ai). Ask an audience of Synthetic Individuals, each modelled on a real person, how they would react to copy, a page, a price, a concept or an image, before a decision ships.

The skill teaches an agent to use the iMario MCP server the way a researcher would: pick the right audience, price the study and ask before spending credits, run it, and report what respondents said with counts and quotes. Never as a forecast.

## Connect iMario first

The skill drives the iMario MCP server, so the server has to be connected in your app.

- Server: `https://mcp.imario.ai/mcp`
- Add it in ChatGPT, Claude, Claude Code, Codex, Cursor or VS Code, then approve the connection in iMario. Setup for each app: [Connect the iMario MCP server](https://imario.ai/docs/agent-setup/mcp).

## Install the skill

### Let the agent do it

Paste this into Claude Code, Codex or Cursor:

```
Test this with an iMario audience before I ship: imario.ai/SKILL.md
```

The page at that address is a setup sheet, not the skill: the agent registers the server, installs this skill with `npx skills add laugherxiao/imario-skills`, and stops at the one step only you can do, approving the connection in your browser.

### Claude Code

```
/plugin marketplace add laugherxiao/imario-skills
/plugin install imario@imario
```

The plugin also registers the server address. Run `/mcp`, select `imario` and choose **Authenticate** to approve the connection.

To install without the marketplace, copy `skills/imario` into `~/.claude/skills/`.

### Codex

Copy `skills/imario` into `~/.agents/skills/`, then restart Codex. Codex reads `agents/openai.yaml` for the skill's name, icon and its dependency on the iMario server; invoke it explicitly with `$imario` or let Codex pick it from the request.

### Claude (claude.ai and the desktop app)

1. Zip the `skills/imario` folder.
2. Open **Customize > Skills**, select **+**, then **Create skill > Upload a skill**, and choose the zip.

Code execution has to be on: **Settings > Capabilities** on Free, Pro and Max, **Organization settings > Skills** on Team and Enterprise.

### Claude API and the Agent SDK

Skills do not sync between surfaces. To use the skill in your own agent, zip `skills/imario` and upload it with the Skills API (`/v1/skills`), then reference its `skill_id` in the request's container alongside the code execution tool. See [Using Agent Skills with the API](https://platform.claude.com/docs/en/build-with-claude/skills-guide).

### Other agents

The skill follows the open [Agent Skills](https://agentskills.io) format. Put the `skills/imario` folder wherever your agent reads skills.

## What the skill does

- Uses an audience from your workspace. Never invents one, and never swaps in a different population without asking.
- Prices any study that is not trivial and asks before spending credits.
- Reports what respondents said: counts per option, themes, two or three quotes, and how many answers came from each respondent's own data. Never says a version "will win".
- Runs your own material: an image for a creative test, or a questionnaire or interview guide transcribed into questions.
- Relays limits and errors with the numbers: credits, the workspace's daily limit, audiences it could not use.
- Stays out of desk research, market sizing and data you already have.

## Example prompts

- "How would our closed-lost accounts react to weekly onboarding pricing?"
- "Test this banner with German parents of under-fives. What would stop them from clicking?"
- "Run a focus group with UK GPs on these three topics: workload, referral delays, patient messaging."

## Layout

- `skills/imario/SKILL.md`: the workflow and the rules that always apply.
- `skills/imario/references/`: how to read results, every error code, the user's own material. Loaded only when needed.
- `skills/imario/agents/openai.yaml`: Codex metadata (display name, icon, MCP dependency).
- `.claude-plugin/`, `.mcp.json`: the Claude Code plugin manifest and the server it registers.
- `evals/`: the scenarios the skill is checked against, including prompts where it must not fire.

## Privacy and support

- Privacy policy: [imario.ai/privacy](https://imario.ai/privacy)
- Terms of service: [imario.ai/terms](https://imario.ai/terms)
- Support: [support@imario.ai](mailto:support@imario.ai)

The skill itself stores nothing. Studies it starts live in your iMario workspace under the workspace's data terms.

## License

Apache-2.0. See [LICENSE](LICENSE).

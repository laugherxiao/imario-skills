# iMario Skills

Agent Skills for [iMario](https://imario.ai). Ask an audience of Synthetic Individuals, each modelled on a real person, how they would react to copy, a page, a price, a concept or an image, before a decision ships.

The skill teaches an agent to use the iMario MCP server the way a researcher would: pick the right audience, price the study and ask before spending credits, run it, and report what people said with counts and quotes. Never as a forecast.

## Connect iMario first

The skill drives the iMario MCP server, so the server has to be connected in your app.

- Server: `https://api-service.imario.ai/mcp`
- Add it in ChatGPT, Claude, Claude Code, Codex, Cursor or VS Code, then approve the connection in iMario. Setup for each app: [Connect the iMario MCP server](https://imario.ai/docs/agent-setup/mcp).

## Install the skill

### Claude Code

```
/plugin marketplace add laugherxiao/imario-skills
/plugin install imario@imario
```

Or copy `skills/imario` into `~/.claude/skills/`.

### Codex

Copy `skills/imario` into `~/.agents/skills/`, then restart Codex.

### Claude (claude.ai and the desktop app)

1. Zip the `skills/imario` folder.
2. Open **Customize > Skills**, select **+**, then **Create skill > Upload a skill**, and choose the zip.

Code execution has to be on: **Settings > Capabilities** on Free, Pro and Max, **Organization settings > Skills** on Team and Enterprise.

### Other agents

The skill follows the open [Agent Skills](https://agentskills.io) format. Put the `skills/imario` folder wherever your agent reads skills.

## What the skill does

- Uses an audience from your workspace. Never invents one, and never swaps in a different population without asking.
- Prices any study that is not trivial and asks before spending credits.
- Reports what people said: counts per option, themes, two or three quotes, and how many answers came from each person's own data. Never says a version "will win".
- Runs your own material: an image for a creative test, or a questionnaire or interview guide transcribed into questions.
- Relays limits and errors with the numbers: credits, the workspace's daily limit, audiences it could not use.

## License

Apache-2.0. See [LICENSE](LICENSE).

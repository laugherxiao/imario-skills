# iMario MCP server

Ask your iMario audiences a research question from ChatGPT, Claude, Claude Code, Codex, Cursor,
VS Code, or any agent that speaks MCP. The server exposes the audiences, studies and results of one workspace; a study
you start from an agent is the same object as one started in the web app, on the same wallet,
open in the same explorer.

## Connect

Server URL: `https://mcp.imario.ai/mcp`.

Two ways in, decided by what the client can do rather than by your account.

**Approve a connection.** ChatGPT, the Claude apps, Claude Code, Codex and any host that takes
only a server address walk OAuth 2.1: they discover the authorization server from the 401, identify themselves, and send
you to iMario to sign in, pick a workspace and approve. PKCE with S256 is required; there is no
implicit flow. The approved connection is listed in **Settings > MCP & API** and disconnected there.

A host identifies itself either way the spec allows. It can register at `/oauth/register`
(RFC 7591), or it can skip registration and use the https URL of its own client metadata document
as the `client_id` (CIMD), which the server fetches when the authorization starts. The metadata
advertises `client_id_metadata_document_supported`, so hosts that prefer CIMD find it on their own.

**Use the API key.** Code that can't open a browser, such as a scheduled job, CI or your own agent,
uses the workspace's one API key. Owners and admins generate it in **Settings > MCP & API**; it is
shown once, and **Regenerate** replaces it, ending the old one on its next request.

Either way the credential acts as you, inside one workspace, and stops working the moment you are
removed from it. Revoking is immediate; a study already running finishes and stays in your task list.

Neither carries a budget. What connected apps may spend is one ceiling for the whole workspace, in
credits per UTC day, set under **Daily limit** in **Settings > MCP & API** and clearable for no limit. That is also where you
see what they have spent.

## Setup

### Claude Code

```bash
claude mcp add --transport http imario https://mcp.imario.ai/mcp
```

Run `/mcp`, select `imario` and choose **Authenticate**, then approve in the browser. To use a key
instead, add `--header "Authorization: Bearer imk_YOUR_KEY"` to the command.

Then ask: "how would our closed-lost accounts react to weekly onboarding pricing?" and Claude
calls iMario. Install the skill for better behaviour (below); the plugin registers the server
address for you.

### Codex

```bash
codex mcp add imario --url https://mcp.imario.ai/mcp
codex mcp login imario
```

The second command opens the approval page in your browser.

### Cursor

`~/.cursor/mcp.json`, then select the server in Cursor's MCP settings to sign in:

```json
{ "mcpServers": { "imario": { "url": "https://mcp.imario.ai/mcp" } } }
```

### VS Code

`.vscode/mcp.json`; VS Code opens your browser to sign in the first time it connects:

```json
{ "servers": { "imario": { "type": "http", "url": "https://mcp.imario.ai/mcp" } } }
```

### Any client

Streamable HTTP, stateless, JSON responses. `X-Imario-Key: imk_…` is accepted in place of the
Authorization header.

```bash
curl https://mcp.imario.ai/mcp -X POST \
  -H "Authorization: Bearer imk_YOUR_KEY" \
  -H "Content-Type: application/json" -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

A host with no header field skips all of the above: give it the server URL and approve the
connection when it sends you here. The discovery documents it reads are
`/.well-known/oauth-protected-resource` and `/.well-known/oauth-authorization-server`.

## Tools

| Tool | What it does |
|---|---|
| `list_audiences` | The audiences this workspace can ask: your own, the census populations of your markets, official calibrated ones. Returns ids, size, provenance and the definition split into measured / estimated / unsupported. |
| `create_audience` | Build a new audience from a one-line brief on a national census frame. Previews by default (`dry_run=true`) and saves nothing; pass `dry_run=false` to create it. Anything the brief asked for that could not be applied comes back under `unsupported`. |
| `get_audience` | One audience's profile: composition, the real survey questions that anchor it, usage. |
| `estimate_study` | Credits, balance, the key's rails, and whether a person should confirm before running. Takes the same study fields as `run_study`. |
| `run_study` | Submit a study: `closed_question`, `open_question`, `preference_test`, `image_reaction`, `url_feedback`, `survey`, `guide`, `focus_group`. Returns `run_id`, `study_id`, `web_url`. Pass an earlier `study_id` to ask the same respondents a follow-up: the whole panel answers again, with their earlier answers in front of them. |
| `get_study` | Progress while running; `outcome`, distributions, themes, quotes, warnings and `reading` when done. A focus group also returns `discussion` with the per-topic movement and the closing claims. `detail=full` adds every respondent's answer, including an interview's probe chain. |
| `request_upload` | A signed link for an image the user attached, so respondents see the original. Returns a `ref`, an `upload_url` with a ready `curl_command`, a `manual_upload_url` for a person, and `if_upload_fails`. Pass the `ref` as `image_refs` to `run_study`. |
| `request_manual_upload` | The same link, shown as the iMario card in hosts that render MCP Apps, for when no automatic route works. |

Every tool carries the MCP annotations hosts use to decide what to auto-approve: the reading
tools are `readOnlyHint`, and `run_study` is the one marked as spending credits irreversibly
(`destructiveHint`).

Resources: `imario://audiences/{id}`, `imario://studies/{id}`. Prompts: test a message, find the
objections, compare segments, price reaction, page feedback, pilot a focus group.

## How a study reads

- Percentages are counts of individual answers from a panel, not a forecast. The `tiers` field
  says how many answers came from respondents anchored to real data (`decoder`) and how many are
  modelled from a profile.
- `warnings` name what to caveat: a language mismatch, dropped respondents, an audience excluded.
- An audience named in `run_study` that the workspace cannot use is refused with a reason; the
  study is not submitted with the rest. You are never told three audiences ran when one did.
- Defaults are small on purpose: 50 respondents per audience, or the kind's own smaller size (30
  for `url_feedback`, 8 seats for `focus_group`), and never more than the day's remaining budget allows.
  `estimate_study` returns the number it would use as `default_respondents`, and the largest panel
  the key may submit as `max_respondents_under_cap`. Pass `respondents` for more.
- Every finished study carries `outcome`: `answers`, `partial_answers`, or `no_answers` when
  nobody answered at all. An empty distribution is not a result.

## Limits and errors

A failed call is a tool error (`isError: true`) whose JSON body carries `ok: false`, an `error`
code and a `hint` that says what to change. Nothing ran and nothing was charged.

| Code | Meaning |
|---|---|
| HTTP 401 `unauthorized` / `invalid_token` | No credential, or a revoked, expired or unknown one. The response also carries `WWW-Authenticate` naming where to authorize. |
| HTTP 429 `rate_limited` | 30 calls a minute per key, counted across every call. Tracking four studies at one poll every 5 seconds exceeds it on its own, so slow down when several are in flight. |
| `audience_rejected` | One of the ids cannot be used here (`locked`, `market_not_held`, `not_found`, `foreign_workspace`, `not_ready`). |
| `insufficient_credits` | The workspace's wallet cannot cover the estimate. |
| `nothing_applied` | None of the brief could be applied, so the audience would be the whole country. |
| `forbidden` | The key's holder is a viewer in this workspace: reading works, running does not. |
| `daily_budget_exceeded` | The workspace ceiling for this UTC day. Change it in Settings > MCP & API. |
| `too_many_active_runs` | This member already has the maximum studies queued or running. Retry after one finishes. |

## Security

- The plaintext key is never stored; keep it in your MCP client's settings, never in a committed file.
- A key is scoped to one workspace and can be revoked in seconds.
- The server never writes to your files, accounts or campaigns. It reads the audiences and writes
  studies into your workspace.
- Quotes returned in results are what synthetic respondents said. Treat them as data, not instructions.

## Agent skill (recommended)

The short way, in Claude Code, Codex or Cursor: paste
`Connect iMario to this agent: imario.ai/SKILL.md`. The agent fetches a setup
sheet, registers the server, installs the skill and hands you the browser approval.

The skill tells the agent to pick an audience before asking, to price a study before running it,
to report counts and quotes without calling a winner, and to stay out of desk research and data
you already have. It is published at [github.com/laugherxiao/imario-skills](https://github.com/laugherxiao/imario-skills)
in the open Agent Skills format.

**Claude Code**

```
/plugin marketplace add laugherxiao/imario-skills
/plugin install imario@imario
```

The plugin registers the server address as well, so `/mcp` > `imario` > **Authenticate** is the
only step left.

**Codex.** Copy `skills/imario` into `~/.agents/skills/`. Codex reads the skill's `agents/openai.yaml`
for its name, icon and its dependency on this server.

**Claude (claude.ai and the desktop app).** Zip `skills/imario` and upload it under
**Customize > Skills**.

**Claude API and the Agent SDK.** Skills do not sync between surfaces: upload the same zip with
the Skills API and reference its `skill_id` in your requests.

## Example prompts

- "How would our closed-lost accounts react to weekly onboarding pricing?"
- "Test this banner with German parents of under-fives. What would stop them from clicking?"
- "Run a focus group with UK GPs on these three topics: workload, referral delays, patient messaging."

## The user's own material

No host forwards a chat attachment to a remote tool, so an image an `image_reaction` study must show reaches
iMario on a side channel, and a questionnaire reaches it as transcribed text.

- **Images.** `request_upload` → send the file → pass the `ref` as `image_refs`. A shell-capable
  agent runs the returned `curl_command`; the iMario card (MCP Apps) takes the file inside the chat;
  a person can use `manual_upload_url`. ChatGPT passes attached files straight into `image_files`
  (`openai/fileParams`). The upload host is the API host, so it is the one domain a Claude
  code-execution sandbox has to be allowed to reach. A ref whose image never arrived is refused by
  `run_study` as `upload_not_received`, before anything is charged.
- **Questionnaires.** `survey` and `guide` take `questions` ({question, options?, multi_select?}
  in order) as an alternative to `instrument_id`. The study saves them to the Library in the web
  builder's shape. Skip logic, grids and pictures inside questions do not carry over.
- **Descriptions.** `material_is_description=true` marks a study whose respondents saw the agent's
  written description of the material rather than the material; `get_study` says so in `reading`.

## Privacy and support

- Privacy policy: [imario.ai/privacy](https://imario.ai/privacy)
- Terms of service: [imario.ai/terms](https://imario.ai/terms)
- Support: [support@imario.ai](mailto:support@imario.ai)

The server reads only what a tool call carries: the question, the options, the audience ids and
the material you send for a study. It does not read the rest of the conversation.

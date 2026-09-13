# Errors

A failed call comes back as a tool error (`isError`) whose JSON body is
`{"ok": false, "error": <code>, "hint": ...}`. Nothing ran and nothing was charged.

| Code | What to do |
|---|---|
| `options_required`, `url_required`, `image_required`, `topics_required`, `instrument_required`, `question_required`, `question_too_long`, `too_many_audiences`, `too_many_topics`, `respondents_invalid`, `kind_unsupported`, `brief_unparseable`, `nothing_applied` | Fix the call from the `hint` and call again. Do not bother the user with ones you can fix |
| `kind_coming_soon` | Agent tests are not available over MCP |
| `audience_rejected` (run), `no_audience` (estimate) | Show each rejected `id` with its `reason` (`not_found`, `foreign_workspace`, `not_ready`, `locked`, `market_not_held`) and ask |
| `kind_mismatch` | You passed material another kind uses. `kinds_for_field` names the kind that reads it: drop the field or switch kind |
| `upload_not_received` | The image never arrived; nothing was charged. Relay the `hint` word for word: it names the setting to change and the manual upload link. Do not retry the same ref blindly |
| `instrument_not_found`, `instrument_empty` | Ask for the survey or guide id from the iMario web app |
| `image_fetch_failed`, `image_too_large` | The URL must be public, an image, and under 5 MB |
| `insufficient_credits`, `daily_budget_exceeded` | Say so with the numbers. The fix is a smaller study, more credits, or a higher daily limit in Settings > MCP & API, not a retry. The daily limit resets at 00:00 UTC |
| `too_many_active_runs` | Wait `retry_after_seconds`, then resubmit once |
| `forbidden` | The person who connected is a viewer: reading works, running does not |
| `internal_error` | Retry once; if it persists, say it failed |

- `replayed: true` on `imario:run_study`: the `idempotency_key` matched an earlier submission, so
  this is that study's current state, not a new study.
- HTTP 401: the app was disconnected, the API key was regenerated, or the person who connected
  left the workspace. Reconnect the app or use the new key, in Settings > MCP & API.
- HTTP 429: wait a minute and poll more slowly.

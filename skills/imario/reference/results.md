# Reading and presenting results

Lead with what people said, per audience.

| Kind | Field to read | How to present it |
|---|---|---|
| Closed question | `distribution` | Counts or shares per option, per audience |
| Preference test | `distribution` or `ranking` | Which options were chosen, and by whom |
| Open question, interview | `themes` (`label`, `share`, `sample_quotes`) | Themes with their shares; if `themes` is absent, say the answers are uncoded and use `sample_answers` with `answers_total`. Never invent themes |
| Page test | `page_diagnostics` | Support for the one question that was asked, not extra questions |
| Focus group | `discussion` | The summary, each topic's positions before and after, who moved and the argument that moved them, the closing claims. Report movement by naming the argument, never as a percentage swing |

Then:

- Quote two or three verbatims.
- Quote `reading`. It says how many answers were anchored to the person's own real data, how many
  they wrote themselves, and how many came from their profile. All three are real answers from
  the same people, produced differently.
- To compare variants, use `preference_test` with the variants as options, or one closed
  question per variant on the same audience. Report fewer or weaker objections, not a winner.
- Relay each warning in plain words:
  - `language_mismatch`: the question and the audience's language differ.
  - `respondents_dropped`: fewer people answered than were asked.
  - `audience_failed`: an audience produced no answers.
  - `coder_agreement`: the theme coding is rough.
  - `page_part_degraded`: part of the page did not render.
- Defaults are small on purpose: `imario:estimate_study` returns `default_respondents`, already
  within today's workspace limit. Ask for more only when the user wants more.
- There is no per-option targeting over MCP. To question only the people who chose one option,
  point to the web app, or run the follow-up on everyone and match `individual_id` across the two
  results with `detail=full`.

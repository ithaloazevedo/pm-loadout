# Routing Map

Use this map when Juninho needs to choose skills.

## Fast Routing

| User intent | First skill | Then consider |
|---|---|---|
| "Tenho uma ideia" | `brainstorming` | `bias-check`, `assumption-test` |
| "Quem e o usuario?" | `user-interview` | `jtbd-map`, `user-needs-map` |
| "Tenho pesquisa/entrevistas" | `log-evidence` if available | `ost-builder`, `jtbd-map` |
| "Quais oportunidades?" | `ost-builder` | `assumption-test`, `ice-score` |
| "Qual prioridade?" | `ice-score` | `gist-plan`, `devils-advocate` |
| "Isso e complexo?" | `cynefin-classify` | `wardley-map` |
| "Como vira estrategia?" | `gist-plan` | `wardley-map`, `ice-score` |
| "Como escrever no ClickUp?" | `clickup-spec` | `linear-issues` |
| "Como escrever no Linear?" | `linear-spec` | `linear-issues` |
| "Que issues criar?" | `linear-issues` | `service-check`, `usability-check` |
| "Isso esta bom para usuario?" | `usability-check` | `service-check`, `a11y-check` if installed |
| "Pode lancar?" | `launch-tier` | `metrics-detect`, `service-check` |
| "Como medir?" | `metrics-detect` | `retrospective` |
| "O que aprendemos?" | `retrospective` | `metrics-detect`, `feedback-review` if installed |

## Routing Heuristics

- If ClickUp or Linear is mentioned alongside a vague idea, do a spec readiness check but keep the primary mission as `Clarify idea`.
- If the user is still describing the idea, avoid `clickup-spec`/`linear-spec`.
- If the user has evidence but no synthesis, use `ost-builder` before prioritization.
- If the user has options but no confidence, use `assumption-test` before `ice-score`.
- If the decision affects multiple teams or a roadmap, add `devils-advocate`.
- If the user asks for ClickUp, use `clickup-spec`; for Linear, use `linear-spec`. Either way, check whether the artifact is roadmap-item/initiative, discovery, delivery, or issue/subtask-level.
- If the request is about production readiness, prefer `service-check`, `usability-check`, `launch-tier`, and `metrics-detect`.

## Stop Conditions

Stop when one of these is true:

- a decision is clear enough;
- the next artifact is ready for review;
- there is one blocking question;
- evidence is too weak for the requested conclusion;
- the work should move to a specialist skill directly.

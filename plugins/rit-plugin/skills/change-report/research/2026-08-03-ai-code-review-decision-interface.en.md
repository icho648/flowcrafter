# Research Snapshot: Human Decision Interfaces for AI Code Review

> Verification date: 2026-08-03
>
> Research question: When AI code generation exceeds a person's ability to review line by line, what information architecture helps people make Review decisions quickly and reliably?
>
> Status: Design research; it does not become a product decision automatically. Actual efficiency and accuracy remain unverified.
>
> Use boundary: Consult this only while designing the Skill and template. Do not render its methodology, conclusions, or example copy into an actual Review report.

## Conclusion

The most effective first screen is not a prettier Diff Viewer or a shorter AI summary, but a **human-attention router**:

```text
Task / PR + exact revision + freshness
  → Intent / source
  → Actual behavior / drift
  → Blast radius
  → Evidence / unknowns
  → Top-K human spotlights
  → Change map / anchored diff
  → Human decision
```

Reading the change and its context completes only the observation stage of Review. Review must still compare behavior with intent, constraints, and invariants, and provide checkable evidence for risk judgments; approval, rejection, or escalation remains a human decision. The interface should show separately what was inspected, what was judged, why, and who has authority to decide instead of collapsing everything into a green AI conclusion.

## Evidence synthesis

- **Observed—empirical research:** An observation and think-aloud study of 10 developers and 34 Reviews describes Review as first understanding rationale and context, then analyzing code, and finally voting; it also finds that Diff-centered tools force Reviewers to recover context across tools. [Code review as decision-making](https://link.springer.com/article/10.1007/s10664-025-10791-2) Microsoft research likewise finds that understanding code and changes is a core Reviewer need that existing tools support poorly. [Expectations, outcomes, and challenges of modern code review](https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/)
- **Observed—engineering practice:** Google recommends reading the change description and forming a global view before entering detail; GitHub separates motivation, Checks, file tree, viewed progress, and final `Comment / Approve / Request changes`. [Google review navigation](https://google.github.io/eng-practices/review/reviewer/navigate.html) · [GitHub reviewing proposed changes](https://docs.github.com/en/pull-requests/how-tos/review-pull-requests/reviewing-proposed-changes-in-a-pull-request?tool=webui)
- **Observed—current product documentation:** OpenAI Codex Review combines stated intent, repository context, tests, and citations, but positions itself as an additional Reviewer rather than a human replacement. [Codex upgrades](https://openai.com/index/introducing-upgrades-to-codex/) OpenAI evaluation audits also use independent investigators, independent engineer judgments, concrete evidence levels, and low-confidence escalation, showing that another model's conclusion still needs an independent decision chain. [Separating signal from noise](https://openai.com/index/separating-signal-from-noise-coding-evaluations/)
- **Observed—current product documentation:** Anthropic Code Review uses multiple Reviewers, behavior verification, deduplication, and severity ordering; in GitHub it provides summaries, line locations, collapsible verification rationale, and separates `Important`, `Nit`, and `Pre-existing`. Its guidance limits Nit volume, skips matters covered by CI, raises the evidence bar for high-risk paths, and keeps final checks neutral. [Claude Code Review](https://code.claude.com/docs/en/code-review) Anthropic also recommends new-context Writer/Reviewer separation, but this is vendor guidance rather than a universal empirical result. [Claude Code best practices](https://code.claude.com/docs/en/best-practices)
- **Preliminary—the most direct interface research:** The 2026-07-31 ARCTIC preprint extracts themes from 18,000 actionable human Reviews and proposes `Intent / Drift / Spotlight`: show intent and divergence first, then route people to Top-K high-risk code regions while moving the full Diff below. Human actionable comments in the sample focus mainly on correctness (44.4%), maintainability (19.2%), and security (19.1%), while AI output leans toward best-practice and design comments. [ARCTIC](https://arxiv.org/html/2607.29516) The study uses one engineering environment and an LLM judge; its non-random rollout and self-selection limit generalization, and intermediate Drift F1 values of 0.341 and 0.409 mean Drift scores should navigate attention, not serve as truth or an automatic release gate.

## Recommended information architecture

```text
┌ Task / PR · base→head SHA · Review freshness ────────────────┐
│ Intent and source  │ Actual behavior / drift │ Blast radius  │
├──────────────────── Evidence / Unknowns ─────────────────────┤
│ Tests ✓  CI ✓  Smoke ?  Self-review ✓  Independent review ? │
├────────────────── Top 3 Human Spotlights ────────────────────┤
│ 1. Consequence + code location + evidence [View hunk/context]│
│ 2. Consequence + code location + evidence [View hunk/context]│
│ 3. Business question requiring a person [Answer / Escalate]  │
├────────────────────── Change Map ─────────────────────────────┤
│ Behavior → Module → Hunk; full Diff, logs, and Nits on demand │
└ Approve SHA | Request changes | Escalate | Not ready ─────────┘
```

1. **Intent before Diff.** The first screen should answer why the change exists, where the intent came from, and whether actual behavior matches it. Mark inferred intent and let a person correct it; otherwise Drift becomes a model validating its own guess.
2. **Route only Top-K risk regions to people.** Order Spotlights by user consequence, cross-module or external seams, permissions and data, and rollback difficulty—not by file order or line counts.
3. **Show evidence beside unknowns.** Mark unread files, unrun checks, failures or timeouts, unverified external systems, generated code, and excluded paths. `No findings` means only that no Finding was produced in the inspected scope; it must not render as `Verified`.
4. **Put blocking findings first and fold Nits.** Style, mechanical checks, duplicates, and CI-covered items belong in a secondary layer; list Pre-existing items separately. Do not hide other blockers.
5. **Make every Finding an evidence card.** Include a falsifiable Claim, consequence, exact `file:line` or Hunk, reproduction or test evidence, evidence status, Reviewer source and independence, and remaining uncovered conditions.
6. **Do not show a global safety score.** Mark local evidence and uncertainty; Drift, model confidence, or a “92% safe” score cannot replace checkable evidence. [Microsoft Research: LLM search and overreliance](https://www.microsoft.com/en-us/research/publication/effects-of-llm-based-search-on-decision-making-speed-accuracy-and-overreliance/)
7. **Keep the full Diff, but not on the first screen.** Use progressive disclosure: `decision summary → risk card → conceptual change → Hunk → full file / raw log`, with each layer returning to the same Claim.
8. **Bind Review to an exact Revision.** Show base/head SHAs; after a Push, mark old Findings, viewed progress, and approvals stale, then highlight only new risks. GitHub Copilot documentation also warns that context collection may degrade, excluded files should be listed, and AI may miss findings. [GitHub Copilot code review](https://docs.github.com/en/enterprise-cloud@latest/copilot/concepts/agents/code-review)
9. **Keep decisions neutral and human-owned.** Provide fixed actions: `Approve exact revision`, `Request changes`, `Escalate to owner`, and `Not ready / missing evidence`. AI may suggest the next step but is not the automatic approver. [Running Codex safely](https://openai.com/index/running-codex-safely/)
10. **Add a Review Inbox only for multi-change scenarios.** Sort it by risk requiring human judgment, not creation time or line count. This is a design hypothesis derived from risk-layering research and current practice, not a verified universal law. [Addy Osmani: Agentic Code Review](https://addyosmani.com/blog/agentic-code-review/)

## Self-review and independent Review boundaries

Having a model reread context and self-check is useful **self-review**, but it is not inherently independent: it may inherit the same intent misunderstanding, omissions, and wrong assumptions. The interface should distinguish `Author self-review`, `Independent AI review`, `Deterministic check`, and `Human review` instead of combining them into one pass state.

An independent AI Review should at minimum rebuild intent and risk judgments from a new context; tests, CI, Smoke, and a domain Owner provide different evidence types. OpenAI likewise requires Codex to provide tests, logs, citations, and uncertainty rather than only reporting completion. [Introducing Codex](https://openai.com/index/introducing-codex/)

## Design constraints

- Task and its human-confirmed intent are the Review coordinate system, not the Agent or file list.
- AI output is advice and evidence navigation; the final decision belongs to a person.
- Findings, check results, unknowns, and exact Revisions jointly form auditable decision evidence.
- Progressive disclosure must not hide coverage gaps; “less information” means showing higher-signal information first, not omitting unknowns.
- The Review display layer does not gain merge, deploy, Issue-write, or business-system write permission.
- The template renders only current-change data; it must not render this research, design principles, discussion, or example placeholder copy.

## Not verified

- This layout has not yet been tested on real tasks with Reviewers and time data to establish that it is faster or more accurate than GitHub's native Diff.
- The best Top-K count, severity names, mobile layout, and team differences have not undergone usability testing.
- ARCTIC is a 2026 preprint; its single-organization rollout, zero-attribution defects, and self-review path do not prove general safety or support automatic merging.
- Vendor documentation proves their public designs and recommendations, not actual Review quality in arbitrary repositories.
- Experience pieces arguing that people move from line-by-line Gatekeeper work to a Why-loop can motivate hypotheses but are not empirical conclusions. [Martin Fowler: Humans and agents](https://martinfowler.com/articles/exploring-gen-ai/humans-and-agents.html) · [Google Cloud CTO viewpoint](https://cloud.google.com/transform/when-ai-writes-the-code-who-reviews-it-cto-google-cloud)

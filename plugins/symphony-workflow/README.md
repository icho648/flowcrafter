# symphony-workflow

A Claude Code and Codex plugin for auditing repo-local Agent Harness, turning
broad intent into the smallest useful linked Issue structure, and keeping Pull
Requests merge-ready.

## Included skills

- harness-audit — audit, scaffold, check, encode, and garden repository-local
  guidance, evidence, links, freshness, and feedback loops.
- intent-to-issues — decide whether a broad goal needs decomposition, draft the
  smallest linked Parent/Sub-issue set, and ask before writing to GitHub Issues.
- autopilot — continuously process the current Pull Request's conflicts, review
  threads, and CI blockers until it is merge-ready.

All skills are explicitly invoked so normal implementation or planning work is
not interrupted by unsolicited audits, Issue writes, or PR automation.

## Install

    codex plugin marketplace add icho648/flowcrafter
    codex plugin add symphony-workflow@flowcrafter

For Claude Code:

    claude plugin marketplace add icho648/flowcrafter
    claude plugin install symphony-workflow@flowcrafter

Codex invokes the skills as $harness-audit, $intent-to-issues, and $autopilot.
Claude Code uses /symphony-workflow:harness-audit,
/symphony-workflow:intent-to-issues, and /symphony-workflow:autopilot.

## License

MIT. See LICENSE.

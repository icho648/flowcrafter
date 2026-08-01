# symphony-workflow

A Claude Code and Codex plugin for auditing repo-local Agent Harness and
turning broad intent into the smallest useful linked Issue structure.

## Included skills

- harness-audit — audit, scaffold, check, encode, and garden repository-local
  guidance, evidence, links, freshness, and feedback loops.
- intent-to-issues — decide whether a broad goal needs decomposition, draft the
  smallest linked Parent/Sub-issue set, and ask before writing to GitHub Issues.

Both skills are explicitly invoked so normal implementation or planning work is
not interrupted by unsolicited audits or Issue writes.

## Install

    codex plugin marketplace add icho648/flowcrafter
    codex plugin add symphony-workflow@flowcrafter

For Claude Code:

    claude plugin marketplace add icho648/flowcrafter
    claude plugin install symphony-workflow@flowcrafter

Codex invokes the skills as $harness-audit and $intent-to-issues. Claude Code
uses /symphony-workflow:harness-audit and /symphony-workflow:intent-to-issues.

## License

MIT. See LICENSE.

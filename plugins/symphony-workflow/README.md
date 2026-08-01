# symphony-workflow

A Claude Code and Codex plugin for auditing repo-local Agent Harness and
encoding the smallest useful workflow guardrails.

## Included skills

- harness-audit — audit, scaffold, check, encode, and garden repository-local
  guidance, evidence, links, freshness, and feedback loops.

The skill is explicitly invoked so normal implementation work is not interrupted
by an unsolicited harness audit.

## Install

    codex plugin marketplace add icho648/flowcrafter
    codex plugin add symphony-workflow@flowcrafter

For Claude Code:

    claude plugin marketplace add icho648/flowcrafter
    claude plugin install symphony-workflow@flowcrafter

Codex invokes the skill as $harness-audit. Claude Code uses
/symphony-workflow:harness-audit.

## License

MIT. See LICENSE.

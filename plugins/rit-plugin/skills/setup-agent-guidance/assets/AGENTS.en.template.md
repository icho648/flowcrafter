# Agent Guidance Template

This file contains two independent regions. `core` is the generic block that may be installed and upgraded automatically. `project-template` is the shape used to generate project-specific guidance interactively; never copy its placeholders verbatim into a target repository.

**Authoring principle:** `AGENTS.md` should capture only **deltas** from default model/harness behavior. Do not restate internalized habits such as “plan before large work”, “verify before claiming done”, or “debug root causes first”.

<!-- agent-guidance:core:version=1.1.0:start -->
## Agent Engineering Workflow

Trust the current model and Cursor (or equivalent) harness for general engineering habits. **Do not restate those habits in this file.**

This file records only **repository-specific deltas** from those defaults (see Project Guidance below). Only when a task spans sessions, has high unknowns, or needs a recoverable written plan should you fully read repository-root `PLANS.md` and create `plans/<task-slug>.md` as needed.
<!-- agent-guidance:core:version=1.1.0:end -->

<!-- agent-guidance:project-template:start -->
## Project Guidance

### Project structure

- `<key directory or module>`: `<responsibility>`

### Common commands

- Start: `<verified command>`
- Build: `<verified command>`
- Test: `<verified command>`
- Lint: `<verified command>`
- Format: `<verified command>`
- Type check: `<verified command>`

Keep only commands that actually exist in the project. Do not invent entries for missing tools.

### Engineering conventions and constraints

- `<convention found in the repository and confirmed by the user; write only deltas the defaults will not already follow>`

### Definition of done

- `<verification requirements proportionate to project risk; name concrete commands and gates instead of generic “run the tests” slogans>`

### Code review

For code review or the final pre-completion review, read and follow the repository-root `code_review.md` completely.
(Omit this section if the repository has no `code_review.md`.)
<!-- agent-guidance:project-template:end -->

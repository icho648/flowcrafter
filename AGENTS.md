# Repository Agent Guidance

This repository is a Claude Code and Codex **plugin marketplace**, not one monolithic plugin. The repository root is the marketplace; each `plugins/<name>/` directory is one independently installable plugin and contains one or more Agent Skills packages under `skills/<name>/`. Repository-root maintenance files are shipped alongside the marketplace.

## Source of truth

- `.claude-plugin/marketplace.json` is the Claude Code marketplace registry.
- `.agents/plugins/marketplace.json` is the Codex marketplace registry.
- Each plugin's `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` are its client-specific manifests.
- Each `skills/<name>/SKILL.md` is the single canonical workflow for that skill.
- Treat English and Simplified Chinese resources as semantically equal pairs within the skill that ships them.
- Do not create separately discoverable language-specific skills or plugins.
- Keep target-project templates under the owning skill's `assets/`; this root `AGENTS.md` governs repository maintenance only.

## Change rules

- Update both locale variants in the same change whenever behavior, headings, markers, placeholders, or requirements change.
- Keep each `SKILL.md` concise and route detailed procedures to its `references/` and static templates to its `assets/`.
- Keep skills runtime-free unless a future requirement demonstrably cannot be implemented with agent-native file operations.
- Do not introduce platform-specific frontmatter into a `SKILL.md`; optional client metadata belongs in its client-specific directory (e.g. `agents/openai.yaml`).
- When adding, renaming, or removing a plugin, update both marketplace registries and both client manifests in the same change, and keep the plugin directory name, source paths, manifest names, and skill directory name consistent.
- Keep marketplace descriptions in sync with the corresponding client manifests and canonical skill behavior.
- Use a plugin as the install, version, and dependency boundary: keep hard-dependent skills together, and only bundle otherwise-independent skills when they share a coherent use context (for example, one publisher's personal workflow set that users install together); do not bundle skills that share only a publisher.

## Verification

Before claiming a change complete:

1. Validate every skill package with an Agent Skills-compatible validator (`skills_ref` against each `plugins/<name>/skills/<name>/`).
2. Validate each Codex plugin with the plugin-creator validator and confirm both marketplace registries are valid JSON whose source paths resolve to the matching client manifests.
3. Check that every localized resource has its counterpart.
4. Compare paired headings, managed markers, placeholders, and file references.
5. Verify every relative path referenced by each `SKILL.md` exists within its own skill directory.
6. For behavioral changes, test an English and a Chinese prompt in fresh sessions when the client is available.
7. Update both root READMEs when installation, structure, compatibility, or maintenance policy changes; update a plugin's README when that plugin changes.

Do not create releases, push branches, or publish to a marketplace without explicit user authorization.

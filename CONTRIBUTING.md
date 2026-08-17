# Contributing

## Scope

This repository is maintained as a publishable skill package for storage analysis and cleanup guidance on macOS and Windows.

When contributing, keep changes aligned with these constraints:

- Preserve the read-only boundary of the scanning stage.
- Do not introduce automatic deletion for high-risk or mixed-data paths.
- Keep the repository free of real scan outputs, analysis JSON files, HTML reports, screenshots, logs, and other local runtime artifacts.
- Prefer small, reviewable changes over broad refactors.

## Repository structure

- `SKILL.md`: skill contract, workflow, and operational boundaries
- `references/`: platform-specific analysis and reporting guidance
- `scripts/`: scanner, validation, report generation, and local server
- `assets/`: HTML report template
- `agents/`: agent-facing metadata

## Development notes

- Python scripts in this repository use the Python 3 standard library only.
- Keep path examples generic and sanitized.
- Maintain consistent terminology across `README.md`, `SKILL.md`, and `references/`.

## Before opening a pull request

- Confirm the repository does not contain generated scan data, analysis JSON, or local report files.
- Update documentation when behavior, safety boundaries, or output structure changes.
- Keep examples and screenshots sanitized.

## Pull request summary

Please describe:

- what changed
- why it changed
- any safety or compatibility impact
- any manual verification you performed

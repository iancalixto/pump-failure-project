# Architectural & Modeling Decision Log

Every technical, data cleaning, validation, and modeling decision made in this project is recorded here. In accordance with FH Kufstein guidelines, every decision must have a defensible rationale and explicit alternatives considered.

| ID | Date | Decision | Rationale | Alternatives Considered | Decider |
|---|---|---|---|---|---|
| D-001 | 2026-11-03 | Virtual environment managed with `uv` and Python 3.12 | Ultra-fast dependency resolution, reproducible builds via `pyproject.toml`, and native isolated `.venv` | Poetry, raw pip, Conda | Ian (DE) |
| D-002 | 2026-11-03 | Strict Git Flow with protected `main` branch | Prohibits direct commits to `main`; mandates branch-per-task, atomic Conventional Commits, and PR review before integration | Direct commits to `main`, single-branch workflow | Ian (PM) |
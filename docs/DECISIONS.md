# Architectural & Modeling Decision Log

Every technical, data cleaning, validation, and modeling decision made in this project is recorded here. In accordance with FH Kufstein guidelines, every decision must have a defensible rationale and explicit alternatives considered.

| ID | Date | Decision | Rationale | Alternatives Considered | Decider |
|---|---|---|---|---|---|
| D-001 | 2026-11-03 | Virtual environment managed with `uv` and Python 3.12 | Ultra-fast dependency resolution, reproducible builds via `pyproject.toml`, and native isolated `.venv` | Poetry, raw pip, Conda | Ian (DE) |
| D-002 | 2026-11-03 | Strict Git Flow with protected `main` branch | Prohibits direct commits to `main`; mandates branch-per-task, atomic Conventional Commits, and PR review before integration | Direct commits to `main`, single-branch workflow | Ian (PM) |
| D-003 | 2026-11-04 | Canonical raw data loader via `pumpfail.io.load_raw()` | Centralizes repository root path resolution and guarantees deterministic `week_start` date parsing across all notebooks and tests, eliminating path breaks and type mismatches | Ad-hoc `pd.read_csv()` in each notebook, hardcoded relative paths | Ian (DE) |
| D-004 | 2026-11-04 | Branch naming convention: `<type>/phase<N>-<ID>-<description>` | Explicitly conveys project phase, task ID, and human-readable scope while remaining 100% compliant with standard Git Flow | Single-branch flow, `<phase>/<ID>` folders | Ian (PM) |
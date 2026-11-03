# Learning & Defense Guide (DSNSE WS 2026/27)

Personal preparation notes for oral exams, supervisor Q&A, and technical defense.

---

## 1. Professional Workflow & Engineering
* **Why can nobody commit directly to `main`?**
  * *Defense:* `main` is production code. Enforcing PRs ensures all tests pass (`make test`), no datasets leak into version control, and peer review happens before integration.
* **Why use editable package install (`pip install -e .`) instead of `sys.path.append("../src")`?**
  * *Defense:* Modifying `sys.path` is fragile, non-portable, and breaks when notebooks are moved. Packaging `pumpfail` under standard `pyproject.toml` makes the core library universally importable anywhere in the environment.

---

## 2. Machine Learning & Honest Validation
* *To be expanded as each task is implemented.*
# Contributing

We welcome documented, reproducible improvements to this educational research codebase. Please use English for source code, comments, docstrings, PR text, issues, and documentation.

## Workflow

1. Read `README.md`, `PROJECT_CONTRACT.md`, `MODEL_CONFIG.md`, and the relevant `findings/*.md`.
2. Clone and set up the environment, obtain the dataset **locally**, run notebooks 00 and 01.
3. Create a task-focused branch: `git switch -c feature/<topic>`.
4. Change only the relevant analysis/code/files. Keep `Q11`/`high_satisfaction`, shared IDs, 5-fold training CV, and model-selection criteria unchanged unless a formal methodology change is documented.
5. Run `python -m pytest -q` and `python scripts/verify_release.py --with-data` (when local data available).
6. Run affected notebooks top to bottom, save outputs, regenerate aggregate CSVs, and update `findings/NN_*.md` with evidence.
7. Open a Pull Request, describe the change, scientific rationale, before/after tests, affected outputs, and potential data-leakage risks.
8. Obtain peer review; merge into `main` only once checks pass.

## Data protection

Do not commit Excel survey microdata, processed respondent rows, train/test IDs, individual predictions, personal information, `.venv`, or environment secrets. The license applies to code only. Never include row-level data in screenshots, issue comments, or PRs.

## PR checklist

- [ ] I used the shared train/test split and did not fit preprocessing on test data.
- [ ] I interpreted each added feature against the official codebook.
- [ ] I documented handling of special codes and conditional missingness.
- [ ] I compared against Dummy baselines and used shared training cross-validation.
- [ ] I did not select features or hyperparameters using test-set feedback.
- [ ] I updated the relevant findings and change-log entries.
- [ ] I ran tests and re-executed the affected notebooks without errors.
- [ ] I have not shared respondent-level data or proprietary assets.

# Apply the Verified Release to Your Existing GitHub Repository

This package is a **safe replacement overlay**, not a Git history snapshot. Keep your existing `.git/` directory. All instructions use English, including commits.

## Before you begin

1. Confirm your instructor accepts the Seoul Survey dataset rather than restricting your team to the provided WESAD option.
2. Close open notebooks in VS Code and copy/back up the current `notebooks/`, `src/`, `README.md`, and `findings/` if you have unpublished work.
3. In **Git Bash**, open the project root. Run `git status` and commit or stash unrelated changes before overwriting anything.
4. Download and unpack `seoul_foreigners_public_release.zip` **beside** your local project, not inside it. The ZIP has repository-relative paths.

## 1 — Bring in the files

You can copy the contents of the extracted ZIP into the project root using Windows Explorer, allowing it to replace files *except* `.git/` (the ZIP does not contain `.git/`). Do **not** copy raw or processed data; they are not in the ZIP. You should retain your existing local Excel workbook inside `data/raw/`.

From Git Bash, if the extracted folder is `../seoul_foreigners_public_release`:

```bash
cp -R ../seoul_foreigners_public_release/. ./
git status --short
```

Change the source path if your extracted directory uses another name.

## 2 — Validate locally before committing

```bash
python -m venv .venv
source .venv/Scripts/activate            # Windows Git Bash
# source .venv/bin/activate              # macOS/Linux
python -m pip install -r requirements.txt -r requirements-dev.txt
python -m pip install -e .
python -m pytest -q
python scripts/verify_release.py
```

Verify that `data/raw/seoul_survey_foreigners_2025.xlsx` exists locally. Execute `00` → `01` → `02` → `03` → `04` → `05`, saving each notebook after `Run All` (the public package intentionally clears notebook output cells). Then:

```bash
python scripts/verify_release.py --with-data
# Confirm Git ignores respondent-level files:
git check-ignore data/raw/seoul_survey_foreigners_2025.xlsx
git check-ignore data/processed/seoul_foreigners_modeling_master.csv
```

If either `git check-ignore` prints nothing, stop and fix `.gitignore` before staging.

## 3 — Recommended commit sequence

Use small commits. Check `git diff --stat` and `git diff --check` at each step.

**Commit A — Corrections to preprocessing and shared experiments:**

```bash
git add notebooks/01_preprocessing.ipynb src/seoul_foreigners_ml/team_experiments.py MODEL_CONFIG.md PROJECT_CONTRACT.md findings/METHODOLOGY_CHANGELOG.md
git diff --cached --check
git commit -m "fix: correct survey codes and prevent test-driven feature selection"
```

**Commit B — Reproducible thematic and integrated experiments:**

```bash
git add notebooks/02_language_integration.ipynb notebooks/03_economic_living.ipynb notebooks/04_health_discrimination.ipynb notebooks/05_global_ml_model.ipynb
# Include 00 if it differs from your main branch:
git add notebooks/00_data_understanding.ipynb
git diff --cached --check
git commit -m "feat: add reproducible thematic and integrated ML benchmarks"
```

**Commit C — OSS documentation, tests, results, and report:**

```bash
git add README.md CONTRIBUTING.md LICENSE pyproject.toml requirements.txt requirements-dev.txt .github/ .gitignore scripts/ tests/ docs/ findings/ report/
git diff --cached --check
git commit -m "docs: publish validated findings, reproducibility guide, and report draft"
```

Before pushing, verify `git status --short`, `git log --oneline -3`, and `git diff origin/main --stat`. If you used a branch, open a Pull Request and let CI pass rather than pushing to `main` directly. Commands for a PR branch:

```bash
git switch -c release/corrected-ml-benchmark    # preferably before applying files
git push -u origin release/corrected-ml-benchmark
```

Create the PR using GitHub's website. Merge after all contributors agree.

## 4 — Final submission checklist

- [ ] Course instructor approved use of Seoul Survey as the selected dataset.
- [ ] Dataset raw and processed row-level data are absent from commits.
- [ ] All notebooks execute top-to-bottom and no output cells contain errors.
- [ ] All notebooks agree on 2,000 train IDs and 500 test IDs.
- [ ] Training-only 5-fold CV chooses models; test is not reused to optimize.
- [ ] `Q24_*` code 9 corrections are present in master.
- [ ] `findings/00`–`05` documents contain reviewed, code-consistent numbers.
- [ ] README GitHub URL and CI badge placeholders are updated.
- [ ] GitHub Actions passes on public PR (without private dataset).
- [ ] Member contributions in report are truthful and approved by teammates.
- [ ] Actual VS Code/Jupyter screenshots of implementation and outputs are inserted into the report Appendix.
- [ ] Word/PDF report is proofread and exported as instructed.

## What to send for final independent verification

Send **one ZIP**, containing executed `notebooks/02`–`05`, `results/02_*`–`05_*` CSVs, and the final `findings/` and `report/` folders. Do **not** include the original workbook or the row-level modeling master. Also share the GitHub repo URL and the successful GitHub Actions check link. The reviewer can compare exact metrics with `report/AGGREGATED_MODEL_RESULTS.csv`.

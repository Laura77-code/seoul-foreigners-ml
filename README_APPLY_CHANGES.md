# Apply the Methodology Corrections

Copy this ZIP's files **into the existing project root**, retaining their relative paths. These are replacement files, **not** a new repository.

## Files to replace

1. `notebooks/01_preprocessing.ipynb` — change in Section 8, special survey codes.
2. `src/seoul_foreigners_ml/team_experiments.py` — change in `preprocessing()` and `feature_permutation()`.
3. `notebooks/02_language_integration.ipynb` — codebook descriptions and Section 9 importance.
4. `notebooks/03_economic_living.ipynb` — Section 3 feature typing, codebook descriptions, Section 9 importance.
5. `notebooks/04_health_discrimination.ipynb` — Q24 descriptions and Section 9 importance.
6. `findings/METHODOLOGY_CHANGELOG.md` — report-ready English explanation of every correction.

**Do not replace `00_data_understanding.ipynb`.** It remains a valid raw-data exploration. Keep your existing `findings/00_data_understanding.md` and `findings/01_preprocessing.md`; append a link to `findings/METHODOLOGY_CHANGELOG.md` to the latter, or reference it from the final report.

## Execution order

1. Run corrected notebook **01**, then save it.
2. Verify the generated dataset now records Q24 code 9 as missing where appropriate.
3. Run each corrected notebook 02–04 with `Run All` and save.
4. Regenerate all `results/02_*`, `results/03_*`, `results/04_*` CSVs.
5. Complete each findings file from these newly executed results.
6. Commit corrections before building Notebook 05.

## Commit suggestion

`fix: align survey coding and training-only model interpretation`

## Important notes

- Executed notebook outputs were cleared intentionally because they represent **pre-correction results**.
- The prior results and test scores are no longer directly comparable numerically with corrected results.
- No private respondent-level dataset is included in this corrections package.
- If a notebook fails to import the corrected module, verify that the local project path is correctly added to `sys.path`, and restart the notebook kernel.

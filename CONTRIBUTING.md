# Contributing

## Branching

Do not work directly on `main`.

```bash
git checkout main
git pull
git checkout -b feature/<short-name>
```

Suggested branches:

```text
feature/language-integration
feature/economic-living
feature/health-discrimination
feature/global-model
```

## Commit Style

Use Conventional Commits:

```text
feat: add language integration analysis
fix: handle missing values in codebook search
docs: document dataset setup
refactor: extract reusable preprocessing functions
test: add dataset validation tests
chore: update development dependencies
```

## Before a Pull Request

```bash
bash scripts/check.sh
```

Make sure:
- the code runs;
- tests pass;
- no raw dataset is staged;
- external code is attributed;
- the pull request explains what changed and why.

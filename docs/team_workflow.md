# Team Workflow

## Main Rule
`main` should contain reviewed and working code.

## Parallel Branches
- `feature/language-integration`
- `feature/economic-living`
- `feature/health-discrimination`
- `feature/global-model`

## Start Work
```bash
git checkout main
git pull
git checkout -b feature/<your-branch>
```

## Before Push
```bash
bash scripts/check.sh
git status
git add <files>
git commit -m "feat: describe the change"
git push -u origin <branch-name>
```

## Merge Rule
Merge only when:
1. the notebook/code runs;
2. tests pass;
3. the raw dataset is not staged;
4. the commit history is understandable;
5. another team member reviews the PR when possible.

#!/usr/bin/env python3
"""Public structure checks and optional private local-data/model-output audit.

Usage:
    python scripts/verify_release.py
    python scripts/verify_release.py --with-data
"""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import nbformat

ROOT = Path(__file__).resolve().parents[1]
NAMES = [
    '00_data_understanding', '01_preprocessing',
    '02_language_integration','03_economic_living',
    '04_health_discrimination','05_global_ml_model'
]
RESULT_STEMS = ['02_language','03_economic','04_health','05_global']


def verify_structure() -> None:
    required = [
        'README.md', 'CONTRIBUTING.md', 'LICENSE',
        'PROJECT_CONTRACT.md','MODEL_CONFIG.md',
        'findings/METHODOLOGY_CHANGELOG.md',
        'src/seoul_foreigners_ml/team_experiments.py',
        'report/FINAL_REPORT_DRAFT.md',
    ] + [f'notebooks/{name}.ipynb' for name in NAMES]
    missing = [p for p in required if not (ROOT / p).is_file()]
    assert not missing, f'Missing project files: {missing}'
    for name in NAMES:
        nb = nbformat.read(ROOT / 'notebooks' / f'{name}.ipynb', as_version=4)
        nbformat.validate(nb)
        for cell in nb.cells:
            if cell.cell_type == 'code':
                compile(cell.source, f'{name}.ipynb', 'exec')
                errors = [output for output in cell.get('outputs', []) if output.output_type == 'error']
                assert not errors, f'Notebook contains stored errors: {name}'
    print('[PASS] Project structure and all notebook code syntax')


def verify_local() -> None:
    data_dir = ROOT / 'data' / 'processed'
    full = pd.read_csv(data_dir / 'seoul_foreigners_modeling_master.csv')
    train = pd.read_csv(data_dir / 'train_ids.csv')['ID']
    test = pd.read_csv(data_dir / 'test_ids.csv')['ID']
    assert len(full) == full.ID.nunique() == 2500
    assert len(train) == train.nunique() == 2000
    assert len(test) == test.nunique() == 500
    assert not set(train).intersection(set(test))
    assert set(train).union(set(test)) == set(full.ID)
    assert full.Q11.notna().all()
    assert (full.high_satisfaction == (full.Q11 >= 8).astype(int)).all()
    for c in ['Q24_3','Q24_4','Q24_5','Q6_2','Q6_6','Q6_8','Q6_10']:
        assert not (full[c] == 9).any(), f'Unrevised special code 9: {c}'
    for prefix in RESULT_STEMS:
        for suffix in ['regression_cv','classification_cv','regression_test','classification_test','confusion_matrix',
                       'regression_importance','classification_importance']:
            p = ROOT / 'results' / f'{prefix}_{suffix}.csv'
            assert p.is_file() and p.stat().st_size > 5, f'Missing result {p.name}'
    print('[PASS] Dataset IDs, targets, special-code recoding, and all 02–05 metric exports')
    print(f'[INFO] Samples={len(full)}, train={len(train)}, test={len(test)}, class1={full.high_satisfaction.mean():.4%}')


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--with-data', action='store_true', help='Also validate locally generated private data and result CSVs')
    args=p.parse_args()
    verify_structure()
    if args.with_data:
        verify_local()

if __name__ == '__main__':
    main()

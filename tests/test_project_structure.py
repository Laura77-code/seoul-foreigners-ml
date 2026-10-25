from seoul_foreigners_ml.paths import PROJECT_ROOT


def test_required_project_files_exist():
    required = [
        "README.md",
        "LICENSE",
        "requirements.txt",
        "requirements-dev.txt",
        "pyproject.toml",
        "CONTRIBUTING.md",
    ]

    missing = [
        item
        for item in required
        if not (PROJECT_ROOT / item).exists()
    ]

    assert not missing, f"Missing required project files: {missing}"

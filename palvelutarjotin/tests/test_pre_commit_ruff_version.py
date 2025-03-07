import re

RUFF_VERSION_PRE_COMMIT_REGEX = re.compile(
    r"rev: v(\d+(\.\d+)+)\s*# ruff-pre-commit version"
)


def get_ruff_version_from_dev_requirements() -> str | None:
    with open("./requirements-dev.txt") as file:
        dev_requirements = file.read()
    for line in dev_requirements.splitlines():
        if line.startswith("ruff=="):
            return line.split("==")[1].strip()
    return None


def get_ruff_version_from_pre_commit_config() -> str | None:
    with open("./.pre-commit-config.yaml") as file:
        pre_commit_config = file.read()
    for line in pre_commit_config.splitlines():
        match = RUFF_VERSION_PRE_COMMIT_REGEX.search(line)
        if match:
            return match.group(1)
    return None


def test_ruff_is_in_dev_requirements():
    ruff_version_dev_requirements = get_ruff_version_from_dev_requirements()
    assert ruff_version_dev_requirements is not None


def test_ruff_is_in_pre_commit_config():
    ruff_version_pre_commit = get_ruff_version_from_pre_commit_config()
    assert ruff_version_pre_commit is not None


def test_ruff_same_in_dev_requirements_and_pre_commit_config():
    ruff_version_dev_requirements = get_ruff_version_from_dev_requirements()
    ruff_version_pre_commit = get_ruff_version_from_pre_commit_config()
    assert ruff_version_dev_requirements == ruff_version_pre_commit

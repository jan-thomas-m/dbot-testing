# dbot-testing

Testing various dependabot grouping update scenarios
Goal: To have dependabot configured to bundle minor and patch updates into same PR, but raise separate PR for each major update

TLDR; Seems impossible to group minor + patch updates into 1 PR, and at the same time allow major updates as separate PRs. (at least as per Jul 14, 2026)

## Baseline config

`requirements.txt`

```text
pytest>=7.0.0
ruff>=0.15.17
check-jsonschema>=0.37.3
```

## Test scenarios

### 1. Without any grouping

`.github/dependabot.yml`

```yaml
---
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 5
    target-branch: "main"
    labels:
      - "dependencies"
      - "python"
```

PRs

Update pytest requirement from >=7.0.0 to >=9.1.1
Update ruff requirement from >=0.15.17 to >=0.15.21
Update check-jsonschema requirement from >=0.37.3 to >=0.37.4

### Group all minor+patch

`.github/dependabot.yml`

```yaml
---
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "daily"
    groups:
      minor-and-patch:
        patterns:
          - "*"
    ignore:
        - dependency-name: "*"
          update-types:
            - "version-update:semver-major"
```

PRs

Updates the requirements on pytest, ruff and check-jsonschema to permit the latest version.
Updates pytest to 7.4.4
Updates ruff to 0.15.21
Updates check-jsonschema to 0.37.4


This kind of work, but pytest is NOT upgraded to 9.y.z, only to latest 7.y.z

### Group all

`.github/dependabot.yml`

```yaml
---
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 5
    target-branch: "main"
    labels:
      - "dependencies"
      - "python"
    groups:
      minor-and-patch:
        applies-to: version-updates
        patterns:
          - "*"
```

PRs

Updates the requirements on pytest, ruff and check-jsonschema to permit the latest version.
Updates pytest to 9.1.1
Updates ruff to 0.15.21
Updates check-jsonschema to 0.37.4

Again, kind of works, but pytest is still bundled into the group, although this time major upgrade to latest.

### Group, with update-types minor+patch

This is what internet and most of GSD is using

`.github/dependabot.yml`

```yaml
---
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 5
    target-branch: "main"
    labels:
      - "dependencies"
      - "python"
    groups:
      minor-and-patch:
        applies-to: version-updates
        patterns:
          - "*"
        update-types:
          # - "major"
          - "minor"
          - "patch"
```

PRs

Update pytest requirement from >=7.0.0 to >=9.1.1
Update ruff requirement from >=0.15.17 to >=0.15.21
Update check-jsonschema requirement from >=0.37.3 to >=0.37.4

dependabot log

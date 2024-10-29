# Contributing to Quipus :knot:

Thank you for your interest in contributing to Quipus! This document provides guidelines for collaborating on the development and improvement of the project.

## Table of Contents
1. [Reporting Issues](#reporting-issues)
2. [Suggestions and Improvements](#suggestions-and-improvements)
3. [Code Contribution](#code-contribution)
4. [Code Style Standards](#code-style-standards)
5. [Commit Format](#commit-format)
6. [Testing](#testing)
7. [Pull Requests](#pull-requests)

---

## Reporting Issues

If you find a bug, please follow these steps:
1. **Check** that the issue hasn’t already been reported [here](https://github.com/Monkey-Market/quipus/issues).
2. **Create a new issue** if there isn’t a similar report. Include:
   - Quipus and Python version.
   - Detailed description of the problem.
   - Steps to reproduce the bug.
   - Relevant error messages, logs, or screenshots.

## Suggestions and Improvements

We welcome improvements! If you have an idea to enhance Quipus:
1. **Check for an existing issue** in case someone has already suggested it.
2. If you don’t find one, **create a new issue** with details about the improvement or feature.

## Code Contribution

If you’d like to contribute code, please follow these steps:
1. **Fork the repository** and clone the fork to your local machine.
2. **Create a branch** using a descriptive naming convention like `fix/issue-XX` or `ft/new-feature`.
3. Add tests for your changes if necessary.
4. Ensure all existing tests pass.
5. Follow the [style standards](#code-style-standards) and [commit format](#commit-format).
6. **Submit a Pull Request** to the `main` branch.

## Code Style Standards

Our code follows **PEP 8** guidelines. We use [Pylint](https://github.com/Monkey-Market/quipus/actions/workflows/pylint.yml) to check style in CI, aiming for a **minimum score of 9.5**. Be sure to:
- Write clear, well-documented code using descriptive variable and function names.
- Use static typing in functions and classes.
- Add docstrings to classes and functions.

To contribute, please install the development dependencies specified in `pyproject.toml`.

## Commit Format

We use the following commit format to aid tracking and reviewing:
- `feat: | [FT]` for a new feature.
- `fix: | [FIX]` for a bug fix.
- `docs: | [DOC]` for documentation changes.
- `style: | [LINT]` for formatting changes (no code logic changes).
- `refactor: | [REF]` for changes that are not a new feature or bug fix.
- `test: | [TEST]` for adding or updating tests.
- `chore: | [CH]` for maintenance tasks.

Example:
```console
$ git commit -m "feat: add SFTP support to TemplateManager"
$ git commit -m "[FT] Add SFTP support to TemplateManager"
```

## Testing

Code contributions should include tests. We use **Pytest** and aim for high coverage on key modules. To run tests:

```bash
pytest tests/
```

If you add functionality, be sure to add relevant tests in the `tests/` directory. Tests also run automatically in CI when you submit a PR.

## Pull Requests

To submit a Pull Request (PR):
1. Make sure your PR targets the `main` branch.
2. Include a clear description of the PR’s purpose and reference any relevant issues.
3. Ensure all tests pass and coverage is acceptable.
4. If relevant, include documentation about the change in the PR.

---

*Thank you for contributing to Quipus!*  
*Your support is essential to improving this tool!* 💙
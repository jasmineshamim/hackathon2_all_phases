# Phase 1 Console App - Claude Code Instructions

This file provides phase-specific context for Claude Code when working on Phase 1.

## Phase Context

- **Phase ID**: `phase-1-console`
- **Status**: ✅ Active
- **Goal**: Build in-memory Python console todo app
- **Points**: 100

## Technology Stack

- Python 3.13+
- UV (package manager)
- In-memory storage (no database)

## Core Features

1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete

## Working Directory

All implementation happens in `phase-1-console/`:

- Source code: `phase-1-console/src/`
- Tests: `phase-1-console/tests/`
- Demo: `phase-1-console/demo.py`

## Running the App

```bash
cd phase-1-console/src
python todo_app.py
```

## Running Tests

```bash
cd phase-1-console/tests
python -m pytest test_app.py -v
```

## Spec Location

Feature specs are in `specs/phase-1-console/core-features/`

## Constraints (Phase-Specific)

- Console-only interface (no GUI, no web)
- In-memory storage (no file persistence, no database)
- No external services or dependencies

## Reference

See `.specify/memory/constitution.md` for global project rules.

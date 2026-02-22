# Agent Instructions for OptOps Project

This file provides guidelines for AI agents working on this codebase.
Read this before writing, editing, or reviewing any code.

---

## Project Overview

This is a Python web application that solves the **Facility Location Problem** (assign customers
to open facilities minimizing total distance). The stack is:

- **Backend**: FastAPI (Python 3.11)
- **Frontend**: Vanilla HTML/CSS/JS (no frameworks)
- **Testing**: pytest
- **Containerization**: Docker
- **CI/CD**: GitHub Actions → deploy to Render

---

## Project Structure

```
app/
  controllers/   # HTTP routing only — no business logic here
  models/        # Pydantic data models — pure data, no logic
  services/      # Business logic and solvers
  static/
    css/         # style.css — one file
    js/          # app.js — one file
    index.html   # single-page UI
  main.py        # App entrypoint, mounts static files and routers
tests/           # Mirrors app/ structure exactly
```

---

## Architecture Rules

- **Controllers** handle HTTP only: parse requests, call services, return responses. No logic.
- **Services** contain all business logic and optimization algorithms.
- **Models** are pure Pydantic data classes. No methods with side effects.
- **main.py** is for app initialization only. Do not add business logic here.
- The frontend communicates with the backend exclusively via the `/api/*` endpoints.
- Do not add new dependencies without explicit discussion.

---

## Python Guidelines

- Python version: **3.11**
- Formatter: follow PEP8. Max line length: **88 characters** (Black-compatible).
- Use **type hints** on all function signatures.
- Use **Pydantic models** for all API request and response bodies — never raw dicts.
- Use **Google-style docstrings** on all public classes and functions.
- Prefer `pathlib.Path` over `os.path`.
- Do not use global mutable state.

---

## Testing Rules

- Framework: **pytest only**.
- Test file location must **mirror the source structure** exactly.
  - `app/services/simple_solver.py` → `tests/services/test_simple_solver.py`
- Every public function must have tests covering:
  - The happy path.
  - Relevant edge cases (empty input, boundary values, invalid input).
- Do not mock unless I/O or external services are involved.
- Tests must pass before any code is merged.

### Test Naming Convention

```
test__<unit>__<behavior>__<expected_result>
```

Examples:
- `test__solve_random__single_facility__all_customers_assigned_to_it`
- `test__solve_random__no_facilities__raises_value_error`

### Test Body — AAA Pattern

Every test must follow the **Arrange / Act / Assert** structure with explicit comments:

```python
def test__solve_random__normal_instance__returns_valid_solution():
    # Arrange
    instance = FacilityLocationInstance(...)

    # Act
    solution = solve_random(instance)

    # Assert
    assert len(solution.assignments) == instance.n_customers
```

---

## API Design Rules

- All endpoints live under the `/api/` prefix.
- Use RESTful conventions (POST for creation/computation, GET for retrieval).
- Always validate with Pydantic — never trust raw input.
- Return meaningful HTTP status codes (422 for validation errors, 500 for server errors).
- Error responses must include a human-readable message.

---

## Frontend Rules

- **Vanilla JS only** — no React, Vue, jQuery, or any external JS framework.
- All JS lives in `app/static/js/app.js`. Do not split into multiple files unless explicitly asked.
- All CSS lives in `app/static/css/style.css`.
- The canvas (500×500px) maps to a 100×100 unit grid. Scale factor is always `CANVAS_SIZE / GRID_SIZE`.
- Keep the two global state variables (`currentInstance`, `currentSolution`) and do not add more globals.
- Always handle loading states on buttons (disable + change text while awaiting).
- Always handle and display API errors in the `#errorContainer` element.

---

## CI/CD Rules

- All tests must pass in GitHub Actions before merging.
- Docker images are published to: `ghcr.io/fjzs/optimization-api`
- Do not modify the Dockerfile or GitHub Actions workflows without explicit instruction.

---

## Principles from *A Philosophy of Software Design* (Ousterhout)

These principles must guide every design decision in this codebase.

### 1. Complexity is the Root of All Evil
Complexity is anything that makes code hard to understand or modify. It manifests as:
- **Change amplification**: a simple change requires edits in many places.
- **Cognitive load**: the reader needs to hold too much in their head to understand the code.
- **Unknown unknowns**: it is unclear what needs to change or where.

> Always ask: *does this change make the system easier or harder to understand?*

### 2. Deep Modules
Good modules have **simple interfaces and rich functionality** hidden behind them.
A deep module does a lot of work but exposes little complexity to its callers.

- Services (e.g. `simple_solver.py`) should be deep: complex logic, simple API.
- Avoid shallow modules that expose more complexity than they hide (e.g. a function
  that is just a one-line wrapper with no added abstraction).

### 3. Information Hiding
Each module should **hide design decisions** that are likely to change. Callers should
not need to know implementation details.

- The solver algorithm is hidden behind the service interface. Controllers do not know
  how the solver works internally.
- Internal data structures of models should not leak into controllers or the frontend.

### 4. Avoid Information Leakage
Information leakage occurs when a design decision is reflected in multiple modules,
creating tight coupling. If you find yourself duplicating a concept across files, it
should be encapsulated in one place.

- Do not duplicate validation logic between the frontend and backend models.
  The backend Pydantic model is the single source of truth.

### 5. General-Purpose Modules (Somewhat General)
Write modules that are slightly more general than the immediate use case. This makes
them easier to reuse and reduces future complexity.

- The `Point` model should not be tied to facilities or customers — it is rightly a
  general coordinate class.
- The `generator.py` should not embed solver-specific assumptions.

### 6. Design Errors Out of Existence
Rather than detecting and handling errors, design your interfaces so that errors
cannot occur in the first place.

- Use Pydantic `Field` constraints (`gt=0`, `le=100`) to make invalid states
  unrepresentable, rather than checking values inside functions.

### 7. Define Errors Out of Existence (for Exceptions)
Do not proliferate special cases and exceptions. If a function can be designed to
handle edge cases naturally (returning an empty list instead of raising), prefer that.

- Only raise exceptions for truly exceptional, unrecoverable situations.

### 8. Pull Complexity Downward
If complexity must exist, push it into lower-level modules (services), not upward
into callers (controllers, frontend). Users of a module should not have to deal with
its complexity.

- The controller should call `solver.solve(instance)` and get back a clean solution.
  The controller should never have to handle solver-internal intermediate states.

### 9. Different Layer, Different Abstraction
Each layer of the system should have a clearly different vocabulary and abstraction
level. If two adjacent layers look very similar, one of them is probably unnecessary.

- The API layer speaks in HTTP requests and JSON.
- The service layer speaks in domain objects (`FacilityLocationInstance`, assignments).
- The model layer speaks in pure data structures.

### 10. Comments Should Describe *What* and *Why*, Not *How*
Code explains *how*. Comments should explain *what* the code is doing at a higher
level and *why* a decision was made.

- If the *how* needs explaining, the code is probably too complex and should be refactored.
- Document every public class and function with a docstring that explains its purpose
  and any non-obvious constraints.
- Use inline comments only when the reason behind a decision is not evident from the code.

### 11. Names Matter
Choose names that make the meaning of variables, functions, and classes unambiguous.
A name should make it unnecessary to look at the implementation to understand its role.

- Prefer `n_customers` over `nc` or `num`.
- Prefer `open_facilities` over `result` or `data`.
- If you struggle to name something, it may be a sign the abstraction is unclear.

### 12. Consistency
Apply the same conventions everywhere. Consistency reduces cognitive load because
readers can apply their existing knowledge.

- If one endpoint uses `snake_case` for JSON fields, all endpoints must.
- If one model uses `Field(gt=0)` for positive integers, all models must do the same.

### 13. Obvious Code
Code is obvious if a reader can understand its behavior quickly, without consulting
documentation or tracing through other files.

- Avoid clever tricks. Prefer clear and explicit code over concise and implicit code.
- Avoid deep nesting. Flatten logic with early returns.

### 14. Write Code Twice (Design Twice)
Before committing to an implementation, sketch at least two alternative designs.
Compare their interfaces and complexity. Choose the simpler interface even if the
implementation is harder.

---

## What NOT To Do

- Do not add logic to `main.py`.
- Do not bypass Pydantic validation by accepting `dict` or `Any` in endpoints.
- Do not introduce new global variables in `app.js`.
- Do not use `print()` for debugging — use Python's `logging` module.
- Do not write a test that only tests that a function runs without error — test the output.
- Do not write shallow wrapper functions that add no abstraction.
- Do not repeat validation logic in multiple places.
- Do not break the existing test structure when adding new features.

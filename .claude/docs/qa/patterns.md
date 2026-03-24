<!-- last_verified: 2026-03-04 -->
# QA Patterns

Reusable patterns for test quality analysis and coverage assessment.

## Coverage Gap Discovery

### Systematic File Walk
1. List all source files (`src/**/*.{py,ts,js,go}`)
2. List all test files (`tests/**/*`, `**/*.test.*`, `**/*.spec.*`)
3. Map source files to their test counterparts
4. Flag source files with no corresponding test file
5. For matched pairs, compare public function count vs test function count

### Boundary Analysis
Every system boundary should have integration tests:
- External API calls (HTTP clients, SDKs)
- Database queries (especially writes, transactions, migrations)
- File system operations (reads, writes, permissions)
- Message queues (publish, consume, retry)
- Auth boundaries (login, token refresh, permission checks)
- User input entry points (forms, API endpoints, CLI args)

### Risk-Based Prioritization Matrix

| Code Characteristic | Coverage Priority |
|---------------------|-------------------|
| Handles money/payments | Critical |
| Auth/authorization logic | Critical |
| Data mutation (writes, deletes) | Critical |
| User-facing error messages | High |
| State machine transitions | High |
| Concurrent/async logic | High |
| Configuration parsing | Medium |
| Logging/telemetry | Low |
| Pure display/formatting | Low |

## Test Quality Signals

### Strong Tests
- Test name describes the scenario and expected outcome
- Single assertion per concept (may be multiple assert statements)
- Uses factory/builder patterns for test data, not hardcoded fixtures
- Tests behavior ("returns 401") not implementation ("calls validateToken once")
- Includes setup, action, and assertion phases (Arrange-Act-Assert)

### Weak Tests
- Test name is `test_1`, `test_function`, or matches function name exactly
- Assertions only check "no exception thrown" or "result is not None"
- Tests pass when you delete the implementation (vacuous truth)
- Snapshot tests on frequently-changing output
- Tests that sleep for fixed durations instead of polling/awaiting
- Tests that depend on system clock, network, or filesystem state

### Test Smell Catalog

| Smell | Symptom | Fix |
|-------|---------|-----|
| Giant test | >50 lines, multiple actions | Split into focused scenarios |
| Mystery guest | Test uses external file/fixture not visible in test | Inline test data or use explicit factory |
| Eager test | Tests multiple behaviors at once | One test per behavior |
| Liar test | Always passes regardless of implementation | Add meaningful assertions |
| Fragile test | Breaks on unrelated changes | Test behavior, not structure |
| Slow test | >5s for a unit test | Mock expensive deps, parallelize |

## Regression Risk Indicators

### High-Risk Patterns
- Recently refactored code with no new tests added
- Functions with cyclomatic complexity >10 and <80% coverage
- Code paths that handle multiple error types with shared recovery logic
- Implicit dependencies (global state, singletons, env vars)
- Areas where bugs have been found before (bug-prone modules)

### Change Impact Analysis
When evaluating a code change for regression risk:
1. What functions were modified?
2. What calls those functions? (blast radius)
3. Are callers tested?
4. Were any contracts (types, schemas, API shapes) changed?
5. Were any default values or fallback behaviors changed?

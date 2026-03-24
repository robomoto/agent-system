<!-- last_verified: 2026-03-21 -->
# QA Footguns

Common testing mistakes that create false confidence or fragile test suites.

## Coverage Theater

High coverage percentage that misses critical paths:
- Testing getters/setters and framework boilerplate inflates numbers
- 90% line coverage with 0% branch coverage on error paths
- Tests that execute code but don't assert meaningful outcomes

**Detection:** Compare coverage report against the risk matrix in `patterns.md`. If critical paths (auth, payments, data mutation) show lower coverage than utility code, coverage is theatrical.

## Test Interdependence

Tests that pass in full suite but fail in isolation (or vice versa):
- Shared mutable state between tests (global variables, class-level state)
- Tests that depend on execution order (`test_create` must run before `test_read`)
- Database tests that don't clean up (shared test DB without transactions)

**Detection:** Run tests in random order. In pytest: `pytest -p random`. In Jest: `--randomize`.

## Over-Mocking

Mocks that mask real failures:
- Mocking the database in integration tests (prod migration breaks, mock passes)
- Mocking internal modules when testing their consumers
- Mocks that return hardcoded success for every input

**Rule of thumb:** Mock at system boundaries (external APIs, clock, filesystem). Don't mock internal collaborators unless they have side effects you can't control.

## Happy-Path-Only Testing

Only testing the success case:
- Login test with valid credentials but no test for invalid, locked, rate-limited
- API test that sends well-formed JSON but never malformed, empty, or oversized
- File upload test with valid files but never empty, too large, wrong type

**Checklist per function:** What happens with null/empty input? Invalid types? Boundary values? Concurrent calls? Permission denied?

## Testing Implementation Details

Tests coupled to internal structure rather than behavior:
- Asserting exact method call counts on internal mocks
- Testing private methods directly
- Asserting specific SQL queries instead of query results
- Tests that break on harmless refactors (renaming internal variables)

**Test behavior:** "given X input, expect Y output" not "given X input, expect method Z to be called 3 times with args A, B, C."

## Brittle Snapshot Tests

Snapshots that capture too much and break on irrelevant changes:
- Full HTML snapshots that break when CSS classes change
- API response snapshots that break when an unrelated field is added
- Large snapshot files that nobody reviews (just `--update` and commit)

**Use snapshots for:** Serialized output formats, error messages, small structured data. **Don't use for:** Rendered HTML, large API responses, anything with timestamps or IDs.

## Flaky Tests from Timing

Tests that pass 95% of the time:
- `setTimeout` / `sleep` in tests waiting for async operations
- Race conditions in concurrent test setups
- Tests that depend on wall-clock time or system timezone
- Network-dependent tests without retry/timeout handling

**Fix:** Use deterministic waits (polling for condition), inject clocks, isolate network calls.

## Inverted Test Pyramid

Too many E2E tests, not enough unit tests:
- Slow test suite (>5min for <1000 LOC)
- E2E tests that duplicate unit test coverage
- No unit tests for business logic, only browser automation

**Target ratio (rough):** 70% unit, 20% integration, 10% E2E. The exact numbers matter less than the shape.

## Assertion-Free Tests

Tests that exercise code but never check results:
```python
# Bad: no assertion
def test_process_order():
    order = create_test_order()
    process_order(order)  # just checking it doesn't throw

# Good: meaningful assertion
def test_process_order():
    order = create_test_order()
    result = process_order(order)
    assert result.status == "completed"
    assert result.total == Decimal("42.00")
```

## Test Data Rot

Test fixtures that drift from production reality:
- Hardcoded test data from 2 years ago that no longer matches schema
- Factory objects that skip required validations
- Seed data that creates impossible states (user with no email, order with negative total)

**Fix:** Use factory libraries (factory_boy, Fishery) that respect model constraints. Validate test data against the same schemas as production data.

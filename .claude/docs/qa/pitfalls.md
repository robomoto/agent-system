# QA Pitfalls

Common mistakes in test strategy and quality assessment.

## Coverage Metric Traps

### Coverage != Quality
- 100% line coverage with no assertions is worthless
- Branch coverage matters more than line coverage for conditional logic
- Mutation testing reveals whether tests actually catch bugs, not just execute code
- A single well-designed property-based test can cover more cases than 20 example-based tests

### Gaming Coverage
- Tests that call functions but don't assert results inflate coverage without adding safety
- Catch-all exception handlers that swallow errors make bad code appear tested
- Testing private methods directly bypasses the public API contract

## Analysis Anti-Patterns

### Over-Flagging
- Don't flag missing tests for trivial code (getters, setters, data classes with no logic)
- Don't flag missing unit tests when good integration tests already cover the path
- Don't recommend tests that would be pure duplication of framework guarantees
- Not every function needs its own test file — assess at the module level

### Under-Flagging
- Don't ignore error paths just because the happy path is tested
- Don't assume concurrency is safe because sequential tests pass
- Don't skip security-relevant code just because "it uses a well-known library"
- Don't dismiss flaky tests — they often indicate real race conditions or state leaks

### False Confidence
- "All tests pass" doesn't mean the code is correct — it means the tests don't fail
- High coverage on the wrong code (utilities, helpers) while core logic is untested
- Tests that mock so heavily they only test the mocking framework
- Tests written after the fact to match existing behavior (cementing bugs as features)

## Test Architecture Pitfalls

### Inverted Pyramid
- Too many slow E2E tests, not enough fast unit tests
- Symptom: CI takes 30+ minutes, developers skip running tests locally
- Fix: Extract testable logic into pure functions, test at unit level

### Missing Middle
- Unit tests + E2E tests but no integration tests
- Symptom: Individual units work but break when connected
- Fix: Add tests at service boundaries (API contracts, DB queries)

### Test Data Drift
- Hardcoded test fixtures that don't match current schema
- Factory/builder patterns that produce invalid objects
- Seed data that assumes a specific database state
- Fix: Derive test data from the same schemas/types as production data

## Process Pitfalls

### "Write Tests Later"
- Tests deferred to "after the feature is done" rarely get written
- The best time to identify test cases is during implementation, not after
- Acceptance criteria should be testable before implementation starts

### Flaky Test Tolerance
- Each flaky test erodes trust in the entire suite
- Developers learn to ignore failures, including real ones
- Quarantine flaky tests immediately; fix or delete within a week

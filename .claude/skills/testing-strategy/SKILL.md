# Skill: Testing Strategy

Framework for deciding what to test, how to test it, and what coverage to target. Used by the implementer when writing tests and the reviewer when evaluating test coverage.

## When to Use

- Implementer is writing tests for a new feature
- Reviewer is evaluating whether test coverage is sufficient
- Architect is specifying testing requirements in a design

## Test Pyramid

Prefer more tests at the bottom, fewer at the top:

```
        /  E2E  \          Few — slow, brittle, high confidence
       /----------\
      / Integration \      Some — test boundaries and contracts
     /----------------\
    /    Unit Tests     \   Many — fast, isolated, specific
   /--------------------\
```

### Unit Tests (most)
- Test a single function or method in isolation
- Mock external dependencies
- Fast (<100ms each)
- Cover: happy path, edge cases, error cases, boundary values

### Integration Tests (some)
- Test interactions between components
- Use real dependencies where practical (test database, local server)
- Moderate speed (<5s each)
- Cover: API contracts, database queries, service interactions

### E2E Tests (few)
- Test complete user flows
- Run against a real (or near-real) environment
- Slow but high confidence
- Cover: critical business paths only (login, payment, core workflow)

## What to Test

### Always Test
- Public API surface (every public function/method/endpoint)
- Error handling paths (not just happy path)
- Boundary values (0, 1, max, empty, null)
- Security-relevant logic (auth, authorization, input validation)
- Business rules (the core logic that justifies the code's existence)

### Test When Relevant
- Concurrent access patterns (if code is shared across threads/requests)
- Performance under load (if there are latency/throughput requirements)
- Configuration variations (if behavior changes based on config)
- Migration paths (if code handles data format changes)

### Don't Test
- Framework internals (trust that Django/React/Spring work)
- Private implementation details (test behavior, not structure)
- Trivial getters/setters with no logic
- Third-party library behavior (unless you're wrapping it)

## Coverage Targets

| Layer | Target | Rationale |
|-------|--------|-----------|
| Business logic | 90%+ | This is why the code exists |
| API handlers | 80%+ | System boundary, needs validation |
| Data access | 70%+ | Test queries, not ORM internals |
| UI components | 60%+ | Test behavior, not rendering details |
| Utilities/helpers | 90%+ | Small, testable, high reuse |
| Config/setup | 30%+ | Mostly declarative, low risk |

These are guidelines, not mandates. 80% coverage of the right code beats 100% coverage of the wrong code.

## Test Naming Convention

```
test_<what>_<scenario>_<expected>

test_authenticate_validToken_returnsUser
test_authenticate_expiredToken_returns401
test_authenticate_missingHeader_returns401
test_createOrder_insufficientStock_throwsError
```

## Edge Cases Checklist

For every function under test, consider:
- [ ] Empty input (empty string, empty list, null/None)
- [ ] Single element (list of one, string of one character)
- [ ] Boundary values (0, -1, MAX_INT, minimum date)
- [ ] Invalid types (string where int expected, if language allows)
- [ ] Unicode and special characters
- [ ] Concurrent calls (if applicable)
- [ ] Very large input (if performance matters)
- [ ] Permission denied / unauthorized access

## Anti-Patterns

- **Testing implementation**: Asserting that a private method was called 3 times. Test the outcome instead.
- **Snapshot overuse**: Snapshots break on any change, including harmless ones. Use for stable output only.
- **Test interdependence**: Tests that must run in order or share state. Each test should be independent.
- **Mocking everything**: If you mock the database, the HTTP client, and the filesystem, what are you actually testing?
- **Happy path only**: If your tests only cover the success case, they're not tests — they're demos.

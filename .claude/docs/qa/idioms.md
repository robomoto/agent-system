<!-- last_verified: 2026-03-21 -->
# QA Idioms

Reusable testing patterns across languages and frameworks.

## Arrange-Act-Assert (AAA)

Every test has three phases. Blank lines separate them:

```python
def test_expired_token_rejected():
    # Arrange
    token = create_token(expires_at=datetime(2020, 1, 1))

    # Act
    result = validate_token(token)

    # Assert
    assert result.is_valid is False
    assert result.error == "token_expired"
```

One Act per test. Multiple asserts are fine if they verify the same logical outcome.

## Test Naming: What_When_Then

Name should describe the scenario, not the implementation:

```python
# Good: describes behavior
test_login_with_expired_password_returns_password_reset_prompt
test_order_total_includes_tax_for_taxable_items
test_upload_rejects_files_over_10mb

# Bad: describes implementation
test_validate_method
test_process_order_calls_calculate_tax
test_file_size_check
```

## Fixture Design: Factory Pattern

Build test objects with factories, not raw constructors:

```python
# Factory with sensible defaults and overrides
def make_user(**overrides):
    defaults = {
        "name": "Test User",
        "email": f"user-{uuid4().hex[:8]}@test.com",
        "role": "member",
        "created_at": datetime.now(UTC),
    }
    return User(**(defaults | overrides))

# Usage: only specify what matters for this test
def test_admin_can_delete_posts():
    admin = make_user(role="admin")
    post = make_post(author=make_user())
    assert admin.can_delete(post) is True
```

**Key principle:** Each test specifies only the data relevant to what it's testing. Everything else gets sensible defaults.

## Boundary Value Analysis

Test at the edges of valid ranges:

| Boundary | Test values |
|----------|-------------|
| Numeric range (1-100) | 0, 1, 2, 99, 100, 101 |
| String length (max 255) | "", "a", "a"*254, "a"*255, "a"*256 |
| Collection (non-empty) | [], [one], [many] |
| Date range | day before start, start, end, day after end |
| File size (max 10MB) | 0 bytes, 1 byte, 9.99MB, 10MB, 10.01MB |

## Equivalence Partitioning

Group inputs that should produce the same behavior, test one from each group:

```
Input: age for ticket pricing
Partitions:
  - Child:  0-12  → test age=6
  - Adult: 13-64  → test age=30
  - Senior: 65+   → test age=70
  - Invalid: <0   → test age=-1
  - Edge: 12, 13, 64, 65 (boundaries between partitions)
```

Don't test age=5 AND age=6 AND age=7 — they're in the same partition.

## Integration Test Isolation

### Database: Transaction Rollback

```python
@pytest.fixture(autouse=True)
def db_transaction(db):
    """Wrap each test in a transaction that rolls back."""
    with db.begin_nested() as savepoint:
        yield db
        savepoint.rollback()
```

### External APIs: Record/Replay

Use VCR/cassette libraries to record real HTTP responses and replay them:
- First run hits the real API and records
- Subsequent runs replay from cassette (fast, deterministic, offline)
- Re-record periodically to catch API changes

### Time: Freeze the Clock

```python
from freezegun import freeze_time

@freeze_time("2025-01-15 12:00:00")
def test_subscription_expires_after_30_days():
    sub = create_subscription()
    assert sub.expires_at == datetime(2025, 2, 14, 12, 0, 0)
```

## Test Pyramid Balance

```
        /  E2E  \        ~10% — Critical user journeys only
       / Integration \    ~20% — System boundaries, API contracts
      /    Unit Tests  \  ~70% — Business logic, pure functions
```

**Unit tests** should be: fast (<100ms each), isolated (no I/O), deterministic.
**Integration tests** should cover: DB queries, API calls, message passing, file I/O.
**E2E tests** should cover: Login flow, core purchase/create/delete journeys, critical paths only.

## Property-Based Testing

When the input space is large and behavior has invariants:

```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_preserves_length(xs):
    assert len(sorted(xs)) == len(xs)

@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs):
    assert sorted(sorted(xs)) == sorted(xs)

@given(st.lists(st.integers(), min_size=1))
def test_sort_first_element_is_minimum(xs):
    assert sorted(xs)[0] == min(xs)
```

**Good for:** parsers, serializers, encoders, mathematical operations, data transformations.
**Overkill for:** simple CRUD, UI interactions, config loading.

## Test Organization

```
tests/
├── unit/           # Pure logic, no I/O
│   ├── test_pricing.py
│   └── test_validation.py
├── integration/    # DB, APIs, file system
│   ├── test_user_repo.py
│   └── test_email_service.py
├── e2e/            # Full user journeys
│   └── test_checkout_flow.py
├── conftest.py     # Shared fixtures
└── factories.py    # Test data factories
```

Run unit tests on every save. Integration on every commit. E2E on every PR.

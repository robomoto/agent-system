# Skill: Code Review

Structured code review framework used by the reviewer agent. Provides a severity-based checklist and consistent finding format.

## When to Use

- Reviewer is assigned to review an implementation
- Lead wants a quality gate before accepting code
- Any agent needs to self-check code quality before handing off

## Review Protocol

### 1. Preparation

- Read the task spec or architect's design to understand intent
- Identify the language and load `.claude/docs/<language>/footguns.md` if it exists
- Run `git diff` or identify changed files to scope the review

### 2. First Pass: Correctness

Walk through the code as if executing it mentally:
- Does it do what the spec says?
- Are edge cases handled (null, empty, boundary values, overflow)?
- Are error paths complete (what happens when external calls fail)?
- Is concurrency handled correctly (race conditions, deadlocks, shared state)?

### 3. Second Pass: Security

Check against OWASP top 10 and language-specific vectors:
- [ ] Injection (SQL, command, template, LDAP)
- [ ] Broken authentication (token handling, session management)
- [ ] Sensitive data exposure (logging secrets, unencrypted storage)
- [ ] Broken access control (authorization checks on every path)
- [ ] Security misconfiguration (debug mode, default credentials, open CORS)
- [ ] XSS (user input in HTML/JS output)
- [ ] Insecure deserialization (untrusted input to deserializers)
- [ ] Dependency vulnerabilities (known CVEs in imports)

### 4. Third Pass: Quality

- Test coverage: are critical paths tested? Are edge cases covered?
- Error messages: helpful to the caller? No internal details leaked?
- Naming: do names communicate intent?
- Complexity: could any function be simplified without losing clarity?
- Duplication: is there copy-paste code that should be shared?

### 5. Adversarial Pass

- What would a malicious user send to this code?
- What happens if this code runs 1000x concurrently?
- What happens if a dependency is 10x slower than expected?
- What assumptions does this code make about its callers?

## Severity Definitions

| Severity | Meaning | Action |
|----------|---------|--------|
| **critical** | Security vulnerability, data loss risk, incorrect core logic | Blocks acceptance. Must fix before proceeding. |
| **warning** | Performance issue, missing validation, insufficient tests | Fix before merge. Can proceed to validation with caveats. |
| **suggestion** | Readability, minor style, documentation | Nice to have. Don't block on these. |

## Finding Format

Each finding must include all fields:

```json
{
  "severity": "critical|warning|suggestion",
  "category": "security|correctness|performance|maintainability|testing",
  "location": "path/to/file:line",
  "description": "What's wrong — be specific",
  "suggested_fix": "How to fix it — be actionable",
  "adversarial_note": "What could go wrong if unfixed — be concrete"
}
```

## Rules

- No finding without a location. "The code has issues" is not a finding.
- No severity without justification. Why is this critical vs. warning?
- No suggested_fix that is just "fix this". Provide the actual fix or a clear approach.
- Verify tests yourself. `status: approved` means you ran the tests and they passed.
- If no issues found, say so explicitly. Don't manufacture findings to look thorough.

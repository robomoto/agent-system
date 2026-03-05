# Skill: Security Audit

Systematic security review framework. Used by the reviewer for security-focused review and by the architect when designing security-sensitive systems.

## When to Use

- Reviewing code that handles authentication, authorization, or user input
- Designing systems that store sensitive data or face the public internet
- Evaluating third-party dependencies for known vulnerabilities
- Any code that processes untrusted input

## OWASP Top 10 Checklist (2021)

### A01: Broken Access Control
- [ ] Every endpoint checks authorization, not just authentication
- [ ] Authorization is deny-by-default (whitelist, not blacklist)
- [ ] No IDOR — users can't access other users' resources by changing IDs
- [ ] CORS is restricted to known origins (not `*` in production)
- [ ] Directory listing is disabled
- [ ] API rate limiting is in place

### A02: Cryptographic Failures
- [ ] Sensitive data encrypted at rest and in transit
- [ ] TLS 1.2+ for all connections
- [ ] No hardcoded secrets, keys, or passwords
- [ ] Passwords hashed with bcrypt/scrypt/argon2 (not MD5/SHA1)
- [ ] No sensitive data in URLs, logs, or error messages

### A03: Injection
- [ ] SQL: parameterized queries or ORM (never string concatenation)
- [ ] Command: no shell execution with user input (or strict allowlist)
- [ ] Template: user input escaped before rendering
- [ ] LDAP/XML/XPath: input sanitized before query construction
- [ ] NoSQL: query operators can't be injected via user input

### A04: Insecure Design
- [ ] Threat model exists for security-critical flows
- [ ] Rate limiting on authentication endpoints
- [ ] Account lockout after repeated failures
- [ ] Security-relevant business logic has unit tests
- [ ] Fail-secure: errors deny access, not grant it

### A05: Security Misconfiguration
- [ ] Debug mode disabled in production
- [ ] Default credentials changed
- [ ] Error messages don't leak stack traces or internal paths
- [ ] Unnecessary features/endpoints/ports disabled
- [ ] Security headers set (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)

### A06: Vulnerable Components
- [ ] Dependencies are pinned to specific versions
- [ ] Known CVEs checked (npm audit, pip-audit, etc.)
- [ ] No unmaintained dependencies in critical paths
- [ ] Dependency update process is documented

### A07: Authentication Failures
- [ ] Passwords meet minimum complexity requirements
- [ ] Session tokens are cryptographically random
- [ ] Tokens expire and can be revoked
- [ ] Multi-factor authentication available for sensitive operations
- [ ] Login failures don't reveal whether username or password was wrong

### A08: Data Integrity Failures
- [ ] Software updates verified with signatures
- [ ] CI/CD pipeline protected against unauthorized modifications
- [ ] Serialized data from untrusted sources validated before use

### A09: Logging & Monitoring Failures
- [ ] Authentication events logged (success and failure)
- [ ] Authorization failures logged
- [ ] Input validation failures logged
- [ ] Logs don't contain sensitive data (passwords, tokens, PII)
- [ ] Alerting exists for suspicious patterns

### A10: SSRF
- [ ] Server-side requests don't follow user-controlled URLs without validation
- [ ] Internal network addresses blocked from user-supplied URLs
- [ ] URL allowlists used where possible

## Threat Modeling (STRIDE)

For security-critical designs, evaluate each component against:

| Threat | Question | Example |
|--------|----------|---------|
| **S**poofing | Can an attacker impersonate a user or component? | Forged JWT, stolen session |
| **T**ampering | Can an attacker modify data in transit or at rest? | Man-in-the-middle, DB manipulation |
| **R**epudiation | Can a user deny performing an action? | Missing audit log |
| **I**nformation disclosure | Can sensitive data leak? | Error messages, logs, side channels |
| **D**enial of service | Can an attacker exhaust resources? | Unbounded queries, no rate limiting |
| **E**levation of privilege | Can a user gain unauthorized access? | IDOR, missing authz checks |

## Finding Severity for Security Issues

| Severity | Criteria | Example |
|----------|----------|---------|
| **critical** | Exploitable without authentication, leads to data breach or RCE | SQL injection in login, command injection |
| **critical** | Authentication or authorization bypass | Missing authz check on admin endpoint |
| **warning** | Exploitable but requires authentication or specific conditions | Stored XSS in user profile |
| **warning** | Information disclosure of sensitive data | Stack trace in error response |
| **suggestion** | Defense-in-depth improvement, low exploitability | Missing CSP header, verbose logging |

## Output Format

Security findings use the standard review finding format with `category: "security"`:

```json
{
  "severity": "critical",
  "category": "security",
  "location": "src/api/users.py:45",
  "description": "User ID from URL path used directly in database query without ownership check (IDOR)",
  "suggested_fix": "Add ownership check: verify request.user.id matches the resource owner before returning",
  "adversarial_note": "Any authenticated user can read any other user's profile by changing the ID in the URL"
}
```

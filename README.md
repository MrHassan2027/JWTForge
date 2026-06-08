# JWTForge

> CLI tool to decode, inspect, sign, and validate JWTs — built for pentest labs and API debugging

## What it does
A fast command-line tool for working with JSON Web Tokens. Decode any JWT without the secret, inspect claims, validate signatures, forge tokens for authorized testing environments, and detect common JWT vulnerabilities (alg:none, weak secrets, expired claims).

## Quick Start
```bash
pip install jwtforge

jwtforge decode eyJhbGc...          # decode + pretty print
jwtforge validate eyJhbGc... --secret mykey
jwtforge forge --payload '{"sub":"1","role":"admin"}' --secret mykey --alg HS256
jwtforge audit eyJhbGc...          # check for common weaknesses
```

## Features
- **Decode**: Base64-decode header + payload, pretty-print claims
- **Validate**: Verify signature with known secret or public key
- **Forge**: Create new tokens with custom payload (for authorized testing)
- **Audit**: Detect vulnerabilities:
  - `alg: none` acceptance
  - Expired tokens (`exp` check)
  - Weak secrets (dictionary attack against common passwords)
  - Missing claims (`iss`, `aud`, `iat`)
- Supports: HS256/384/512, RS256/384/512, ES256
- `--crack` flag: dictionary attack against a list of common secrets

## Tech Stack
| Tool | Why |
|------|-----|
| Python 3.11+ | Core logic |
| `PyJWT` | JWT encode/decode |
| `cryptography` | RSA/EC key handling |
| `click` | CLI |
| `rich` | Pretty-print output |

## Example
```
$ jwtforge decode eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjMifQ.abc

Header:
  alg: HS256
  typ: JWT

Payload:
  sub: 123

Signature: [unverified - no secret provided]
```

> **For authorized testing and CTF challenges only.**

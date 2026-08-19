# Authentication

## Overview

The API uses JWT bearer authentication. Authentication establishes the user identity used to scope documents, chat sessions, and other private resources.

## Registration

Registration accepts an email/password request, checks whether the email already exists, hashes the password, stores the user, and returns the public registration response.

## Login

Login verifies the submitted credentials and issues an access token containing user identity claims. Clients send the token in the HTTP `Authorization` header using the bearer scheme.

```text
Authorization: Bearer <access-token>
```

## Protected routes

FastAPI dependencies decode and validate the bearer token. The current user's `sub` claim is used as the authenticated user ID by protected application services/routes.

## Authorization

Authentication answers "who is the user?" Authorization answers "may this user access this resource?" Every document/session operation should enforce ownership at the query/service layer rather than trusting IDs received from the client.

## Token configuration

The environment defines settings such as:

```env
SECRET_KEY=replace_with_a_secure_random_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Generate a strong secret locally with `openssl rand -hex 32` and use managed secrets in production.

## Client behavior

The frontend should avoid exposing tokens in logs/errors. On `401`, it should treat the session as unauthenticated/expired. Production traffic must use HTTPS.

## Future hardening

Potential additions include refresh-token strategy, revocation/logout semantics, login rate limiting, account verification/recovery, security audit events, and automated authorization tests for cross-user resource access.
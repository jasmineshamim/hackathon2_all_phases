---
id: 001
title: Update-project-constitution-for-full-stack-web-app
stage: constitution
date: 2026-01-12
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Lenovo
command: sp.constitution
labels: [constitution, spec-driven-development, full-stack, web-application, jwt-authentication]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ../.specify/memory/constitution.md
tests: []
---

## Prompt

```
text
Project: Todo Full-Stack Web Application (Next.js + FastAPI + Neon + Better Auth)

Core principles:
- Correctness of business logic (task ownership, CRUD consistency)
- Security-first design (JWT authentication, user isolation)
- API reliability and predictable behavior
- Scalability and maintainability
- Clear separation of concerns (frontend, backend, auth)
- Spec-driven development compliance

Key standards:
- All API endpoints must follow RESTful conventions
- Every request must validate authenticated user identity using JWT
- Task data must always be filtered by authenticated user ID
- Database schema must enforce data integrity and relationships
- Error handling must return proper HTTP status codes and messages
- Frontend must consume APIs using typed, reusable services
- Code must be readable, modular, and documented
- No hard-coded secrets; environment variables only
- Authentication failures must return 401 Unauthorized
- Unauthorized resource access must return 403 Forbidden

Constraints:
- Frontend: Next.js 16+ using App Router
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- API must be stateless and token-based
- JWT secret must be shared via environment variable BETTER_AUTH_SECRET
- All endpoints require valid JWT token
- Data persistence required (no in-memory storage)
- Responsive UI required for mobile and desktop
- Must implement all 5 basic task features as web app

Success criteria:
- Users can securely sign up and sign in
- JWT token is issued and attached to every API request
- Backend validates JWT and identifies authenticated user
- Users can only access and modify their own tasks
- All CRUD operations function correctly
- Data persists across sessions and reloads
- API returns correct status codes and responses
- Unauthorized requests are blocked correctly
- Application runs without critical runtime errors
- System passes functional and security validation
```

## Response snapshot

Updated the project constitution to version 3.0.0 to reflect the requirements for the Todo Full-Stack Web Application with Next.js, FastAPI, Neon Serverless PostgreSQL, and Better Auth. The updated constitution includes:

- Enhanced security-first principles with JWT authentication requirements
- Detailed technology stack constraints for frontend, backend, database, and authentication
- Updated Phase II constraints with specific requirements for the full-stack web application
- API standards requiring JWT validation and user isolation
- Code standards for Python, TypeScript, and API development
- Success criteria for the web application implementation

## Outcome

- ✅ Impact: Major version update (2.0.0 → 3.0.0) with significant architectural constraints added
- 🧪 Tests: No tests created
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Ready for specification phase of the web application
- 🧠 Reflection: Constitution now properly reflects the full-stack web application requirements with JWT authentication and proper security constraints

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin specification for the web application features
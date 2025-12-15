# MksU Sports Hub — Project Plan and Roles

## Problem Statement (Graduation Clearance)
- Machakos University currently runs a fully manual, paper-based graduation clearance. Students must walk forms across Finance, Faculty, Library, Mess, and Hostels to collect stamps, causing long queues, repeated visits, and frequent errors.
- Payments (tuition plus a KES 5,500 graduation fee) are verified by hand with no digital sync, so mismatches and delays are common and force students to return multiple times.
- Forms are printed, stamped, duplicated, and scanned to a shared drive; records are inconsistent, easily lost or damaged, and lack audit trails.
- Every department visit is in person, creating barriers for students off-campus or with work commitments; staff rely on ledgers and spreadsheets, driving slow service and operational strain.
- Students cannot track progress centrally, so they face confusion, lost time, and risk missing deadlines; staff have limited transparency, accountability, and historical retrieval.
- Overall, the clearance experience is slow, error-prone, and stressful, leading to congestion during peak periods and delaying graduation readiness.

## Solution (Digital Clearance System)
- Single web portal: students initiate clearance online, upload required info once, and track status across all departments in one place.
- Role-based workflows: Finance, Faculty, Library, Mess, and Hostels each get dashboards to approve/reject with reasons; no physical stamps.
- Payments digitized: graduation fee (KES 5,500) and outstanding balances paid via online channels; receipts auto-matched to student records.
- Automated verification: payment confirmations and departmental approvals update the student’s clearance state in real time with clear SLAs.
- Document management: forms and evidence stored centrally with versioning and audit logs; no printing, stamping, or ad-hoc shared drives.
- Notifications and tracking: students get alerts on approvals/rejections and can see a step-by-step checklist with who owns the next action.
- Integrity and audit: every action is logged (who, when, what changed) to reduce disputes and improve accountability.



## Team
- Mwangi Stephen
- Jane Mutie
- Brian Kuria
- Hezron Kipchirchir
- Quizane Onyango

## Roles and Responsibilities
- Backend (Django, MySQL): authentication and closed-loop provisioning, APIs, business rules, integrations (internal systems and calendars), data security, role-based access.
- Frontend (React): user flows for admin and students, dashboards, forms, calendars, sponsor showcase, client-side validation, accessibility.
- Shared: API contracts, error handling conventions, logging/monitoring, testing, CI/CD checks.

## Phased Plan (MVP)
- Week 1: Requirements, security model, DB schema, API contracts.
- Weeks 2–4 (Backend): Auth, RBAC, core domain models, services, integrations, unit tests.
- Weeks 5–7 (Frontend): Layout/system shell, key pages, API wiring, validations, UX polish.
- Week 8: Integration, API/client tests, security testing, UAT with Sports Dept.
- Weeks 9–10: Deploy, train admins, docs handover, post-deploy support.

## Backend Work (Step by Step)
1) Foundations
- Set up Django project, env configs (.env templates), logging, CORS, security headers.
- Configure MySQL connection, migrations baseline, health checks.
2) Auth and Access Control
- Closed-loop provisioning: admin-only user creation; no open signup.
- Implement JWT/Session auth, password policies, MFA-ready hooks.
- Role-based access: Admin, Coach/Staff, Student, Sponsor-Viewer.
3) Core Domain Models (initial tables)
- users (id, name, email, role, status, last_login, created_at, updated_at)
- students (id, user_id FK, reg_number, faculty, program, year, eligibility_status)
- teams (id, name, sport, coach_name, captain_student_id FK)
- tournaments (id, name, sport, season, start_date, end_date, venue)
- fixtures (id, tournament_id FK, home_team_id FK, away_team_id FK, match_datetime, venue, status, score_home, score_away)
- results (id, fixture_id FK, summary, highlights_url)
- achievements (id, student_id FK, title, description, date_awarded, media_url)
- grievances (id, student_id FK, category, description, status, priority, assigned_admin_id FK, resolution_notes)
- sponsors (id, name, logo_url, contact_email, tier)
- sponsor_contributions (id, sponsor_id FK, amount, payment_reference, paid_at, purpose)
- calendar_events (id, source_type, source_id, title, start, end, visibility, sync_status)
- audit_logs (id, actor_id FK, action, entity, entity_id, metadata, created_at)
4) Services and APIs
- User provisioning endpoints (admin-only), login/logout, password reset.
- Student profile CRUD, eligibility verification status updates.
- Team and tournament management, fixtures CRUD, result posting.
- Grievance submission and triage flows (create, assign, update status, resolve).
- Sponsor portal: sponsor CRUD and contribution recording.
- Calendar sync service: create/update events, push to Google Calendar where linked.
- File/media handling: logos, highlights; store URLs (S3/minio-ready), validate types/size.
5) Integrations
- Google Calendar API: service account config, per-user opt-in tokens, retry/backoff.
6) Security and Compliance
- Input validation, rate limiting, RBAC checks on every endpoint.
- Encrypt secrets at rest, use env vars, rotate keys procedure documented.
- Audit logging for admin actions and financial events.
7) Testing
- Unit tests for services/models, API contract tests (e.g., pytest + DRF).
- Mock external integrations; happy-path and failure-path cases.
8) Delivery
- Migrations for all tables, seed scripts for roles/admin account.
- API docs (OpenAPI/Swagger), postman collection, runbook for ops.

## Frontend Work (Step by Step)
1) Foundations
- Set up React app structure, routing, state (lightweight store), env configs.
- Global theming, layout shell, navigation, role-aware menus.
2) Auth Flows
- Login, logout, token storage/refresh, guard routes by role.
- Password reset screens aligned with backend.
3) Admin Dashboard
- User provisioning UI (create/disable users by role), eligibility status view.
- Teams/tournaments management: CRUD forms, validation, table/list views.
- Fixtures/results management with status updates and score entry.
- Grievance triage board: filter/search, assign admin, update status, resolution notes.
- Sponsor portal admin: sponsor CRUD, upload logo, view contributions, flag anomalies.
4) Student Portal
- Profile view/edit, achievements timeline, eligibility status indicator.
- Fixtures and results: cards/table, filters by sport/date, match details view.
- Grievance submission form with status tracking.
- Calendar sync: connect Google, show sync status, allow disconnect.
5) Sponsor/Viewer Pages
- Public-ish sponsor gallery (within closed loop), logos, tiers, contributions summary.
- Showcase tournaments and upcoming fixtures.
6) UX and Validation
- Form validation, inline errors, loading/empty states, optimistic updates where safe.
- Accessible components (keyboard, ARIA), responsive layouts.
7) Testing
- Component and integration tests for critical flows (auth, forms, tables, sync).
- Contract tests against mocked API; snapshot key UI states.
8) Delivery
- Build pipeline, environment configs per stage, error reporting hook (e.g., Sentry-ready).

## Integration and Testing (Week 8)
- End-to-end happy paths: auth, profile edit, fixture browse, grievance lifecycle, sponsor payment webhook.
- Security checks: role gating, broken auth/IDOR attempts, rate limits, input fuzzing.
- Performance sanity: key pages/API p95 targets, DB index review.
- UAT with Sports Dept on pre-prod data; capture sign-offs.

## Deployment and Training (Weeks 9–10)
- Deploy backend (gunicorn + reverse proxy) and MySQL with backups; seed initial admin.
- Deploy frontend build to hosting/CDN with correct env vars.
- Admin training: account provisioning, grievance handling, fixture/result updates, sponsor reconciliations.
- Documentation: runbooks, FAQ, onboarding guides; set up monitoring/alerts.
- Post-deploy hypercare window and ticket channel.

## Risks and Mitigations (Condensed)
- Integration failures (Google): mock-first, retry/backoff, clear timeouts.
- Security gaps: RBAC on every endpoint/view, audit logs, regular dependency scans.
- Scope creep/schedule slips: change control, weekly demos, prioritized backlog.
- Low adoption: early comms with student reps, simple UX, calendar sync promotion.
- Data errors/complaint overload: validation, required fields, triage queues, SLAs.

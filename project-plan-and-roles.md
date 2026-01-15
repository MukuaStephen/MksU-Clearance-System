# MKSU CLEARANCE — Project Plan and Roles

## Project Summary

**Machakos University Digital Graduation & Clearance System**

A centralized web platform designed to automate the currently manual graduation clearance process at Machakos University. The system streamlines the workflow by allowing students to complete every step online, moving away from physical forms and inter-departmental movement.

## Problem Statement

Machakos University currently relies on a fully manual clearance process where students must physically move between multiple departments (COD, Finance, Library, Mess, Hostels, Workshops, Sports & Games) to obtain physical stamps.

- Students face long queues and repeated trips to campus.
- Forms must be manually downloaded, printed, and stamped.
- There is no centralized system to track progress, leading to lost documents and delays.
- Clearance forms are currently scanned and uploaded manually via Google Drive, which is inefficient (e.g., repetitive entry of information already stored in the university database and errors due to handwriting/incorrect information).

## Proposed Solution

A unified online platform that automates the entire clearance lifecycle:

- **Digital Forms:** Forms are auto-filled with student records to eliminate manual entry.
- **Departmental Dashboards:** Departments (Finance, Library, Mess, Hostels, etc.) can approve or decline requests digitally.
- **Finance Integration:** A specific module for the automatic verification of fees and graduation charges.
- **Real-time Tracking:** Students can track their clearance status and view approvals or rejections instantly.
- **Notification System:** Alerts for pending actions, approvals, or rejections.
- **Document Management:** Forms and evidence stored centrally with versioning and audit logs; no printing or ad-hoc shared drives.
- **Accountability:** Automated digital records and transparent approval trails.

## Why a Web-Based System

- **Remote Access:** Allows students to complete clearance from anywhere without visiting campus.
- **Centralization:** Unifies all departmental approvals into a single platform.
- **Efficiency:** Reduces clearance time by up to 80% and eliminates paper-based workflows.
- **Accountability:** Provides automated digital records and enhances transparency in the process.

## Technology Stack

- **Frontend:** HTML, CSS, Javascipt, Typescript
- **Framework:** Angular.
- **Backend:** Python
- **Framework:** Django
- **Database:** MySQL

## Target Users

- **Students:** Graduating students requiring clearance.
- **University Departments:** Finance, Library, COD, Mess, Hostels, Workshops, Sports & Games.
- **Administration:** Staff responsible for verifying student status and approving clearances.

## Competitive Advantage

The system transforms a tedious physical process into a seamless digital experience. It eliminates the need for physical queues, ensures documents are never lost, and reduces the workload for staff by replacing manual stamping with one-click digital approvals.

## Feasibility Summary

- **Technical:** Utilizes standard, secure technologies (Django/React) and integrates with existing University SSO (e.g., students using their university emails @mksu.ac.ke or admission numbers as authentication).
- **Operational:** Reduces repetitive manual work for staff, though change management is required to handle staff resistance to new workflows.
- **Schedule:** The project is scoped to be completed within a 10-week timeline.

## Project Timeline (MVP)

| Phase | Duration | Timeline |
|-------|----------|----------|
| Phase 1: Requirements & Analysis | 1 week | Week 1 |
| Phase 2: Backend Development | 3 weeks | Weeks 2–4 |
| Phase 3: Frontend Development | 3 weeks | Weeks 5–7 |
| Phase 4: Integration & Testing | 1 week | Week 8 |
| Phase 5: Deployment | 2 weeks | Weeks 9–10 |

## Phased Breakdown

### Phase 1 (Week 1): Requirements & Analysis
- Stakeholder meetings with departments and students.
- Map existing clearance workflows and pain points.
- Design database schema for students, departments, clearance records, and approvals.
- Define API contracts between frontend and backend.
- Plan security model and role-based access control.

### Phase 2 (Weeks 2–4): Backend Development
- Set up Django project, environment configs, logging, CORS, security headers.
- Configure MySQL connection and migrations baseline.
- Implement authentication (SSO with university email/admission number).
- Implement role-based access control (Admin, Department Staff, Student).
- Create core domain models and database tables.
- Build departmental approval APIs.
- Build student clearance tracking APIs.
- Implement notification system (email/SMS alerts).
- Add audit logging for all actions.
- Write unit tests and API tests.

### Phase 3 (Weeks 5–7): Frontend Development
- Set up React app structure, routing, and state management.
- Build login/authentication flows (SSO integration).
- Build student dashboard (clearance status tracker, form submission, history).
- Build departmental dashboards (Finance approval, Library approval, Mess approval, etc.).
- Build admin dashboard (user management, system overview, reports).
- Implement real-time status notifications.
- Add form validation and error handling.
- Ensure responsive design and accessibility.
- Write component and integration tests.

### Phase 4 (Week 8): Integration & Testing
- End-to-end testing of clearance workflows.
- Security testing (authentication, authorization, input validation).
- Performance testing and optimization.
- UAT with departments and select students.
- Bug fixes and refinements.

### Phase 5 (Weeks 9–10): Deployment & Training
- Deploy backend to university servers/cloud with database backup.
- Deploy frontend to hosting/CDN.
- Conduct staff training on departmental approval workflows.
- Conduct student awareness and onboarding.
- Set up monitoring and alerts.
- Provide documentation and runbooks.
- Post-deployment support and hypercare.

## Roles and Responsibilities

### Backend Team (Django, MySQL)
- Project initialization and environment setup.
- Authentication system (SSO integration with university email).
- Role-based access control (Admin, Department Staff, Student).
- Database design and migrations.
- Core domain models (Users, Students, Departments, Clearance Records, Approvals).
- RESTful API endpoints for all features.
- Clearance status tracking and workflow logic.
- Notification system integration (email/SMS).
- Audit logging and security.
- Integration testing and unit testing.
- API documentation (OpenAPI/Swagger).

### Frontend Team (React, HTML/CSS)
- Project initialization and structure setup.
- Authentication UI (SSO login).
- Student dashboard and clearance form submission.
- Student clearance progress tracker.
- Departmental approval dashboards for each department.
- Admin dashboard for system overview and management.
- Real-time notification display.
- Form validation and error handling.
- Responsive design and accessibility.
- Component and integration testing.
- Build pipeline and deployment configuration.

### Shared Responsibilities
- API contract definition and adherence.
- Error handling conventions.
- Logging and monitoring setup.
- Testing standards and code review.
- CI/CD pipeline configuration.
- Security practices and compliance.

## Backend Work (Step by Step)

### 1) Foundations
- Set up Django project with settings for dev, staging, and production.
- Configure environment variables (.env files for secrets).
- Set up logging, CORS, security headers (CSRF, HTTPS, etc.).
- Configure MySQL connection, connection pooling.
- Create migrations baseline and health check endpoints.

### 2) Authentication & Access Control
- Implement SSO integration with university email/admission number.
- JWT or Session-based authentication.
- Password policies and account management.
- Role-based access control (RBAC): Admin, Department Staff, Student.
- Implement permission checks on every endpoint.

### 3) Core Domain Models (Database Tables)
- **users** (id, email, admission_number, full_name, role, is_active, last_login, created_at, updated_at)
- **students** (id, user_id FK, reg_number, faculty, program, graduation_year, eligibility_status)
- **departments** (id, name, code, head_email, type) — e.g., Finance, Library, Mess, Hostels
- **clearance_requests** (id, student_id FK, status, submission_date, completion_date, created_at, updated_at)
- **clearance_approvals** (id, clearance_request_id FK, department_id FK, status, approved_by_id FK, approval_date, rejection_reason, notes)
- **finance_records** (id, student_id FK, tuition_balance, graduation_fee_status, last_verified_date)
- **notifications** (id, user_id FK, message, type, read, created_at, sent_at)
- **audit_logs** (id, actor_id FK, action, entity, entity_id, changes, created_at, ip_address)

### 4) Services and APIs
- **Authentication Endpoints:** SSO login, logout, password reset, profile update.
- **Student Endpoints:** Initiate clearance, submit forms, view status, view approval history.
- **Department Endpoints:** View pending approvals, approve/reject clearance, add notes.
- **Admin Endpoints:** User management, department management, system reports, audit logs.
- **Notification Service:** Send email/SMS alerts on status changes.
- **Finance Verification Service:** Integrate with finance system to verify fees and graduation charges.
- **File Handling:** Store uploaded documents, manage versions.
- **Clearance Workflow Engine:** Manage states and transitions.

### 5) Security and Compliance
- Input validation on all endpoints.
- Rate limiting to prevent abuse.
- RBAC checks on every endpoint.
- Encrypt passwords and secrets at rest.
- Use environment variables for all secrets.
- Audit logging for sensitive actions.
- HTTPS enforcement.

### 6) Testing
- Unit tests for services and models (pytest).
- API integration tests.
- Mock external integrations.
- Happy-path and failure-path test cases.
- Security testing (SQL injection, XSS, etc.).

### 7) Delivery
- Database migrations for all tables.
- Seed scripts for initial admin users and departments.
- API documentation (OpenAPI/Swagger).
- Runbook for operations and troubleshooting.

## Frontend Work (Step by Step)

### 1) Foundations
- Set up React app with routing (React Router).
- Global state management (Context API or Redux).
- Environment configs for dev, staging, production.
- Global styling and theme.
- Navigation and layout shell.

### 2) Authentication Flows
- SSO login form with university email/admission number.
- Token storage (localStorage/sessionStorage) and refresh logic.
- Route guards based on user role.
- Logout functionality.
- Password reset flows (if supported).

### 3) Student Portal
- Dashboard with student clearance status overview.
- Clearance form (auto-filled with student data).
- Step-by-step clearance progress tracker showing which departments have approved/pending.
- Notification center showing alerts and updates.
- Clearance history and past records.

### 4) Departmental Dashboards
- Dashboard for each department (Finance, Library, Mess, Hostels, etc.).
- List/table of pending clearance requests assigned to the department.
- Approval form (approve/reject with optional notes).
- Filter and search for requests.
- Bulk approval actions.
- Status overview and metrics.

### 5) Admin Dashboard
- System overview and metrics (total students, pending approvals, completion rate).
- User management (create/disable users by role).
- Department management.
- Audit log viewer.
- Reports and analytics.

### 6) UX and Validation
- Form validation with inline error messages.
- Loading states and spinners.
- Empty states and error fallbacks.
- Success notifications.
- Responsive design (mobile, tablet, desktop).
- Accessibility (WCAG 2.1 compliance).

### 7) Testing
- Component tests (Jest/React Testing Library).
- Integration tests for critical workflows.
- Contract tests against mocked API.
- Accessibility tests.

### 8) Delivery
- Build pipeline (npm build, minification).
- Environment-specific configuration.
- Error reporting (e.g., Sentry-ready).
- Performance optimization.

## Integration and Testing (Week 8)

### End-to-End Testing
- Student completes clearance from form submission to final approval.
- Department staff approve and reject clearances.
- Notifications are sent and displayed correctly.
- Status tracking updates in real time.

### Security Testing
- Authentication and authorization checks.
- Input validation and sanitization.
- Rate limiting verification.
- Audit logging verification.

### Performance Testing
- Key pages load within acceptable times.
- API responses within SLA targets.
- Database query optimization.

### UAT with Departments
- Real workflows with Finance, Library, Mess, Hostels.
- Capture feedback and sign-offs.
- Final refinements and bug fixes.

## Deployment and Training (Weeks 9–10)

### Backend Deployment
- Deploy Django app to university servers or cloud (e.g., AWS, DigitalOcean).
- Configure gunicorn/uWSGI and reverse proxy (Nginx/Apache).
- Set up MySQL database with backups and replication.
- Configure SSL/TLS certificates.
- Set up environment variables and secrets management.

### Frontend Deployment
- Build production-optimized React bundle.
- Deploy to hosting (CDN, university servers, or cloud).
- Configure domain and DNS.

### Staff Training
- Training sessions for Finance, Library, Mess, Hostels staff.
- Walkthrough of departmental dashboards and approval workflows.
- Troubleshooting and support.

### Student Awareness
- Communication campaign via email, messaging, campus announcements.
- Step-by-step guides for students.
- FAQ and support channel setup.

### Documentation and Support
- System runbook for IT operations.
- Troubleshooting guides.
- User documentation for students and staff.
- Support contact and escalation procedures.
- Post-deployment monitoring and alerts.

## Expected Impact

- **Reduced Clearance Time:** From weeks to days.
- **Improved Transparency:** Students always know status and next steps.
- **Reduced Paper Usage:** Fully digital workflows.
- **Reduced Errors:** Auto-filled forms and digital verification.
- **Better Accountability:** Audit trails and digital records.
- **Reduced Staff Workload:** One-click approvals instead of manual stamping.
- **Enhanced Student Experience:** Remote access and clear tracking.

## Risks and Mitigations

### Technical Risks
- **Database/Server Failures:** Regular backups, replication, monitoring, and alert systems.
- **Integration Issues:** Thorough testing of SSO and finance system integration before deployment.
- **Security Vulnerabilities:** Regular security audits, dependency scanning, code review.

### Project Management Risks
- **Scope Creep:** Strict change control, prioritized backlog, weekly demos.
- **Schedule Delays:** Buffer time in timeline, regular progress tracking, escalation procedures.

### Organizational Risks
- **Staff Resistance:** Early communication, training, support, highlighting benefits.
- **Low Student Adoption:** Clear communication, ease of use, incentives (e.g., faster clearance).

### Operational Risks
- **Data Entry Errors:** Validation, required fields, auto-fill from existing records.
- **High Support Load:** FAQ, self-service guides, ticketing system.

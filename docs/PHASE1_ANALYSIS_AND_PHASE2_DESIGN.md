# Phase 1: Project Analysis & Phase 2: System Design

## Phase 1: Project Analysis

### 1. Current Architecture Overview

The project is a **Django 5.2** web application with four main apps:

| App | Purpose |
|-----|--------|
| **config** | Project settings, root URL config, WSGI/ASGI. |
| **accounts** | User registration, role assignment, home/portal landing. |
| **student_portal** | Student profiles, resumes, jobs, applications, interviews, messages. |
| **tpo_portal** | TPO (Training & Placement Officer) dashboard (minimal). |
| **recruiter_portal** | Recruiter dashboard (minimal). |

- **Templates**: Single `templates/` directory at project root; `BASE_DIR / 'templates'` in settings; app-specific subdirs: `accounts/`, `student_portal/`, `tpo_portal/`, `recruiter_portal/`, `registration/`, `errors/`.
- **Static**: `static/css/site.css` only; Bootstrap 5.3.3 and Bootstrap Icons 1.11.3 via CDN.
- **Database**: SQLite (`db.sqlite3`).
- **Auth**: Django’s built-in `User` model; `LOGIN_URL`, `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL` set.

---

### 2. App-wise Responsibility Summary

#### accounts
- **Models**: `Profile` (OneToOne to User; `role`: unknown | student | tpo | recruiter).
- **Views**: `home` (role-based redirect or generic home), `portal` (registration choice), `register_student`, `register_tpo`, `register_recruiter`.
- **Forms**: `RegistrationForm` (email + role); `StudentRegistrationForm`, `TpoRegistrationForm`, `RecruiterRegistrationForm` (set `Profile.role` on save).
- **Signals**: `post_save` on User → create `Profile` with role `unknown` (role updated on role-specific registration).
- **URLs**: `/`, `/portal/`, `/register/student/`, `/register/tpo/`, `/register/recruiter/`.
- **Templates**: `home.html`, `accounts/portal.html`, `accounts/register.html`.

#### student_portal
- **Models**: All placement-related models live here:
  - **Profile**: `StudentProfile` (OneToOne User), `Skill`, `Certification`, `Resume`, `PortfolioItem`, `Document`.
  - **Jobs**: `JobPosting` (posted_by → User), `Application`, `SavedJob`.
  - **Workflow**: `Interview` (OneToOne Application).
  - **Communication**: `Message`, `Notification`.
  - **Development**: `SkillGapAnalysis`, `PracticeTest`, `MockInterview`.
- **Views**: Dashboard, profile/skills/certifications, resume CRUD, portfolio CRUD, document CRUD, job search/detail, apply/save job, application list/detail, saved jobs, interview list, messages send/list, notifications, skill gap, practice tests, mock interviews. All use `@login_required` and role check (`Profile.Role.STUDENT`).
- **Forms**: `StudentProfileForm`, `SkillForm`, `CertificationForm`, `ResumeForm`, `PortfolioItemForm`, `DocumentForm`, `ApplicationForm`, `MessageForm`, `MockInterviewForm`, `JobSearchForm`.
- **URLs**: Under `/student/` with `app_name = "student"`.
- **Templates**: dashboard, profile, job_search, job_detail, application_list, application_detail, resume_list, resume_form; **missing**: portfolio_list, portfolio_form, document_list, document_form, saved_jobs, interview_list, message_list, message_form, notification_list, skill_gap_analysis, practice_tests, mock_interview_list, mock_interview_form.

#### tpo_portal
- **Models**: None (empty).
- **Views**: `dashboard` (login + TPO role check, renders template with placeholder stats and quick actions).
- **URLs**: `/tpo/` → dashboard only.
- **Templates**: `tpo_portal/dashboard.html` (hardcoded 0s for stats; quick action links are `#`).

#### recruiter_portal
- **Models**: None (empty).
- **Views**: `dashboard` (login + RECRUITER role check, placeholder stats and quick actions).
- **URLs**: `/recruiter/` → dashboard only.
- **Templates**: `recruiter_portal/dashboard.html` (hardcoded 0s; links `#`).

---

### 3. ER Relationship Overview

- **User** (Django) ←→ **Profile** (accounts): OneToOne, role.
- **User** ←→ **StudentProfile** (student_portal): OneToOne (for students).
- **StudentProfile** → Skill, Certification, Resume, PortfolioItem, Document, Application, SavedJob, SkillGapAnalysis, MockInterview: 1:N.
- **User** → **JobPosting**: 1:N (posted_by).
- **JobPosting** → Application, SavedJob: 1:N.
- **Application** → Interview: 1:1.
- **User** → Message (sender/recipient), Notification: 1:N.
- **PracticeTest**: standalone (no FK to student).

No **Company** entity yet; company name is a field on `JobPosting`. Recruiters are identified only by `User` + `Profile.role = recruiter`.

---

### 4. Authentication Flow

1. **Anonymous**: Can open `/`, `/portal/`, `/login/` (Django auth), and role-specific register URLs.
2. **Registration**: User picks portal (portal → register_student | register_tpo | register_recruiter). Form creates User + sets `Profile.role` via form `save()`. User is logged in and redirected to `home`.
3. **Login**: Django’s `LoginView`; redirects to `LOGIN_REDIRECT_URL` (`home`).
4. **Home** (`accounts.views.home`): If authenticated, redirects by role: Student → `student:dashboard`, TPO → `tpo:dashboard`, Recruiter → `recruiter:dashboard`. Otherwise shows generic home with links to all three portals.
5. **Role-based access**: Student portal views check `request.user.profile.role == Profile.Role.STUDENT`; TPO/Recruiter dashboards check TPO/RECRUITER. Wrong role → 403 (errors/403.html).

---

### 5. Identified Extension Points (Safe to Add)

- **accounts**: Add optional fields to `Profile` if needed (e.g. phone); do not change role enum or User link.
- **student_portal**: Add fields to `StudentProfile` (e.g. `placement_eligible`); add fields to `JobPosting` (e.g. `min_cgpa`, `eligibility_criteria`); add validation in application flow. Keep all existing models and views; add new views/urls/templates for missing pages.
- **tpo_portal**: Add views/urls/templates only; optionally add TPO-specific models (e.g. PlacementDrive) in a new migration. Use existing `StudentProfile`, `JobPosting`, `Application`, `Interview` for listing and actions.
- **recruiter_portal**: Add Company model (optional); add views for JobPosting CRUD (filter by `posted_by=request.user`); use existing `Application`, `Interview` for candidate pipeline. No change to existing student_portal models except optional FK from JobPosting to Company.
- **Reports**: New app `reports` or views under `tpo_portal` for placement stats, department-wise, salary analytics, PDF export; read-only over existing models.
- **Templates**: Reusable base (e.g. `base_dashboard.html`) with sidebar/nav per role; extend in each portal without changing `base.html` structure used by public pages.
- **Static**: Add JS/CSS in `static/` without removing existing `site.css`.

---

## Phase 2: System Design (Extension Plan)

### 1. Module Structure (Role-Based)

| Module | Apps / Areas | Responsibility |
|--------|---------------|----------------|
| **Admin** | Django admin + optional staff dashboard | User/Profile/StudentProfile/JobPosting/Application/Interview management; no new app required. |
| **Placement Officer (TPO)** | tpo_portal | Students list, recruiters/companies list, applications review, shortlist, schedule interview, reports. |
| **Student** | student_portal | Already comprehensive; add eligibility, missing templates, and base dashboard layout. |
| **Company/Recruiter** | recruiter_portal | Company profile (optional), JobPosting CRUD, view applications, shortlist, schedule interview. |
| **Reports & Analytics** | tpo_portal (or reports app) | Placement statistics, department-wise, salary analytics, export PDF. |

### 2. Role-Based Access Control

- **Student**: All `/student/*` views; `StudentProfile` and related data owned by `request.user`.
- **Recruiter**: All `/recruiter/*` views; JobPosting filtered by `posted_by=request.user`; applications for own jobs only.
- **TPO**: All `/tpo/*` views; read/write across students, jobs, applications, interviews (coordinator).
- **Staff/Superuser**: Django admin at `/admin/`.
- Enforcement: `@login_required` + role check in view (or mixin); 403 on wrong role.

### 3. Model Relationships (Additions Only)

- **StudentProfile**: Add `placement_eligible` (Boolean, default True) for eligibility flag.
- **JobPosting**: Add `min_cgpa` (Decimal, null/blank), `eligibility_criteria` (TextField, optional). Keep `posted_by` → User.
- **recruiter_portal**: Optional **Company** model (name, website, logo, etc.) with FK from User or from JobPosting; if omitted, keep using `company_name` on JobPosting.
- No breaking changes to existing FKs or unique_together.

### 4. Separation of Concerns

- **student_portal**: Student-facing only; no recruiter/TPO logic.
- **recruiter_portal**: Recruiter-facing; creates/edits JobPosting; manages applications for own jobs.
- **tpo_portal**: TPO-only; lists students/jobs/applications; updates application status and interview; runs reports.
- **accounts**: Registration and home routing only.
- Shared models (JobPosting, Application, Interview) remain in student_portal to avoid migration complexity; access by other apps via imports.

### 5. Reusable Templates

- **base.html**: Kept for public and simple pages (login, register, portal, 403).
- **base_dashboard.html**: New; extends base; sidebar + top bar + content block; include role-specific sidebar partials (`_sidebar_student.html`, `_sidebar_tpo.html`, `_sidebar_recruiter.html`).
- Portal templates extend `base_dashboard.html` and fill `content` and optional `title`.

### 6. Maintainable Code Structure

- Use Class-Based Views (ListView, DetailView, CreateView, UpdateView) for new list/detail/create/edit where appropriate; keep existing FBVs that work.
- Forms: ModelForms in respective app `forms.py`; validation in form clean methods (e.g. eligibility).
- URL names: namespaced (`student:…`, `tpo:…`, `recruiter:…`); consistent naming.
- Pagination: `Paginator` with page size (e.g. 15–25) for all list views.
- Search/filter: Query params; preserve in pagination links.
- Messages: Django messages framework for success/error after POST.
- File uploads: Keep `Document.file` with `upload_to`; validate content type and size in form.

---

## Implementation Order (High Level)

1. Add optional `placement_eligible` and job eligibility fields; application eligibility check.
2. Create all missing student_portal templates so existing views do not 404.
3. Add base_dashboard and role-based sidebar; adapt student dashboard to use it.
4. Recruiter: JobPosting list/create/update/delete; application list for own jobs; dashboard with real stats.
5. TPO: Student list, recruiter/job list, application review (status, shortlist), schedule interview; dashboard with real stats.
6. Reports: Placement stats, department-wise, salary; PDF export.
7. Security pass: CSRF, login_required, role checks, file upload validation, no raw SQL.

---

*End of Phase 1 Analysis and Phase 2 Design.*

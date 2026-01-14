# College Placement Management System (CPMS)

This repo currently includes the starter **authentication module** (professional UI) for:

- Login
- Registration
- Logout

## Run locally

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Start server:

```bash
python manage.py runserver
```

## URLs

- Login: `/accounts/login/`
- Register: `/register/`
- Home (requires login): `/`
- Admin: `/admin/`
Web-Based College Placement Management System


1. STUDENT MODULE
Profile Management

    Registration & Account Setup: Create account with academic details

    Profile Creation: Personal information, academic records, skills, certifications

    Resume Builder: Create/edit multiple resume versions

    Portfolio Upload: Projects, GitHub links, publications

    Document Management: Upload transcripts, certificates, ID proofs

Job Search & Applications

    Browse Opportunities: View available jobs/internships

    Advanced Filters: Filter by role, company, salary, location, etc.

    Application Tracking: View status (Applied, Under Review, Shortlisted, Rejected)

    One-Click Apply: Submit applications with pre-filled information

    Saved Jobs: Bookmark opportunities for later

Placement Activities

    Eligibility Check: Auto-check eligibility criteria for each opportunity

    Interview Schedule: View upcoming interviews with calendar integration

    Company Research: Access recruiter profiles and company information

    Slot Booking: Register for placement drives and events

Communication & Updates

    Notification Center: Get alerts for new opportunities, deadlines, interviews

    Message System: Communicate with TPO and recruiters

    Announcements: View placement-related notices

    Placement Statistics: View past placement records

Skill Development

    Skill Gap Analysis: Identify required vs. current skills

    Resource Recommendations: Suggested courses/training

    Practice Tests: Aptitude, technical, psychometric tests

    Mock Interview Scheduler: Request practice interviews

2. TPO (TRAINING & PLACEMENT OFFICER) MODULE
Dashboard & Analytics

    Placement Dashboard: Overview of placement statistics

    Real-time Analytics: Application rates, placement percentages

    Reports Generation: Detailed placement reports for management

    Trend Analysis: Year-over-year placement comparisons

Student Management

    Student Database: Access complete student profiles and records

    Eligibility Management: Set criteria for different placement drives

    Batch Management: Organize students by branch, CGPA, etc.

    Performance Tracking: Monitor student application/interview performance

Recruiter Management

    Recruiter Onboarding: Approve/register company recruiters

    Company Database: Manage recruiter profiles and history

    Relationship Management: Track interactions with companies

    Feedback Collection: Gather recruiter feedback on students/process

Drive Coordination

    Event Creation: Schedule placement drives, workshops, seminars

    Calendar Management: Coordinate multiple placement activities

    Slot Allocation: Manage interview schedules and venues

    Resource Allocation: Assign rooms, equipment, support staff

Communication & Administration

    Bulk Notifications: Send announcements to students/recruiters

    Document Management: Upload offer letters, MOUs, agreements

    Role Assignment: Delegate tasks to placement coordinators

    Policy Management: Set placement rules and guidelines

Verification & Approval

    Application Screening: Pre-screen student applications

    Document Verification: Validate student credentials

    Offer Approval: Review and approve job offers

    Conflict Resolution: Manage scheduling conflicts, multiple offers

3. RECRUITER MODULE
Company Profile Management

    Registration & Verification: Create account with company verification

    Company Profile Setup: Company info, brochure, videos, website

    Team Management: Add multiple recruiters/team members

    Branding: Customize company presence on the portal

Job Posting & Management

    Job Creation: Post jobs/internships with detailed requirements

    Template Management: Save and reuse job description templates

    Requirement Specification: Define skills, qualifications, packages

    Drive Scheduling: Plan campus visit dates and activities

Candidate Search & Screening

    Student Database Access: Search students by skills, CGPA, branch

    Advanced Filters: Filter candidates by multiple criteria

    Resume Shortlisting: Review and shortlist candidates

    Auto-Screening: Auto-filter candidates based on criteria

Interview Management

    Schedule Setup: Create interview slots and timelines

    Panel Assignment: Assign interviewers to different rounds

    Feedback System: Rate candidates and provide comments

    Score Management: Maintain candidate evaluation scores

Selection Process

    Candidate Status Update: Move candidates through selection stages

    Offer Management: Generate and send offer letters

    Waitlist Management: Maintain alternate candidate lists

    Analytics: View application/interview statistics

Communication & Coordination

    Direct Messaging: Communicate with shortlisted candidates

    Bulk Communication: Send updates to multiple candidates

    TPO Coordination: Schedule drives, share requirements

    Document Exchange: Share JD, offer letters, joining kits

Feedback & Reporting

    Process Feedback: Provide feedback on placement process

    Campus Feedback: Rate overall campus experience

    Placement Reports: Download hiring statistics and reports

    Future Planning: Indicate future hiring needs

COMMON FEATURES ACROSS MODULES
Authentication & Security

    Role-based access control

    Secure login with password reset

    Session management

Notification System

    Email notifications

    In-app alerts

    SMS integration for critical updates

Reporting

    Customizable reports

    Export to PDF/Excel

    Dashboard widgets

Calendar Integration

    Sync with Google/Outlook Calendar

    Event reminders

    Schedule conflict detection

Mobile Responsiveness

    Mobile-friendly interface

    Progressive Web App capabilities

SYSTEM ADMINISTRATION (Backend)
User Management

    Manage all user accounts

    Role permissions configuration

    Activity logging and audit trails

System Configuration

    Academic year setup

    Department/branch management

    Placement cycle configuration

Data Management

    Database backups

    Archive old records

    Data export/import

Technical Features

    API for integration with college ERP

    Third-party tool integration (video interviews, assessments)

    Scalable infrastructure for placement drives

This system provides a complete digital ecosystem for college placements, reducing manual work, improving transparency, and enhancing the experience for all stakeholders involved in the placement process.

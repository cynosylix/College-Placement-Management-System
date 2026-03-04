# College Placement Management System (CPMS) — Student Guide

This document explains the **whole project** and how **students** use it.

---

## 1. What is CPMS?

**CPMS** is a **web-based College Placement Management System**. It helps:

- **Students** — build profile, upload resume, search jobs, apply, and track applications and interviews.
- **Companies / Recruiters** — post jobs, see applications, shortlist candidates, and schedule interviews.
- **Placement officers (TPO)** — manage students, see all applications, set eligibility, and run reports.

Everyone uses the **same website**; after login you are taken to your role’s dashboard (Student, TPO, or Recruiter).

---

## 2. How do I get an account?

1. Open the site and go to **Create account** (or **Portal**).
2. Choose **Register as Student**.
3. Fill in **username**, **email**, and **password**, then submit.
4. You are logged in and taken to the **Student Dashboard**.

To sign in later, use **Login** with the same username and password.

---

## 3. What can I do as a student?

After login you get the **Student Dashboard** with a sidebar. Here’s what each part does.

### Dashboard
- See **counts**: total applications, shortlisted, pending, interviews, saved jobs.
- **Quick links** to Profile, Browse Jobs, and Resumes.
- **Recent applications** and **upcoming interviews**.
- **Recent notifications**.

### Profile
- **Personal**: phone, date of birth, address, LinkedIn, GitHub, portfolio URL.
- **Academic**: enrollment number, course, branch, year, CGPA, graduation year.
- **Bio and achievements**.
- **Skills**: add/remove skills with proficiency (Beginner → Expert).
- **Certifications**: add name, issuer, dates, credential link.

You must **complete your profile** (especially branch, course, CGPA) because many jobs use this for **eligibility**.

### Resumes
- **Create** multiple resumes (e.g. for different roles).
- Each resume has a **title**, **content** (text), and optionally an **uploaded file** (PDF/DOC).
- Set one as **default**; it will be pre-selected when you apply.
- **Edit** or **delete** resumes anytime.

### Browse Jobs
- See **active job postings** from companies.
- **Filter** by search text, job type (Full Time, Internship, etc.), and location.
- **Save** jobs to apply later.
- Open a job to see **description**, **requirements**, **salary**, **deadline**, and **eligibility** (e.g. minimum CGPA).

### Apply for a job
On a job’s page you can:

- **Select** one of your existing resumes from the dropdown, **or**
- **Upload a new resume** (PDF or Word, max 5 MB). If you upload, that file is used for this application.
- Add an optional **cover letter**.
- Click **Submit Application**.

You can apply only if:

- You are **placement eligible** (TPO has not disabled you).
- You meet **job criteria** (e.g. minimum CGPA if the job has one).

If you don’t meet criteria, you’ll see a message and the Apply section may be hidden.

### Applications
- **List** of all your applications with **status**: Applied, Under Review, Shortlisted, Interview Scheduled, Rejected, Accepted.
- **Filter** by status.
- Open any application to see **details**, **cover letter**, and **interview** info (date, time, location/link) if scheduled.

### Saved jobs
- List of jobs you **saved** for later.
- From here you can open a job and **apply** when ready.

### Interviews
- **Upcoming** interviews (date, time, job, company).
- **Past** interviews and status.

### Documents
- **Upload** documents (e.g. transcript, certificate, ID proof).
- **View** or **delete** them later.

### Portfolio
- Add **projects**, **GitHub** links, **publications** with title, description, technologies, date.

### Messages
- **Send** messages (e.g. to TPO or recruiters).
- **View** sent and received messages.

### Notifications
- **View** system notifications (job alerts, application updates, interview reminders, etc.).

### Skill development (optional)
- **Skill gap analysis** (if the placement cell uses it).
- **Practice tests** (when available).
- **Mock interview** request and list.

---

## 4. Placement eligibility

- The **TPO** can mark you as **placement eligible** or **not**.
- Only **eligible** students can apply to jobs.
- Some jobs also have **minimum CGPA**; you must meet it to apply.
- If you think you should be eligible but can’t apply, contact the **placement cell (TPO)**.

---

## 5. Typical flow (step by step)

1. **Register** as Student and **log in**.
2. **Complete your profile** (academic details, skills, etc.).
3. **Add at least one resume** (text and/or upload PDF/DOC).
4. **Browse jobs** and **save** the ones you like.
5. **Apply** by choosing a resume or uploading one, and adding a cover letter if you want.
6. **Track** status under **Applications** and **Interviews**.
7. Check **Notifications** and **Messages** for updates.

---

## 6. Tech stack (for reference)

- **Backend**: Python, Django  
- **Database**: SQLite  
- **Frontend**: HTML, CSS, Bootstrap 5  
- **Auth**: Login/Register with username and password; role (Student/TPO/Recruiter) decides your dashboard and permissions.

---

## 7. Summary

| You want to…              | Where to go                    |
|---------------------------|--------------------------------|
| See overview               | Dashboard                      |
| Edit personal/academic info | Profile                      |
| Add or edit resume         | Resumes                        |
| Search and apply for jobs  | Browse Jobs → open job → Apply |
| Track applications         | Applications                   |
| See interview schedule     | Interviews                     |
| Upload documents           | Documents                      |
| Save jobs for later        | Saved Jobs                     |
| Check updates              | Notifications, Messages        |

If something doesn’t work (e.g. you can’t apply although you think you’re eligible), contact your **placement officer (TPO)**.

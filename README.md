# Personal Learning Tracker

A structured web application designed to plan, track, and optimize technical learning using a goal-oriented system.

> ⚠️ This project is currently under active development.  
> The features described below represent the **final scope of the MVP**.

---

## Overview

Personal Learning Tracker is a backend-driven web application that helps developers structure and monitor their learning process.

Instead of vague goals like "Learn Linux", the system enforces a clear hierarchy:

Goal → Sub-goal → Skill → Resources

It also integrates time tracking and structured review cycles to create a consistent learning feedback loop.

The primary objective of this project is to build a minimal but powerful system that supports long-term, disciplined technical growth.

---

## teck stack

## Core Concept

The application is built around a hierarchical learning model:

### 1. Goals
High-level learning objectives.
Examples:
- Linux
- Backend Development
- DevOps

### 2. Sub-goals
Major domains within a goal.
Example (Linux):
- Command Line
- File System
- Process Management

### 3. Skills
Concrete, actionable competencies.
Examples:
- File management (cp, mv, rm)
- Pipes and redirection
- User and group permissions

### 4. Resources
Each skill can contain multiple resources:
- Articles
- Documentation
- Tutorials
- Videos

This allows cross-referencing and efficient revision.

---

## MVP Features

The following features define the final scope of the MVP:

### Goal Management
- Create, update, delete goals
- Organize sub-goals within goals
- Attach skills to sub-goals

### Resource Tracking
- Link multiple resources to each skill
- Store notes for future reference

### Daily Reviews
- Log worked-on skills
- Track time spent (stored in minutes)
- Lightweight logging system

### Weekly Reviews
- Summarize sub-goal progress
- Add short structured reflection
- Time aggregation calculated automatically

### Monthly Reviews
- High-level overview of learning progress
- Goal completion tracking
- Trend visualization (via aggregated data)

---

## Design Principles

This project follows strict engineering principles:

- Learning-first, tool-second
- No duplicated data
- Minimal cognitive overhead
- Clear separation between raw logs and summaries
- Extensible architecture for future roadmap integration

---

## 🛠 Tech Stack

- Backend: Django
- Database: PostgreSQL
- Containerization: Docker & Docker Compose
- ORM: Django ORM
- pytest
- django-pytest
- factory-boy
- Faker
- Tailwindcss
- daisyui
- htmx
- django-allauth

---

## Project Status

The project is actively developed and used as a personal learning system.

All features listed above represent the intended final scope of the MVP.  
Future expansions (such as shared roadmaps or public learning plans) are intentionally postponed to maintain focus and simplicity.

---

# Running the Project Locally

This project is fully containerized using Docker.

## 1️ Prerequisites

Make sure you have installed:

- Docker
- Docker Compose

Check installation:

```bash
docker --version
docker compose version
```

## 2 Clone the Repository

```
https://github.com/serialcoder-io/Progress-log.git

cd progress-log
```

## 3 Environment Variables

```
SECRET_KEY='your-django-secret-key'
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000

SMTP_HOST=smtp.gmail.com # or other smtp_host
SMTP_USER=your@gmail.com
SMTP_PASS=your_password # your have to go to google cloud console to create one

#Cloudinary (this is for media storage on cloudinary)
CLOUD_NAME=your_cloudinary_cloud_name
API_KEY=your_cloudinary_api_key
API_SECRET=your_cloudinary_api_secret

#PROVIDERS
#google (create an app in google cloud console)
CLIENT_ID=your_cloud_id
SECRET=your_secret

POSTGRES_TAG=latest


DB_NAME=db_name
DB_USER=user
DB_PASS=your_strong_password
DB_HOST=localhost
DB_PORT=5432
```

## 4 Build and Start Containers

**This will :**

- Build the Django container

- Start PostgreSQL in a separate container

- Run the development server

## 5 Apply migrations

```
docker compose exec web python manage.py migrate
```

## 6 Create Superuser

```
docker compose exec web python manage.py createsuperuser
```

## 7 Access the Application

- App
    - http://localhost:8000
- Admin
    - http://localhost:8000/admin


# Author
**Anli omar**

Backend-focused developer building structured systems for disciplined technical growth.

- github [Github](https://github.com/anliomar-dev)
- portfolio [Portfolio](https://omartech.site)
- email: anliomar@outlook.com


# Licence
**Read license.txt and licence.md file**
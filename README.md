# SummitGO - Trekking Management App 


A full stack web application to manage trekking operations including trekker registrations, staff
assignments, trek scheduling and admin operations.



## Tech Stack

- Frontend: Vue 3, Vue Router, Bootstrap 5, Axios, Vite

- Backend: Flask, SQLAlchemy, Flask-JWT-Extended, Flask-Caching, Celery, Redis

- Database: SQLite (via SQLAlchemy)

- Email Testing: MailHog


## Project Structure

Backend            Flask REST API 
- app.py
- applications/
  - controllers/
  - models.py
  - config.py
- static/
- templates/
- celery_worker.py
- tasks.py

Frontend          Vue 3 frontend app
- src/
  - components/
  - views/
  - router/
  - App.vue

README.md


## Features

- JWT based authentication with role(trekker, admin and staff) based access
- Admin, Staff, and Trekker user roles
- Background task processing with Celery + Redis
- Email notifications via MailHog
- API caching with Flask redis Caching


## Roles & Access


- Role    │ Access                                   

- Admin   │ Full access — users, treks, reports      

- Staff   │ Manage trekkers and trek assignments     

- Trekker │ View assigned treks and personal history 



## Setup & Running

**check setup_guide.md**



### Default Admin Credentials

- Username: admin
- Password: admin


### API

API is defined in backend/api.yaml. You can open it in any OpenAPI/Swagger viewer.
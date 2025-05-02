# 🧠 Life Hacks Sharing App

A full-stack web application for sharing and discovering life hacks — built with **Django REST Framework** on the backend and **React (Vite)** on the frontend.

## 🔗 Demo

Coming soon... (Add your deployment URL here if available)

---

## 🚀 Features

- 📋 Create, read, update, and delete (CRUD) life hacks
- 🔐 User authentication & registration
- 👍 Like / favorite hacks
- 🔍 Search & filter hacks
- 🖼️ Responsive frontend with Vite + React
- ⚙️ RESTful API with Django DRF
- 🐳 Dockerized for easy deployment

---

## 🛠️ Tech Stack

| Backend         | Frontend    | Deployment          |
|----------------|-------------|---------------------|
| Django + DRF    | React (Vite) | Docker & Docker Compose |
| PostgreSQL      | Axios       | Nginx (optional)    |

---

## 📁 Project Structure

```
project-root/
│
├── backend/                  # Django project
│   ├── manage.py
│   ├── life-hacks/           # Main Django project folder
│   └── api/                  # Django apps (e.g. accounts, hacks)
│
├── frontend/
│   └── life-hacks/           # React (Vite) app source
│       ├── index.html
│       ├── src/
│       └── vite.config.js
│
├── .env                      # Environment variables
├── docker-compose.yml        # Docker Compose configuration
└── README.md
```


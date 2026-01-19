# CloudVault ☁️  
### Secure Cloud File Storage & Sharing Platform

CloudVault is a **cloud-based file storage and sharing web application** inspired by the core features of Google Drive.  
It allows users to securely upload, organize, search, and share files using **role-based access control**, built with a **FastAPI backend** and **React frontend**.

---

## 🚀 Features

### 🔐 Authentication & Security
- Email & password authentication
- Google OAuth support
- JWT-based authentication (HttpOnly cookies)
- Role-based access control (Owner, Editor, Viewer)
- Secure signed URLs for file access
- Server-side permission enforcement

### 📁 File & Folder Management
- Upload & download files (drag & drop)
- Nested folder hierarchy
- Rename, move, and delete files/folders
- Breadcrumb-based navigation
- Starred files
- Trash with restore (soft delete)

### 🤝 File Sharing
- Share files/folders with users
- Viewer / Editor permissions
- Public shareable links
- Optional link expiry & password protection

### 🔍 Search & Organization
- Search by file name
- Filter by file type
- Sorting (name, size, date)
- Pagination & lazy loading

---

## 🧱 Tech Stack

### Frontend
- React (Vite)
- Tailwind CSS
- React Query (TanStack)
- Axios
- React Dropzone

### Backend
- Python (FastAPI)
- SQLAlchemy / SQLModel
- Pydantic
- JWT Authentication

### Database & Storage
- PostgreSQL (Supabase)
- Supabase Storage (Signed URLs)

### Deployment
- Frontend: Vercel / Netlify
- Backend: Render / Fly.io
- Database & Storage: Supabase

---

## 🏗️ System Architecture

[ React Client ]
|
v
[ FastAPI Backend ]
|
v
[ PostgreSQL (Supabase) ] ---- [ Supabase Storage ]


---

## 📂 Project Structure

### Backend

backend/
├── app/
│ ├── main.py
│ ├── models/
│ ├── schemas/
│ ├── routes/
│ ├── services/
│ ├── core/
│ └── utils/
├── requirements.txt
└── .env


### Frontend

frontend/
├── src/
│ ├── components/
│ ├── pages/
│ ├── services/
│ ├── hooks/
│ └── styles/
├── tailwind.config.js
└── vite.config.js


---

## 🔑 User Roles & Permissions

| Role   | Permissions |
|-------|-------------|
| Owner | Full control |
| Editor | Upload, edit, delete |
| Viewer | Read-only |
| Public User | Access via shared link |

All permission checks are enforced **server-side**.

---

## 🔌 API Endpoints (Sample)

### Auth
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

### Files
- `POST /files/init-upload`
- `POST /files/complete-upload`
- `GET /files/{id}`
- `DELETE /files/{id}`

### Folders
- `POST /folders`
- `GET /folders/{id}`

### Sharing
- `POST /shares`
- `POST /public-link`

---

## 🛡️ Security Measures
- JWT stored in HttpOnly cookies
- Input validation with Pydantic
- Role-based access middleware
- Rate limiting
- Signed URLs for uploads/downloads

---

## 🧪 Testing
- API testing using Postman
- Basic unit tests with Pytest
- End-to-end manual testing

---

## 📦 Installation & Setup

### Backend

cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

### Frontend

cd frontend
npm install
npm run dev

🎯 Future Enhancements

File version history

Activity logs

Tags & labels

Storage quota management

Desktop sync client (optional)

📚 Skills Gained

Full-stack development with React & FastAPI

Secure authentication & authorization

Cloud storage & signed URL workflows

Database schema design

Scalable API architecture

Cloud deployment

🏁 Final Outcome

CloudVault is a resume-ready cloud storage SaaS MVP, demonstrating real-world backend, frontend, security, and cloud deployment skills.

👤 Author
SHREYANSH JAIN
Information Technology Student / Python Developer
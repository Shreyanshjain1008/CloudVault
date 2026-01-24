# CloudVault ☁️  
### Secure Cloud File Storage & Sharing Platform

CloudVault is a full-stack cloud storage application inspired by Google Drive. It allows users to securely upload, manage, preview, star, delete, and restore files with authentication and modern UI., built with a **FastAPI backend** and **React frontend**.

---

## 🚀 Features

### 🔐 Authentication & Security
- User registration & login
- JWT-based authentication
- Protected routes (My Drive, Trash, Shared)

### 📁 File & Folder Management
- Upload files (multi-file supported)
- Drag & drop upload
- Upload progress bar
- File preview (images, documents)
- Star / Unstar files
- Move files to Trash
- Restore from Trash
- Permanent delete

### 🤝 File Sharing
- Share files/folders with users
- Public shareable links
- Optional link expiry & password protection

---

## 🧱 Tech Stack

### Frontend
- React (Vite)
- Tailwind CSS
- React Router
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
- Frontend: Vercel 
- Backend: Render 
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
python -m venv venv
venv\Scripts\activate
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
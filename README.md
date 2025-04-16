# 📢 College Online Notice Board

An online web application to simplify notice sharing between college admins and students. Built using **Flask**, **MySQL**, **HTML/CSS/JS**, this system allows secure admin logins to manage notices, and gives students an easy interface to view and search them.

## 🚀 Features

- 👨‍🏫 **Admin Login System** (via Flask-Login)
- 📄 **Add, Edit, Delete Notices**
- 📎 **Upload Attachments** (PDFs, Images, Docs, etc.)
- 🔍 **Search Functionality** (by title or content)
- 🎓 **Student View Page** (publicly accessible)
- ☁️ **Deployed Separately for Admin & Students**

## 🛠️ Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask)
- **Database:** MySQL
- **Authentication:** Flask-Login

## 🗃️ Folder Structure


## 📦 Setup Instructions

1. **Clone the Repository**


2. **Install Requirements**


3. **Configure MySQL**
- Create a database `college_notices`
- Import the SQL schema provided in `schema.sql`

4. **Run the App**

5. **Access Pages**
- Admin: `http://localhost:5000/login`
- Student: `http://localhost:5000/`

## 🌐 Deployment

Use platforms like:
- [Render](https://render.com/)
- [Vercel + Flask API via serverless](https://vercel.com/)
- [Railway](https://railway.app/)
- [Replit](https://replit.com/)

Admin and Student pages can be deployed on different URLs for clarity.


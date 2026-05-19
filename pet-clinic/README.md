# Pet Clinic Management System

ระบบจัดการคลินิกรักษาสัตว์ built with Python Flask, SQLite, Flask-SQLAlchemy และ Flask-Login.

## Features

- Authentication: Login/Register/Logout
- Role-based access: Admin / User
- CRUD for pets, doctors, appointments, vaccines, payments
- Appointment booking และ treatment records
- Responsive Bootstrap 5 UI
- Flash messages และ form validation
- SQLite database auto-created
- Admin dashboard และ search system

## Project Structure

- `app.py` - แอป Flask หลัก
- `config.py` - ตั้งค่าการเชื่อมต่อ
- `requirements.txt` - Dependencies
- `models/` - SQLAlchemy models
- `routes/` - Blueprints สำหรับ auth, user, admin, appointment
- `templates/` - Jinja2 templates
- `static/` - CSS, JS, uploads
- `instance/` - โฟลเดอร์ instance

## Installation

1. เปิด terminal แล้วเข้าสู่โฟลเดอร์โปรเจกต์:

```bash
cd '/Users/sirichaikhamsukloet/Desktop/Healing Paws/pet-clinic'
```

2. สร้าง virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. ติดตั้ง dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

จากนั้นเปิดเว็บเบราว์เซอร์ที่ `http://127.0.0.1:5000`

## Default Sample Accounts

- Admin: `admin@clinic.com` / `admin123`
- User: `user@clinic.com` / `user123`

## Deployment

ระบบนี้พร้อมใช้งานบน PythonAnywhere และแพลตฟอร์มอื่นที่รองรับ Flask โดยใช้คำสั่ง `python app.py` หรือปรับเป็น WSGI ตามแพลตฟอร์ม

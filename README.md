# 📌 Bongofiverr – Freelance Marketplace Platform

**Bongofiverr** is a full-stack freelancing marketplace built with **Django** and **Django REST Framework (DRF)**.  
It allows buyers to hire services, place orders, and make payments, while sellers can list services, complete orders, and receive earnings.  

---

## 🚀 Features

### 🔹 Authentication & Users
- User registration & login (JWT Authentication)  
- Separate roles: **Buyer** and **Seller**  
- Profile management with profile picture, bio, and contact info  

### 🔹 Services & Orders
- Sellers can create and manage services  
- Buyers can browse, search, and filter services  
- Buyers can place orders on active services  
- Sellers can accept / reject / deliver orders  

### 🔹 Reviews & Ratings
- Buyers can leave reviews and ratings on completed orders  
- Sellers can manage received feedback  

### 🔹 Payments (Planned/Future Integration)
- Buyers can pay securely online  
- Sellers can withdraw earnings  
- Payment history & invoices  

### 🔹 Admin Panel
- Manage users, services, orders, and reviews from Django Admin  

---

## 🛠️ Tech Stack

- **Backend:** Django, Django REST Framework  
- **Database:** PostgreSQL (can use SQLite for development)  
- **Authentication:** JWT (via `djangorestframework-simplejwt`)  
- **Frontend (optional):** Django Templates / React / Vue (future)  
- **Deployment:** Gunicorn + Nginx (Linux) / Vercel (demo setup)  

---

## ⚙️ Installation & Setup

### 1. Clone Repository
```bash
git clone https://github.com/your-username/bongofiverr.git
cd bongofiverr
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# Activate (Windows)
venv\Scripts\activate
# Activate (Linux/Mac)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Run Server
```bash
python manage.py runserver
```

Server will start at 👉 `http://127.0.0.1:8000/`

---

## 🧑‍💻 Contributing

1. Fork the repo  
2. Create a new branch (`feature-new`)  
3. Commit changes  
4. Push to your fork and create a PR  


Quick start:
1. python -m venv venv && source venv/bin/activate (or venv\Scripts\activate on Windows)
2. pip install -r requirements.txt
3. python manage.py migrate
4. python manage.py createsuperuser
5. python manage.py runserver

API examples:
- POST /api/users/register/  (username,email,password,role)
- POST /api/users/login/     (username,password) -> returns JWT
- GET  /api/users/me/        -> user info (auth)
- GET  /api/services/        -> list (filter ?category=slug, ordering=price or -price)
- POST /api/services/        -> create (seller)
- POST /api/orders/          -> create order (buyer)
- POST /api/reviews/         -> create review (after order completed)


# Birthday Reminders API 🎉
This is a Django-based API for managing birthdays and sending notifications to staff members on their birthdays.

## 📌 Features
- Add Staff
- Store staff birthdays 📅
- Create reusable notification templates ✉️
- Log and track sent notifications 📊
- JWT-based authentication 🔑

## 🚀 Installation & Setup
1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo
   ```

2. **Create a virtual environment and activate it**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**  
   ```bash
   python manage.py migrate
   ```

5. **Start the server**  
   ```bash
   python manage.py runserver
   ```

## 📜 API Endpoints
All API endpoints and details can be found in Swagger.
Once the server is running, open Swagger UI in your browser:

http://127.0.0.1:8000/swagger/


## 🛠 Technologies Used
- **Django** 🐍 (Backend Framework)
- **Django REST Framework** (API Handling)
- **APScheduler** (Scheduled Task Management)
- **JWT Authentication** (User Authentication)
- **SQLite/MySQL** (Database)

## 🎯 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss.

## 📜 License
This project is open-source and available under the **MIT License**.

## 🐝 TaskHive – Smart Task Management System
live link:https://taskhive-q35c.onrender.com

**TaskHive** is a Django-based smart task management system designed to simplify team task allocation, employee management, and work progress tracking.

Unlike traditional to-do applications, TaskHive helps managers assign tasks to employees based on their skills, monitor task progress, and manage employee responses such as task acceptance, blocking, and change requests.

## 🚀 Key Features

### 👨‍💼 Manager Dashboard
- Create and manage tasks.
- Define task priorities and required skills.
- View employees based on their skill sets.
- Assign tasks to suitable employees.
- Monitor assigned tasks and their progress.

### 👩‍💻 Employee Dashboard
- View assigned tasks.
- Accept or respond to assigned tasks.
- Update task status.
- Track ongoing work.
- Request changes when task requirements need modification.

### 🎯 Skill-Based Task Allocation
- Maintain employee skill profiles.
- Define skills required for each task.
- Match employees with tasks based on their skills.
- Help managers make better task allocation decisions.

### 🏠 Work From Home Tracking
- Track employee work-from-home status.
- Maintain employee work activity visibility.

### 📊 Task Management
- Manage task priorities:
  - Low
  - Medium
  - High
  - Urgent
- Track task statuses:
  - Assigned
  - Accepted
  - In Progress
  - Blocked

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| HTML5 | Frontend structure |
| CSS3 | Styling |
| JavaScript | Frontend interactions |
| SQLite | Database (development) |
| Git & GitHub | Version control |

## 🏗️ Project Architecture

```text
TaskHive/
│
├── taskhiveproject/
│   ├── manage.py
│   ├── taskhiveproject/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── tasks/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── forms.py
│   │   ├── urls.py
│   │   └── templates/
│   │
│   └── db.sqlite3
│
└── README.md
```

*Note: Update the folder structure according to your final project structure.*

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/TaskHive.git
```

### 2. Navigate to the Project Directory

```bash
cd TaskHive/taskhiveproject
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install django
```

### 6. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

## 🔄 How TaskHive Works

1. Manager logs into the system.
2. Manager creates a task with a description, priority, and required skills.
3. System identifies employees with matching skills.
4. Manager selects and assigns an employee.
5. Employee views and responds to the assigned task.
6. Employee updates task progress.
7. Manager monitors task status and employee activity.

## 🎯 Project Objective

The main objective of TaskHive is to improve team productivity by making task allocation more organized, skill-oriented, and transparent.

It aims to reduce manual task assignment efforts while providing managers with better visibility into employee activities and task completion.

## 🔮 Future Enhancements

- AI-based employee and task matching.
- Real-time notifications.
- Task deadline and reminder management.
- Advanced analytics and productivity reports.
- Attendance and work activity tracking.
- Team collaboration and communication features.

## 👩‍💻 Developer

**Rutika Nerkar**

Electronics & Telecommunication Engineering Graduate

- GitHub: https://github.com/rutikanerkar15-sudo
- LinkedIn: https://www.linkedin.com/in/rutika-nerkar-76b896308

---

⭐ If you find this project interesting, feel free to explore the repository!

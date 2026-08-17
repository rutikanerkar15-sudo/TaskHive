from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Employee, Task, TaskAssignment,TaskUpdate,  ChangeRequest,Notification
from .forms import EmployeeRegistrationForm, TaskForm, TaskUpdateForm,ChangeRequestForm
from django.contrib.auth.decorators import login_required


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    employee = Employee.objects.get(
        user=request.user
    )

    return render(
        request,
        "taskhiveapp/dashboard.html",
        {
            "employee": employee
        }
    )
    


def employee_list(request):
    employees = Employee.objects.all()

    return render(
        request,
        "taskhiveapp/employees.html",
        {
            "employees": employees
        }
    )


def register_employee(request):

    if request.method == "POST":

        form = EmployeeRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect("login")

    else:
        form = EmployeeRegistrationForm()

    return render(
        request,
        "taskhiveapp/register.html",
        {
            "form": form
        }
    )


def employee_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            employee = Employee.objects.get(
                user__email=email
            )

            user = authenticate(
                request,
                username=employee.user.username,
                password=password
            )

            if user is not None:
                login(request, user)

                return redirect("dashboard")

            error = "Invalid email or password."

        except Employee.DoesNotExist:

            error = "No employee account found with this email."

        return render(
            request,
            "taskhiveapp/login.html",
            {
                "error": error
            }
        )

    return render(
        request,
        "taskhiveapp/login.html"
    )


def employee_logout(request):

    logout(request)

    return redirect("login")

def create_task(request):

    if not request.user.is_authenticated:
        return redirect("login")

    employee = Employee.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Your account is not registered as an employee."
            }
        )

    # Only managers can create tasks
    if employee.role != "manager":
        return render(
            request,
            "taskhiveapp/access_denied.html"
        )

    if request.method == "POST":

        form = TaskForm(request.POST)

        if form.is_valid():

            task = form.save(commit=False)

            task.created_by = employee

            task.save()

            form.save_m2m()

            return redirect(
                "task_matching",
                task_id=task.id
            )

    else:

        form = TaskForm()

    return render(
        request,
        "taskhiveapp/create_task.html",
        {
            "form": form
        }
    )


def task_matching(request, task_id):

    if not request.user.is_authenticated:
        return redirect("login")

    manager = Employee.objects.get(
        user=request.user
    )

    if manager.role != "manager":
        return render(
            request,
            "taskhiveapp/access_denied.html"
        )

    task = Task.objects.get(
        id=task_id
    )

    required_skills = set(
        task.required_skills.values_list(
            "id",
            flat=True
        )
    )

    employees = Employee.objects.exclude(
        id=manager.id
    )

    matches = []

    for employee in employees:

        employee_skills = set(
            employee.skills.values_list(
                "id",
                flat=True
            )
        )

        matched_skills = required_skills & employee_skills

        match_count = len(matched_skills)

        if match_count > 0:

            percentage = round(
                (match_count / len(required_skills)) * 100
            )

            matches.append({
                "employee": employee,
                "matched_skills": match_count,
                "total_skills": len(required_skills),
                "percentage": percentage,
            })

    matches.sort(
        key=lambda x: x["percentage"],
        reverse=True
    )

    return render(
        request,
        "taskhiveapp/task_matching.html",
        {
            "task": task,
            "matches": matches,
        }
    )
def assign_task(request, task_id, employee_id):

    if not request.user.is_authenticated:
        return redirect("login")

    manager = Employee.objects.filter(
        user=request.user
    ).first()

    if manager is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Manager profile not found."
            }
        )

    if manager.role != "manager":
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Only managers can assign tasks."
            }
        )

    task = Task.objects.filter(
        id=task_id,
        created_by=manager
    ).first()

    if task is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Task not found."
            }
        )

    employee = Employee.objects.filter(
        id=employee_id,
        role="employee"
    ).first()

    if employee is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Employee not found."
            }
        )

    # Check if already assigned
    assignment = TaskAssignment.objects.filter(
        task=task,
        employee=employee,
        is_active=True
    ).first()

    if assignment is None:

        TaskAssignment.objects.create(
            task=task,
            employee=employee
        )

        Notification.objects.create(
            employee=employee,
            notification_type="task",
            message=f"You have been assigned a new task: {task.title}"
        )

    return redirect(
        "task_matching",
        task_id=task.id
    )


def my_tasks(request):

    if not request.user.is_authenticated:
        return redirect("login")

    employee = Employee.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Employee profile not found."
            }
        )

    assignments = TaskAssignment.objects.filter(
        employee=employee,
        is_active=True
    ).select_related("task")

    return render(
        request,
        "taskhiveapp/my_tasks.html",
        {
            "employee": employee,
            "assignments": assignments
        }
    )


@require_POST
def update_task_status(request, task_id, status):

    if not request.user.is_authenticated:
        return redirect("login")

    employee = Employee.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Employee profile not found."
            }
        )

    assignment = TaskAssignment.objects.filter(
        task_id=task_id,
        employee=employee,
        is_active=True
    ).first()

    if assignment is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "This task is not assigned to you."
            }
        )

    allowed_statuses = ["accepted", "in_progress", "completed"]

    if status not in allowed_statuses:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Invalid status."
            }
        )

    task = assignment.task

    if status == "accepted":
        task.status = "accepted"
        assignment.accepted_at = timezone.now()
        assignment.save()

    elif status == "in_progress":
        task.status = "in_progress"

    elif status == "completed":
        task.status = "completed"
        task.progress = 100

    task.save()

    return redirect("my_tasks")

def manager_tasks(request):

    if not request.user.is_authenticated:
        return redirect("login")

    manager = Employee.objects.filter(
        user=request.user
    ).first()

    if manager is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Employee profile not found."
            }
        )

    if manager.role != "manager":
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Only managers can access this page."
            }
        )

    tasks = Task.objects.filter(
        created_by=manager
    ).prefetch_related(
        "assignments__employee",
        "updates__employee"
    )

    return render(
        request,
        "taskhiveapp/manager_tasks.html",
        {
            "tasks": tasks
        }
    )

def verify_task(request, task_id):

    if not request.user.is_authenticated:
        return redirect("login")

    manager = Employee.objects.filter(
        user=request.user
    ).first()

    if manager is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Employee profile not found."
            }
        )

    if manager.role != "manager":
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Only managers can verify tasks."
            }
        )

    task = Task.objects.filter(
        id=task_id,
        created_by=manager
    ).first()

    if task is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Task not found."
            }
        )

    if task.status == "completed":
        task.status = "verified"
        task.progress = 100
        task.save()

    return redirect("manager_tasks")

def request_change(request, task_id):

    if not request.user.is_authenticated:
        return redirect("login")

    employee = Employee.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Employee profile not found."
            }
        )

    assignment = TaskAssignment.objects.filter(
        task_id=task_id,
        employee=employee,
        is_active=True
    ).first()

    if assignment is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "This task is not assigned to you."
            }
        )

    task = assignment.task

    if request.method == "POST":

        form = ChangeRequestForm(request.POST)

        if form.is_valid():

            change_request = form.save(commit=False)

            change_request.task = task
            change_request.employee = employee

            change_request.save()

            return redirect("my_tasks")

    else:

        form = ChangeRequestForm()

    return render(
        request,
        "taskhiveapp/change_request.html",
        {
            "task": task,
            "form": form
        }
    )



# Notification View


@login_required
def notification(request):

    employee = Employee.objects.filter(
        user=request.user
    ).first()

    if employee is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Employee profile not found."
            }
        )

    notifications = Notification.objects.filter(
        employee=employee
    ).order_by("-created_at")

    return render(
        request,
        "taskhiveapp/notifications.html",
        {
            "notifications": notifications
        }
    )
def manager_change_requests(request):

    if not request.user.is_authenticated:
        return redirect("login")

    manager = Employee.objects.filter(
        user=request.user
    ).first()

    if manager is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Employee profile not found."
            }
        )

    if manager.role != "manager":
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Only managers can review change requests."
            }
        )

    change_requests = ChangeRequest.objects.filter(
        task__created_by=manager,
        status="pending"
    ).select_related("task", "employee").order_by("-created_at")

    return render(
        request,
        "taskhiveapp/change_requests.html",
        {
            "change_requests": change_requests
        }
    )


def review_change_request(request, change_request_id, decision):

    if not request.user.is_authenticated:
        return redirect("login")

    manager = Employee.objects.filter(
        user=request.user
    ).first()

    if manager is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Employee profile not found."
            }
        )

    if manager.role != "manager":
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Only managers can review change requests."
            }
        )

    change_request = ChangeRequest.objects.filter(
        id=change_request_id,
        task__created_by=manager,
        status="pending"
    ).select_related("task", "employee").first()

    if change_request is None:
        return render(
            request,
            "taskhiveapp/access_denied.html",
            {
                "message": "Change request not found or already reviewed."
            }
        )

    if decision == "approve":

        change_request.status = "approved"
        change_request.save()

        if change_request.requested_deadline:
            change_request.task.deadline = change_request.requested_deadline
            change_request.task.save()

        Notification.objects.create(
            employee=change_request.employee,
            notification_type="change_request",
            message=f"Your deadline change request for '{change_request.task.title}' was approved."
        )

    elif decision == "reject":

        change_request.status = "rejected"
        change_request.save()

        Notification.objects.create(
            employee=change_request.employee,
            notification_type="change_request",
            message=f"Your deadline change request for '{change_request.task.title}' was rejected."
        )

    return redirect("manager_change_requests")
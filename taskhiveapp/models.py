from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    ROLE_CHOICES = [
        ("employee", "Employee"),
        ("manager", "Manager"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="employee")
    department = models.CharField(max_length=100, blank=True)
    skills = models.ManyToManyField(Skill, blank=True)
    is_wfh = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("urgent", "Urgent"),
    ]

    STATUS_CHOICES = [
        ("assigned", "Assigned"),
        ("accepted", "Accepted"),
        ("in_progress", "In Progress"),
        ("blocked", "Blocked"),
        ("completed", "Completed"),
        ("verified", "Verified"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    created_by = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="created_tasks"
    )

    required_skills = models.ManyToManyField(
        Skill,
        blank=True,
        related_name="tasks"
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="assigned"
    )

    progress = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    deadline = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class TaskAssignment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="assignments"
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="task_assignments"
    )

    assigned_at = models.DateTimeField(auto_now_add=True)
    accepted_at = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.employee} → {self.task}"


class TaskUpdate(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="updates"
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="task_updates"
    )

    progress = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} - {self.progress}%"


class ChangeRequest(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="change_requests"
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="change_requests"
    )

    reason = models.TextField()

    requested_deadline = models.DateTimeField(
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Change request - {self.task.title}"


class WorkSession(models.Model):
    WORK_MODE_CHOICES = [
        ("office", "Office"),
        ("wfh", "Work From Home"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="work_sessions"
    )

    work_mode = models.CharField(
        max_length=20,
        choices=WORK_MODE_CHOICES
    )

    date = models.DateField(auto_now_add=True)

    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)

    last_activity = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee} - {self.work_mode} - {self.date}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ("task", "Task"),
        ("deadline", "Deadline"),
        ("reminder", "Reminder"),
        ("change_request", "Change Request"),
        ("wfh", "WFH"),
        ("system", "System"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    notification_type = models.CharField(
        max_length=30,
        choices=NOTIFICATION_TYPES
    )

    message = models.TextField()

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # DASHBOARD
    # =========================

    path(
        "",
        views.dashboard,
        name="dashboard"
    ),


    # =========================
    # EMPLOYEES
    # =========================

    path(
        "employees/",
        views.employee_list,
        name="employee_list"
    ),


    # =========================
    # AUTHENTICATION
    # =========================

    path(
        "register/",
        views.register_employee,
        name="register"
    ),

    path(
        "login/",
        views.employee_login,
        name="login"
    ),

    path(
        "logout/",
        views.employee_logout,
        name="logout"
    ),


    # =========================
    # CREATE TASK
    # =========================

    path(
        "tasks/create/",
        views.create_task,
        name="create_task"
    ),


    # =========================
    # TASK MATCHING
    # =========================

    path(
        "tasks/<int:task_id>/matching/",
        views.task_matching,
        name="task_matching"
    ),


    # =========================
    # ASSIGN TASK
    # =========================

    path(
        "tasks/<int:task_id>/assign/<int:employee_id>/",
        views.assign_task,
        name="assign_task"
    ),


    # =========================
    # TASK STATUS
    # =========================

    path(
        "tasks/<int:task_id>/status/<str:status>/",
        views.update_task_status,
        name="update_task_status"
    ),


    # =========================
    # TASK UPDATE
    # =========================

    path(
        "tasks/<int:task_id>/update/",
        views.TaskUpdate,
        name="TaskUpdate"
    ),


    # =========================
    # EMPLOYEE TASKS
    # =========================

    path(
        "my-tasks/",
        views.my_tasks,
        name="my_tasks"
    ),


    # =========================
    # MANAGER TASKS
    # =========================

    path(
        "manager/tasks/",
        views.manager_tasks,
        name="manager_tasks"
    ),


    # =========================
    # VERIFY TASK
    # =========================

    path(
        "manager/tasks/<int:task_id>/verify/",
        views.verify_task,
        name="verify_task"
    ),


    # =========================
    # CHANGE REQUEST
    # =========================

    path(
        "tasks/<int:task_id>/change-request/",
        views.request_change,
        name="request_change"
    ),

   
    path(
        "notification/",
        views.notification,
        name="notification"
                    
            
    ),
    # =========================
    # CHANGE REQUEST REVIEW
    # =========================

    path(
        "manager/change-requests/",
        views.manager_change_requests,
        name="manager_change_requests"
    ),

    path(
        "manager/change-requests/<int:change_request_id>/<str:decision>/",
        views.review_change_request,
        name="review_change_request"
    ),
    




]


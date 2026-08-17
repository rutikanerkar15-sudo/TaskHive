from django.contrib import admin
from .models import (
    Skill,
    Employee,
    Task,
    TaskAssignment,
    TaskUpdate,
    ChangeRequest,
    WorkSession,
    Notification,
)


admin.site.register(Skill)
admin.site.register(Employee)
admin.site.register(Task)
admin.site.register(TaskAssignment)
admin.site.register(TaskUpdate)
admin.site.register(ChangeRequest)
admin.site.register(WorkSession)
admin.site.register(Notification)

from django import forms
from django.contrib.auth.models import User

from .models import (
    Employee,
    Skill,
    Task,
    TaskUpdate,
    ChangeRequest,
)


class EmployeeRegistrationForm(forms.Form):

    first_name = forms.CharField(
        max_length=100
    )

    last_name = forms.CharField(
        max_length=100
    )

    email = forms.EmailField()

    password = forms.CharField(
        widget=forms.PasswordInput
    )

    department = forms.CharField(
        max_length=100
    )

    role = forms.ChoiceField(
        choices=Employee.ROLE_CHOICES
    )

    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    is_wfh = forms.BooleanField(
        required=False,
        label="Working from Home"
    )

    def clean_email(self):

        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def save(self):

        user = User.objects.create_user(
            username=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )

        employee = Employee.objects.create(
            user=user,
            role=self.cleaned_data["role"],
            department=self.cleaned_data["department"],
            is_wfh=self.cleaned_data["is_wfh"],
        )

        employee.skills.set(
            self.cleaned_data["skills"]
        )

        return employee


class TaskForm(forms.ModelForm):

    class Meta:

        model = Task

        fields = [
            "title",
            "description",
            "required_skills",
            "priority",
            "deadline",
        ]

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter task title"
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "placeholder": "Describe the task",
                    "rows": 5
                }
            ),

            "required_skills": forms.CheckboxSelectMultiple(),

            "deadline": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local"
                }
            ),
        }


class TaskUpdateForm(forms.ModelForm):

    class Meta:

        model = TaskUpdate

        fields = [
            "progress",
            "message",
        ]

        widgets = {

            "progress": forms.NumberInput(
                attrs={
                    "min": 0,
                    "max": 100,
                    "placeholder": "Enter progress %"
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Describe your work update"
                }
            ),
        }

class ChangeRequestForm(forms.ModelForm):

    class Meta:

        model = ChangeRequest

        fields = [
            "reason",
            "requested_deadline",
        ]

        widgets = {

            "reason": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Explain why you need a deadline change"
                }
            ),

            "requested_deadline": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local"
                }
            ),
        }
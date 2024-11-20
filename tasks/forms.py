import re
from django import forms

class TaskForm(forms.Form):
    task = forms.CharField(label="Task Name")
    user_id = forms.CharField(label="user_id")
    priority = forms.IntegerField(label="Task Priority")
    kickoff = forms.DateTimeField(
        label="Task Kick Off Date And Time",
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M:%S.%f"]  # Specify the required format
    )
from django import forms

class UsersForm(forms.Form):
    username = forms.CharField(label="Username", min_length=5, max_length=100)
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput, min_length=8)
    image = forms.ImageField(label="Profile Image", required=False)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 5:
            raise forms.ValidationError("Username must be at least 5 characters long.")
        if not username.isalnum():
            raise forms.ValidationError("Username must contain only letters and numbers.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        if not re.match(email_regex, email):
            raise forms.ValidationError("Invalid email format.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError("Password must contain at least one number.")
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError("Password must contain at least one letter.")
        return password

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and not image.name.lower().endswith(('jpg', 'jpeg', 'png')):
            raise forms.ValidationError("Image must be in JPG, JPEG, or PNG format.")
        return image

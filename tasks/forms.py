from django import forms
class TaskForm(forms.Form):
    task     = forms.CharField(label="Task Name")
    priority = forms.IntegerField(label="Task Priority")
    kickoff  = forms.DateTimeField(
        label="Task Kick Off Date And Time",
        widget=forms.DateTimeInput(attrs={"type":"datetime-local"})
    )

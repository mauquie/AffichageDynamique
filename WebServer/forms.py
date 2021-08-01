from django import forms
from ApiServer import models
from django.contrib.auth.models import Group

class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "username"]

    groups = forms.ModelChoiceField(queryset=Group.objects.all(), initial=1, widget=forms.Select(attrs={'class': 'form-select my-2'}))
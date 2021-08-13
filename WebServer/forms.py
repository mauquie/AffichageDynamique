from django import forms
from ApiServer import models
from django.contrib.auth.models import Group

class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "username"]

    groups = forms.ModelChoiceField(queryset=Group.objects.all(), initial=1, widget=forms.Select(attrs={'class': 'form-select my-2'}))

class changeOwnAccount(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["username", "email", "profile_picture"]

    email = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False)

class changeOthersAccount(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ["username", "first_name", "last_name", "email", "profile_picture"]

    email = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False)

class ArticleForm(forms.ModelForm):
    class Meta: 
        model = models.Article
        fields = ["title", "article", "image", "expiration_date"]

    image = forms.ImageField(required=False)
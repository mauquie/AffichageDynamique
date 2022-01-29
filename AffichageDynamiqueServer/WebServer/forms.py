from django import forms
from ApiServer import models
from django.contrib.auth.models import Group

class UserForm(forms.ModelForm):
    """
    Classe contenant le formulaire pour la création d'un compte
    """
    class Meta:
        model = models.Users
        fields = ["first_name", "last_name", "username"]

    groups = forms.ModelChoiceField(queryset=Group.objects.all(), initial=1, widget=forms.Select(attrs={'class': 'form-select my-2'}))

class changeOwnAccount(forms.ModelForm):
    """
    Classe contenant le formulaire pour la modification du compte de l'user lui
    même 
    """
    class Meta:
        model = models.Users
        fields = ["username", "email", "profile_picture", "first_name", "last_name"]

    email = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False)

class changeOthersAccount(forms.ModelForm):
    """
    Classe contenant le formulaire pour la modification d'un compte autre que 
    celui de l'user 
    """
    class Meta:
        model = models.Users
        fields = ["username", "first_name", "last_name", "email", "profile_picture", "groups"]

    email = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False)

class ArticleForm(forms.ModelForm):
    """
    Classe contenant le formulaire pour la création/modification d'un article
    """
    class Meta: 
        model = models.Articles
        fields = ["title", "content", "image", "date_end", "is_shown"]

    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "form-control", "id": "imageInput", "hidden": ""}))

class InformationForm(forms.ModelForm):
    """
    Classe contenant le formulaire pour la création/modification d'une info
    """
    class Meta:
        model = models.Informations
        fields = ["type", "message", "date_end", "is_shown"]

class ScreenForm(forms.ModelForm):
    """
    Classe contenant le formulaire pour la création/modification d'un écran
    """
    class Meta:
        model = models.Screens
        fields = ["name", "code_name"]

class PageForm(forms.ModelForm):
    """
    Classe contenant le formulaire pour la création/modification d'une page
    """
    class Meta:
        model = models.Pages
        fields = ["description", "filename"]
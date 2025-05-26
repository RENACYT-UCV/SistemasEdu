from django.contrib.auth.models import User,Group
from django.contrib.auth.forms import UserCreationForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Grupo")

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2','group','is_active','is_staff']
		

	def clean_email(self):
		email = self.cleaned_data['email']

		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Este correo electrónico ya está registrado')
		return email
class CustomUserCreationFormExternal(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
		

	def clean_email(self):
		email = self.cleaned_data['email']

		if User.objects.filter(email=email).exists():
			raise forms.ValidationError('Este correo electrónico ya está registrado')
		return email


class CustomUserChangeForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Grupo")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff','group']

    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.instance.username

        if User.objects.exclude(username=username).filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado')
        return email
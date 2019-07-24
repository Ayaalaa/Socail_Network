from django import forms
from django.contrib.auth.models import User
from Home.models import User , Post ,Likes ,Comments ,search

class signup_form(forms.ModelForm):
	username = forms.CharField(max_length=20 , widget = forms.TextInput)
	First_Name = forms.CharField(max_length=20 , widget = forms.TextInput)
	Last_Name = forms.CharField(max_length=20 , widget = forms.TextInput)
	Email = forms.EmailField(widget = forms.EmailInput)
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['username','First_Name','Last_Name','Email','password','confirm_password']

class create_post_form(forms.ModelForm):
	content = forms.CharField(max_length=500 , widget = forms.Textarea(attrs={'autocomplete':'off'}))
	class Meta:
		model = Post
		fields = {'content'}


class create_comment_form(forms.ModelForm):
	comment_content = forms.CharField(max_length=500 , widget = forms.TextInput(attrs={'autocomplete':'off'}))
	class Meta:
		model = Comments
		fields = {'comment_content'}


class search_form(forms.ModelForm):
	content = forms.CharField(max_length=500 , widget = forms.TextInput(attrs={'autocomplete':'off'}))
	class Meta:
		model = search
		fields = {'content'}
	
def clean_username(self):
	user = self.cleaned_data['username']
	try:
		match = User.objects.get(username = user)
	except:
		return self.cleaned_data['username']
	raise forms.ValidationError("username already exist")

def clean_email(self):
	email = self.cleaned_data['email']
	try:
		mt = validate_email(email)
	except:
		return forms.ValidationError("Email is not in correct format")
	return email

def clean_confirm_password(self):
	pas = self.cleaned_data['password']
	cpas = self.cleaned_data['confirm_password']
	MIN_LENGTH = 8
	if pas and caps:
		if pas != caps:
			raise forms.ValidationError("Password and confirm password not matched")
		else :
			if len(pas) < MIN_LENGTH:
				raise forms.ValidationError("Password should have at least %d characters "%MIN_LENGTH)
			if pas.isdigit():
				raise forms.ValidationError("Password should not all numeric")

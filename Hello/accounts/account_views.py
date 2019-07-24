from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import login 
from django.contrib.auth import logout
from django.http import *
from .import forms
from django.contrib.auth.models import User
from Home.models import  Post ,Likes ,Comments 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Home.models import Friend

def SignUp(request):
	if request.method == 'POST':
		form1 = forms.signup_form(request.POST)
		if form1.is_valid():
			# save the user to the db
			username = form1.cleaned_data['username']
			first_Name = form1.cleaned_data ['First_Name']
			last_Name = form1.cleaned_data['Last_Name']
			email = form1.cleaned_data['Email']
			password = form1.cleaned_data ['password']
			#confirm_password = form1.cleaned_data['confirm_password']
			loged_user = User.objects.create_user(username = username,first_name =first_Name,last_name =last_Name, email=email,
				password=password)
			loged_user.save()
			login(request,loged_user)
			messages.success(request,'user Registration successfully')
			Friend.make_friend(request.user,request.user)
			return redirect('/homepage/')

	else:
		form1 = forms.signup_form()
		return render(request,'signup.html',{'form1':form1})


def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(data = request.POST)
		if form.is_valid():
			loged_user = form.get_user()
			login(request,loged_user)
			#log in the user
			if'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				return redirect('/homepage/')

	else:
		form = AuthenticationForm()
	return render(request,'login.html',{'form':form})


def logout_view(request):
	logout(request)
	return redirect('/accounts/login/')



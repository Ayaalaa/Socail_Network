from django.http import HttpResponseRedirect 
from django.shortcuts import render ,redirect
from Home.models import Post
from django.contrib.auth.decorators import login_required
from accounts import forms
from django.contrib.auth.models import User
from django.db.models import Q
from Home.models import User , Post ,Likes ,Comments ,search ,Friend

def search_add(request):
	form_search = forms.search_form(request.POST)
	if form_search.is_valid():
		search_content = search(content=request.POST['content'])
		search_content.save()
		match = User.objects.all().filter(Q(username__icontains = search_content))
	return render(request,"search.html",{'match':match})

@login_required(login_url = "/accounts/login/")
def view_post_Home (request):
	if Friend.objects.all().exists() :
		friend = Friend.objects.get(current_user=request.user)
		friends_list = friend.users.all()

	existing_users = User.objects.exclude(pk=request.user.pk)
	posts_list = Post.objects.all().order_by('-time')
	form_search = forms.search_form()
	form_comment = forms.create_comment_form()
	comment_list=Comments.objects.all()

	if request.method == 'POST':
		form2 = forms.create_post_form(request.POST)
		if form2.is_valid():
			content = form2.cleaned_data['content']
			log_post = form2.save(commit = False)
			log_post.userr = request.user
			log_post.save()
			return redirect('/homepage/')
	else:
		form2 = forms.create_post_form()
		return render(request,'Home.html',{'comment_list':comment_list,'form_comment':form_comment,
			'form_search':form_search,'form2':form2 ,
			'posts_list':posts_list,'existing_users':existing_users,'friends_list':friends_list})

def view_post_Timeline (request):
	if Friend.objects.exists():
		friend = Friend.objects.get(current_user = request.user)
		friends_list = friend.users.exclude(pk=request.user.pk)
	posts_list = Post.objects.all().filter(userr = request.user)
	posts_list = posts_list.order_by('-time')
	form_comment = forms.create_comment_form()
	comment_list=Comments.objects.all()
	if request.method == 'POST':
		form2 = forms.create_post_form(request.POST)
		if form2.is_valid():
			content = form2.cleaned_data['content']
			log_post = form2.save(commit = False)
			log_post.userr = request.user
			log_post.save()
			return redirect('/homepage/TimeLine/')
	else:
		form2 = forms.create_post_form()
		return render(request,'TimeLine.html',{'comment_list':comment_list,'form_comment':form_comment,'form2':form2 ,'posts_list':posts_list ,'zft':request.user ,
			'friends_list':friends_list})


def view_post_Timeline_spec (request ,idd):
	if Friend.objects.exists():
		current_ = User.objects.get(pk = idd)
		friend = Friend.objects.get(current_user = current_)
		friends_list = friend.users.exclude(pk=current_.pk)
	user = User.objects.get(pk = idd)
	posts_list = Post.objects.all().filter(userr = user)
	posts_list = posts_list.order_by('-time')
	form_comment = forms.create_comment_form()
	comment_list=Comments.objects.all()
	context = {
	'posts_list':posts_list,
	'userr':user,
	'comment_list':comment_list,
	'form_comment':form_comment,
	'friends_list':friends_list
	}
	return render(request,"TimeLine.html",context)

def change_friend(request , operation , idd):
	new_friend = User.objects.get(pk = idd)
	if operation == 'add':
		Friend.make_friend(request.user , new_friend)
		return redirect('/homepage/')
	elif operation == 'remove':
		Friend.lose_friend(request.user , new_friend)
		return redirect('/homepage/TimeLine/')


def createComment (request,idd):
	if request.method == 'POST':
		form_comment = forms.create_comment_form(request.POST)
		thispost=Post.objects.get(pk= idd)
		thispost.comment=thispost.comment+1
		thispost.save()
		if form_comment.is_valid():
			comment_content =Comments(comment_content = request.POST['comment_content'], userr = request.user,postt=Post.objects.get(pk = idd))
			comment_content.save()
			return redirect('/homepage/')
	else:
		form_comment = forms.create_comment_form()
	return render(request,'Home.html',{'form_comment':form_comment})

def createComment_timeline (request,idd):
	if request.method == 'POST':
		form_comment = forms.create_comment_form(request.POST)
		thispost=Post.objects.get(pk= idd)
		thispost.comment=thispost.comment+1
		thispost.save()
		if form_comment.is_valid():
			comment_content =Comments(comment_content = request.POST['comment_content'], userr = request.user,postt=Post.objects.get(pk = idd))
			comment_content.save()
			if thispost.userr.pk == request.user.pk :
				return redirect('/homepage/TimeLine/')
			else :
				return redirect('/homepage/TimeLine/%s/'%(thispost.userr.pk))
			#return HttpResponseRedirect("") 
	else:
		form_comment = forms.create_comment_form()
	return render(request,'TimeLine.html',{'form_comment':form_comment})

def creatlike (requset,idd):
	thispost = Post.objects.get(pk= idd)
	user = requset.user
	like = Likes.objects.all()
	for li in like:
		if li.userr == user:
			if li.postt == thispost:
				return redirect('/homepage/')
	else:
		thispost.like = thispost.like +1
		thispost.save()
		Like = Likes(userr = requset.user , postt = thispost)
		Like.save()
		return redirect('/homepage/')

def creatlike_timeline (requset,idd):
	thispost = Post.objects.get(pk= idd)
	user = requset.user
	like = Likes.objects.all()
	for li in like:
		if li.userr == user:
			if li.postt == thispost:
				if thispost.userr.pk == requset.user.pk :
					return redirect('/homepage/TimeLine/')
				else :
					return redirect('/homepage/TimeLine/%s/'%(thispost.userr.pk))
	else:
			thispost.like = thispost.like +1
			thispost.save()
			Like = Likes(userr = requset.user , postt = thispost)
			Like.save()
			if thispost.userr.pk == requset.user.pk :
				return redirect('/homepage/TimeLine/')
			else :
				return redirect('/homepage/TimeLine/%s/'%(thispost.userr.pk))
	




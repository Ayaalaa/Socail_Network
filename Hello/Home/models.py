from django.db import models
from django.contrib.auth.models import User

class search (models.Model):
	content = models.CharField(max_length = 500 ,blank = False ,null= True)
	def __str__(self):
		return self.content

class Comments (models.Model):
	comment_content = models.CharField(max_length = 500 ,blank = False ,null= True)
	userr = models.ForeignKey(User, on_delete = models.CASCADE , blank = True)
	postt = models.ForeignKey('Post', on_delete = models.CASCADE , blank = True)
	def __str__(self):
		return self.comment_content

class Likes(models.Model):
	userr = models.ForeignKey(User, on_delete = models.CASCADE , blank = True)
	postt = models.ForeignKey('Post', on_delete = models.CASCADE , blank = True)

class Post(models.Model):
	content = models.CharField(max_length = 500 ,blank = False ,null= True)
	userr = models.ForeignKey(User, on_delete = models.CASCADE , blank = True)
	like = models.PositiveIntegerField(default= 0)
	comment = models.PositiveIntegerField(default=0)
	time = models.DateTimeField(auto_now_add = True , auto_now = False)
	def __str__(self):
		return self.content

class Friend(models.Model):
	users = models.ManyToManyField(User, related_name='friend_set')
	current_user = models.ForeignKey(User, related_name='owner', null = True , on_delete = models.CASCADE)

	@classmethod
	def make_friend(cls, current_user, new_friend):
		friend , created = cls.objects.get_or_create(current_user = current_user)
		friend.users.add(new_friend)

	@classmethod
	def lose_friend(cls, current_user, new_friend):
		friend , created = cls.objects.get_or_create(current_user = current_user)
		friend.users.remove(new_friend)

def Create_Like(self):
	Like_Object = Likes(postt = self, userr = self)
	Like_Object.save()
	return Like_Object.postt.content




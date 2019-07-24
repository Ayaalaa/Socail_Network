from django.contrib import admin
from .models import  User , Post , Comments , Likes ,search , Friend

class PostAdmin(admin.ModelAdmin):
	list_display = ["__str__","time","userr","like","comment"]
	list_filter = ['time']
	search_fields = ['userr']
	class Meta:
		model = Post

class likeAdmin(admin.ModelAdmin):
	list_display = ["userr","postt"]
	class Meta:
		model = Likes

class CommentAdmin(admin.ModelAdmin):
	list_display = ["__str__","userr","postt"]
	class Meta:
		model = Comments

admin.site.register(Post , PostAdmin)
admin.site.register(Likes , likeAdmin )
admin.site.register(Comments , CommentAdmin)
admin.site.register(search)
admin.site.register(Friend)



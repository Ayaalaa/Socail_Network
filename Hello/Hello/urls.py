from django.contrib import admin
from django.urls import path , include
from accounts import  account_views 
from Home import  Home_views
from .import view
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

extra_patterns =[
    path('signup/',account_views.SignUp , name = "signup"),
    path('login/',account_views.login_view , name = "login"),
    path('logout/',account_views.logout_view , name = "logout"),
]

urlpatterns =[
    path('admin/', admin.site.urls),
    path('homepage/', view.view_post_Home),
    path('homepage/search/', view.search_add),
    path('homepage/TimeLine/', view.view_post_Timeline),
    path('homepage/TimeLine/<int:idd>/', view.view_post_Timeline_spec ),
    path('homepage/<slug:operation>/<int:idd>/', view.change_friend , name = "make_friend"),
    path('homepage/<int:idd>/',view.createComment),
    path('TimeLine/<int:idd>/', view.createComment_timeline),
    path('this/<int:idd>/',view.creatlike),
    path('thiss/<int:idd>/',view.creatlike_timeline),
    path('accounts/',include(extra_patterns))
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
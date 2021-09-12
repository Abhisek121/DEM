from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #re_path(r'^login/$', auth_views.LoginView.as_view(), name='login'),
	#re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('attendance.urls')),
	path('attendance/', include('attendance.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='attendance/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='attendance/logout.html'), name='logout'),
]

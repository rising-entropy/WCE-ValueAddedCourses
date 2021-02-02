"""WCECourses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Teknath-jha added this 
admin.site.site_header = "WCE Value Added Courses Admin"
admin.site.site_title = "WCE Value Added Courses Admin Portal"
admin.site.index_title = "Welcome to WCE Value Added Courses Researcher Portal"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landingPage.as_view(), name="landingPage"),
    path('register/', views.register.as_view(), name="register"),
    path('login/', views.Login.as_view(), name="Login"),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.profile.as_view(), name="profile"),
    path('changePassword/', views.changePassword.as_view(), name="changePassword"),
    path('pythonForEverybody/', views.pythonForEverybody.as_view(), name="pythonForEverybody"),
    path('about/',views.about.as_view(),name="about"),
    path('deepLearning/',views.deepLearning.as_view(),name="deepLearning"),
    path('enrollPython/',views.enrollPython.as_view(),name="enrollPython"),
    path('enrollDL/',views.enrollDL.as_view(),name="enrollDL"),
    path('facultyHome/', views.facultyLandingPage.as_view(), name="facultyLandingPage"),
    path('enrollmentForPython/', views.enrollListPython.as_view(), name="enrollListPython"),
    path('enrollmentForDL/', views.enrollListDL.as_view(), name="enrollListDL"),
   path('paymentDetailsPy/<str:stud>/', views.paymentDetailsPy.as_view(), name="paymentDetailsPy"),
   path('paymentDetailsDL/<str:stud>/', views.paymentDetailsDL.as_view(), name="paymentDetailsDL"),
  
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

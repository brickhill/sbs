from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('', views.home, name="home"),
    path('page/<str:pk>/', views.showPage, name="showpage"),
    path('blog/', views.showBlog, name="blog"),
    path('ckeditor/', include('ckeditor_uploader.urls'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
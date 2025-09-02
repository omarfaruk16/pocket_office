from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("student.urls")),
    path('', include("teacher.urls")),
    path('', include("course.urls")),
    path('', include("todo.urls")),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


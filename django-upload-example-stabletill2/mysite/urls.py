from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from mysite.core import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    # here the first argument is shown in browser when you click on Object and Scene Detection in nav_bar
    # when you click on any option on nav_bar then http://127.0.0.1:8000/option(mean which you click on nav bar is displayed)
    path('object-and-scene-detection/', views.object_and_scene_Detection, name='ons'),
    path('image-moderation/', views.image_moderation, name='im'),
    path('books/upload/', views.upload_book, name='upload_book'),
    path('books/<int:pk>/', views.delete_book, name='delete_book'),
    path('class/books/', views.BookListView.as_view(), name='class_book_list'),
    path('class/books/upload/', views.UploadBookView.as_view(), name='class_upload_book'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

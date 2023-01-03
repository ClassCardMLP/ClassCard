from django.urls import path
from . import views

app_name = 'magazine'

urlpatterns = [
    path('index/',views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('create/', views.create_, name='create'),
    path('<int:pk>/update/', views.update_, name='update'),
    path('<int:pk>/delete/', views.delete_magazine, name='delete_magazine'),
    path('<int:pk>/mzcomment_create/', views.mzcomment_create, name='mzcomment_create'),
    path('<int:mz_pk>/mzcomment_delete/<int:mzcm_pk>/', views.mzcomment_delete, name='mzcomment_delete'),
    path('<int:mz_pk>/mzcomment_update/<int:mzcm_pk>/', views.mzcomment_update, name="mzcomment_update"),
    path('<int:mz_pk>/reply_create/<int:mzcm_pk>/', views.reply_create, name='reply_create'),
    path('<int:mz_pk>/<int:mzcm_pk>/reply_delete/<int:mzreply_pk>/', views.reply_delete, name='reply_delete'),
    path('<int:mz_pk>/mzbookmark/',views.magazine_bookmark, name='mzbookmark'),
]
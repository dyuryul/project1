from django.urls import path

from . import views

app_name='reviews'
urlpatterns = [
    path('', views.index, name= 'index'),
    path('<int:review_id>/', views.detail, name='detail'),
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('<int:review_id>/edit/', views.edit, name='edit'),
    path('<int:review_id>/update/', views.update, name='update'),
    path('<int:review_id>/delete/', views.delete, name='delete'),
    path('<int:review_id>/like/', views.like, name='like'),
    #테스트
    path('youtube/', views.youtube, name='youtube'),
]
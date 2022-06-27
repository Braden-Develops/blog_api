from django.urls import path
from blog import views

urlpatterns = [
    path('posts/', views.BlogPosts.as_view())
]

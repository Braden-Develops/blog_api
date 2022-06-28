from django.urls import path
from blog import views

urlpatterns = [
    path('posts/', views.BlogPosts.as_view()),
    path('register/', views.RegisterUser.as_view()),
    path('login/', views.Login.as_view()),
    path('user/', views.UserView.as_view()),
    path('logout/', views.Logout.as_view()),
]

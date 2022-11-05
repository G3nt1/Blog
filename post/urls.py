from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostHome, name='home'),
    path("deatils/<str:slug>", views.Details, name="details"),
    path("new_post", views.CreatePost, name='new_post'),
    path('login/', views.UserLogin, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path("register/", views.UserRegister, name="register"),
    path("profile-update/", views.UpdateProfile, name='profile-update'),
    path("search/", views.Query, name='search'),
    path("profile<str:pk>/", views.UserProfile, name='profile'),
    path("like/", views.Like, name='like_post'),

]

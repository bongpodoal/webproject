from django.urls import path
from . import views
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path("new/", views.PostCreate.as_view(), name="post_create"),
    path("<int:pk>", views.post_detail, name="post_detail"),
    path("<int:pk>/edit/", views.post_edit, name="post_edit"),
    path("<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("signup/", views.signup, name="signup"),
    path("commtents/<int:pk>/edit", views.comment_edit, name="comment_edit"),
    path("commtents/<int:pk>/delete", views.comment_delete, name="comment_delete"),
    path("profiles/edit/", views.profile_edit, name="profile_edit"),
    path("profiles/<str:username>/", views.profile_detail, name="profile_detail"),
    path(
        "<int:pk>/vote/<str:direction>/",
        views.post_vote,
        name="post_vote",
    ),
    path(
        "comments/<int:pk>/vote/<str:direction>/",
        views.comment_vote,
        name="comment_vote",
    ),

]
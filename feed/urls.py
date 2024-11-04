from django.urls import path

from .views import HomePage, PostDetailView, CreateNewPost, DeletePostView
app_name = "feed"

urlpatterns = [
    path("", HomePage.as_view(), name="index"),
    path("<int:pk>/", PostDetailView.as_view(), name='detail'),
    path("new/", CreateNewPost.as_view(), name='new_post'),
    path('post/<int:post_id>/delete/', DeletePostView.as_view(), name='delete_post'),
]

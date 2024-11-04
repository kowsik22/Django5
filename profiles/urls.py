from django.urls import path
from . import views


app_name= "profiles"

urlpatterns = [
    path("<str:username>/", views.ProfileDetailView.as_view(), name='detail'),
    path("<str:username>/follow/", views.FollowView.as_view(), name='follow'),
    path("<str:username>/upload-image/", views.ProfileImageUploadView.as_view(), name='upload_image'),  # Ensure this line is correct
]
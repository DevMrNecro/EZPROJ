from django.urls import path, include
from .views import FileUploadView, FileDownloadView, FileListView, UserLoginAPIView, UserSignupAPIView

urlpatterns = [
    path('signup/', UserSignupAPIView.as_view(), name='user-signup'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('download/<int:pk>/', FileDownloadView.as_view(), name='file-download'),
    path('files/', FileListView.as_view(), name='file-list'),
]
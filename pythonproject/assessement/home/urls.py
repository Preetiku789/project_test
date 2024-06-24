from django.urls import path
from.views import login_view, signup_view, email_verify_view, file_upload_view, file_list_view, file_download_view

urlpatterns = [
    path('login/', login_view),
    path('signup/', signup_view),
    path('email_verify/<str:token>/', email_verify_view),
    path('file_upload/', file_upload_view),
    path('file_list/', file_list_view),
    path('file_download/<int:pk>/', file_download_view),
]
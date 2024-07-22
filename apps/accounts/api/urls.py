from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('user/register/', views.RegisterAPI.as_view()),
    path('user/update/', views.UpdateUserAPI.as_view()),
    path('user/profile/', views.UserProfileAPI.as_view()),
    path('user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('staff/add/', views.AddNewStaffMemberAPI.as_view()),
    path('staff/list/', views.GetStaffMembersDetailAPI.as_view()),
    path('staff/update/', views.UpdateStaffMemberDetailsAPI.as_view()),

]

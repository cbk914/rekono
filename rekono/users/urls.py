from django.urls import include, path
from rest_framework.routers import SimpleRouter
from users.views import (ChangeUserPasswordView, ChangeUserRoleView,
                         CreateUserView, EnableUserView, ResetPasswordView,
                         UserViewSet, RequestResetPasswordView)
from rest_framework.authtoken import views

router = SimpleRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('api-token/', views.obtain_auth_token),
    path('users/<int:pk>/create/', CreateUserView.as_view()),
    path('users/<int:pk>/role/', ChangeUserRoleView.as_view()),
    path('users/<int:pk>/enable/', EnableUserView.as_view()),
    path('users/change-password/', ChangeUserPasswordView.as_view()),
    path('users/reset-password/', RequestResetPasswordView.as_view()),
    path('users/reset-password/', ResetPasswordView.as_view()),
    path('', include(router.urls)),
]
from django.urls import path
from rest_framework_nested import routers
from .views import (
    LoginView,
    RegisterCustomerView
)
from . import views


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("registration/", RegisterCustomerView.as_view(), name="register"),
    # path("event_team_register/", RegisterEventTeamView.as_view(), name="register"),
    # path("userslist/", ListUsersView.as_view(), name="list_users"),
    # path(
    #     "event_management_users/",
    #     EventManagementUsersView.as_view(),
    #     name="event_management_users",
    # ),
]

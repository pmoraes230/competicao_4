from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("home/", views.home, name="home"),
    path("register_event/", views.register_event, name="register_event"),
    path("update_event/<int:id_event>", views.update_event, name="update_event"),
    path("delete_event/<int:id_event>", views.delete_event, name="delete_event"),
    path("details_event/<int:id_event>/", views.deteils_event, name="details_event"),
    path("register_setor", views.register_setor, name="register_setor"),
    path("buy_ticket/<int:id_event>/", views.buy_ticket, name="buy_ticket"),
    path("list_setor/", views.list_setor, name="list_setor"),
    path("update_setor/<int:id_setor>/", views.update_setor, name="update_setor"),
    path("delete_setor/<int:id_setor>/", views.delete_setor, name="delete_setor"),
    path("list_user/", views.list_user, name="list_user"),
    path("register_user/", views.register_user, name="register_user"),
    path("update_user/<int:id_user>/", views.update_user, name="update_user"),
    path("delete_user/<int:id_user>", views.delete_user, name="delete_user"),
    path("list_client", views.list_client, name="list_client"),
    path("register_client", views.register_client, name="register_client"),
    path("update_client/<int:id_client>/", views.update_client, name="update_client"),
    path("delete_client/<int:id_client>", views.delete_client, name="delete_client")
]

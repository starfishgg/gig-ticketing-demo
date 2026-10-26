from django.urls import path


from . import views

app_name = "gigs"

urlpatterns = [
    path("", views.gig_list, name="gig_list"),
]

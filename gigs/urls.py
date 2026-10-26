from django.urls import path


from . import views

app_name = "gigs"

urlpatterns = [
    path("", views.gig_list, name="gig_list"),
    path("<int:pk>/", views.gig_detail, name="gig_detail"),
    
    path(
        "booking/<uuid:reference>/",
        views.booking_confirmation,
        name="booking_confirmation",
    ),
    path(
        "<int:pk>/book<int:ticket_type_id>/",
        views.book_ticket,
        name="book_ticket",
    ),
]

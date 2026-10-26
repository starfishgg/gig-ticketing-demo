from django.contrib import admin

from .models import Gig, TicketType, Venue




@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "city")
    search_fields = ("name", "city")


@admin.register(Gig)
class GigAdmin(admin.ModelAdmin):
    list_display = ("title", "venue", "starts_at", "published")
    list_filter = ("published", "venue")
    search_fields = ("title", "venue__name")
    list_select_related = ("venue",)


@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "gig", "price", "quantity_available")
    list_select_related = ("gig",)
    search_fields = ("name", "gig__title")
from django.contrib import admin

from .models import Booking, BookingItem, Gig, TicketType, Venue




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




class BookingItemInline(admin.TabularInline):
    model = BookingItem
    extra = 0
    readonly_fields = ("line_total",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "customer_name",
        "customer_email",
        "status",
        "total_price",
        "created_at",
    )
    list_filter = ("status", "created_at")
    search_fields = (
        "reference",
        "customer_name",
        "customer_email",
    )
    readonly_fields = ("reference", "created_at", "total_price")
    inlines = [BookingItemInline]

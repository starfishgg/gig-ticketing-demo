from django.db import transaction
from django.db.models import Min, F
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Booking, BookingItem, Gig, TicketType
from .forms import TicketBookingForm





def gig_list(request):
    """Display published gigs with their starting ticket prices."""

    gigs =(
        Gig.objects
        .filter(published=True)
        .select_related("venue")
        .annotate(starting_price=Min("ticket_types__price"))
    )

    return render(request, "gigs/gig_list.html", {"gigs": gigs})


def gig_detail(request, pk):
    """Display a published gig and its ticket types."""

    gig = get_object_or_404(
        Gig.objects
        .filter(published=True)
        .select_related("venue")
        .prefetch_related("ticket_types"),
        pk=pk,
    )

    return render(request, "gigs/gig_detail.html", {"gig": gig})


def book_ticket(request, pk, ticket_type_id):
    """Create a pending booking for a published gig."""

    gig = get_object_or_404(
        Gig.objects.filter(published=True).select_related("venue"),
        pk=pk,
    )
    ticket_type = get_object_or_404(
        TicketType,
        pk=ticket_type_id,
        gig=gig,
    )

    if request.method == "POST":
        form = TicketBookingForm(request.POST)

        if form.is_valid():
            quantity = form.cleaned_data["quantity"]

            with transaction.atomic():
                # Only reduce stock if enough tickets remain.
                updated = TicketType.objects.filter(
                    pk=ticket_type.pk,
                    gig=gig,
                    quantity_available__gte=quantity,
                ).update(
                    quantity_available=F("quantity_available") - quantity
                )

                if updated:
                    # Read the price after successfully reserving stock.
                    ticket_type.refresh_from_db()

                    total_price = ticket_type.price * quantity

                    booking = Booking.objects.create(
                        customer_name=form.cleaned_data["customer_name"],
                        customer_email=form.cleaned_data["customer_email"],
                        total_price=total_price,
                        status=Booking.Status.PENDING,
                    )

                    BookingItem.objects.create(
                        booking=booking,
                        ticket_type=ticket_type,
                        quantity=quantity,
                        unit_price=ticket_type.price,
                    )

                    return redirect(
                        "gigs:booking_confirmation",
                        reference=booking.reference,
                    )

            form.add_error(
                None,
                "There aren't enough tickets available for that quantity. "
                "Please try a smaller number.",
            )

    else:
        form = TicketBookingForm()

    return render(
        request,
        "gigs/booking_form.html",
        {
            "gig": gig,
            "ticket_type": ticket_type,
            "form": form,
        },
    )


def booking_confirmation(request, reference):
    """Display the result of a subnitted booking."""

    booking = get_object_or_404(
        Booking.objects.prefetch_related("items__ticket_type__gig"),
        reference=reference,
    )

    return render(
        request,
        "gigs/booking_confirmation.html",
        {"booking": booking},
    )




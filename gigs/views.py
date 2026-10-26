from django.db.models import Min
from django.shortcuts import render

from .models import Gig




def gig_list(request):
    """Display published gigs with their starting ticket prices."""

    gigs =(
        Gig.objects
        .filter(published=True)
        .select_related("venue")
        .annotate(starting_price=Min("ticket_types__price"))
    )

    return render(request, "gigs/gig_list.html", {"gigs": gigs})

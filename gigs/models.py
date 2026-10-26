import uuid

from django.core.validators import MinValueValidator
from django.conf import settings
from django.db import models




class Venue(models.Model):
    """A physical location where gigs take place."""

    name = models.CharField(max_length=150)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.city}"




class Gig(models.Model):
    """A live music event at a venue."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    venue = models.ForeignKey(
        Venue,
        on_delete=models.PROTECT,
        related_name="gigs",
    )
    starts_at = models.DateTimeField()
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["starts_at"]

    def __str__(self):
        return f"{self.title} - {self.starts_at:%d %b %Y}"




class TicketType(models.Model):
    """A ticket category and its price and available quantity."""

    gig = models.ForeignKey(
        Gig,
        on_delete=models.CASCADE,
        related_name="ticket_types",
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    quantity_available = models.PositiveBigIntegerField(
        validators=[MinValueValidator(1)],
    )

    class Meta:
        ordering = ["price"]
        constraints = [
            models.UniqueConstraint(
                fields=["gig", "name"],
                name="unique_ticket_type_per_gig",
            ),
        ]

    def __str__(self):
        return f"{self.gig.title} - {self.name}"




class Booking(models.Model):
    """A customer's booking for one or more ticket types."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    reference = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    customer_name = models.CharField(max_length=150)
    customer_email = models.EmailField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference} - {self.customer_name}"




class BookingItem(models.Model):
    """A ticket type and quantity included in a booking."""

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="items",
    )

    ticket_type = models.ForeignKey(
        TicketType,
        on_delete=models.PROTECT,
        related_name="booking_items",
    )

    quantity=models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )

    unit_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["booking", "ticket_type"],
                name="unique_ticket_typeper_booking",
            ),
        ]

    def __str__(self):
        return f"{self.quantity} * {self.ticket_type.name}"

    @property
    def line_total(self):
        return self.quantity * self.unit_price
    
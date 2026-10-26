from django.core.validators import MinValueValidator
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
    
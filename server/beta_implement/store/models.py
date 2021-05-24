from activity import models as activity_models
from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify

from activity import models as activity_models
from payments import models as payment_models

# Create your models here.


class MasIntentionDescription(models.Model):
    class IntnetionType(models.IntegerChoices):
        Thanksgiving = 0
        Late = 1
        other = 2

    type = models.PositiveSmallIntegerField(choices=IntnetionType.choices, default=0)
    text = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class Massintentions(MasIntentionDescription):
    amount = models.DecimalField(default=100.00, decimal_places=2, max_digits=10)
    activity = models.ForeignKey(activity_models.Activity, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        payment_models.Transaction, on_delete=models.PROTECT, null=True, blank=True
    )
    by = models.TextField()


# Abstract true for all the models below


class Category(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    slug = models.SlugField(editable=False)
    category = models.ManyToManyField(Category, null=True, blank=False)

    def __str__(self):
        return self.title

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title + self.id)
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse("core:product", kwargs={
    #         'slug': self.slug
    #     })

    # def get_add_to_cart_url(self):
    #     return reverse("core:add-to-cart", kwargs={
    #         'slug': self.slug
    #     })

    # def get_remove_from_cart_url(self):
    #     return reverse("core:remove-from-cart", kwargs={
    #         'slug': self.slug
    #     })
    class Meta:
        abstract = True


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()

    class Meta:
        abstract = True


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code

    class Meta:
        abstract = True



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    payment = models.ForeignKey(
        payment_models.Transaction, on_delete=models.SET_NULL, blank=True, null=True
    )
    coupon = models.ForeignKey(
        "Coupon", on_delete=models.SET_NULL, blank=True, null=True
    )
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    """
    1. Item added to cart
    3. Payment
    (Preprocessing, processing, packaging etc.)
    4. Being delivered
    5. Received
    6. Refunds
    """

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total -= self.coupon.amount
        return total

    class Meta:
        abstract = True

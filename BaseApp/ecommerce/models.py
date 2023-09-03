from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)


class store(models.Model):
    uid = models.UUIDField(default = uuid.uuid4,editable = False)
    name = models.CharField(blank=False, null=False, max_length=50)
    address = models.CharField(blank=False, null=False, max_length=50)
    phone = models.CharField(blank=False, null=False, max_length=13)
    email = models.CharField(blank=False, null=False, max_length=50)
    about = models.TextField(blank=False, null=False, max_length=500)
    facebook = models.CharField(blank=False, null=False, max_length=50)
    instagram = models.CharField(blank=False, null=False, max_length=50)
    twitter = models.CharField(blank=False, null=False, max_length=50)
    youtube = models.CharField(blank=False, null=False, max_length=50)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + "       " + self.email + "       " + self.phone


class category(models.Model):
    uid = models.UUIDField(default = uuid.uuid4,editable = False)
    name = models.CharField(blank=False, null=False, max_length=30)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class product(models.Model):
    uid = models.UUIDField(default = uuid.uuid4,editable = False)
    name = models.CharField(blank=False, null=False, max_length=30)
    description = models.TextField(blank=True, null=True, max_length=1000)
    category = models.ForeignKey("category", on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    weight = models.FloatField(null=True, blank=True)
    top_product = models.BooleanField(null=True, blank=True)
    img = models.ImageField(upload_to='product_img/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def getPrice(self):
        return "variant.objects.filter(product=self.id).order_by('-id')[0].price"


    def save(self, *args, **kwargs):
        # Check if the price field has been updated
        if self.pk:
            instance = self.__class__.objects.get(id=self.pk)
            PriceHistory.objects.create(product=instance, price=self.price)
            # original_product = product.objects.get(pk=self.pk)
            # PriceHistory.objects.create(product=self, price=self.price)
        else:
            PriceHistory.objects.create(product=self, price=self.price)
            # original_product = product.objects.all().order_by('-id').first()
            # PriceHistory.objects.create(product=original_product, price=original_product.price)



            # if original_product.price != self.price:
            #     # Update the latest PriceHistory record with the new price
            #     chk= PriceHistory.objects.filter(product=self).exists()
            #     if chk:
            #         latest_price_history = PriceHistory.objects.filter(product=self).order_by('-id')[0]
            #         latest_price_history.price = original_product.price
            #         latest_price_history.save()
            #     else:
            #         PriceHistory.objects.create(product=self, price=original_product.price)


        super().save(*args, **kwargs)



class PriceHistory(models.Model):
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.price} ({self.date_modified})"


class productImg(models.Model):
    uid = models.UUIDField(default = uuid.uuid4,editable = False)
    product = models.ForeignKey("product", on_delete=models.CASCADE)
    img = models.ImageField(upload_to='productImg_img/')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)


class variant(models.Model):
    uid = models.UUIDField(default = uuid.uuid4,editable = False)
    product = models.ForeignKey(product, on_delete=models.CASCADE)
    price = models.FloatField(blank=False, null=False, default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.product.name + "\t" + str(self.price) + " $"


class blog(models.Model):
    uid = models.UUIDField(default = uuid.uuid4,editable = False)
    title = models.CharField(blank=False, null=False, max_length=50)
    desciption = models.TextField(blank=True, null=True, max_length=1000)
    img = models.ImageField(upload_to='blog_img/')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class inventory(models.Model):
    uid = models.UUIDField(default = uuid.uuid4,editable = False)
    variantref = models.ForeignKey("variant", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

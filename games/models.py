from django.db import models
from django.contrib.auth.models import User


class Developer(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Publiher(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Image(models.Model):
    image_path = models.ImageField(upload_to='images')

    def __str__(self):
        return self.image_path.name

class Game(models.Model):
    name = models.CharField(max_length=100, default="DefaultName")
    title = models.TextField(null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    release_date = models.DateField()
    main_image = models.ImageField(upload_to='images', default='images/default_image.jpg')
    genres = models.ManyToManyField(Genre,related_name='games')
    images = models.ManyToManyField(Image,related_name='games')

    publisher_id = models.ForeignKey(Publiher,on_delete=models.CASCADE)
    developer_id = models.ForeignKey(Developer,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class MinSystemRequirements(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    os = models.CharField(max_length=100)
    processor = models.CharField(max_length=100)
    memory = models.CharField(max_length=100)
    graphics = models.CharField(max_length=100)
    directx = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)

class RecommendedSystemRequirements(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    os = models.CharField(max_length=100)
    processor = models.CharField(max_length=100)
    memory = models.CharField(max_length=100)
    graphics = models.CharField(max_length=100)
    directx = models.CharField(max_length=100)
    storage = models.CharField(max_length=100)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
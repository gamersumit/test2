from django.db import models

# Create your models here.


def upload_to(instance, filename):
    return '{filename}'.format(filename=filename)


CATEGORIES = (('Breakfast', 'Breakfast'),
              ('Lunch', 'Lunch'), ('Shakes', 'Shakes'))


class Menu(models.Model):
    category = models.CharField(max_length=9, choices=CATEGORIES)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to=upload_to, default='default.png')

    def __str___(self):
        return f'{self.title}'

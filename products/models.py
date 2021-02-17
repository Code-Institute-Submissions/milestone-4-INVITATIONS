from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from colorfield.fields import ColorField


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    display_name = models.CharField(max_length=254, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        'Category', null=True, blank=True,
        on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    description = models.TextField()
    customizable = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    featured = models.BooleanField(default=False)
    date_created = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    raw_image = models.ImageField(blank=True)
    view_image = models.ImageField(blank=True)
    customize_image = models.ImageField(blank=True)

    def __str__(self):
        return self.name


class CustomDetailLine(models.Model):
    FONT_CHOICES = [
        ("'Arial', sans-serif", "'Arial', sans-serif"),
        ("'Clicker Script', cursive", "'Clicker Script', cursive"),
        ("'Londrina Solid', cursive", "'Londrina Solid', cursive"),
    ]

    FONT_SIZE_CHOICES = [
        ('72', '72'),
        ('96', '96'),
        ('32', '32'),
        ('160', '160'),
        ('192', '192'),
        ('240', '240'),
        ('288', '288'),
        ('384', '384'),
    ]

    STROKE_WIDTH_CHOICES = [
        ('0px', 'no stroke'),
        ('1px', '1px'),
        ('2px', '2px'),
        ('4px', '4px'),
    ]

    product = models.ForeignKey(Product, null=False,
                                blank=False, on_delete=models.CASCADE,
                                related_name='customlines')
    name = models.CharField(max_length=12, null=False, blank=False)
    text = models.CharField(max_length=60, null=False, blank=False)
    y_pos = models.IntegerField(validators=[MaxValueValidator(2320),
                                            MinValueValidator(25)],
                                null=False, blank=False)
    font = models.CharField(max_length=60,
                            choices=FONT_CHOICES,
                            default="'Clicker Script', cursive",)
    raw_size = models.CharField(max_length=3,
                                choices=FONT_SIZE_CHOICES,
                                default='160',)
    color = ColorField(default='#000000')
    stroke_fill = ColorField(default='#000000')
    stroke_width = models.CharField(max_length=3,
                                    choices=STROKE_WIDTH_CHOICES,
                                    default='0px',)

    def __str__(self):
        return f'{self.name} for product {self.product.name}'

from django.db import models
from django.db import models
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
from barcode import EAN13
from PIL import Image, ImageDraw
import os
import datetime as dt

# Create your models here.

class Category(models.Model):
    
    name=models.CharField(max_length=255)

    def __str__(self):
        return self.name
    @property
    def products_count(self):
        return self.product_set.count()
class School(models.Model):
    
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    barcode = models.ImageField(upload_to='media/barcodes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    prod_id= models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product_name}'
    @classmethod
    def get_total_product_count(cls):
        return cls.objects.count()


    def save(self, *args, **kwargs):
        if not self.barcode:  # Only generate a barcode if it's not already set
            # Get the count of products for the current category and all products
            category_product_count = Product.objects.filter(category=self.category).count()
            all_product_count = Product.objects.all().count()
            timestamp = dt.datetime.now()
            # Increment the counts by 1 to get the next value
            category_product_count += 1
            all_product_count += 1

            # Generate the barcode code using school and category counts and the product count
            code = f'{self.school.id:01}{self.category.id:01}{category_product_count:05}{all_product_count:06}'
            ean = EAN13(code, writer=ImageWriter())

            buffer = BytesIO()
            ean_img = ean.render()  # Render the barcode as an Image

            # Get the directory path where the barcode image should be saved
            save_directory = os.path.join('media', 'barcodes', self.school.name, self.category.name, self.product_name, )

            # Ensure the directory exists; create it if not
            os.makedirs(save_directory, exist_ok=True)

            barcode_image_path = os.path.join(save_directory, f'{timestamp}{self.product_name}_{all_product_count}_{category_product_count}.png')
            ean_img.save(barcode_image_path, format='PNG')
            

            # Set the saved barcode image path for the model instance
            self.barcode.name = os.path.relpath(barcode_image_path, 'media')
            # for i in range(self.nt):  # Generate multiple barcodes based on num_barcodes
            #     barcode_image_path = os.path.join(save_directory, f'{self.product_name}_{all_product_count}_{category_product_count}_{i+1}.png')
            #     ean_img = ean.render()  # Render the barcode as an Image
            #     ean_img.save(barcode_image_path, format='PNG')  # Save the Image to the buffer as PNG bytes


            buffer.close()  # Close the buffer after use

        super().save(*args, **kwargs)  # Call the superclass's save() method to save the instance

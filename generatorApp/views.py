from django.shortcuts import render, redirect
import os
from django.http import HttpResponse
from django.views.generic import View
import zipfile
from io import BytesIO
import shutil
from django.conf import settings
from .forms import (
    ProductForm
)
from .models import (
    Product
)
# Create your views here.
def home(request):
    return HttpResponse('Hello')
    

from django.shortcuts import render, redirect
from .forms import ProductForm

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            copies = form.cleaned_data['copies']  # Get the number of copies from the form
            product_data = form.cleaned_data.copy()  # Make a copy of the form data

            # Remove the 'copies' field from the data to avoid saving it as part of the Product instance
            del product_data['copies']
            # Generate the barcodes and store the file paths in a list
            
            # Generate multiple copies of the Product instance
            for _ in range(copies):
                product = form.Meta.model(**product_data)  # Create the Product instance
                product.save()  # Save the instance and generate barcode (assuming the barcode generation is in the save() method)
            return redirect('product_list')
    else:
        form = ProductForm()

    return render(request, 'product_form.html', {'form': form})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
    



def download_barcode(request, barcode_path):
    generated_barcodes = request.POST.getlist('barcode')  # Get the list of selected barcode URLs from the form
    if generated_barcodes:
        # Create a zip file containing all the barcode images
        zip_file_path = os.path.join(settings.MEDIA_ROOT, 'barcodes.zip')
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            for barcode_url in generated_barcodes:
                barcode_path = os.path.join(settings.BASE_DIR, barcode_url[1:])  # Convert the URL to a local file path
                zip_file.write(barcode_path, os.path.relpath(barcode_path, settings.MEDIA_ROOT))

        # Serve the zip file for download
        with open(zip_file_path, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="barcodes.zip"'
            return response
    else:
        return HttpResponse("No barcodes to download.", status=404)



def download_all_barcodes(request):
    generated_barcodes = request.POST.getlist('barcode')  # Get the list of selected barcode URLs from the form
    if generated_barcodes:
        # Create a zip file containing all the barcode images
        zip_file_path = os.path.join(settings.MEDIA_ROOT, 'barcodes.zip')
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            for barcode_url in generated_barcodes:
                barcode_path = os.path.join(settings.BASE_DIR, barcode_url[1:])  # Convert the URL to a local file path
                zip_file.write(barcode_path, os.path.relpath(barcode_path, settings.MEDIA_ROOT))

        # Serve the zip file for download
        with open(zip_file_path, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="barcodes.zip"'
            return response
    else:
        return HttpResponse("No barcodes to download.", status=404)
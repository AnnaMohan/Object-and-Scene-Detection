from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
import binascii
import codecs
import os
from .forms import BookForm
from .models import Book
from django.conf import settings
import csv #import csv library 
import boto3 # importing aws official library boto3
import requests
import base64
import glob

class Home(TemplateView):
    template_name = 'home.html'


def object_and_scene_Detection(request):
    context={}
    list_dic_nc=[] # List of dictionaries containing name and confidence
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        
        if(1):
            with open('credentials.csv','r') as input: # opening credentials.csv file. r represents in readable format
                next(input) #next is a method in csv library which says to skip first line and go to next
                reader=csv.reader(input)
                for line in reader:
                    access_key_id = line[2]
                    secret_access_key=line[3]
                    continue
      

            list_of_files = glob.glob('C:\\Users\\annam\\django-upload-example\\media\\*') # * means all if need specific format then *.csv
            print("INlist between")
            latest_file = max(list_of_files, key=os.path.getctime)
            print(latest_file)
            photo = uploaded_file
            print(type(photo.read()))
            #try:  
            #  img  = Image.open(photo)  
            #   database.docx=img
            #except IOError: 
            #    pass
            #to write into a file.
            # f = open("database.docx", "a")
            # f.write(photo)
            # f.close()
            client = boto3.client('rekognition',aws_access_key_id= access_key_id,aws_secret_access_key= secret_access_key,
            region_name='us-west-2')
            #we need to convert our image into 64 encoded byte
            with open(latest_file, 'rb') as source_image:
                source_bytes=source_image.read()
               
            #source_image= open(uploaded_file,'rb').read() #rb means open in binary read mode
             #   source_bytes=source_image.read() #by using read method i can easily convert my image to bytes.
               # source_bytes = binascii.hexlify(source_image)
            #source_bytes = codecs.encode(source_image, "hex_codec")
            response = client.detect_labels(Image={'Bytes': source_bytes})
            #print(response)
            print(response.get('Labels',''))
            #requests.get(url).json()
            labels=response['Labels']
            for label in labels:
                nc={
                    'name':label['Name'],
                    'confidence':round(label['Confidence'],2)
                    }
                # Name and Confidence Dictionary
                list_dic_nc.append(nc)
                # context is used to send data after processing the request received
            

    return render(request, 'upload.html', { 'list_dic_nc':list_dic_nc })
            


def image_moderation(request):
    context={}
    # list_dic_nc=[] # List of dictionaries containing name and confidence
    # to remove following error we defined list_dict_cnp here
    # local variable 'list_dict_cnp' referenced before assignment
    list_dict_cnp = [] 
    # list_dic_nc=[] # List of dictionaries containing name,confidence and parentName
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
        
        if(1):
            with open('credentials.csv','r') as input: # opening credentials.csv file. r represents in readable format
                next(input) #next is a method in csv library which says to skip first line and go to next
                reader=csv.reader(input)
                for line in reader:
                    access_key_id = line[2]
                    secret_access_key=line[3]
                    continue
      

            list_of_files = glob.glob('C:\\Users\\annam\\django-upload-example\\media\\*') # * means all if need specific format then *.csv
            print("INlist between")
            latest_file = max(list_of_files, key=os.path.getctime)
            print(latest_file)
            photo = uploaded_file
            print(type(photo.read()))
            client = boto3.client('rekognition',aws_access_key_id= access_key_id,aws_secret_access_key= secret_access_key,
            region_name='us-west-2')
            with open(latest_file, 'rb') as source_image:
                source_bytes=source_image.read()

            response = client.detect_moderation_labels(Image={'Bytes': source_bytes})
           
            ModerationLabels = response['ModerationLabels']
            for moderationlabels in ModerationLabels:
                ml={
                    "Name":moderationlabels['Name'],
                    "Confidence":moderationlabels['Confidence'],
                    "ParentName":moderationlabels['ParentName']
                }
                list_dict_cnp.append(ml)
            
            # print(response.get('ModerationLabels',''))
    return render(request, 'Imagemoderationupload.html', { 'list_dict_cnp':list_dict_cnp })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


class BookListView(ListView):
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'

    #   Advanced Technology For Common people(ATFC)

   
    #from PIL import Image



from django.shortcuts import render
from django.http import HttpResponse

# TODO: Remove temp Index page
def index(request):
    return HttpResponse("Temporary Index, visit addtags/create")

# Create tag submission form view
def create(request):
    return HttpResponse("Create Tags")

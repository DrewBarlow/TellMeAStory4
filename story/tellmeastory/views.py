from django.http import HttpResponse
from django.shortcuts import render

# temp, obviously
def index(req) -> HttpResponse:
    return HttpResponse("Tell Me a Story: TEMP INDEX")

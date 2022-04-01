from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from story.models import NodeStory


def index(request):
     story = NodeStory.MyMap.save('MyMap.html')
     context = {
          'story': story,
     }
     return render(request, 'story/MyMap.html', context=context)
    # return HttpResponse('Lets get started')
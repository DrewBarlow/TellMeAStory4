from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template import loader

from . import models,forms

def deletePost(request,post_id):
    post = models.Post.objects.get(pk=post_id)  # primary key is the post_id
    post.delete()
    return redirect('userPosts')


#Updating a specific post chosen by the user
def editPost(request, post_id):
    post = models.Post.objects.get(pk=post_id) #primary key is the post_id
    form = forms.PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('userPosts')


    return render(request, 'updatePost.html',
                  {'form':form,'post':post})


#Viewing the user's own posts
def viewPost(request):


    posts = models.Post.objects.all()
    return render(request, 'posts_user_view.html',
                  {
                      'posts': posts


                  })


#inserting a post into the database
def InsertPost(request):

    if request.method == 'POST':
        if request.POST.get('postText'):
            saveRecord = models.Post()
            saveRecord.user_id = request.POST.get('user_id')
            print(saveRecord.user_id)
            saveRecord.post_id = request.POST.get('post_id')
            print(saveRecord.post_id)
            saveRecord.postText = request.POST.get('postText')
            print(saveRecord.postText)
            saveRecord.save()
            return render(request,'homepage.html')
    else:
        return render(request, 'homepage.html')
        
def homepage(request):
    template = loader.get_template('homepage.html')
    context = {




    }
    return HttpResponse(template.render(context, request))


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

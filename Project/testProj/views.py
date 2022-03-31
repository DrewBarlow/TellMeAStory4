from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template import loader

from . import models,forms

#Remove a post then redirect to all the posts of the current user (needs a confirm prompt)
def deletePost(request,post_id):
    post = models.Post.objects.get(pk=post_id)  # pk is the primary key
    post.delete()
    return redirect('userPosts')


#Editing a post chosen by the current user redirect to all the posts of the current user (includes input validation based off the model)
def editPost(request, post_id):
    post = models.Post.objects.get(pk=post_id) #primary key is the post_id
    form = forms.PostForm(request.POST or None, instance=post)

    #if the fields are valid, save and redirect
    if form.is_valid():
        form.save()
        return redirect('userPosts')

    #form is a form specified by forms.py, post becomes the Post object specified by the post_id
    return render(request, 'updatePost.html',
                  {'form':form,'post':post})


#Viewing the user's own posts
def viewPost(request):

    #posts are all the posts in the database
    posts = models.Post.objects.all()

    #pass all the objects to the html page
    return render(request, 'posts_user_view.html',
                  {
                      'posts': posts
                  })


#inserting a post into the database, NOT USED
def homepage(request):

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




import json

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from hashlib import sha512
from .forms import LoginForm, NameChangeForm, RegisterForm, PostForm, ReportForm
from .models import User, Post, Report
from .constants import *
from django.shortcuts import render,redirect

API_TOKEN = APIKEY
COOKIE_NAME: str = "StoryUserLoggedIn"


# temp, obviously
def index(req: HttpRequest) -> HttpResponse:
    # if the user has a cookie, they've already logged in
    logged_user: str = req.COOKIES.get("StoryUserLoggedIn")

    return render(req, "tellmeastory/index.html", {
        "logged_in_username": logged_user
    })

# account stub for now
def account(req: HttpRequest, username) -> HttpResponse:

    user: User = get_object_or_404(User, username=username)
    user_posts =  Post.objects.all().filter(username__username__istartswith = username)
    form: NameChangeForm = None
    form_msg: str = None

    if req.COOKIES.get(COOKIE_NAME) == username:
        if req.method == "POST":
            form = NameChangeForm(req.POST)

            # update the User model and check if the new
            # display name is valid
            old_dname: str = user.display_name
            user.display_name = form["new_display_name"].value().strip()

            if user.is_valid_display_name():
                user.save()
                form_msg = "Successfully changed display name."
            else:
                user.display_name = old_dname
                form_msg = "Failed to change display name."

        else:
            # just display the form if the cookie is present and
            # we aren't trying to post data
            form = NameChangeForm()

    return render(req, "tellmeastory/account.html", {
        "user": user,
        "form": form,
        "change_message": form_msg,
        "user_posts": user_posts,
    })

# https://docs.djangoproject.com/en/4.0/topics/forms/
def login(req: HttpRequest) -> HttpResponse:
    form: LoginForm = None
    err_msg: str = None

    if req.method == "POST":
        form: LoginForm = LoginForm(req.POST)

        if form.is_valid():
            username: str = form["username"].value().strip()

            # im just now realizing this means we're sending a password in the clear...
            # too bad!
            # (just kidding... I'll fix this...)
            password: str = sha512(form["password"].value().encode("utf-8")).hexdigest()
            form = LoginForm()

            user: User = None
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                err_msg = "No account with that username."

            # only validate password iff user account was found
            if not err_msg:
                if user.password == password:
                    # using a cookie here...
                    # super spoofable. Too bad!
                    # cookie will be valid until the browser is closed (i.e. max_age=None)
                    res: HttpResponse = HttpResponseRedirect(f"/story/account/{username}")
                    res.set_cookie(
                        COOKIE_NAME,
                        username
                    )

                    return res
                else:
                    err_msg = "Incorrect password."

    else:
        form: LoginForm = LoginForm()

    return render(req, "tellmeastory/login.html", {
        "form": form,
        "error_message": err_msg
    })

# https://docs.djangoproject.com/en/4.0/topics/forms/
def register(req: HttpRequest) -> HttpResponse:
    form: RegisterForm = None
    err_msg: str = None

    if req.method == "POST":
        form = RegisterForm(req.POST)

        if form.is_valid():
            # display_name is optional--
            # if one isn't specified, default the username
            display_name: str = form["display_name"].value()
            if display_name is None or not len(display_name):
                display_name = form["username"].value()

            # hash the user's password for at least a bit of security
            hashed_pw: str = sha512(form["password"].value().encode("utf-8")).hexdigest()
            new_user: User = User(
                username=form["username"].value(),
                password=hashed_pw,
                display_name=display_name
            )

            form = RegisterForm()
            # TODO: Make these more informative?
            if not new_user.is_valid_username():
                err_msg = "Invalid username."
            elif not new_user.is_unique_username():
                err_msg = "Username is already taken."
            elif not new_user.is_valid_display_name():
                err_msg = "Invalid display name."
            else:
                new_user.save()
                return HttpResponseRedirect("/story/login/")

    else:
        form = RegisterForm()

    return render(req, "tellmeastory/register.html", {
        "form": form,
        "error_message": err_msg
    })

def map(req: HttpRequest) -> HttpResponse:

    DATA_TO_INSERT = []

    # THIS DATA IS TEMPORARY - Used only to visualize how stories will appear on the map - not apart of the story
    DATA_TO_INSERT.insert(0, [[-76.611, 39.301], "Story 1 Location"])
    DATA_TO_INSERT.insert(0, [[-76.864, 39.1935], "Story 2 Location"])
    DATA_TO_INSERT.insert(0, [[-77.10415, 39.00532], "Story 3 Location"])
    DATA_TO_INSERT.insert(0, [[-80.13701, 25.901808], "Story 4 Location"])
    DATA_TO_INSERT.insert(0, [[-97.6889, 30.32606], "Story 5 Location"])


    # Converts our data to JSON format
    CONVERT_JSON = json.dumps(DATA_TO_INSERT);

    return render(req, "tellmeastory/map.html", {
        "mapbox_token": API_TOKEN,
        "map_data": CONVERT_JSON,
    })

#Remove a post then redirect to all the posts of the current user (needs a confirm prompt)
def deletePost(req: HttpRequest, post_id)-> HttpResponse:
    post = Post.objects.get(post_id=post_id)  # pk is the primary key
    get_user = str(post.username)

    post.delete()
    return redirect("/account/{0}/".format(get_user))


#Editing a post chosen by the current user redirect to all the posts of the current user (includes input validation based off the model)
def editPost(req: HttpRequest, post_id)-> HttpResponse:

    post = Post.objects.get(post_id=post_id)
    form = PostForm(req.POST or None, instance=post)

    get_user = str(post.username)

    #if the fields are valid, save and redirect
    if form.is_valid():
        form.save()
        return redirect("/account/{0}/".format(get_user))

    #form is a form specified by forms.py, post becomes the Post object specified by the post_id
    return render(req, 'tellmeastory/updatePost.html',
                  {'form':form,'post':post})


#Viewing all the post's in the database
def viewPost(req: HttpRequest)-> HttpResponse:

    username = req.COOKIES.get(COOKIE_NAME)

    #posts are all the posts in the database
    posts = Post.objects.all()



    #pass all the objects to the html page
    return render(req, 'tellmeastory/viewAllPosts.html',
                  {
                      'posts': posts,
                      'username': str(username),
                  })

def reportPost(req: HttpRequest, post_id) -> HttpResponse:
    post = Post.objects.get(post_id=post_id)
    form = ReportForm(req.POST or None, instance=post)

    currentUser = req.COOKIES.get(COOKIE_NAME)
    getUser = User.objects.get(username = currentUser)
    # if the fields are valid, save and redirect
    if form.is_valid():
        new_report = Report(reporting_username = getUser,reported_id = str(post.post_id),report_reason = form.cleaned_data.get('report_reason'))
        Report.save(new_report)
        return redirect("/allPosts")

    # form is a form specified by forms.py, post becomes the Post object specified by the post_id
    return render(req, 'tellmeastory/reportPost.html',
                  {'form': form,
                   'post': post,
                   'username': str(post.username)

                   })

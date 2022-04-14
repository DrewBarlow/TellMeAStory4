import json
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

# Create your views here.
#from story.models import NodeStory

import json

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from hashlib import sha512
from .forms import LoginForm, NameChangeForm, RegisterForm, AudioForm, TextForm, ThumbForm
from .models import User, Node
from .constants import *

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
def account(req: HttpRequest, username: str) -> HttpResponse:
    user: User = get_object_or_404(User, username=username)
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
        "change_message": form_msg
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

# Adds audio to node
def Audio_store(req: HttpRequest) -> HttpResponse:
    msg: str = "choose audio file"
    all_nodes = Node.objects.filter()
    # if this is a POST request process form data
    if req.method == 'POST':
        # create form instance for text data
        form = AudioForm(req.POST, req.FILES or None)
        # check whether it is valid
        if form.is_valid():
            # process data as required
            node: Node = form["node_id"].value()
            node = Node.objects.get(id=node)
            if node is None:
                msg = "cannot attach audio to node"
            # attach new audio
            else:
                try:
                    audio_file = req.FILES.get('node_audio', None)
                except:
                    audio_file = None
                # if audio is read save
                if audio_file is not None:
                    if node.add_audio(sound=audio_file):
                        node.save()
                        msg = "audio update"
                    else:
                        msg = "Unknown audio, try again"

        # go through stages with new change and leave msg     [form.save()]
        return render(req, "tellmeastory/audio.html", {
            "form": form,
            "msg": msg,
            "audio_file": None,
            "id": None,
            "nodes": all_nodes
        })
    else: # ask for audio to be added
        return render(req, "tellmeastory/audio.html", {
                    "form": AudioForm,
                    "msg": msg,
                    "audio_file": None,
                    "id": None,
                    "nodes": all_nodes
        })
           # return HttpResponse('successfully uploaded')
    # if a GET(or any other method) create a blank form
    #else:
    #    form = AudioForm()
    #return render(req, 'tellmeastory/audio.html', {'form': form})

def get_Text(req: HttpRequest) -> HttpResponse:
    # if this is a POST request process form data
    if req.method == 'POST':
        # create form instance for text data
        form = TextForm(req.POST)
        # check whether it is valid
        if form.is_valid():
            # process data as required
            return HttpResponse('Got it')
    # if a GET(or any other method) create a blank form
    else:
        form = TextForm()
    return render(req, 'tellmeastory/text.html', {'form': form})

def thumb_upload(req: HttpRequest) -> HttpResponse:
    if req.method == 'POST':
        form = ThumbForm(req.POST)
        if form.is_valid():
            # process data as required
            return HttpResponse('Got it')
    # if a GET(or any other method) create a blank form
    else:
        form = TextForm()
    return render(req, 'tellmeastory/thumbnail.html', {'form': form})
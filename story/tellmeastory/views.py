import json

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from hashlib import sha512
from typing import Any, Dict
from .forms import LoginForm, NameChangeForm, NodeCreationForm, RegisterForm
from .models import Node, User
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

# to create a story, we need:
#  - a title
#  - some content
#  - some location
#  - the author
# I am not dealing with how location is parsed, so I'll make "location" a string for now.
# ^ removed the above for now
def create_node(req: HttpRequest) -> HttpResponse:
    form: NodeCreationForm = None
    logged_in: bool = False
    err_message: str = None

    # the cookie stores the username.
    # grab the stored username, then follow the generic steps
    alleged_username: str = req.COOKIES.get(COOKIE_NAME)
    if alleged_username:
        user: User = None
        try:
            user = User.objects.get(username=alleged_username)
            logged_in = True
        except User.DoesNotExist:
            err_message = "We could not find your account..."

        if req.method == "POST":
            form: NodeCreationForm = NodeCreationForm(req.POST)

            if form.is_valid():
                # gather all of the form data and make the node
                node_args: Dict[str, Any] = {
                    "image": None,
                    "node_title": form["node_title"].value().strip(),
                    "node_content": form["node_content"].value().strip(),
                    #"longitude": 0,
                    #"latitude": 0,
                    "node_author": user
                }

                new_node: Node = Node(**node_args)
                # validate the new node
                # TODO: make these more informative?
                if not new_node.is_valid_title():
                    err_message = "Invalid title."
                elif not new_node.is_valid_content():
                    err_message = "The content must be less than 10,000 characters!"
                else:
                    new_node.save()

                    # this should redirect to VIEWING the node
                    # for now, I'll just go to the index
                    return HttpResponseRedirect("/story/")
        else:
            form = NodeCreationForm()

    return render(req, "tellmeastory/make_node.html", {
        "form": form,
        "logged_in": logged_in,
        "error_message": err_message
    })

# need some node id
"""def view_node(req: HttpRequest, node_id: int) -> HttpResponse:
    # get id or 404, display node
    return"""

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

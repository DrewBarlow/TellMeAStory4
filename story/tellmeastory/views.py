import json

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from hashlib import sha512
from .forms import LoginForm, NameChangeForm, AddImageForm, NodeCreationForm, RegisterForm, PostStoryForm
from .models import User, Post, Node
from managetags.models import Tag
from typing import Any, Dict
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

    logged_user: str = req.COOKIES.get("StoryUserLoggedIn")

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
        "logged_in_username": logged_user
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
                display_name=display_name,
                mature=form["maturity"].value()
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

# may need location data as args, not sure
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
                # ISSUE: I have no idea why, but I get kwarg issues
                #   on longitude and latitude...
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
                    if form["mature_node"].value():
                        new_node.attach_mature_tag()

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

    logged_user: str = req.COOKIES.get("StoryUserLoggedIn")

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
        "logged_in_username": logged_user
    })

# Takes an existing node to add an image onto it
def add_image(req: HttpRequest) -> HttpResponse:
    err_msg: str = "Please enter only one image field and an id from an existing Node."
    all_nodes = Node.objects.filter()
    # Verify a valid POST request
    if req.method == "POST":
        form = AddImageForm(req.POST)
        if form.is_valid():
            # Check if Node object is given, otherwise prompt
            # with undefined node error.
            # TODO: Redirect to view all Nodes page
            #  once Node page is created for an account.
            node = form["node_id"].value()
            if Node.objects.filter(id=node).exists():
                node = Node.objects.get(id=node)
            else:
                node = None
            if node is None:
                err_msg = "Undefined Node. Image cannot be attached to this node. Please try another node."
            # Otherwise, try to attach new image given
            else:
                # Null image if empty
                try:
                    image_file = req.FILES.get('image_file', None)
                except:
                    # Image_file should be none if no files given.
                    # Failsafe if get throws an exception instead
                    # of setting image_file to None for no files.
                    image_file = None
                image_url: str = form["image_url"].value()
                # Null url if blank
                if image_url == "":
                    image_url = None
                # If Node receives an image from an image file
                if image_file is not None and image_url is None:
                    # Only save if new image is valid
                    if node.add_image(newFile=image_file):
                        node.save()
                        err_msg = "Thank you! Your node has been updated for Node id: " + str(node.id)
                    else:
                        err_msg = "Undefined Image. Please try again."
                # If Node receives an image from an url
                elif image_url is not None and image_file is None:
                    # Only save if new image is valid
                    if node.add_image(newURL=image_url):
                        node.save()
                        err_msg = "Thank you! Your node has been updated for Node id: " + str(node.id)
                    else:
                        err_msg = "Invalid Image URL. Please try again."
                # If Node receives no image or two images (retains features)
                elif image_url is not None and image_file is not None:
                    err_msg = "Try again. Please enter only one one field."
                # If no images are given (retains features)
                else:
                    err_msg = "Try again. No image given."
        # Reprompt for another change with applied new changes
        # Provide an error message if relevant. Otherwise,
        # provide a success message.
        return render(req, "tellmeastory/addnodeimage.html", {
            "form": form,
            "err_msg": err_msg,
            "image_file": None,
            "image_url": None,
            "id": None,
            "nodes": all_nodes
        })
    # Otherwise, prompt for image source info to add to node
    else:
        return render(req, "tellmeastory/addnodeimage.html", {
                    "form": AddImageForm,
                    "err_msg": err_msg,
                    "image_file": None,
                    "image_url": None,
                    "id": None,
                    "nodes": all_nodes
                })


def profile(req: HttpRequest, username:str) -> HttpResponse:

    logged_user: str = req.COOKIES.get("StoryUserLoggedIn")
    user: User = None

    try:
        user = User.objects.get(username=username)

    except User.DoesNotExist:
        return render(req , "tellmeastory/profileNotFound.html" , {
            "logged_in_username": logged_user ,
        })

    storiesFromUser = Post.objects.filter(username_id=user.id)
    storyCount = storiesFromUser.count()

    return render(req , "tellmeastory/profile.html" , {
        "user": user ,
        "logged_in_username": logged_user ,
        "stories": storiesFromUser,
        "story_count": storyCount,
    })


def author_story(req: HttpRequest, username: str) -> HttpResponse:
    user: User = get_object_or_404(User, username=username)
    err_msg = None
    all_nodes = Node.objects.filter()
    my_nodes = []
    all_tags = Tag.objects.filter()
    form = PostStoryForm()
    logged_user: str = req.COOKIES.get(COOKIE_NAME)

    # Find all of a user's stories
    if logged_user == username:
        # User account should exist, otherwise they have no nodes
        try:
            user = User.objects.get(username=username)
            for curNode in all_nodes:
                if curNode.node_author == user:
                    my_nodes.append(curNode)
        except User.DoesNotExist:
            my_nodes = []

    # If POST, then process new node authored by user, else
    # send to node creation page.
    if req.method == "POST":
        # Check for a valid POST request and that
        # the given username is what their cookie
        # shows.
        form: PostStoryForm() = PostStoryForm(req.POST)
        if form.is_valid():
            if logged_user == username:
                # User account should exist, otherwise send them
                # to the login page.
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    err_msg = "Account does not exist."
                    form: LoginForm = LoginForm()
                    return render(req, "tellmeastory/login.html", {
                        "form": form,
                        "error_message": err_msg
                    })
                # CREATE STORY NODE FROM PROVIDED INFORMATION
                err_msg = user.post_node({
                    "node_title": form["node_title"].value().strip(),
                    "node_content": form["node_content"].value().strip(),
                    "image_file": form["image_file"].value(),
                    "image_url": form["image_url"].value(),
                    "main_tag_id": form["main_tag_id"].value(),
                    "mature_node": form["mature_node"].value(),
                    "latitude": form["latitude"].value(),
                    "longitude": form["longitude"].value()
                })
                # Present error if any exists, update my nodes and present
                # blank form.
                form = PostStoryForm()
                return render(req, "tellmeastory/author_a_node.html", {
                    "user": user,
                    "form": form,
                    "error_message": err_msg,
                    "nodes": my_nodes,
                    "tags": all_tags,
                    "logged_in_username": logged_user
                })
            # If cookie does not match username, send to
            # login page.
            else:
                form: LoginForm = LoginForm()
                err_msg = "Account not found. Try adding a story later."
                return render(req, "tellmeastory/login.html", {
                    "form": form,
                    "error_message": err_msg
                })
        else:
            # Reprompt when invalid form is submitted
            form = PostStoryForm(req.POST)
            err_msg = "Invalid Story. All fields are required except the image. Only one image is allowed."
            return render(req, "tellmeastory/author_a_node.html", {
                "user": user,
                "form": form,
                "error_message": err_msg,
                "nodes": my_nodes,
                "tags": all_tags,
                "logged_in_username": logged_user
            })
    # Prompt with node creation page.
    else:
        # Render the page with node creation form and
        # all nodes of current user.
        return render(req, "tellmeastory/author_a_node.html", {
                "user": user,
                "form": form,
                "error_message": err_msg,
                "nodes": my_nodes,
                "tags": all_tags,
                "logged_in_username": logged_user
            })

import json
import uuid
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from hashlib import sha512
from typing import Any, Dict
from .forms import LoginForm, NameChangeForm, RegisterForm, PostForm, ReportForm, AddImageForm, NodeCreationForm
from .models import User, Report, Ban, Node
from .constants import *
from django.shortcuts import render,redirect
from django.core.exceptions import PermissionDenied
import uuid

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

    #get the current username
    username = req.COOKIES.get(COOKIE_NAME)

    #check if the person logged in has been banned already
    checkBan = Ban.objects.filter(bannedUser=username)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")

    #get the current user object from the database
    user: User = get_object_or_404(User, username=username)

    #get all the post from the current user
    user_posts =  Node.objects.all().filter(node_author__username__istartswith = username)

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

            #check if the username was banned
            checkBan = Ban.objects.filter(bannedUser=str(form["username"].value()))

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
            elif checkBan.exists():
                err_msg = "That username is banned."
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

                #create a post id
                create_post_id = uuid.uuid1()
                checkID = Node.objects.filter(post_id=create_post_id)
                while (checkID.count() != 0):
                    create_post_id = uuid.uuid1()
                    checkID = Node.objects.filter(post_id=create_post_id)


                node_args: Dict[str, Any] = {
                    "image": None,
                    "node_title": form["node_title"].value().strip(),
                    "node_content": form["node_content"].value().strip(),
                    #"longitude": 0,
                    #"latitude": 0,
                    "node_author": user,
                    "post_id": create_post_id
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

    #get the current user logged in
    username = req.COOKIES.get(COOKIE_NAME)

    #check if the current user logged in has been banned
    checkBan = Ban.objects.filter(bannedUser=username)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")

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

    #get the current user logged in
    username = req.COOKIES.get(COOKIE_NAME)

    #if the current user has been banned
    checkBan = Ban.objects.filter(bannedUser=username)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")



    #get the current post
    post = Node.objects.get(post_id=post_id)

    # if another user is trying to edit someone else's post
    current_post_user = str(post.node_author)
    if (current_post_user != username):
        return HttpResponseRedirect("/allPosts/")

    get_user = str(post.node_author)

    #delete current post
    post.delete()

    #redirect to the users page
    return redirect("/account/{0}/".format(get_user))


#Editing a post chosen by the current user redirect to all the posts of the current user (includes input validation based off the model)
def editPost(req: HttpRequest, post_id)-> HttpResponse:

    # get the current user logged in
    username = req.COOKIES.get(COOKIE_NAME)

    # if the current user has been banned
    checkBan = Ban.objects.filter(bannedUser=username)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")

    #get current post
    post = Node.objects.get(post_id=post_id)

    #if another user is trying to edit someone else's post
    current_post_user = str(post.node_author)
    if (current_post_user != username):
        return HttpResponseRedirect("/allPosts/")

    #get the form for posting
    form = PostForm(req.POST or None, instance=post)

    get_user = str(post.node_author)

    #if the fields are valid, save and redirect
    if form.is_valid():
        form.save()
        return redirect("/account/{0}/".format(get_user))

    #form is a form specified by forms.py, post becomes the Post object specified by the post_id
    return render(req, 'tellmeastory/editPost.html',
                  {'form':form,'post':post})


#Viewing all the post's in the database
def viewPost(req: HttpRequest)-> HttpResponse:

    # get the current user logged in
    username = req.COOKIES.get(COOKIE_NAME)

    # if the current user has been banned
    checkBan = Ban.objects.filter(bannedUser=username)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")


    #posts are all the posts in the database
    posts = Node.objects.all()



    #pass all the objects to the html page
    return render(req, 'tellmeastory/viewAllPosts.html',
                  {
                      'posts': posts,
                      'username': str(username),
                  })

def reportPost(req: HttpRequest, post_id) -> HttpResponse:

    #get the current user
    currentUser = req.COOKIES.get(COOKIE_NAME)


    #check if the current user is banned first
    checkBan = Ban.objects.filter(bannedUser=currentUser)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")

    #get the current post and the form we need
    post = Node.objects.get(post_id=post_id)
    form = ReportForm(req.POST or None, instance=post)


    #get the current user
    getUser = User.objects.get(username=currentUser)

    # if the fields are valid, save and redirect
    if form.is_valid():

        #get a report id
        taken_id = True

        #get a random id
        getId = None
        while (taken_id == True):
            getId = str(uuid.uuid4())
            try:
                Report.objects.get(id_for_report=getId)
            except Report.DoesNotExist:
                taken_id = False

        #get a report object
        new_report = Report(reporting_username = getUser,reported_id = str(post.node_author),report_reason = form.cleaned_data.get('report_reason'), id_for_report = getId, post = Node.objects.get(post_id=post_id))

        #save the new report to the database and redirect to all the posts
        Report.save(new_report)
        return redirect("/allPosts")

    # form is a form specified by forms.py, post becomes the Post object specified by the post_id
    return render(req, 'tellmeastory/reportPost.html',
                  {'form': form,
                   'post': post,
                   'node_author': str(post.node_author)

                   })

#Admin view for viewing reports
def adminReportPage(req: HttpRequest)-> HttpResponse:

    #get current user
    username = req.COOKIES.get(COOKIE_NAME)

    #check if the current user is banned
    checkBan = Ban.objects.filter(bannedUser=username)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")


    #posts are all the posts in the database
    reports = Report.objects.all()

    #get the current user to check privileges
    user = User.objects.get(username=username)

    #if the user is not an admin, deny permission to view the website
    if (user.admin == False):
        raise PermissionDenied
    else:
        # pass all the objects to the html page
        return render(req, 'tellmeastory/adminReportPage.html',
                      {
                          'reports': reports,

                      })



def adminReportPost(req: HttpRequest, report_id) -> HttpResponse:

    username = req.COOKIES.get(COOKIE_NAME)

    checkBan = Ban.objects.filter(bannedUser=username)
    if checkBan.exists():
        return HttpResponseRedirect("/banned/")


    # get the current user to check privileges
    user = User.objects.get(username=username)


    #get the report from the database
    report = Report.objects.get(id_for_report=report_id)



    reported_username = str(report.reporting_username)

    #if the user is not an admin, deny permission to view the website
    if (user.admin == False):
        raise PermissionDenied
    else:
        #if a dropdown option is saved
        if req.method == "POST":

            #get the dropdown option (Ban or Delete)
            getChoice = req.POST["choice"]

            #Ban the offender
            if (getChoice) == "Ban":
                reportedUser = str(report.post.node_author)
                Ban.save(Ban(bannedUser=str(reportedUser)))
                User.objects.get(username=reportedUser).delete()
            #Delete the report
            else:
                Report.delete(report)

            #redirect to a list of the reports
            return HttpResponseRedirect("/adminReportList/")
        else:
            # pass all the objects to the html page
            return render(req, 'tellmeastory/adminReportPost.html',
                        {
                            'report': report,
                            'reported_username': reported_username,
                        })


#Ban page
def banned(req: HttpRequest)-> HttpResponse:
    return render(req, 'tellmeastory/ban.html')

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

    storiesFromUser = Node.objects.filter(node_author=user)
    storyCount = storiesFromUser.count()

    return render(req , "tellmeastory/profile.html" , {
        "user": user ,
        "logged_in_username": logged_user ,
        "stories": storiesFromUser,
        "story_count": storyCount,
    })
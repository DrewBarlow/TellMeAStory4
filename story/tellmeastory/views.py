from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import LoginForm, RegisterForm
from .models import User

# temp, obviously
def index(req) -> HttpResponse:
    return HttpResponse("Tell Me a Story: TEMP INDEX")

# https://docs.djangoproject.com/en/4.0/topics/forms/
def login(req) -> HttpResponse:
    if req.method == "POST":
        form: LoginForm = LoginForm(req.POST)

        if form.is_valid():
            return HttpResponseRedirect("/story/index/")  # temp redirect

    else:
        form: LoginForm = LoginForm()

    return render(req, "tellmeastory/login.html", {"form": form})

# https://docs.djangoproject.com/en/4.0/topics/forms/
def register(req) -> HttpResponse:
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

            # TODO: validate password and hash it

            new_user: User = User(
                username=form["username"].value(),
                password=form["password"].value(),
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


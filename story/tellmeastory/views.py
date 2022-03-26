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
    if req.method == "POST":
        form: RegisterForm = RegisterForm(req.POST)

        if form.is_valid():
            # TODO: VALIDATE USER/PASS
            new_user: User = User(
                username=form["username"],
                password=form["password"],
                display_name=["display_name"]
            )
            return HttpResponseRedirect("/story/login/")

    else:
        form: RegisterForm = RegisterForm()

    return render(req, "tellmeastory/register.html", {"form": form})


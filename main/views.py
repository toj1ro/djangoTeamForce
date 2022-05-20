from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect

from . import services
from .forms import NewUserForm
from .models import User, Tag


def redirect_view(request):
    if request.user.is_authenticated:
        response = redirect('/homepage')
        return response
    else:
        response = redirect('/register')
        return response


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})


@login_required
def home_page(request):
    dict_data = {}
    users = User.objects.all()
    for user in users:
        tag_values = services.get_user_tags(user.id)
        dict_data[user] = tag_values
    return render(request=request, template_name="main/homepage.html", context={'data': dict_data})


@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        tag = request.POST.get('tag', '')
        value = request.POST.get('value', '')
        tag_ = services.create_tag(tag)
        value_ = services.create_tag_value(value)
        services.create_user_tag_value(user, tag_, value_)
    tag_values = services.get_user_tags(user.id)
    return render(request, 'main/profile.html', context={'data': tag_values})


def autocmplete(request):
    if 'term' in request.GET:
        qs = Tag.objects.filter(name__icontains=request.GET.get('term'))
        tags = list()
        for tag in qs:
            tags.append(tag.name)
        return JsonResponse(tags, safe=False)
    return render(request, 'main/autoc.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import UserLoginForm, UserRegisterForm

from .forms import ProfileForm
from .models import Profile


# Create your views here.

# user login
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            # check if account and password match the user in the database
            # if so return this user object
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                # store user data into "seesion" so the user will be in 
                # login status
                login(request, user)
                return redirect("article:article_list")
            else:
                return HttpResponse("The username or password is incorrectly. Please try again")
        else:
            return HttpResponse("Invalid account or password input")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = { 'form': user_login_form }
        return render(request, 'account/login.html', context)
    else:
        return HttpResponse("Please use GET or POST method to request data")


def user_logout(request):
    logout(request)
    return redirect("article:article_list")


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save()
            # Return to the blog home page onece register inform was stored
            login(request, new_user)
            return redirect("article:article_list")
        else:
            # the defaul form has "check" funtion that check of password vaild, and many other inform, like complxity, etc.
            return HttpResponse("Password is invalid, please make sure entered a password meets the standard!")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = { 'form': user_register_form }
        return render(request, 'account/signup.html', context)
    else:
        return HttpResponse("Please use GET or POST method to request data")


# delete user
# A decorator that validates the if the user is logged in
@login_required(login_url='/accounts/login/')
def user_delete(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        # Verify that the logged in user and the user to be deleted are the same
        if request.user == user:
            #logout, delete the user data and return to blog home page
            logout(request)
            user.delete()
            return redirect("article:article_list")
        else:
            return HttpResponse("You do not have permission to delete the account!")
    else:
        return HttpResponse("Only POST request is acceptable!")


# Edit user profile
@login_required(login_url='/accounts/login/')
def profile_edit(request, id):
    user = User.objects.get(id=id)

    # get the profile
    if Profile.objects.filter(user_id=id).exists():
        profile = Profile.objects.get(user_id=id)
    else:
        profile = Profile.objects.create(user=user)


    if request.method == 'POST':
        # check if the user is vaild
        if request.user != user:
            return HttpResponse("You do not have permission to modify this user profile!")

        # save the upload file in request.FILES, and use paramenter to transfter to the form object
        profile_form = ProfileForm(request.POST, request.FILES)

        if profile_form.is_valid():
            # get the data after clearning
            profile_cd = profile_form.cleaned_data

            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']

            # if request.FILES have files, save
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]

            profile.save()
            return redirect("userprofile:edit", id=id)
        else:
            return HttpResponse("The registration form was entered incorrectly. Please try again!")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = { 'profile_form': profile_form, 'profile': profile, 'user': user }
        return render(request, 'userprofile/edit.html', context)
    else:
        return HttpResponse("Please use POST/GET to request data")

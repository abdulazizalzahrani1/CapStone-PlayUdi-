from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from tournament.models import Profile, Trophy, Tournament
from django.contrib.auth import authenticate, login, logout


# Create your views here.


def register_user_view(request : HttpRequest):

    if request.method == "POST":
        if request.POST["states"] == "1":
            new_user = User.objects.create_user(first_name=request.POST["first_name"], last_name=request.POST["last_name"], username=request.POST["username"], email=request.POST["email"], password=request.POST["password"])
            new_user.save()
    
            user_porifle = Profile(user=new_user,birth_date=request.POST["birth_date"], states=request.POST["states"],bio=request.POST['bio'])
            if "avatar" in request.FILES:
                    user_porifle.avatar = request.FILES["avatar"]
            user_porifle.save()
            return redirect("accounts:login_user_view")
        
        elif request.POST["states"] == "2":
            new_user = User.objects.create_user(first_name=request.POST["first_name"], last_name=request.POST["last_name"], username=request.POST["username"], email=request.POST["email"], password=request.POST["password"])
            new_user.is_active = False
            new_user.save()
            
    
            user_porifle = Profile(user=new_user,birth_date=request.POST["birth_date"], states=request.POST["states"])
            if "avatar" in request.FILES:
                    user_porifle.avatar = request.FILES["avatar"]
            user_porifle.save()

                    
            return redirect("accounts:login_user_view")


    return render(request, "accounts/register.html")


def login_user_view(request: HttpRequest):

    msg = None
    
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])

        if user:
            login(request, user)
            return redirect("main:home_view")
        else:
            msg = "Username or password is no correct. No user found."


    return render(request, "accounts/login.html", {"msg": msg})



def logout_user_view(request: HttpRequest):

    logout(request)

    return redirect("accounts:login_user_view")


def profile_page(request:HttpRequest, user_id):

    profile = Profile.objects.get(user__id=user_id)

    trophies = Trophy.objects.filter(winner=profile)



    return render(request, "accounts/profile.html", {"profile" : profile, "trophies":trophies})



def update_profile_page(request:HttpRequest, user_id):

    #make sure only the owner of the profile can update it


    user = User.objects.get(id=user_id)
    profile= Profile.objects.get(user=user)    
    if request.method == "POST":
        profile.birth_date = request.POST["birth_date"]
        if "avatar" in request.FILES:
            profile.avatar = request.FILES["avatar"]
        profile.save()

        return redirect("accounts:profile_page", user_id=user_id)
    
    return render(request, "accounts/update_profile.html", {"profile" : profile})


def user_admin_view(request: HttpRequest):
     users = User.objects.all()
     profiles= Profile.objects.all()
     touremnts=Tournament.objects.all()
     if request.method=="POST":
        status= request.POST["status"]
        profile_id=request.POST["profile_id"]

        profile = User.objects.get(id=profile_id)

        if status == "non_active":
            profile.is_active= False
        else:
              profile.is_active= True
        profile.save()


     
     return render(request, "accounts/user_admin.html",context = {"users" :users ,"profiles":profiles,"touremnts":touremnts})  
  





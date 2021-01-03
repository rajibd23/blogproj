from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.models import User
from avatar.models import Avatar
from avatar.views import _get_avatars
from .forms import ProfileForm, AvatarForm, CustomSignupForm
# Create your views here.



def get_user_profile(request, username):

    user = User.objects.get(username=username)
    avatar = _get_avatars(user)
    print(avatar[0])
    if not avatar[0]:
        return render(request, 'profile.html', {'user': user,'avatar':avatar, 'isavatar':False})
    else:
        return render(request, 'profile.html', {'user': user, 'avatar': avatar, 'isavatar':True})



def avatar_update(request, username):
    title = 'Update Avatar'
    print("Inside update avatar")
    #print(user.first_name)

    user = get_object_or_404(User, username=username)
    #avatar = Avatar.objects.get(id=user.pk)
    avatar = _get_avatars(username)

    if request.method == "POST":
        aform = AvatarForm(request.POST, instance=avatar)

        if aform.is_valid():
            print("Inside update avatar is valid")
            new_avatar = aform.save()

            return redirect(reverse("profile-home", kwargs={
                    'username': username
                }))
        else:
            aform = aform
    else:
        aform = AvatarForm(request.POST or None,request.FILES or None, instance=avatar)

    return render(request, 'update_profile.html', {'avatar_form': aform, 'ind':1})

def user_profile_update(request, username):
    title = 'Update Profile'
    print("Inside update profile")
    #print(user.first_name)

    user = get_object_or_404(User, username=username)
    #avatar = Avatar.objects.get(id=user.pk)


    if request.method == "POST":
        print("Inside update post")
        pform = ProfileForm(request.POST, instance=user)
        if pform.is_valid():
            #usernamenew = pform.username
            print("Inside update isvalid")
            new_profile = pform.save()

            return redirect(reverse("profile-home", kwargs={
                    'username': new_profile.username
            }))
        else:
            print("Inside update else")
            return render(request, 'update_profile.html', {'profile_form': pform, 'ind': 2})
    else:
        print("Inside update else else profile")
        pform = ProfileForm(request.POST or None, request.FILES or None, instance=user)

    return render(request, 'update_profile.html', {'profile_form': pform, 'ind':2})


def comma_splitter(tag_string):
    return [t.strip().lower() for t in tag_string.split(',') if t.strip()]
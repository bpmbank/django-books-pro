from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required
from utils.CommonUtils import get_base_context_map, is_superuser

# Create your views here.


def init_context(request, user_id=0):
    context_map = get_base_context_map(request)
    user = request.user
    context_map['user'] = user
    context_map['is_self'] = False
    context_map['friend'] = False

    if bool(user_id):
        view_user = User.objects.get(pk=user_id)
        context_map['view_user'] = view_user
    else:
        view_user = user
        context_map["view_user"] = user

    print context_map.get("friend"), context_map.get("is_self"), context_map.get("user"), context_map.get("view_user")
    return context_map, user, view_user


def index(request, user_id=0):
    context_map, user, view_user = init_context(request, user_id=user_id)

    return render_to_response('userprofile/index.html', context_map)


@login_required
def avatar(request):
    def save_tmp_img(img):
        import os

        filename = os.path.join(settings.ROOT_PATH, 'tmp_img.tmp')
        imgfile = open(filename, 'wb')
        for chunk in img.chunks():
            imgfile.write(chunk)
        imgfile.close()
        return filename


    context_map = get_base_context_map(request)
    user = request.user
    form = AvatarForm()  # user.get_profile().__dict__
    if request.method == 'POST':  # if request.POST:
        form = AvatarForm(request.POST, files=request.FILES)
        if form.is_valid():
            clean_data = form.cleaned_data
            if clean_data['avatar']:
                avatar = clean_data['avatar']
                # FIXME move the tmp img
                tmp_img = save_tmp_img(avatar)
                upload_avatar(tmp_img, user.id)
                user.get_profile().avatar = str(user.id) + '.jpg'
            else:
                user.get_profile().avatar = ''
            user.get_profile().save()
            return HttpResponseRedirect('/userprofile/')
    context_map['form'] = form
    return render_to_response('userprofile/avatar.html', context_map)

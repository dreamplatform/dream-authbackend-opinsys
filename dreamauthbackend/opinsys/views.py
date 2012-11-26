
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth import login
from dreamauthbackend.opinsys.forms import PuavoLoginForm, PuavoRegisterForm, PuavoAssociateForm

def puavo_login(request, extra_context=None):
    if request.method == 'POST':
        form = PuavoLoginForm(data=request.POST)
        if form.is_valid():
            login(request, form.association.user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = PuavoLoginForm()
    context = {
        'form': form,
    }
    if extra_context:
        context.update(extra_context)
    return render(request, 'dreamauthbackend/opinsys/puavo_login.html', context)


def puavo_register(request, extra_context=None):
    if request.method == 'POST':
        form = PuavoRegisterForm(data=request.POST)
        if form.is_valid():
            login(request, form.association.user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = PuavoRegisterForm()
    context = {
        'form': form,
    }
    if extra_context:
        context.update(extra_context)
    return render(request, 'dreamauthbackend/opinsys/puavo_register.html', context)


@login_required
def puavo_associate(request, extra_context=None):
    if request.method == 'POST':
        form = PuavoAssociateForm(data=request.POST, user=request.user)
        if form.is_valid():
            return redirect(settings.DREAMAUTHBACKEND_OPINSYS_NEW_ASSOCIATION_REDIRECT_URL)
    else:
        form = PuavoAssociateForm(user=request.user)
    context = {
        'form': form,
    }
    if extra_context:
        context.update(extra_context)

    return render(request, 'dreamauthbackend/opinsys/puavo_associate.html', context)

from config.scripts import auth_code_generator
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from .forms import InviteForm, PhoneForm, VerifyForm
from .models import CustomUser


@require_http_methods(['GET'])
def main(request):
    """Главная страница."""

    users = CustomUser.objects.all()
    paginator = Paginator(users, 6)
    page_obj = paginator.get_page(request.GET.get('page'))
    template = 'main.html'
    context = {
        'users': users,
        'page_obj': page_obj}
    return render(request, template, context)


@require_http_methods(['GET', 'POST'])
def signup(request):
    """Страница с формой для ввода номера."""

    form_class = PhoneForm(request.POST or None)
    template_name = 'signup.html'
    context = {
        'form': form_class}

    if request.user.is_authenticated:
        return redirect('frontend:main')

    if request.method != "POST":
        return render(request, template_name, context)

    if form_class.is_valid():
        phone = request.POST.get('phonenumber')
        request.session['phone'] = phone
        request.session['code'] = auth_code_generator()
        request.session.set_expiry(300)
        return redirect('frontend:verification')
    return render(request, template_name, context)


@require_http_methods(['GET', 'POST'])
def verification(request):
    """Страница с формой для sms-верификации/входа."""

    if (
        request.user.is_authenticated or
        not request.session.get('code') or
        not request.session.get('phone')
    ):
        return redirect('frontend:signup')

    code = request.session.get('code')
    form_class = VerifyForm(request.POST or None, request=request)
    template = 'verify.html'
    context = {
        'form': form_class,
        'code': code}

    if request.method != "POST":
        return render(request, template, context)

    if form_class.is_valid():
        user = form_class.save()
        request.session.flush()
        login(request, user)
        return redirect('frontend:main')

    return render(request, template, context)


@require_http_methods(['GET', 'POST'])
@login_required
def profile(request):
    """Профиль пользователя, с формой для отправки инвайт-кода."""

    form_class = InviteForm(request.POST or None, request=request)
    template = 'profile.html'
    context = {
        'user': request.user,
        'form': form_class}

    if request.method != "POST":
        return render(request, template, context)

    if form_class.is_valid():
        invite_code = request.POST.get("invite_code")
        user = CustomUser.objects.get(invite_code=invite_code)
        request.user.invitations.add(user)
        return redirect('frontend:me')

    return render(request, template, context)

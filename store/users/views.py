from django.contrib import auth, messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from users.models import User
from users.forms import UserLoginForm, UserRegisterationForm, UserProfileForm
from products.models import Basket
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from common.views import CommonMixin


class UserLoginView(CommonMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'

    def get_success_url(self):
        return reverse_lazy('index')


class UserRegistrationView(CommonMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegisterationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Регистрация прошла успешно'
    title = 'Store - Регистрация'


class UserProfileView(CommonMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store - Личный кабинет'

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        user = queryset.get(pk=self.request.user.id)
        return user

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context


class UserLogoutView(LogoutView):
    pass


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {'form': form}
#
#     return render(request, 'users/login.html', context)

# def registration(request):
#     if request.method == 'POST':
#         form = UserRegisterationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Регистрация прошла успешно')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegisterationForm()
#     context = {'form': form}
#     return render(request, 'users/registration.html', context)

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     baskets = Basket.objects.filter(user=request.user)
#     context = {'title': 'Store - Профиль',
#                'form': form,
#                'baskets': baskets,
#                }
#     return render(request, 'users/profile.html', context)

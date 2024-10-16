from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy
from .models import CustomUser
from django.contrib.auth import logout


def logout_view(request):
    logout(request)
    return redirect('login')



class LoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def get(self, request):
        context = {'form':self.form_class}
        context['title']='Login'

        return render(request, self.template_name, context)
    

    def form_invalid(self, form: AuthenticationForm):
        username = form.cleaned_data.get('username')
        user_existis = CustomUser.objects.filter(username=username)
        error_messages = {
            'invalid_login':gettext_lazy('verifique o usuario e senha e tente novamente'),
            'inactive':gettext_lazy('Usuario Inativo'),
        }
        response = super().form_invalid(form)

        if not user_existis:
            response['erro'] = error_messages['invalid_login']
        else:
            response['erro'] = error_messages['inactive']
        
        return response
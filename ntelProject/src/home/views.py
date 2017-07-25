from django.contrib.auth.forms import UserCreationForm
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView


# Create your views here.
class IndexView(TemplateView):
    template_name = 'index.html'

class HomeView(TemplateView):
    template_name = 'home.html'

class LoginView(TemplateView):
    template_name = 'registration/login.html'

class UserCreateView(CreateView):
    """  사용자 추가
    """
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_docne')
    
class UserCreateDoneView(TemplateView):
    """  사용자 추가 완료
    """
    template_name = 'registration/register_done.html'






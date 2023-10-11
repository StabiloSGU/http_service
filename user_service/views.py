from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class LoginView(auth_views.LoginView):
    template_name = 'login.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_page = kwargs.get('from_page', reverse_lazy("csv_import:uploads_list"))
        self.redirect_authenticated_user = True


class LogoutView(auth_views.LogoutView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.next_page = reverse_lazy("csv_import:uploads_list")


class RegisterView(auth_views.FormView):
    pass
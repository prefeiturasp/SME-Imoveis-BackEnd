from django.contrib import admin, messages
from .models import Perfil, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "perfil")

    def save_model(self, request, obj, form, change):
        error = False
        if (change and
                form.data.get('perfil') and
                'perfil' in form.changed_data):
            if (Perfil.objects.get(id=form.data.get('perfil')).nome == 'ADMIN' and
                    User.objects.filter(perfil__nome='ADMIN').count() == 3):
                messages.set_level(request, messages.ERROR)
                messages.error(request, 'Excedeu o limite de usuários ADMIN no sistema.')
                error = True
            elif (Perfil.objects.get(id=form.data.get('perfil')).nome == 'SECRETARIA' and
                    User.objects.filter(perfil__nome='SECRETARIA').count() == 3):
                messages.set_level(request, messages.ERROR)
                messages.error(request, 'Excedeu o limite de usuários SECRETARIA no sistema.')
                error = True
        if not error:
            super(UserAdmin, self).save_model(request, obj, form, change)


admin.site.register(Perfil)

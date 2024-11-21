from django.contrib import admin
from .models import User


from .models import UserToken
from django.apps import AppConfig






from django.shortcuts import render
from django.contrib.auth.models import User

def show_logged_in_users(request):
    logged_in_users = User.objects.filter(is_active=True)
    return render(request, 'your_template.html', {'logged_in_users': logged_in_users})


admin.site.register(User)

admin.site.register(UserToken)





@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'last_active', 'is_active')

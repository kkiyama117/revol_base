from django.contrib import admin

# Register your models here.
from society.models import Profile, Society


class ProfileInline(admin.StackedInline):
    model = Profile
    max_num = 1
    can_delete = False


class SocietyInline(admin.StackedInline):
    model = Society
    max_num = 1
    can_delete = False


class ProfileAdmin(admin.ModelAdmin):
    model = Profile
    # fields = '__all__'


admin.site.register(Profile, ProfileAdmin)

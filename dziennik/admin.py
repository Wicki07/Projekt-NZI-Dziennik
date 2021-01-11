from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User
from dziennik.models import Institution, Employee, Activity, Child

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('id','email', 'admin','first_name','last_name','phone','role','active')
    list_filter = ('admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','phone','active')}),
        ('Permissions', {'fields': ('admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','first_name','last_name','phone','role','active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.register(Institution)
admin.site.register(Employee)
admin.site.register(Activity)
#admin.site.register(Podglad)
admin.site.register(Child)



# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)
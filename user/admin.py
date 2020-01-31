from django import forms
from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User

# Register your models here.
class UserCreationForm(forms.ModelForm):
    """
    Create a user using the required fields and the password
    """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Repeat Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['id_number']

    def clean_password(self,):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Check if they match
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two Passwords must match")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'

    def clean_password(self):
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    #Forms to add and update the user
    form = UserChangeForm
    add_form = UserCreationForm

    #Fields to display on the User Admin interface
    list_display = ['id_number', 'surname', 'phone_number']
    list_filter = ['is_admin', 'location', 'gender']

    fieldsets = (
        (None, {"fields": ('id_number', 'password',)}),
        ('Personal Information', {"fields": ('surname', 'first_name','last_name','phone_number', 'dob', 'gender','email')}),
        ('Permissions', {"fields": ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
        'classes': ('wide',),
        'fields': ('id_number', 'password1', 'password2')}
        ),
    )

    search_fields = ('id_number',)
    ordering = ['id_number']
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# Since we're not using Django's built-in permissions, # unregister the Group model from admin.
admin.site.unregister(Group)

from django import forms
from django.contrib.auth.forms import UserCreationForm
from validators import validate_email_domain_restriction
from validators import validate_existence_email_domain
from validators import validate_email_domain_to_exclude
from django.contrib.auth.models import User
import logging
from ldap_people.models import LdapPerson
from django.utils.translation import ugettext as _

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required',
                             validators=[validate_email_domain_restriction,
                                         validate_existence_email_domain])

    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email) \
                                 .filter(is_active=True) \
                                 .exclude(username=username) \
                                 .exists():
            raise forms.ValidationError(_('email_must_be_unique'))
        return email

    
    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
            # if user exists, raise an error
            raise forms.ValidationError( 
                _('duplicate_username'),  # custom error
                code='username',   #set the error message key
            )
        except User.DoesNotExist:
            return username # continue registration process


    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


        
class ResetPasswordForm(forms.ModelForm):
    email = forms.EmailField(
        max_length=200,
        help_text='Required',
        validators=[validate_existence_email_domain])

    def clean_email(self):
        email = self.cleaned_data.get('email')
        person = LdapPerson.get_by_email(str(email))

        if person is None:
            # there is no person associated with the mail
            raise forms.ValidationError(_('invalid_alternative_email'))

        if person and not person.alternative_email:
            # the person does not have an alternative email to recover
            raise forms.ValidationError(_('without_alternative_email'))

        return email
    
    class Meta:
        model = User
        fields = ('email',)

        
class DefinePasswordForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('password1', 'password2')

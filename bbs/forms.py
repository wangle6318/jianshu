from django import forms
from bbs.models import User, UserInfo
from django.core.validators import RegexValidator


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=20,
                           error_messages={'required': u'昵称不能为空'},
                           widget=forms.TextInput(attrs={'class': 'acct_name', 'placeholder': u'昵称'}))
    acct = forms.CharField(min_length=5,
                           error_messages={'required': u'用户名不能为空', 'min_length': u'最少为5个字符'},
                           validators=[RegexValidator(r'^(?=.*[a-z])(?=.*[0-9])[A-Za-z0-9]{5,}$', "用户名至少包含一个字母")],
                           widget=forms.TextInput(attrs={'class': 'acct_user', 'placeholder': u'用户名'}))
    password = forms.CharField(min_length=8,
                               error_messages={'required': u'密码不能为空', 'min_length': u'最少为8个字符'},
                               widget=forms.PasswordInput(attrs={'class': 'acct_password', 'placeholder': u'密码'}))

    def clean_name(self):
        cd = self.cleaned_data
        is_exsit = UserInfo.objects.filter(name__exact=cd['name'])
        if is_exsit:
            raise forms.ValidationError(message='昵称已存在', code='invalid')
        return cd['name']

    def clean_acct(self):
        cd = self.cleaned_data
        is_exsit = User.objects.filter(username__exact=cd['acct'])
        if is_exsit:
            raise forms.ValidationError(message='用户名已存在', code='invalid')
        return cd['acct']


class LoginForm(forms.Form):
    acct = forms.CharField(min_length=5,
                           error_messages={'required': u'用户名不能为空', 'min_length': u'最少为5个字符'},
                           widget=forms.TextInput(attrs={'class': 'acct_name', 'placeholder': u'用户名、手机号或邮箱'}))
    password = forms.CharField(min_length=8,
                               error_messages={'required': u'密码不能为空', 'min_length': u'最少为8个字符'},
                               widget=forms.PasswordInput(attrs={'class': 'acct_password', 'placeholder': u'密码'}))
    remember = forms.BooleanField(required=False, initial=False,
                                  widget=forms.CheckboxInput(attrs={"value": "true", "checked": "checked"}))

    def clean_acct(self):
        cd = self.cleaned_data
        is_exsit = User.objects.filter(username__exact=cd['acct'])
        if is_exsit is None:
            raise forms.ValidationError(message='用户名不存在', code='invalid')
        return cd['acct']


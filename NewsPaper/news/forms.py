from django.forms import ModelForm, CharField
from django.contrib.auth.models import Group

from allauth.account.forms import SignupForm

from .models import Post

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['postAuthor', 'postType', 'category', 'head', 'postText', ]

    #def __init__(self, *args, **kwargs):
    #    #user = kwargs.pop('user', '')
    #    super(PostForm, self).__init__(*args, **kwargs)
    #    self.fields['writer'] = ModelChoiceField(queryset=User.objects.all())
    #    self.fields['code'] = ModelChoiceField(queryset=Category.objects.all())

class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
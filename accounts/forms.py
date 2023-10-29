from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

class CommonSignupForm(SignupForm):
  
   def save(self, request):
       user = super(CommonSignupForm, self).save(request)
       basic_group = Group.objects.get_or_create(name='common')[0]
       basic_group.user_set.add(user)
       return user
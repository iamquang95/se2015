from django.db import models
from django.contrib.auth.models import User


class UserAccountManager(models.Manager):
    def create_user(self, username, name, email, password, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        # if not kwargs.get('username'):
            # raise ValueError('Users must have a valid username.')

        user = User.objects.create_user(username,
                                        email, password)
        user.first_name = name
        user.save()

        account = self.model(
            user=user,
            school=kwargs.get('school'),
            class_in_school=kwargs.get('class_in_school')
        )
        account.save()

        return account


class UserAccount(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    avatar = models.ImageField(
        upload_to='static/img/',
        default='static/img/default.jpg'
    )
    facebook_id = models.CharField(max_length=200, null=True, blank=True)

    # date_of_birth = models.DateField(null=True, blank=True)
    school = models.CharField(max_length=50, null=True, blank=True)
    class_in_school = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserAccountManager()

    @property
    def user__username(self):
        return self.user.username

    def __unicode__(self):
        return self.user.username

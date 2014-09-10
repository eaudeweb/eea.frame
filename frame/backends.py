from django.contrib.auth.backends import RemoteUserBackend
from django.contrib.auth.models import Group


class FrameUserBackend(RemoteUserBackend):
    def clean_username(self, userdata):
        self._userdata = userdata
        return userdata.get('user_id')

    def configure_user(self, user):
        for role in self._userdata.get('user_roles', []):
            group, new = Group.objects.get_or_create(name=role)
            group.user_set.add(user)
        return user


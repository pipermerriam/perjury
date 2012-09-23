from pyrite.generators import ModelGenerator, UsernameGenerator, SimplePasswordGenerator, EmailAddressGenerator
from django.contrib.auth.models import User


class UserGenerator(ModelGenerator):
    """
    Not quite here yet.
    """
    fields = (
            ('username', UsernameGenerator),
            ('password', SimplePasswordGenerator),
            ('email', EmailAddressGenerator),
            )
    model = User

    def __init__(self, *args, **kwargs):
        super(UserGenerator, self).__init__(*args, **kwargs)
        self.name_generator = FullNameGenerator(self.size).__iter__()

    def create_model(self, **kwargs):
        user = User.objects.create_user(**kwargs)
        user.first_name, user.last_name = self.name_generator.next()
        user.save()
        return user

from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from core.models import TimestampedModel
from post.models import Post
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser, PermissionsMixin, TimestampedModel):
    username = None
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + self.last_name


@receiver(post_save, sender=CustomUser)
def create_related_profile(sender, instance, created, *args, **kwargs):
    if instance and created:
        Profile.objects.create(user=instance)


class Profile(TimestampedModel):
    user = models.OneToOneField(
        'CustomUser', on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)
    # follows = models.ManyToManyField(
    #     'self',
    #     related_name='followed_by',
    #     symmetrical=False
    # )

    # likes = models.ManyToManyField(
    #     'Post',
    #     related_name='liked_by'
    # )

    def __str__(self):
        return self.user.get_full_name()

    # def follow(self, profile):
    #     """Follow `profile` if we're not already following `profile`."""
    #     self.follows.add(profile)

    # def unfollow(self, profile):
    #     """Unfollow `profile` if we're already following `profile`."""
    #     self.follows.remove(profile)

    # def is_following(self, profile):
    #     """Returns True if we're following `profile`; False otherwise."""
    #     return self.follows.filter(pk=profile.pk).exists()

    # def is_followed_by(self, profile):
    #     """Returns True if `profile` is following us; False otherwise."""
    #     return self.followed_by.filter(pk=profile.pk).exists()

    def like(self, post):
        """like `post` if we haven't already liked it."""
        self.likes.add(post)

    def unlike(self, post):
        """Unlike `post` if we've already liked it."""
        self.likes.remove(post)

    def has_liked(self, post):
        """Returns True if we have liked `post`; else False."""
        return self.likes.filter(pk=post.pk).exists()

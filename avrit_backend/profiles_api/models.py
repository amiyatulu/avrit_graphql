from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from PIL import Image
from avrit_backend.settings import MEDIA_ROOT


class UserProfileManager(BaseUserManager):
    """Helps Django work with our custom user model."""
    def create_user(self, email, name, password=None):
        """Creates a new user profile object."""
        if not email:
            raise ValueError("Users must have an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, name, password):
        """Creates and saves a new superuser with given details."""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff= True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Represents a user profile inside our system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)


    # Object manager is a class to manage the userprofile, giving it extra functionality

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Used to get a users full name."""

        return self.name

    def get_short_name(self):
        """Used to get a users short name."""

        return self.name



ALLOW_PUBLIC_VIEW = (
            ('Y','YES'),
            ('N','NO')
                   )
class ProfileDetails(models.Model):
    """Profile Details"""
    user = models.OneToOneField(UserProfile, primary_key=True, on_delete=models.CASCADE)
    address = models.TextField()
    research_interest = models.TextField()
    education = models.TextField(null=True,blank=True)
    experience = models.TextField(null=True,blank=True)
    publications = models.TextField(null=True,blank=True)
    allow_public_view = models.CharField(max_length=100, choices=ALLOW_PUBLIC_VIEW)
    arrange = models.CharField(max_length=225, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.allow_public_view:
            self.allow_public_view ='N'
        super(ProfileDetails, self).save(*args, **kwargs)
    def __str__(self):
        """Return profile user name"""
        return self.user.name

class ProfileImage(models.Model):
    """ProfileImage"""
    user = models.OneToOneField(UserProfile,
                    on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profileimagesdata")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if self.image.name:
            super(ProfileImage, self).save(*args, **kwargs)
            filename = MEDIA_ROOT + "/" + self.image.name
            size = (300,300)
            image = Image.open(filename)
            image.thumbnail(size,Image.ANTIALIAS)
            image.save(image.filename)        
    def __str__(self):
        """Return profile image"""
        return self.image.url  


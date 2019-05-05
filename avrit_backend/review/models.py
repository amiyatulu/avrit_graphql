from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager


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

class Post(models.Model):
    """Submit your content for review."""
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    title = models.CharField(max_length=225)
    SUB_TYPE = (
              ('EL', 'Evidence of Learning'),
              ('CG','Curriculum Guide'),
              ('TK','Assignment Task'), 
              ('WB','Workbook'),
              ('PC', 'Practical'),
              ('PJ', 'Project'),
              ('LM', 'Learning Material'),
              ('BS', 'Brainstorm'),
              ('OD', 'Others')
                )
    type_of_submission = models.CharField(max_length = 3, choices= SUB_TYPE)
    course_name = models.CharField(max_length=225)
    subject = models.CharField(max_length=225)
    description = models.TextField()
    backup_link = models.CharField(max_length=225,blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PostUpload(models.Model):
    """Post Upload"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="post_upload",
        related_query_name="post_upload",
    )
    description = models.TextField()
    revision = models.BooleanField(default=False)
    file_upload = models.FileField(upload_to="post")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        """Return post title"""
        return self.post.title

class PostComment(models.Model):
    """Post Comments"""
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="postcomments",
        related_query_name="postcomment",
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        """Return post title"""
        return self.post.title


class Review(models.Model):
    user_profile = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    post_id = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE,
        related_name="reviews",
        related_query_name="review",
        )
    description = models.TextField()
    backup_link = models.CharField(max_length=225,blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together= ('user_profile', 'post_id')

    def __str__(self):
        return self.post.title



class ReviewUpload(models.Model):
    """Post Upload"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="review_upload",
        related_query_name="review_upload",
    )
    description = models.TextField()
    revision = models.BooleanField(default=False)
    file_upload = models.FileField(upload_to="review")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        """Return post title"""
        return self.review.post_id.title


class ReviewComment(models.Model):
    """Review Comments"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="reviewcomments",
        related_query_name="reviewcomment",
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        """Return post title"""
        return self.review.post_id.title

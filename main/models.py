from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)


class TagValue(models.Model):
    value = models.CharField(max_length=20, unique=True)


class UsersTag(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)
    tag_value_id = models.ForeignKey(TagValue, on_delete=models.CASCADE)

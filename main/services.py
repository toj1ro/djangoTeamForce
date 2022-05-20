from .models import Tag, TagValue, UsersTag, User


def create_tag(tag: str):
    tag = tag.capitalize()
    tag_in_db = Tag.objects.filter(name=tag).first()
    if tag_in_db:
        return tag_in_db
    tag_new = Tag(name=tag)
    tag_new.save()
    return tag_new


def create_tag_value(value: str):
    value = value.capitalize()
    value_in_db = TagValue.objects.filter(value=value).first()
    if value_in_db:
        return value_in_db
    value_new = TagValue(value=value)
    value_new.save()
    return value_new


def create_user_tag_value(user: User, tag, value):
    user_tags_in_db = UsersTag.objects.filter(user_id=user, tag_id=tag, tag_value_id=value).first()
    if user_tags_in_db:
        return user_tags_in_db
    user_tags = UsersTag(user_id=user, tag_id=tag, tag_value_id=value)
    user_tags.save()


def get_user_tags(user_id):
    dict_ = {}
    user_tags = UsersTag.objects.filter(user_id=user_id).all()
    tags = [i.tag_id for i in user_tags]
    for tag in tags:
        values = [i.tag_value_id for i in UsersTag.objects.filter(user_id=user_id).filter(tag_id=tag.id).all()]
        dict_[tag] = values
    return dict_

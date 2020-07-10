#import string

from django.utils.text import slugify


#def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
  #  return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(model_instance ,title, slug_field):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    slug = slugify(title)
    model_class = model_instance.__class__
    while model_class._default_manager.filter(slug=slug).exists():
        object_pk = model_class._default_manager.latest('pk')
        object_pk = object_pk.pk+1

        slug = f'{slug}-{object_pk}'
    return slug 
    
    
    
    """if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug"""
    
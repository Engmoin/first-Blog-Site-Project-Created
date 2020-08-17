from django.db import models
from django.utils import timezone
from webapp1.utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.utils.text import slugify # new
from django.urls import reverse



# Create your models here
class PublishedManager(models.Manager):
      def get_queryset(self):
        return super(PublishedManager,
        self).get_queryset()\
          .filter(status='published')

class Post(models.Model):
  
    STATUS_CHOICES ={
      ('draft','Draft'),
      ('published','Published'),
      } 
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete= models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES, default='draft')
    objects = models.Manager() # the default Manager
    published = PublishedManager() # our custom Manager
    class Meta:
      ordering = ('-publish',)
    
    
    def __str__(self):
      return self.title 
      
    """def get_absolute_url(self):
       return reverse('post-detail', kwargs={'pk':self.pk,'slug':self.slug})"""

    def get_absolute_url(self):
      return reverse('post_detail', kwargs={
        'slug': self.slug 
        })

    """def slug_save(sender,instance,*args,**kwargs):
      if not instance.slug:
        instance.slug = unique_slug_generator(instance, instance.title, instance.slug)

pre_save.connect(slug_save, sender=Post)"""


class Comment(models.Model):
  post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
  name = models.CharField(max_length=80)
  email = models.EmailField()
  body = models.TextField()
  created = models.DateTimeField(auto_now_add=True)
  updated = models.DateTimeField(auto_now_add=True)
  active = models.BooleanField(default=True)

  class Meta:
    ordering =('created',)
  
  def __str__(self):
    return f'Comment by{self.name} on {self.post}'








        #return super().save(*args, **kwargs)

def slug_generator(sender,instance,*args,**kwargs):
  if not instance.slug:
    instance.slug = unique_slug_generator(instance)
    
def pre_save_post_recever(sender,instance,*args,**kwargs):
   slug = slugify(instance.title)
   exists = Post.objects.filter(slug=slug).exists()
   if exists:
     slug="%s-%s" %(slug,instance.id)
     instance.slug = slug




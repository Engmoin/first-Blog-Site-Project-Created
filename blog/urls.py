from django.urls import path
from django.conf.urls import url
from .views import( PostListView ,
 PostDetailView,
 PostCreateView,
 PostUpdateView,
 PostDeleteView,
UserPostListView,
)
from.import views
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    #path('latest/<int:pk>', views.PostLatest, name='post-latest'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
   # path('<slug:slug>/', views.post_detail, name='post-detail'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
   # url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'r'(?P<post>[-\w]+)/$',views.post_detail,name='post_detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    #path('post/<int:pk>/', PostDetailView.as_view, name='latest-post'),
    path('<int:post_id>/share/',views.post_share, name='post_share'),
    path('about/', views.about, name='blog-about'),
   
   
   

   
    
]

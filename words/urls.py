from django.urls import path

from words import views

app_name = 'words'
urlpatterns = [
    path('', views.WordListView.as_view(), name='all'),
    path('word/<int:pk>/', views.WordDetailView.as_view(), name='word_detail'),
    path('word/<int:pk>/favorite/', views.AddFavoriteView.as_view(), name='word_favorite'),
    path('word/<int:pk>/unfavorite/', views.DeleteFavoriteView.as_view(), name='word_unfavorite'),
    path('fav/', views.WordFavView.as_view(), name='word_fav'),
    path('word_translate/', views.WordTranslateView.as_view(), name='word_translate'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),

]

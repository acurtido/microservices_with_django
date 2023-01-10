from django.urls import path

from .views import *


urlpatterns = [
    path('categories', ListCategoriesView.as_view()),
    path('details/<slug>', CategoryDetailView.as_view()),
    path('create', CategoryCreateView.as_view()),
    path('edit', CategoryEditView.as_view()),
    path('delete', CategoryDeleteView.as_view()),
    path('popular', ListPopularTopicsView.as_view()),
]

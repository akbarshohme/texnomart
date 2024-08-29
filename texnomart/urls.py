from django.urls import path
from texnomart.views import CategoryListAPI, ProductListAPI, CreateCategoryView, DeleteCategoryView, \
    UpdateCategoryView, ProductDetailView, ProductUpdateView, ProductDeleteView, ProductAttribute, AttributeKeyListAPI, \
    AttributeValueListAPI
from texnomart.auth_views import LoginAPIView, LogoutAPIView, RegisterAPIView

urlpatterns = [
    #for category
    path('categories/', CategoryListAPI.as_view(), name='categories'),
    path('category/<slug:category_slug>/',ProductListAPI.as_view(), name='products'),
    path('category/add-category', CreateCategoryView.as_view(), name='add-category'),
    path('category/<slug:category_slug>/delete', DeleteCategoryView.as_view(), name='delete-category'),
    path('category/<slug:category_slug>/edit', UpdateCategoryView.as_view(), name='update-category'),

    #for product

    path('product/detail/<int:id>/', ProductDetailView.as_view()),
    path('product/<int:id>/edit/',ProductUpdateView.as_view()),
    path('product/<int:id>/delete/', ProductDeleteView.as_view()),

    #for attribute
    path('attribute-key/', AttributeKeyListAPI.as_view()),
    path('attribute-value/',AttributeValueListAPI.as_view()),

    #for authentication
    path('login/',LoginAPIView.as_view()),
    path('logout/',LogoutAPIView.as_view()),
    path('register/', RegisterAPIView.as_view()),






]
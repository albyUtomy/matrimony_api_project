from django.urls import path

from .views import (
    CreateCategoryView,
    UpdateCategory,
    DeleteCategoryAndValues, 
    AddCategoryValuesView,
    UpdateCategoryValues,
    ListCategory,
    ListCategoryValues,
    )

from .views_subscription import (SubscriptionAPIView)

urlpatterns = [
    path('create_category/', CreateCategoryView.as_view(), name='create-category'),
    path('category/<int:category_id>/add_values/', AddCategoryValuesView.as_view(), name='add-category-values'),
    path('update_category/<int:category_id>/', UpdateCategory.as_view(), name='update-category'),
    path('categories/<int:category_id>/values/<int:category_value_id>/update/', UpdateCategoryValues.as_view(), name='update-category-value'),
    path('categories/', ListCategory.as_view(), name='list-all-categories'),
    path('categories/<int:category_id>/values/', ListCategoryValues.as_view(), name='category_values'),
    path('category/<int:category_id>/delete/', DeleteCategoryAndValues.as_view(), name='delete-category'),
    path('subscriptions/', SubscriptionAPIView.as_view(), name='subscriptions-list'),
    path('subscriptions/<int:subscription_id>/', SubscriptionAPIView.as_view(), name='subscription-detail'),
]
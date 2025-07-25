from django.urls import path
from . import views

urlpatterns = [
    path('properties/', views.PropertyListView.as_view(), name='property-list'),
    path('properties/<int:pk>/', views.PropertyDetailView.as_view(), name='property-detail'),
    path('properties/<int:property_id>/tax/', views.property_tax_calculation, name='property-tax'),
    path('neighborhoods/', views.neighborhood_list, name='neighborhood-list'),
    path('owner-types/', views.owner_type_list, name='owner-type-list'),
    path('purposes/', views.property_purpose_list, name='property-purpose-list'),
    path('age-factors/', views.age_factor_list, name='age-factor-list'),
    path('addresses/', views.address_list, name='address-list'),
    path('statistics/', views.tax_statistics, name='tax-statistics'),
    path('calculate-tax/', views.calculate_tax, name='calculate-tax'),
    path('simulate-tax/', views.simulate_tax, name='simulate-tax'),
]

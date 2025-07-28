from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import (
    Neighborhood, OwnerType, PropertyPurpose, AgeFactor, 
    ConstructionPrice, Address, Property, FimipaIpra
)

@admin.register(Neighborhood)
class NeighborhoodAdmin(SimpleHistoryAdmin):
    list_display = ['cod_b1', 'cod_b', 'description', 'factor']
    list_filter = ['factor']
    search_fields = ['description', 'cod_b1', 'cod_b']
    ordering = ['cod_b1']

@admin.register(OwnerType)
class OwnerTypeAdmin(SimpleHistoryAdmin):
    list_display = ['code', 'description']
    search_fields = ['description', 'code']
    ordering = ['code']

@admin.register(PropertyPurpose)
class PropertyPurposeAdmin(SimpleHistoryAdmin):
    list_display = ['code', 'description']
    search_fields = ['description', 'code']
    ordering = ['code']

@admin.register(AgeFactor)
class AgeFactorAdmin(SimpleHistoryAdmin):
    list_display = ['code', 'id_range', 'residential_factor', 'commercial_factor']
    list_filter = ['residential_factor', 'commercial_factor']
    search_fields = ['code', 'id_range']
    ordering = ['code']

@admin.register(ConstructionPrice)
class ConstructionPriceAdmin(SimpleHistoryAdmin):
    list_display = ['year', 'price']
    list_filter = ['year']
    ordering = ['-year']

@admin.register(Address)
class AddressAdmin(SimpleHistoryAdmin):
    list_display = ['cod_r', 'street_name']
    search_fields = ['street_name', 'cod_r']
    ordering = ['cod_r']

@admin.register(Property)
class PropertyAdmin(SimpleHistoryAdmin):
    list_display = ['ncontr', 'name', 'neighborhood', 'owner_type', 'purpose', 'patrimonial_value']
    list_filter = ['neighborhood', 'owner_type', 'purpose', 'property_type']
    search_fields = ['ncontr', 'name', 'matrix', 'nuit']
    raw_id_fields = ['neighborhood', 'owner_type', 'purpose']
    ordering = ['ncontr']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('ncontr', 'name', 'status', 'ipra_code', 'matrix')
        }),
        ('Location', {
            'fields': ('location_code', 'neighborhood', 'entrance_number', 'floor_number', 'flat', 'room', 'house_number', 'district_code')
        }),
        ('Property Details', {
            'fields': ('property_type', 'purpose', 'built_area', 'land_area', 'age_type', 'age_factor_code')
        }),
        ('Owner Information', {
            'fields': ('owner_type', 'contact_phone', 'previous_contract', 'nuit')
        }),
        ('Financial', {
            'fields': ('patrimonial_value', 'price', 'location_factor', 'collection')
        }),
        ('Timestamps', {
            'fields': ('creation_date', 'creation_date_alt', 'creation_time_alt'),
            'classes': ('collapse',)
        }),
    )

@admin.register(FimipaIpra)
class FimipaIpraAdmin(SimpleHistoryAdmin):
    list_display = ['ncontr', 'ipra_value', 'year']
    list_filter = ['year']
    search_fields = ['ncontr']
    ordering = ['ncontr']

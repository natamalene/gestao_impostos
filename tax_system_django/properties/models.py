from django.db import models
from simple_history.models import HistoricalRecords

class Neighborhood(models.Model):
    cod_b1 = models.IntegerField(unique=True)
    cod_b = models.IntegerField()
    description = models.CharField(max_length=255)
    cod_dist_urb = models.CharField(max_length=255, null=True, blank=True)
    factor = models.FloatField()
    history = HistoricalRecords()
    
    class Meta:
        db_table = 'neighborhoods'
        indexes = [
            models.Index(fields=['cod_b1']),
            models.Index(fields=['cod_b']),
        ]
    
    def __str__(self):
        return self.description

class OwnerType(models.Model):
    code = models.IntegerField(unique=True)
    description = models.CharField(max_length=255)
    history = HistoricalRecords()
    
    class Meta:
        db_table = 'owner_types'
    
    def __str__(self):
        return self.description

class PropertyPurpose(models.Model):
    code = models.IntegerField(unique=True)
    description = models.CharField(max_length=255)
    history = HistoricalRecords()
    
    class Meta:
        db_table = 'property_purposes'
    
    def __str__(self):
        return self.description

class AgeFactor(models.Model):
    code = models.CharField(max_length=10, unique=True)
    id_range = models.CharField(max_length=20)
    residential_factor = models.FloatField()
    commercial_factor = models.FloatField()
    history = HistoricalRecords()
    
    class Meta:
        db_table = 'age_factors'
    
    def __str__(self):
        return f"{self.code} - {self.id_range}"

class ConstructionPrice(models.Model):
    price = models.FloatField()
    year = models.IntegerField()
    history = HistoricalRecords()
    
    class Meta:
        db_table = 'construction_prices'
        unique_together = ['year']
    
    def __str__(self):
        return f"{self.year}: {self.price}"

class Address(models.Model):
    cod_r = models.CharField(max_length=10, unique=True)
    street_name = models.CharField(max_length=255)
    history = HistoricalRecords()
    
    class Meta:
        db_table = 'addresses'
        indexes = [
            models.Index(fields=['cod_r']),
        ]
    
    def __str__(self):
        return self.street_name

class Property(models.Model):
    ncontr = models.IntegerField(unique=True)
    status = models.CharField(max_length=10, null=True, blank=True)
    ipra_code = models.FloatField(null=True, blank=True)
    matrix = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    location_code = models.CharField(max_length=255, null=True, blank=True)
    entrance_number = models.CharField(max_length=255, null=True, blank=True)
    floor_number = models.CharField(max_length=255, null=True, blank=True)
    flat = models.CharField(max_length=255, null=True, blank=True)
    room = models.CharField(max_length=255, null=True, blank=True)
    house_number = models.CharField(max_length=255, null=True, blank=True)
    district_code = models.FloatField(null=True, blank=True)
    neighborhood = models.ForeignKey(Neighborhood, on_delete=models.SET_NULL, null=True, blank=True, to_field='cod_b1')
    property_type = models.CharField(max_length=10, null=True, blank=True)
    location_factor = models.FloatField(null=True, blank=True)
    collection = models.FloatField(null=True, blank=True)
    patrimonial_value = models.FloatField(null=True, blank=True)
    owner_type = models.ForeignKey(OwnerType, on_delete=models.SET_NULL, null=True, blank=True, to_field='code')
    contact_phone = models.CharField(max_length=255, null=True, blank=True)
    previous_contract = models.CharField(max_length=255, null=True, blank=True)
    nuit = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    age_type = models.CharField(max_length=10, null=True, blank=True)
    age_factor_code = models.CharField(max_length=10, null=True, blank=True)
    land_area = models.CharField(max_length=255, null=True, blank=True)
    built_area = models.CharField(max_length=255, null=True, blank=True)
    purpose = models.ForeignKey(PropertyPurpose, on_delete=models.SET_NULL, null=True, blank=True, to_field='code')
    creation_date = models.DateTimeField(null=True, blank=True)
    creation_date_alt = models.CharField(max_length=200, null=True, blank=True)
    creation_time_alt = models.CharField(max_length=200, null=True, blank=True)
    history = HistoricalRecords()
    
    class Meta:
        db_table = 'properties'
        indexes = [
            models.Index(fields=['ncontr']),
            models.Index(fields=['neighborhood']),
            models.Index(fields=['owner_type']),
            models.Index(fields=['purpose']),
            models.Index(fields=['location_code']),
        ]
    
    def __str__(self):
        return f"{self.ncontr} - {self.name or 'Unnamed Property'}"
    
    @property
    def address(self):
        if self.location_code:
            try:
                return Address.objects.get(cod_r=self.location_code)
            except Address.DoesNotExist:
                return None
        return None

class FimipaIpra(models.Model):
    ncontr = models.IntegerField(unique=True)
    ipra_value = models.FloatField(null=True, blank=True)
    year = models.IntegerField(default=2025)
    history = HistoricalRecords()
    
    class Meta:
        db_table = 'fimipa_ipra'
        indexes = [
            models.Index(fields=['ncontr']),
        ]
    
    def __str__(self):
        return f"NCONTR {self.ncontr}: {self.ipra_value}"

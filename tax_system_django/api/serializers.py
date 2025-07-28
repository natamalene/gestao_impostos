from rest_framework import serializers
from properties.models import (
    Property, Neighborhood, OwnerType, PropertyPurpose, 
    AgeFactor, Address, FimipaIpra
)

class NeighborhoodSerializer(serializers.ModelSerializer):
    descricao = serializers.CharField(source='description')
    fact = serializers.FloatField(source='factor')
    
    class Meta:
        model = Neighborhood
        fields = ['id', 'cod_b1', 'cod_b', 'descricao', 'fact']

class OwnerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerType
        fields = ['id', 'code', 'description']

class PropertyPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyPurpose
        fields = ['id', 'code', 'description']

class AgeFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgeFactor
        fields = ['id', 'code', 'id_range', 'residential_factor', 'commercial_factor']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'cod_r', 'street_name']

class PropertySerializer(serializers.ModelSerializer):
    codigo = serializers.IntegerField(source='ncontr')
    nome = serializers.CharField(source='name')
    matriz = serializers.CharField(source='matrix')
    valpatr = serializers.FloatField(source='patrimonial_value')
    bairro = serializers.CharField(source='neighborhood.description', read_only=True)
    localizacao = serializers.SerializerMethodField()
    proprietar = serializers.IntegerField(source='owner_type_id')
    ipra_value = serializers.SerializerMethodField()
    
    neighborhood_name = serializers.CharField(source='neighborhood.description', read_only=True)
    owner_type_name = serializers.CharField(source='owner_type.description', read_only=True)
    purpose_name = serializers.CharField(source='purpose.description', read_only=True)
    address_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = [
            'id', 'codigo', 'nome', 'matriz', 'valpatr', 'ipra_value', 'bairro', 
            'proprietar', 'nuit', 'localizacao', 'ncontr', 'status', 'ipra_code',
            'location_code', 'entrance_number', 'floor_number', 'flat', 'room', 'house_number',
            'district_code', 'neighborhood', 'neighborhood_name', 'property_type',
            'location_factor', 'collection', 'patrimonial_value', 'owner_type', 'owner_type_name',
            'contact_phone', 'previous_contract', 'price', 'age_type', 'age_factor_code',
            'land_area', 'built_area', 'purpose', 'purpose_name', 'address_name',
            'creation_date', 'creation_date_alt', 'creation_time_alt'
        ]
    
    def get_localizacao(self, obj):
        if obj.location_code:
            try:
                address = Address.objects.get(cod_r=obj.location_code)
                return address.street_name
            except Address.DoesNotExist:
                return None
        return None
    
    def get_address_name(self, obj):
        return self.get_localizacao(obj)
    
    def get_ipra_value(self, obj):
        try:
            from properties.models import FimipaIpra
            fimipa = FimipaIpra.objects.get(ncontr=obj.ncontr)
            return fimipa.ipra_value
        except FimipaIpra.DoesNotExist:
            return None

class PropertyUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = [
            'name', 'neighborhood', 'owner_type', 'purpose', 'built_area', 'land_area',
            'age_factor_code', 'property_type', 'contact_phone', 'nuit'
        ]

class FimipaIpraSerializer(serializers.ModelSerializer):
    class Meta:
        model = FimipaIpra
        fields = ['id', 'ncontr', 'ipra_value', 'year']

class TaxCalculationSerializer(serializers.Serializer):
    built_area = serializers.FloatField()
    construction_price = serializers.FloatField()
    age_factor = serializers.FloatField()
    logradouro_area = serializers.FloatField()
    location_factor = serializers.FloatField()
    property_type = serializers.CharField(default="residential")

class TaxSimulationSerializer(serializers.Serializer):
    built_area = serializers.FloatField()
    land_area = serializers.FloatField(default=0.0)
    neighborhood_id = serializers.IntegerField()
    age_factor_code = serializers.CharField()
    purpose_id = serializers.IntegerField(default=1)

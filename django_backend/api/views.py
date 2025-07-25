from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.shortcuts import get_object_or_404
from properties.models import (
    Property, Neighborhood, OwnerType, PropertyPurpose, 
    AgeFactor, Address, FimipaIpra
)
from properties.services import TaxCalculator
from .serializers import (
    PropertySerializer, PropertyUpdateSerializer, NeighborhoodSerializer,
    OwnerTypeSerializer, PropertyPurposeSerializer, AgeFactorSerializer,
    AddressSerializer, FimipaIpraSerializer, TaxCalculationSerializer,
    TaxSimulationSerializer
)

class PropertyPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

class PropertyListView(generics.ListCreateAPIView):
    serializer_class = PropertySerializer
    pagination_class = PropertyPagination
    
    def get_queryset(self):
        queryset = Property.objects.select_related('neighborhood', 'owner_type', 'purpose').all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(ncontr__icontains=search) |
                Q(matrix__icontains=search) |
                Q(nuit__icontains=search)
            )
        return queryset.order_by('ncontr')
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        limit = int(request.query_params.get('limit', 20))
        skip = int(request.query_params.get('skip', 0))
        
        total = queryset.count()
        queryset = queryset[skip:skip + limit]
        
        serializer = self.get_serializer(queryset, many=True)
        
        return Response({
            'total': total,
            'skip': skip,
            'limit': limit,
            'properties': serializer.data
        })

class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.select_related('neighborhood', 'owner_type', 'purpose').all()
    serializer_class = PropertySerializer
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = PropertyUpdateSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        full_serializer = PropertySerializer(instance)
        return Response(full_serializer.data)

@api_view(['GET'])
def property_tax_calculation(request, property_id):
    try:
        calculator = TaxCalculator()
        result = calculator.calculate_property_tax(property_id)
        return Response(result)
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def neighborhood_list(request):
    neighborhoods = Neighborhood.objects.all().order_by('cod_b1')
    serializer = NeighborhoodSerializer(neighborhoods, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def owner_type_list(request):
    owner_types = OwnerType.objects.all().order_by('code')
    serializer = OwnerTypeSerializer(owner_types, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def property_purpose_list(request):
    purposes = PropertyPurpose.objects.all().order_by('code')
    serializer = PropertyPurposeSerializer(purposes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def age_factor_list(request):
    age_factors = AgeFactor.objects.all().order_by('code')
    serializer = AgeFactorSerializer(age_factors, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def address_list(request):
    addresses = Address.objects.all().order_by('cod_r')
    serializer = AddressSerializer(addresses, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def tax_statistics(request):
    calculator = TaxCalculator()
    stats = calculator.get_tax_statistics()
    return Response(stats)

@api_view(['POST'])
def calculate_tax(request):
    serializer = TaxCalculationSerializer(data=request.data)
    if serializer.is_valid():
        calculator = TaxCalculator()
        result = calculator.calculate_ipra_tax(**serializer.validated_data)
        return Response(result)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def simulate_tax(request):
    serializer = TaxSimulationSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        calculator = TaxCalculator()
        
        construction_price = calculator.get_construction_price()
        age_factor = calculator.get_age_factor(data['age_factor_code'], data['purpose_id'])
        location_factor = calculator.get_neighborhood_factor(data['neighborhood_id'])
        property_type = "commercial" if data['purpose_id'] == 2 else "residential"
        
        result = calculator.calculate_ipra_tax(
            built_area=data['built_area'],
            construction_price=construction_price,
            age_factor=age_factor,
            logradouro_area=data['land_area'],
            location_factor=location_factor,
            property_type=property_type
        )
        return Response(result)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

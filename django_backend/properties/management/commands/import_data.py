import os
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from properties.models import (
    Neighborhood, OwnerType, PropertyPurpose, AgeFactor, 
    ConstructionPrice, Address, Property, FimipaIpra
)

class Command(BaseCommand):
    help = 'Import data from Excel files'
    
    def add_arguments(self, parser):
        parser.add_argument('--data-dir', type=str, default='data', help='Directory containing Excel files')
    
    def handle(self, *args, **options):
        data_dir = options['data_dir']
        
        if not os.path.exists(data_dir):
            self.stdout.write(self.style.ERROR(f'Data directory {data_dir} does not exist'))
            return
        
        try:
            self.import_neighborhoods(data_dir)
            self.import_owner_types(data_dir)
            self.import_purposes(data_dir)
            self.import_age_factors(data_dir)
            self.import_construction_prices(data_dir)
            self.import_addresses(data_dir)
            self.import_properties(data_dir)
            self.import_fimipa_ipra(data_dir)
            
            self.stdout.write(self.style.SUCCESS('Successfully imported all data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {str(e)}'))
    
    def import_neighborhoods(self, data_dir):
        file_path = os.path.join(data_dir, 'Bairros.xlsx')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'File {file_path} not found, skipping neighborhoods'))
            return
        
        df = pd.read_excel(file_path)
        self.stdout.write(f'Importing {len(df)} neighborhoods...')
        
        with transaction.atomic():
            for _, row in df.iterrows():
                Neighborhood.objects.get_or_create(
                    cod_b1=int(row['Cod_B1']),
                    defaults={
                        'cod_b': int(row['Cod_B1']),
                        'description': str(row['Descricao']),
                        'cod_dist_urb': str(row['Cod_DistUrb']) if pd.notna(row['Cod_DistUrb']) else None,
                        'factor': float(row['fact'])
                    }
                )
    
    def import_owner_types(self, data_dir):
        file_path = os.path.join(data_dir, 'TblPROPRIETARIO.xlsx')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'File {file_path} not found, skipping owner types'))
            return
        
        df = pd.read_excel(file_path)
        self.stdout.write(f'Importing {len(df)} owner types...')
        
        with transaction.atomic():
            for _, row in df.iterrows():
                OwnerType.objects.get_or_create(
                    code=int(row['CODIGO']),
                    defaults={'description': str(row['DESCRICAO'])}
                )
    
    def import_purposes(self, data_dir):
        file_path = os.path.join(data_dir, 'TblFINALIDADE.xlsx')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'File {file_path} not found, skipping purposes'))
            return
        
        df = pd.read_excel(file_path)
        self.stdout.write(f'Importing {len(df)} purposes...')
        
        with transaction.atomic():
            for _, row in df.iterrows():
                PropertyPurpose.objects.get_or_create(
                    code=int(row['CODIGO']),
                    defaults={'description': str(row['DESCRICAO'])}
                )
    
    def import_age_factors(self, data_dir):
        file_path = os.path.join(data_dir, 'tblfactant.xlsx')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'File {file_path} not found, skipping age factors'))
            return
        
        df = pd.read_excel(file_path)
        self.stdout.write(f'Importing {len(df)} age factors...')
        
        with transaction.atomic():
            for _, row in df.iterrows():
                AgeFactor.objects.get_or_create(
                    code=str(row['cod']),
                    defaults={
                        'id_range': str(row['id']),
                        'residential_factor': float(row['tiphab']),
                        'commercial_factor': float(row['tipcom'])
                    }
                )
    
    def import_construction_prices(self, data_dir):
        file_path = os.path.join(data_dir, 'tblp.xlsx')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'File {file_path} not found, skipping construction prices'))
            return
        
        df = pd.read_excel(file_path)
        self.stdout.write(f'Importing {len(df)} construction prices...')
        
        with transaction.atomic():
            for _, row in df.iterrows():
                ConstructionPrice.objects.get_or_create(
                    year=int(row['Ano']),
                    defaults={'price': float(row['Preco'])}
                )
    
    def import_addresses(self, data_dir):
        file_path = os.path.join(data_dir, 'FENDEREC.xlsx')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'File {file_path} not found, skipping addresses'))
            return
        
        df = pd.read_excel(file_path)
        self.stdout.write(f'Importing {len(df)} addresses...')
        
        with transaction.atomic():
            for _, row in df.iterrows():
                Address.objects.get_or_create(
                    cod_r=str(row['COD_R']),
                    defaults={'street_name': str(row['MORADA'])}
                )
    
    def import_properties(self, data_dir):
        file_path = os.path.join(data_dir, 'FCADIPA.xlsx')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'File {file_path} not found, skipping properties'))
            return
        
        df = pd.read_excel(file_path)
        self.stdout.write(f'Importing {len(df)} properties...')
        
        with transaction.atomic():
            for _, row in df.iterrows():
                try:
                    neighborhood = None
                    if pd.notna(row['cod_bairro']):
                        try:
                            neighborhood = Neighborhood.objects.get(cod_b1=int(row['cod_bairro']))
                        except Neighborhood.DoesNotExist:
                            pass
                    
                    owner_type = None
                    if pd.notna(row['PROPRIETAR']):
                        try:
                            owner_type = OwnerType.objects.get(code=int(row['PROPRIETAR']))
                        except OwnerType.DoesNotExist:
                            pass
                    
                    purpose = None
                    if pd.notna(row.get('finalidade_id')):
                        try:
                            purpose = PropertyPurpose.objects.get(code=int(row['finalidade_id']))
                        except PropertyPurpose.DoesNotExist:
                            pass
                    
                    Property.objects.get_or_create(
                        ncontr=int(row['NCONTR']),
                        defaults={
                            'status': str(row['SITUA']) if pd.notna(row['SITUA']) else None,
                            'ipra_code': float(row['CODIPRA']) if pd.notna(row['CODIPRA']) else None,
                            'matrix': str(row['MATRIZ']) if pd.notna(row['MATRIZ']) else None,
                            'name': str(row['NOME']) if pd.notna(row['NOME']) else None,
                            'location_code': str(row['Cod_LOCALIZACA']) if pd.notna(row['Cod_LOCALIZACA']) else None,
                            'entrance_number': str(row['NU_ENTRADA']) if pd.notna(row['NU_ENTRADA']) else None,
                            'floor_number': str(row['Andar_N']) if pd.notna(row['Andar_N']) else None,
                            'flat': str(row['Flat']) if pd.notna(row['Flat']) else None,
                            'room': str(row['QRT']) if pd.notna(row['QRT']) else None,
                            'house_number': str(row['Nu_casa']) if pd.notna(row['Nu_casa']) else None,
                            'district_code': float(row['cod_DISTR_MUNI']) if pd.notna(row['cod_DISTR_MUNI']) else None,
                            'neighborhood': neighborhood,
                            'property_type': str(row['TIPHAB']) if pd.notna(row['TIPHAB']) else None,
                            'location_factor': float(row['Fl']) if pd.notna(row['Fl']) else None,
                            'collection': float(row['RECOLEC']) if pd.notna(row['RECOLEC']) else None,
                            'patrimonial_value': float(row['VALPATR']) if pd.notna(row['VALPATR']) else None,
                            'owner_type': owner_type,
                            'contact_phone': str(row['TELEF_CONT']) if pd.notna(row['TELEF_CONT']) else None,
                            'previous_contract': str(row['CONTR_ANTE']) if pd.notna(row['CONTR_ANTE']) else None,
                            'nuit': str(row['NUIT']) if pd.notna(row['NUIT']) else None,
                            'price': float(row['Preco']) if pd.notna(row['Preco']) else None,
                            'age_type': str(row['Thidade']) if pd.notna(row['Thidade']) else None,
                            'age_factor_code': str(row['Factant']) if pd.notna(row['Factant']) else None,
                            'land_area': str(row['ARE_TERENO']) if pd.notna(row['ARE_TERENO']) else None,
                            'built_area': str(row['ARE_CONSTR']) if pd.notna(row['ARE_CONSTR']) else None,
                            'purpose': purpose,
                            'creation_date_alt': str(row['DATA_CR_AL']) if pd.notna(row['DATA_CR_AL']) else None,
                            'creation_time_alt': str(row['HORA_CR_AL']) if pd.notna(row['HORA_CR_AL']) else None,
                        }
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error importing property {row["NCONTR"]}: {str(e)}'))
    
    def import_fimipa_ipra(self, data_dir):
        file_path = os.path.join(data_dir, 'FIMIPA2.xlsx')
        if not os.path.exists(file_path):
            self.stdout.write(self.style.WARNING(f'File {file_path} not found, skipping FIMIPA IPRA'))
            return
        
        df = pd.read_excel(file_path)
        self.stdout.write(f'Importing {len(df)} FIMIPA IPRA records...')
        
        with transaction.atomic():
            for _, row in df.iterrows():
                try:
                    FimipaIpra.objects.get_or_create(
                        ncontr=int(row['NCONTR']),
                        defaults={
                            'ipra_value': float(row['IIMPPAG']) if pd.notna(row['IIMPPAG']) else None,
                            'year': 2025
                        }
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error importing FIMIPA IPRA {row["NCONTR"]}: {str(e)}'))

import pandas as pd
from sqlalchemy.orm import Session
from .models import (
    Bairro, TipoProprietario, Finalidade, FatorAntiguidade, 
    PrecoReferencia, Endereco, Propriedade
)
from .database import SessionLocal
import os
from datetime import datetime

class DataImporter:
    def __init__(self, excel_files_path: str):
        self.excel_files_path = excel_files_path
        self.db = SessionLocal()
    
    def import_all_data(self):
        """Import data from all Excel files"""
        try:
            print("Starting data import...")
            
            self.import_bairros()
            self.import_tipos_proprietario()
            self.import_finalidades()
            self.import_fatores_antiguidade()
            self.import_precos_referencia()
            self.import_enderecos()
            
            self.import_propriedades()
            
            print("Data import completed successfully!")
            
        except Exception as e:
            print(f"Error during data import: {e}")
            self.db.rollback()
            raise
        finally:
            self.db.close()
    
    def import_bairros(self):
        """Import neighborhoods data"""
        file_path = os.path.join(self.excel_files_path, "Bairros.xlsx")
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
            
        df = pd.read_excel(file_path)
        print(f"Importing {len(df)} neighborhoods...")
        
        imported_count = 0
        for _, row in df.iterrows():
            existing = self.db.query(Bairro).filter(Bairro.cod_b1 == int(row['Cod_B1'])).first()
            if existing:
                continue
                
            bairro = Bairro(
                cod_b1=int(row['Cod_B1']),
                cod_b=int(row['Cod_B1']),
                descricao=str(row['Descricao']),
                cod_dist_urb=str(row['Cod_DistUrb']) if pd.notna(row['Cod_DistUrb']) else None,
                fact=float(row['fact'])
            )
            self.db.add(bairro)
            imported_count += 1
        
        self.db.commit()
        print(f"Neighborhoods imported successfully! Imported: {imported_count}")
    
    def import_tipos_proprietario(self):
        """Import owner types data"""
        file_path = os.path.join(self.excel_files_path, "TblPROPRIETARIO.xlsx")
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
            
        df = pd.read_excel(file_path)
        print(f"Importing {len(df)} owner types...")
        
        imported_count = 0
        for _, row in df.iterrows():
            existing = self.db.query(TipoProprietario).filter(TipoProprietario.codigo == int(row['CODIGO'])).first()
            if existing:
                continue
                
            tipo = TipoProprietario(
                codigo=int(row['CODIGO']),
                descricao=str(row['DESCRICAO'])
            )
            self.db.add(tipo)
            imported_count += 1
        
        self.db.commit()
        print(f"Owner types imported successfully! Imported: {imported_count}")
    
    def import_finalidades(self):
        """Import property purposes data"""
        file_path = os.path.join(self.excel_files_path, "TblFINALIDADE.xlsx")
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
            
        df = pd.read_excel(file_path)
        print(f"Importing {len(df)} property purposes...")
        
        imported_count = 0
        for _, row in df.iterrows():
            existing = self.db.query(Finalidade).filter(Finalidade.codigo == int(row['CODIGO'])).first()
            if existing:
                continue
                
            finalidade = Finalidade(
                codigo=int(row['CODIGO']),
                descricao=str(row['DESCRICAO'])
            )
            self.db.add(finalidade)
            imported_count += 1
        
        self.db.commit()
        print(f"Property purposes imported successfully! Imported: {imported_count}")
    
    def import_fatores_antiguidade(self):
        """Import age factors data"""
        file_path = os.path.join(self.excel_files_path, "tblfactant.xlsx")
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
            
        df = pd.read_excel(file_path)
        print(f"Importing {len(df)} age factors...")
        
        imported_count = 0
        for _, row in df.iterrows():
            existing = self.db.query(FatorAntiguidade).filter(FatorAntiguidade.cod == str(row['cod'])).first()
            if existing:
                continue
                
            fator = FatorAntiguidade(
                cod=str(row['cod']),
                id_range=str(row['id']),
                tiphab=float(row['tiphab']),
                tipcom=float(row['tipcom'])
            )
            self.db.add(fator)
            imported_count += 1
        
        self.db.commit()
        print(f"Age factors imported successfully! Imported: {imported_count}")
    
    def import_precos_referencia(self):
        """Import reference prices data"""
        file_path = os.path.join(self.excel_files_path, "tblp.xlsx")
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
            
        df = pd.read_excel(file_path)
        print(f"Importing {len(df)} reference prices...")
        
        for _, row in df.iterrows():
            preco = PrecoReferencia(
                preco=float(row['Preco']),
                ano=int(row['Ano'])
            )
            self.db.add(preco)
        
        self.db.commit()
        print("Reference prices imported successfully!")
    
    def import_enderecos(self):
        """Import addresses data"""
        file_path = os.path.join(self.excel_files_path, "FENDEREC.xlsx")
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
            
        df = pd.read_excel(file_path)
        print(f"Importing {len(df)} addresses...")
        
        imported_count = 0
        for _, row in df.iterrows():
            existing = self.db.query(Endereco).filter(Endereco.cod_r == str(row['COD_R'])).first()
            if existing:
                continue
                
            endereco = Endereco(
                cod_r=str(row['COD_R']),
                morada=str(row['MORADA'])
            )
            self.db.add(endereco)
            imported_count += 1
        
        self.db.commit()
        print(f"Addresses imported successfully! Imported: {imported_count}")
    
    def import_propriedades(self):
        """Import properties data (main table)"""
        file_path = os.path.join(self.excel_files_path, "FCADIPA.xlsx")
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
            
        df = pd.read_excel(file_path)
        print(f"Importing {len(df)} properties...")
        
        df_unique = df.drop_duplicates(subset=['NCONTR'], keep='first')
        print(f"After removing duplicates: {len(df_unique)} unique properties")
        
        batch_size = 1000
        imported_count = 0
        error_count = 0
        
        for i in range(0, len(df_unique), batch_size):
            batch = df_unique.iloc[i:i+batch_size]
            
            for _, row in batch.iterrows():
                try:
                    existing = self.db.query(Propriedade).filter(Propriedade.ncontr == int(row['NCONTR'])).first()
                    if existing:
                        continue
                    
                    propriedade = Propriedade(
                        ncontr=int(row['NCONTR']),
                        situa=str(row['SITUA']) if pd.notna(row['SITUA']) else None,
                        codipra=float(row['CODIPRA']) if pd.notna(row['CODIPRA']) else None,
                        matriz=str(row['MATRIZ']) if pd.notna(row['MATRIZ']) else None,
                        nome=str(row['NOME']) if pd.notna(row['NOME']) else None,
                        cod_localizaca=str(row['Cod_LOCALIZACA']) if pd.notna(row['Cod_LOCALIZACA']) else None,
                        endereco_cod=str(row['Cod_LOCALIZACA']) if pd.notna(row['Cod_LOCALIZACA']) else None,
                        nu_entrada=str(row['NU_ENTRADA']) if pd.notna(row['NU_ENTRADA']) else None,
                        andar_n=str(row['Andar_N']) if pd.notna(row['Andar_N']) else None,
                        flat=str(row['Flat']) if pd.notna(row['Flat']) else None,
                        qrt=str(row['QRT']) if pd.notna(row['QRT']) else None,
                        nu_casa=str(row['Nu_casa']) if pd.notna(row['Nu_casa']) else None,
                        cod_distr_muni=float(row['cod_DISTR_MUNI']) if pd.notna(row['cod_DISTR_MUNI']) else None,
                        cod_bairro=int(row['cod_bairro']) if pd.notna(row['cod_bairro']) else None,
                        tiphab=str(row['TIPHAB']) if pd.notna(row['TIPHAB']) else None,
                        fl=float(row['Fl']) if pd.notna(row['Fl']) else None,
                        recolec=float(row['RECOLEC']) if pd.notna(row['RECOLEC']) else None,
                        valpatr=float(row['VALPATR']) if pd.notna(row['VALPATR']) else None,
                        proprietar=int(row['PROPRIETAR']) if pd.notna(row['PROPRIETAR']) else None,
                        telef_cont=str(row['TELEF_CONT']) if pd.notna(row['TELEF_CONT']) else None,
                        contr_ante=str(row['CONTR_ANTE']) if pd.notna(row['CONTR_ANTE']) else None,
                        nuit=str(row['NUIT']) if pd.notna(row['NUIT']) else None,
                        preco=float(row['Preco']) if pd.notna(row['Preco']) else None,
                        thidade=str(row['Thidade']) if pd.notna(row['Thidade']) else None,
                        factant=str(row['Factant']) if pd.notna(row['Factant']) else None,
                        are_tereno=str(row['ARE_TERENO']) if pd.notna(row['ARE_TERENO']) else None,
                        are_constr=str(row['ARE_CONSTR']) if pd.notna(row['ARE_CONSTR']) else None,
                        data_cria=row['DATA_CRIA'] if pd.notna(row['DATA_CRIA']) else None,
                        data_cr_al=str(row['DATA_CR_AL']) if pd.notna(row['DATA_CR_AL']) else None,
                        hora_cr_al=str(row['HORA_CR_AL']) if pd.notna(row['HORA_CR_AL']) else None
                    )
                    self.db.add(propriedade)
                    imported_count += 1
                except Exception as e:
                    print(f"Error importing property {row['NCONTR']}: {e}")
                    error_count += 1
                    continue
            
            try:
                self.db.commit()
                print(f"Imported batch {i//batch_size + 1}/{(len(df_unique)-1)//batch_size + 1}")
            except Exception as e:
                print(f"Error committing batch: {e}")
                self.db.rollback()
        
        print(f"Properties import completed! Imported: {imported_count}, Errors: {error_count}")

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Bairro(Base):
    __tablename__ = "bairros"
    
    id = Column(Integer, primary_key=True, index=True)
    cod_b1 = Column(Integer, nullable=False)
    cod_b = Column(Integer, nullable=False)
    descricao = Column(String(255), nullable=False)
    cod_dist_urb = Column(String(255))
    fact = Column(Float, nullable=False)
    
    propriedades = relationship("Propriedade", back_populates="bairro")

class TipoProprietario(Base):
    __tablename__ = "tipos_proprietario"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(Integer, unique=True, nullable=False)
    descricao = Column(String(255), nullable=False)
    
    propriedades = relationship("Propriedade", back_populates="tipo_proprietario")

class Finalidade(Base):
    __tablename__ = "finalidades"
    
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(Integer, unique=True, nullable=False)
    descricao = Column(String(255), nullable=False)

class FatorAntiguidade(Base):
    __tablename__ = "fatores_antiguidade"
    
    id = Column(Integer, primary_key=True, index=True)
    cod = Column(String(10), unique=True, nullable=False)
    id_range = Column(String(20), nullable=False)
    tiphab = Column(Float, nullable=False)  # Fator para habitação
    tipcom = Column(Float, nullable=False)  # Fator para comércio

class PrecoReferencia(Base):
    __tablename__ = "precos_referencia"
    
    id = Column(Integer, primary_key=True, index=True)
    preco = Column(Float, nullable=False)
    ano = Column(Integer, nullable=False)

class Endereco(Base):
    __tablename__ = "enderecos"
    
    id = Column(Integer, primary_key=True, index=True)
    cod_r = Column(String(10), unique=True, nullable=False)
    morada = Column(String(255), nullable=False)

class Propriedade(Base):
    __tablename__ = "propriedades"
    
    id = Column(Integer, primary_key=True, index=True)
    ncontr = Column(Integer, unique=True, nullable=False)
    situa = Column(String(10))
    codipra = Column(Float)
    matriz = Column(String(50))
    nome = Column(String(255))
    cod_localizaca = Column(String(50))
    nu_entrada = Column(String(50))
    andar_n = Column(String(50))
    flat = Column(String(50))
    qrt = Column(String(50))
    nu_casa = Column(String(50))
    cod_distr_muni = Column(Float)
    cod_bairro = Column(Integer, ForeignKey("bairros.cod_b1"))
    tiphab = Column(String(10))
    fl = Column(Float)
    recolec = Column(Float)
    valpatr = Column(Float)  # Valor patrimonial
    proprietar = Column(Integer, ForeignKey("tipos_proprietario.codigo"))
    telef_cont = Column(String(50))
    contr_ante = Column(String(50))
    nuit = Column(String(50))
    preco = Column(Float)
    thidade = Column(String(10))
    factant = Column(String(10))
    are_tereno = Column(String(50))
    are_constr = Column(String(50))
    data_cria = Column(DateTime)
    data_cr_al = Column(String(50))
    hora_cr_al = Column(String(50))
    
    bairro = relationship("Bairro", back_populates="propriedades")
    tipo_proprietario = relationship("TipoProprietario", back_populates="propriedades")
    endereco = relationship("Endereco", primaryjoin="Propriedade.cod_localizaca == foreign(Endereco.cod_r)", uselist=False)


class FimipaIpra(Base):
    __tablename__ = "fimipa_ipra"
    
    id = Column(Integer, primary_key=True, index=True)
    ncontr = Column(Integer, unique=True, nullable=False, index=True)
    iimppag = Column(Float, nullable=True)
    ano = Column(Integer, nullable=False, default=2025)

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db import Base

class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, index=True)
    cpf = Column(String(14), unique=True, nullable=True)
    nis = Column(String(20), nullable=True)
    nome = Column(String(255), nullable=True)

    beneficios = relationship("Beneficio", back_populates="pessoa")
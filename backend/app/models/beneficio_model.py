from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from db import Base

class Beneficio(Base):
    __tablename__ = "beneficios"

    id = Column(Integer, primary_key=True, index=True)
    beneficio = Column(Text)
    imagem_base64 = Column(Text)

    pessoa_id = Column(Integer, ForeignKey("pessoas.id"))
    pessoa = relationship("Pessoa", back_populates="beneficios")
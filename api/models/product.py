from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from api.database import Base

class Product(Base):
    __tablename__ = "products"
    
    # TODO: Definir los campos del modelo Product
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(255), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)  # hasta 99999999.99
    stock = Column(Integer, default=0, nullable=False)
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price}, stock={self.stock})>"
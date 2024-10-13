from sqlalchemy import (Column, Integer, 
                        Float, String, 
                        ForeignKey)
from sqlalchemy.orm import (DeclarativeBase, 
                            mapped_column, 
                            relationship)


class Base(DeclarativeBase):
    pass

class Customer(Base):

    __tablename__ = 'customer'

    id = mapped_column(Integer, primary_key=True)
    country = Column(String)

class Product(Base):

    __tablename__ = 'product'

    id = mapped_column(Integer, primary_key=True)
    description = Column(String)
    price = Column(Float)

class CustomerOrder(Base):

    __tablename__ = 'customer_order'

    id = mapped_column(Integer, primary_key=True)
    invoice_nb = Column(Integer)
    
    customer_id = mapped_column(ForeignKey("customer.id"))
    customer = relationship("Customer")

class OrderDetail(Base):

    __tablename__ = 'order_detail'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)

    order_id = mapped_column(ForeignKey("customer_order.id"))
    order = relationship("CustomerOrder")

    product_id = mapped_column(ForeignKey("product.id"))
    product = relationship("Product")

ORM_MODELS = {
    "customer": Customer,
    "product": Product,
    "customer_order": CustomerOrder,
    "order_detail": OrderDetail
}

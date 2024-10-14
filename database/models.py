# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 14, 2024 19:25:51
# Database: sqlite:////tmp/tmp.ugjT5j4p1D/crm/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Customer(SAFRSBaseX, Base):
    """
    description: Stores customer details such as name, contact information, and address.
    """
    __tablename__ = 'customer'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100))
    phone = Column(String(15))
    address = Column(String(250))

    # parent relationships (access parent)

    # child relationships (access children)
    CustomerFeedbackList : Mapped[List["CustomerFeedback"]] = relationship(back_populates="customer")
    OrderList : Mapped[List["Order"]] = relationship(back_populates="customer")



class Employee(SAFRSBaseX, Base):
    """
    description: Lists employees and their roles within the company.
    """
    __tablename__ = 'employee'
    _s_collection_name = 'Employee'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    role = Column(String(50))

    # parent relationships (access parent)

    # child relationships (access children)
    DepartmentList : Mapped[List["Department"]] = relationship(back_populates="manager")



class Product(SAFRSBaseX, Base):
    """
    description: Stores product details including name, description, and price.
    """
    __tablename__ = 'product'
    _s_collection_name = 'Product'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(250))
    price = Column(Float, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    InventoryList : Mapped[List["Inventory"]] = relationship(back_populates="product")
    OrderDetailList : Mapped[List["OrderDetail"]] = relationship(back_populates="product")



class Promotion(SAFRSBaseX, Base):
    """
    description: Defines promotions applicable to orders.
    """
    __tablename__ = 'promotion'
    _s_collection_name = 'Promotion'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    discount_percentage = Column(Float, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    OrderPromotionList : Mapped[List["OrderPromotion"]] = relationship(back_populates="promotion")



class Supplier(SAFRSBaseX, Base):
    """
    description: Contains supplier details such as name and contact information.
    """
    __tablename__ = 'supplier'
    _s_collection_name = 'Supplier'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    contact_name = Column(String(50))
    phone = Column(String(15))

    # parent relationships (access parent)

    # child relationships (access children)
    InventoryList : Mapped[List["Inventory"]] = relationship(back_populates="supplier")



class CustomerFeedback(SAFRSBaseX, Base):
    """
    description: Records feedback from customers about products and services.
    """
    __tablename__ = 'customer_feedback'
    _s_collection_name = 'CustomerFeedback'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'), nullable=False)
    feedback_date = Column(DateTime)
    comments = Column(String(250))

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("CustomerFeedbackList"))

    # child relationships (access children)



class Department(SAFRSBaseX, Base):
    """
    description: Organizes employees into departments.
    """
    __tablename__ = 'department'
    _s_collection_name = 'Department'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    manager_id = Column(ForeignKey('employee.id'))

    # parent relationships (access parent)
    manager : Mapped["Employee"] = relationship(back_populates=("DepartmentList"))

    # child relationships (access children)



class Inventory(SAFRSBaseX, Base):
    """
    description: Tracks product inventory levels by supplier.
    """
    __tablename__ = 'inventory'
    _s_collection_name = 'Inventory'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('product.id'), nullable=False)
    supplier_id = Column(ForeignKey('supplier.id'), nullable=False)
    quantity_in_stock = Column(Integer, nullable=False)

    # parent relationships (access parent)
    product : Mapped["Product"] = relationship(back_populates=("InventoryList"))
    supplier : Mapped["Supplier"] = relationship(back_populates=("InventoryList"))

    # child relationships (access children)



class Order(SAFRSBaseX, Base):
    """
    description: Records customer orders with references to customers and the total amount.
    """
    __tablename__ = 'order'
    _s_collection_name = 'Order'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_date = Column(DateTime)
    customer_id = Column(ForeignKey('customer.id'), nullable=False)
    total_amount = Column(Float)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    OrderDetailList : Mapped[List["OrderDetail"]] = relationship(back_populates="order")
    OrderPromotionList : Mapped[List["OrderPromotion"]] = relationship(back_populates="order")
    ShipmentList : Mapped[List["Shipment"]] = relationship(back_populates="order")



class OrderDetail(SAFRSBaseX, Base):
    """
    description: Stores order details referencing orders and products, including quantity and unit price.
    """
    __tablename__ = 'order_detail'
    _s_collection_name = 'OrderDetail'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'), nullable=False)
    product_id = Column(ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("OrderDetailList"))
    product : Mapped["Product"] = relationship(back_populates=("OrderDetailList"))

    # child relationships (access children)



class OrderPromotion(SAFRSBaseX, Base):
    """
    description: Links promotions to orders to show applicable discounts.
    """
    __tablename__ = 'order_promotion'
    _s_collection_name = 'OrderPromotion'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'), nullable=False)
    promotion_id = Column(ForeignKey('promotion.id'), nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("OrderPromotionList"))
    promotion : Mapped["Promotion"] = relationship(back_populates=("OrderPromotionList"))

    # child relationships (access children)



class Shipment(SAFRSBaseX, Base):
    """
    description: Manages shipments of orders including destination and status.
    """
    __tablename__ = 'shipment'
    _s_collection_name = 'Shipment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'), nullable=False)
    destination = Column(String(250))
    shipped_date = Column(DateTime)
    status = Column(String(50))

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("ShipmentList"))

    # child relationships (access children)

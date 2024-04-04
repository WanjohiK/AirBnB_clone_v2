#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class Amenity(BaseModel, Base):
    '''amenity class'''
    __tablename__ = 'amenities'

    storage_type = getenv("HBNB_TYPE_STORAGE")
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
    else:
        name = ""

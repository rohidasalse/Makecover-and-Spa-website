
from __init__ import db
from datetime import datetime
from sqlalchemy import inspect
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import inspect



class Customize_files(db.Model):
    __tablename__ = 'customize_files'
    customizeId = db.Column(db.String(50), primary_key=True)

    position = db.Column(db.String(50), nullable=False)
    index = db.Column(db.Integer, nullable=True)
    title = db.Column(db.String(1000), nullable=True)
    category = db.Column(db.String(50), nullable=False)
    fileUrl = db.Column(db.String(500), nullable=False)
    link = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
   

    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def toDictWithUrl(self):
        data_dict = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        if self.file:
            data_dict['fileUrl'] = self.file.fileUrl
        return data_dict

    def toDictWithExceptFields(self):
        excluded_fields = ['customizeId', 'date']
        columns = inspect(self.__class__).mapper.column_attrs
        fields = [c.key for c in columns if c.key not in excluded_fields]
        file_dict = {field: getattr(self, field) for field in fields}
        return file_dict

    @classmethod
    def get_by_id(cls, customizeId):
        return cls.query.get(customizeId)


class Files(db.Model):
    __tablename__ = 'files'
    fileId = db.Column(db.String(50), primary_key=True)
    filepath=db.Column(db.String(250), nullable=False)
    fileUrl = db.Column(db.String(500), nullable=False, unique=True)  # Make fileUrl unique
    fileType = db.Column(db.String(25), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
   
    def toDict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    def toDictWithExceptFields(self):
        excluded_fields = ['fileId', 'date']
        columns = inspect(self.__class__).mapper.column_attrs
        fields = [c.key for c in columns if c.key not in excluded_fields]
        file_dict = {field: getattr(self, field) for field in fields}
        return file_dict

    @classmethod
    def get_by_id(cls, fileId):
        return cls.query.get(fileId)


class Admin(db.Model):
    __tablename__ = 'admin'

    id=db.Column(db.Integer,primary_key=True,autoincrement=True,unique=True)
    publicId=db.Column(db.String(50),nullable=False,unique=True)
    name=db.Column(db.String(50),nullable=False)
    username=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(75),nullable=False,unique=True)
    password=db.Column(db.String(50),nullable=False)
    secretkey=db.Column(db.String(100),nullable=False)
    date=db.Column(db.DateTime, default=datetime.now(),nullable=True)
    def toDict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
    
    
    








 
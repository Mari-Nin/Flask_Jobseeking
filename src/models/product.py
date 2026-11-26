from flask import url_for
from src.ext import db
from src.models.base import BaseModel


class IpekItems(BaseModel):
        __tablename__ = 'Ipekyols'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100))
        price = db.Column(db.Float)
        stock = db.Column(db.Integer())
        created_at = db.Column(db.DateTime(),nullable=True)
        
        
        category_id = db.Column(db.Integer(),db.ForeignKey('categories.id'),nullable=False)
        category=db.relationship('Category',back_populates='ipeks')


        img = db.Column(db.String(255),nullable=False)
        @property
        def img_url(self):
            return url_for('static',filename = f"uploads/{self.img}")
            

        def __repr__(self):
            return f"{self.name or 'Unnamed Item'}"
        
class Category(BaseModel):
     __tablename__='categories'
     id=db.Column(db.Integer(),primary_key=True)
     name = db.Column(db.String())
     ipeks = db.relationship('IpekItems',back_populates='category')

     def __repr__(self):
         return f"{self.name}"



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    



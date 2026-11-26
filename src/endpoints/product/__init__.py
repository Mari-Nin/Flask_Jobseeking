from flask_restx import fields,reqparse
from flask_restx.reqparse import RequestParser
from src.ext import api
from werkzeug.datastructures import FileStorage


ipek_ns = api.namespace('Ipek',description = 'Ipek namespace')

ipek_model = api.model('ipek',{
                        'id':fields.Integer,
                        'name':fields.String,
                        'price':fields.Float, 
                        'stock':fields.Integer,
                        'category_id':fields.Integer,
                        'category_name':fields.String(attribute='category.name'),
                        'created_at':fields.DateTime,
                        'img':fields.String}     )

ipek_delete_parser = RequestParser()
ipek_delete_parser.add_argument('id', type=int,required=True,location='args')

ipek_create_parser = RequestParser()
ipek_create_parser.add_argument('name',type=str,required=True,location='form')
ipek_create_parser.add_argument('price',type=int,required=True,location='form')
ipek_create_parser.add_argument('stock',type=int,required=True,location='form')
ipek_create_parser.add_argument('category_id',type=int,required=True,location='form')
ipek_create_parser.add_argument('img',type=FileStorage,required=True,location='files')




ipek_update_parser = RequestParser()
ipek_update_parser.add_argument('id', type=int,required=True,location='args')
ipek_update_parser.add_argument('name',type=str,required=False,location='form')
ipek_update_parser.add_argument('price',type=int,required=False,location='form')
ipek_update_parser.add_argument('stock',type=int,required=False,location='form')
ipek_update_parser.add_argument('category_id',type=int,required=False,location='form')
ipek_update_parser.add_argument('img',type=FileStorage,required=False,location='files') 



                      
                        
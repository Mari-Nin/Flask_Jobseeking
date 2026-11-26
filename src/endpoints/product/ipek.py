
from flask_restx import Resource
import os
from os import path
from uuid import uuid4
from src.ext import api
from src.admin_views.utils import generate_name
from src.conf import Config
from src.endpoints.product import ipek_model,ipek_delete_parser,ipek_ns,ipek_create_parser,ipek_update_parser
from src.models.product import IpekItems,Category


@ipek_ns.route('/')

class IpekAPI(Resource):
    @ipek_ns.marshal_with(ipek_model)
    def get(self):
        ipeks=IpekItems.query.all()
        return ipeks

    @ipek_ns.expect(ipek_delete_parser)
    def delete(self):
        args=ipek_delete_parser.parse_args()
        ipek=IpekItems.query.get(args['id'])
        if not ipek:
            return {'message': f'Product N{args["id"]} not found!'}, 400
      
        ipek.delete()
        return {'message':f'Product N{args['id']}  {ipek} deleted!'}, 200
 
    @ipek_ns.expect(ipek_create_parser)
    def post(self):
        args=ipek_create_parser.parse_args()
        category = Category.query.get(args['category_id']) 
        if not category: 
             return {'message': 'Invalid category!'}, 400

        file = args['img']
        new_filename=generate_name(None,file)
        upload_folder = Config.UPLOAD_PATH
        os.makedirs(upload_folder, exist_ok=True)
        file_path = path.join(upload_folder, new_filename)
        file.save(file_path)
  
        new_ipek = IpekItems(name= args['name'],
                        price= args['price'],
                        stock= args['stock'],
                        category_id= args['category_id'],
                        img=new_filename)
        new_ipek.create()

        return 'New product added!', 201


    @ipek_ns.expect(ipek_update_parser)
    def put(self):
        args = ipek_update_parser.parse_args()

        ipek = IpekItems.query.get(args['id'])

        if not ipek:
            return {
                'message': f'Product N{args["id"]} not found'
            }, 404

        fields = ['category_id','name','price','stock','img']
        for field in fields:
            if args.get(field) is not None:
                setattr(ipek,field,args[field])

        ipek.save()

        return {
            'message': f'Product N{ipek.id} updated!'
        }, 200
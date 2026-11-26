from src.admin_views.base import SecureModelView
from flask_admin.form import ImageUploadField
from flask import url_for
from wtforms.fields import FloatField
from markupsafe import Markup
from src.admin_views.utils import generate_name
from src.conf import Config
from flask_admin.model import InlineFormAdmin
from src.models.product import IpekItems

class IpekView(SecureModelView):
    can_delete = True
    can_create = True
    can_edit = True
    can_view_details = True
    
    edit_modal = True
    create_modal = True
  

    column_editable_list = [ 'name']
    column_filters = ['price', 'category']
    column_searchable_list = ['name']

    form_overrides = {
        'price': FloatField,
        'img': ImageUploadField
    }


    form_args = {
    'img': {
        'base_path': Config.UPLOAD_PATH,
        'relative_path': '',
        'url_relative_path': 'uploads/',
        'endpoint': 'static',
        'namegen': generate_name
    }
}
    column_formatters = {
    'img': lambda v, c, m, n: Markup(f'<img src="{m.img_url}" width="100">') if m.img else ''
}
    column_list=['category', 'name', 'price','stock','img']
   
class CategoryView (SecureModelView):

        form_columns = ['name']
        can_delete=True
        can_create=True
        can_edit = True
        can_view_details=True
    
        edit_modal = True
        create_modal=True

        edit_modal = True
        create_modal=True

       
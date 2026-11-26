
from  src.admin_views.base import SecureModelView
from wtforms.fields import SelectField

class UserView (SecureModelView):
  
    can_delete=True
    can_create=True
    can_edit = True
    can_view_details=True

    edit_modal = True
    create_modal=True

    form_overrides={
        'role':SelectField
    }
    form_args = {
        'role':{'choices':['user','admin']}
    }
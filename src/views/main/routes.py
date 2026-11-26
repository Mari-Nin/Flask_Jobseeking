from flask import render_template,Blueprint
from src.models.product import IpekItems
from src.views.product.forms import IpekForm


main_bp=Blueprint('main',__name__)
@main_bp.route('/')
def index():
    ipeks=IpekItems.query.all()
    return render_template('main/index.html',ipeks=ipeks,title='Our products')    
from flask import Blueprint,render_template,url_for,redirect,request,abort
from os import path
from flask_login import login_required,current_user
from src.models.product import IpekItems,Category
from src.views.product.forms import IpekForm,ShoppingForm
from src.conf import Config 
from src.admin_views.utils import generate_name


ipek_bp=Blueprint('ipek',__name__)

@ipek_bp.route('/ipeks')
def all_ipeks():
    search_by=request.args.get('search_by')
    search=request.args.get('search')

    if search_by=='name':
        ipeks= IpekItems.query.filter(IpekItems.name.ilike(f'%{search}%')).all()

    elif search_by=='category':
        category=Category.query.filter(Category.name.ilike(f"{search}")).first()
        if category:
            ipeks = IpekItems.query.filter_by(category_id = category.id).all()
        else:
            return 'No sush category'

    else:
        ipeks = IpekItems.query.all()

    return render_template('ipek/ipeks.html', ipeks=ipeks)

@ipek_bp.route('/ipeks/<int:id>')
def ipek(id):
    ipek=IpekItems.query.get(id)
    if ipek is None:
        return 'Product not found', 404
    return render_template('ipek/ipek.html',ipek=ipek)


@ipek_bp.route('/create',methods=["GET","POST"])
@login_required
def create():
    if current_user.role != 'admin':
        abort(403)

    form = IpekForm()
    categories = Category.query.all()
    form.category.choices = [(category.id,category.name) for category in categories]
  
    if form.validate_on_submit():
         
         existing_ipek = IpekItems.query.filter_by(name = form.name.data,
                                                   category_id = form.category.data).first()
         if existing_ipek:
            form.name.errors.append(f"Product '{existing_ipek}' in this category already exists'")
            return render_template('ipek/create.html',form=form)
         img = form.img.data
         unique_filename = generate_name(None,img)
         img_place=path.join(Config.UPLOAD_PATH,unique_filename)
         img.save(img_place)
  
         image_path = unique_filename
         category=Category.query.get(form.category.data)
     
         ipek=IpekItems(name=form.name.data,price=form.price.data,category=category,stock=form.stock.data,img=image_path)
         ipek.create()

         return redirect(url_for('ipek.all_ipeks'))
    else:
         print("FORM INVALID")
         print(form.errors)
    return render_template('ipek/create.html', form=form)



@ipek_bp.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.role != 'admin':
            abort(403)
    ipek=IpekItems.query.get(id)
    if ipek is None:
        return 'Product not found', 404
    ipek.delete()
    return redirect(url_for('ipek.all_ipeks'))

@ipek_bp.route('/shop/<int:id>',methods=["GET","POST"])
@login_required
def shop(id):
    form=ShoppingForm()
    ipek=IpekItems.query.get_or_404(id)

    if request.method=='GET':
        form.id.data = ipek.id
        form.name.data = ipek.name
        form.price.data =ipek.price
        form.stock.data  = ipek.stock
    
    if form.validate_on_submit():
        quantity = form.quantity.data
        if quantity:   
            if ipek.stock >=quantity and quantity>0:
                ipek.stock-=quantity
                ipek.save()
                form.quantity.errors.append('Success shoping')
                success_shopping = True
                return render_template('ipek/shop.html',form=form,ipek=ipek,success_shopping=success_shopping)
            else:
                
                form.quantity.errors.append('Wrong shopping')
                success_shopping=False
                return render_template('ipek/shop.html',form=form,ipek=ipek,success_shopping=success_shopping)
        else:
            form.id.data = ipek.id
            form.name.data = ipek.name
            form.price.data =ipek.price
            form.stock.data  = ipek.stock 
            form.quantity.errors.append('Wrong shopping')
            print(form.validate_on_submit())
           
            return render_template('ipek/shop.html',form=form,ipek=ipek)
     

    return render_template('ipek/shop.html',form=form,ipek=ipek)

@ipek_bp.route('/update/<int:id>',methods=["GET","POST"])
@login_required
def update(id):
    if current_user.role != 'admin':
            abort(403)
    form = IpekForm()
    updated_ipek=IpekItems.query.get(id)
    if updated_ipek is None:
        return f'Product with id {id} not found'
 
    categories = Category.query.all()
    form.category.choices = [(category.id, category.name) for category in categories]
    if form.validate_on_submit():

         category = Category.query.get(form.category.data)
         ipek_name = updated_ipek.name
         ipek_price = updated_ipek.price
         ipek_stock = updated_ipek.stock
         ipek_category = updated_ipek.category_id
         ipek_img = updated_ipek.img

         updated_ipek.name =form.name.data
         updated_ipek.price = form.price.data
         updated_ipek.stock = form.stock.data
         updated_ipek.category_id = category.id

         img=form.img.data
         if img:
             unique_filename = generate_name(None,img)
             img_place = path.join(Config.UPLOAD_PATH, unique_filename)
             img.save(img_place)
             updated_ipek.img = unique_filename


         changes = [updated_ipek.name!=ipek_name,
                    updated_ipek.price!=ipek_price,
                    updated_ipek.stock!=ipek_stock,
                    updated_ipek.category_id !=ipek_category,
                    updated_ipek.img!=ipek_img
        ]
         check_changes = sum(changes)
         
         if check_changes>0:
            existing_ipek = IpekItems.query.filter(
                IpekItems.name == form.name.data,
                IpekItems.category_id == form.category.data,
                IpekItems.id!=id).first()
            
            if existing_ipek:
                form.name.errors.append(f"Product '{existing_ipek}' in this category already exists'")
                return render_template('ipek/create.html', form=form)
            updated_ipek.update()
            
            return redirect(url_for('ipek.all_ipeks'))
         else:
            form.name.errors.append('No changes')
    
    else:
         form.name.data = updated_ipek.name
         form.price.data = updated_ipek.price
         form.stock.data = updated_ipek.stock
         form.category.data = updated_ipek.category_id

    return render_template('ipek/create.html', form=form)

@ipek_bp.route('/liquid',methods=['GET'])
@login_required
def liquid():
    if current_user.role != 'admin':
            abort(403)
    liquid_stocks=IpekItems.query.filter_by(stock=0).all()
    return render_template('ipek/liquid.html',liquid_stocks=liquid_stocks,title='Liquid stocks')

        


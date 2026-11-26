from flask_login import current_user
from src.models.product import IpekItems, Category
from pathlib import Path
import os

def test_products(client):
    response = client.get('/ipeks')
    assert response.status_code == 200


def test_product(client,app):
    with app.app_context():
        category = Category.query.first()

        ipek = IpekItems(
            name='Test Product',
            price=150,
            stock=15,
            img='uploads/test.jpg',
            category_id=category.id
        )

        ipek.create()
        ipek_id = ipek.id

    response = client.get(f'/ipeks/{ipek_id}')

    assert response.status_code == 200


def test_add_product_unathenticated(client,app):
    img_path = Path(__file__).parent / 'resources' / 'ipek.jpg'

    with open(img_path, 'rb') as img_file:
        response = client.post(
            '/create',
            data={
                'name': 'test_name',
                'price': 100,
                'stock': 10,
                'category': 2,
                'img': (img_file, 'ipek.jpg')
            },
            content_type='multipart/form-data'
        )
    with app.app_context():
        create_product = IpekItems.query.filter_by(name='test_name').first()

        assert not create_product
    assert response.status_code == 302

def test_add_product_authenticated(client,app):

    with client:
        client.post('/login',data={'name':'admin', 'password':os.getenv('ADMIN_PASSWORD')})

        img_path = Path(__file__).parent / 'resources' / 'ipek.jpg'

        with open(img_path, 'rb') as img_file:
            response = client.post(
                '/create',
                data={
                    'name': 'test_name',
                    'price': 100,
                    'stock': 10,
                    'category': 2,
                    'img': (img_file, 'ipek.jpg')
                },
                content_type='multipart/form-data'
            )
       
    with app.app_context():
        create_product = IpekItems.query.filter_by(name='test_name').first()

        assert create_product is not None
    assert response.status_code == 302
from flask_restx import Resource
from flask_login import login_user
from src.endpoints.auth import auth_ns,login_parser
from src.models.user import User
from werkzeug.security import check_password_hash


@auth_ns.route('/login')
class LoginApi(Resource):
    @auth_ns.doc(parser=login_parser)

    def post(self):
        args = login_parser.parse_args()

        user = User.query.filter_by(name = args['name']).first()
        
        if not user:
            return 'User not found',404

        if not check_password_hash(user.password,args['password']):
            return 'Incorrect password',401
        
        login_user(user)
        return {'message': 'Successfully logged in'}, 200


from app import create_app, db
from app.models.user import User
from flask_jwt_extended import create_access_token
import json

app = create_app('development')
with app.app_context():
    user = User.query.filter_by(email='student@qualilearn.com').first()
    if not user:
        print("User not found")
        exit()
    
    token = create_access_token(identity=str(user.id))
    
    with app.test_client() as client:
        response = client.get(
            '/api/analytics/dashboard-stats?portal=secondary',
            headers={'Authorization': f'Bearer {token}'}
        )
        print(json.dumps(response.get_json(), indent=2))

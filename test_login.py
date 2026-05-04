from app import create_app
import os

app = create_app('development')

@app.route('/api/auth/crash', methods=['POST'])
def crash():
    raise Exception("Intentional crash")

if __name__ == '__main__':
    app.run(port=5001)

from flask import Flask, jsonify, render_template
import requests

app = Flask(__name__)

# اطلاعات مدیر
ADMIN_ID = 765041693  # شناسه عددی مدیر
API_TOKEN = '7308080366:AAEZlSs4KRjLcwXsRF2jyDwriDkx-2egbpg'  # توکن ربات تلگرام شما
USER_DATA = {}  # برای ذخیره اطلاعات کاربران

# روت برای نمایش صفحه HTML
@app.route('/')
def index():
    return render_template('index.html')

# روت برای بررسی مدیر بودن کاربر
@app.route('/api/check_user_role/<int:user_id>')
def check_user_role(user_id):
    try:
        # درخواست به API تلگرام برای بررسی وضعیت کاربر
        response = requests.get(f'https://api.telegram.org/bot{API_TOKEN}/getChatMember?chat_id=@your_channel_username&user_id={user_id}')
        data = response.json()

        if 'result' in data:
            user_status = data['result']['status']
            if user_status == 'administrator' or user_status == 'creator' or user_id == ADMIN_ID:
                return jsonify({'is_admin': True, 'user_id': user_id})
            else:
                return jsonify({'is_admin': False, 'user_id': user_id})
        else:
            return jsonify({'is_admin': False, 'error': 'User not found or error in API call'})
    except Exception as e:
        return jsonify({'is_admin': False, 'error': str(e)})

# روت برای نمایش اطلاعات کاربران به مدیر
@app.route('/api/user_data')
def get_user_data():
    if ADMIN_ID in USER_DATA:
        return jsonify(USER_DATA)
    else:
        return jsonify({'error': 'Only admin can view user data'})

if __name__ == '__main__':
    app.run(debug=True)

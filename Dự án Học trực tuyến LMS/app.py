import os
from flask import Flask, jsonify, request, send_from_directory, redirect
from flask_cors import CORS
from database import SessionLocal
from models import User, Course, Category

app = Flask(__name__)
CORS(app)

# =====================================================================
# PHẦN 1: CẤU HÌNH GIAO DIỆN 
# =====================================================================

# 1. Tự động dẫn vào trang chủ khi mở http://127.0.0.1:5001
@app.route('/')
def home():
    return redirect('/Html/home/index.html')

# 2. Xử lý đường dẫn file HTML (Hỗ trợ cả /Html/ và /html/)
@app.route('/Html/<path:filename>')
@app.route('/html/<path:filename>')
def serve_html(filename):
    # Tìm thư mục thực tế trên máy Tuấn (dù là Html hay html)
    folder = 'Html' if os.path.exists('Html') else 'html'
    return send_from_directory(folder, filename)

# 3. Xử lý đường dẫn CSS (Quan trọng: Sửa lỗi trắng trang)
# Flask sẽ nhận diện cả CSS, Css, css để đảm bảo không bị lỗi 404
@app.route('/CSS/<path:filename>')
@app.route('/Css/<path:filename>')
@app.route('/css/<path:filename>')
def serve_css(filename):
    # Ưu tiên tìm thư mục viết hoa CSS theo cấu trúc của Tuấn
    if os.path.exists('CSS'):
        return send_from_directory('CSS', filename)
    elif os.path.exists('Css'):
        return send_from_directory('Css', filename)
    return send_from_directory('css', filename)

# 4. Xử lý đường dẫn JS
@app.route('/Js/<path:filename>')
@app.route('/JS/<path:filename>')
@app.route('/js/<path:filename>')
def serve_js(filename):
    if os.path.exists('Js'):
        return send_from_directory('Js', filename)
    elif os.path.exists('JS'):
        return send_from_directory('JS', filename)
    return send_from_directory('js', filename)


# =====================================================================
# PHẦN 2: API BACKEND (Xử lý dữ liệu SQL Server)
# =====================================================================

@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.json
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.username == data.get('username')).first()
        if existing_user:
            return jsonify({"status": "error", "message": "Tên đăng nhập đã tồn tại!"}), 400
        new_user = User(
            username=data.get('username'),
            password=data.get('password'),
            role='student'
        )
        db.add(new_user)
        db.commit()
        return jsonify({"status": "success", "message": "Đăng ký thành công!"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    db = SessionLocal()
    try:
        user = db.query(User).filter(
            User.username == data.get('username'), 
            User.password == data.get('password')
        ).first()
        if user:
            if not user.is_active:
                return jsonify({"status": "error", "message": "Tài khoản bị khóa!"}), 403
            return jsonify({
                "status": "success", 
                "message": "Đăng nhập thành công!",
                "user": {"id": user.id, "username": user.username, "role": user.role}
            }), 200
        else:
            return jsonify({"status": "error", "message": "Sai tài khoản hoặc mật khẩu!"}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

@app.route('/api/courses', methods=['GET'])
def get_courses():
    db = SessionLocal()
    try:
        courses = db.query(Course, Category.name.label("category_name"))\
                    .join(Category, Course.category_id == Category.id)\
                    .filter(Course.status == 'published').all()
        result = []
        for course, cat_name in courses:
            result.append({
                "id": course.id,
                "title": course.title,
                "price": course.price,
                "category": cat_name
            })

        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

if __name__ == '__main__':
    print("--------------------------------------------------")
    print("🚀 HỆ THỐNG LMS ĐANG CHẠY TOÀN DIỆN")
    print("👉 Truy cập ngay: http://127.0.0.1:5001")
    print("--------------------------------------------------")
    app.run(debug=True, port=5001)
# 5. Dạy Flask cách tìm file Ảnh (Thêm đoạn này vào PHẦN 1 của app.py)
@app.route('/Images/<path:filename>')
@app.route('/images/<path:filename>')
def serve_images(filename):
    folder = 'Images' if os.path.exists('Images') else 'images'
    return send_from_directory(folder, filename)
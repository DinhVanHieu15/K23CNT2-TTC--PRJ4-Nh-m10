import os
from flask import Flask, jsonify, request, send_from_directory, redirect
from flask_cors import CORS
from database import SessionLocal
from models import User, Course, Category, Quiz # Đã thêm Quiz vào đây

app = Flask(__name__)
CORS(app)

# =====================================================================
# PHẦN 1: CẤU HÌNH GIAO DIỆN & FILE TĨNH
# =====================================================================

# 1. Tự động dẫn vào trang chủ
@app.route('/')
def home():
    return redirect('/Html/home/index.html')

# 2. Xử lý file HTML
@app.route('/Html/<path:filename>')
@app.route('/html/<path:filename>')
def serve_html(filename):
    folder = 'Html' if os.path.exists('Html') else 'html'
    return send_from_directory(folder, filename)

# 3. Xử lý file CSS
@app.route('/CSS/<path:filename>')
@app.route('/Css/<path:filename>')
@app.route('/css/<path:filename>')
def serve_css(filename):
    for folder in ['CSS', 'Css', 'css']:
        if os.path.exists(folder):
            return send_from_directory(folder, filename)
    return "Folder CSS không tồn tại", 404

# 4. Xử lý file JS
@app.route('/Js/<path:filename>')
@app.route('/JS/<path:filename>')
@app.route('/js/<path:filename>')
def serve_js(filename):
    for folder in ['Js', 'JS', 'js']:
        if os.path.exists(folder):
            return send_from_directory(folder, filename)
    return "Folder JS không tồn tại", 404

# 5. Xử lý file Ảnh (Images)
@app.route('/Images/<path:filename>')
@app.route('/images/<path:filename>')
def serve_images(filename):
    folder = 'Images' if os.path.exists('Images') else 'images'
    return send_from_directory(folder, filename)


# =====================================================================
# PHẦN 2: API BACKEND (Xử lý dữ liệu SQL Server)
# =====================================================================

# --- API ĐĂNG KÝ ---
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

# --- API ĐĂNG NHẬP ---
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

# --- API LẤY KHÓA HỌC ---
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
                "price": float(course.price), # Đảm bảo giá là số thực
                "category": cat_name
            })
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()

# --- API LẤY BÀI TẬP (QUIZZES) - MỚI THÊM ---
@app.route('/api/quizzes', methods=['GET'])
def get_quizzes():
    db = SessionLocal()
    try:
        # Lấy danh sách bài tập từ SQL Server
        quizzes = db.query(Quiz).all()
        result = []
        for q in quizzes:
            # Phân loại cấp độ dựa trên điểm vượt qua
            level = "Dễ" if q.pass_score < 5.0 else "Trung bình"
            if q.pass_score >= 8.0: level = "Khó"

            result.append({
                "id": q.id,
                "title": f"Thử thách bài tập #{q.id}", 
                "time": q.time_limit,
                "level": level,
                "pass_score": q.pass_score
            })
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        db.close()


# =====================================================================
# CHẠY HỆ THỐNG
# =====================================================================
if __name__ == '__main__':
    print("--------------------------------------------------")
    print("🚀 HỆ THỐNG LMS ĐANG CHẠY TOÀN DIỆN")
    print("👉 Trang chủ: http://127.0.0.1:5001")
    print("--------------------------------------------------")
    app.run(debug=True, port=5001)
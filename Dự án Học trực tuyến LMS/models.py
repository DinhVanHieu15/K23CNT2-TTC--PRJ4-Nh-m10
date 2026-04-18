from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text, Numeric
from database import Base
import datetime

# ==========================================
# 1. NGƯỜI DÙNG & HỆ THỐNG
# ==========================================
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50))
    is_active = Column(Boolean, default=True)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(String(500), nullable=False)
    is_read = Column(Boolean, default=False)

# ==========================================
# 2. KHÓA HỌC & BÀI HỌC
# ==========================================
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    instructor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    price = Column(Numeric(18, 2), nullable=False) # Đã đổi thành Numeric cho khớp Decimal trong DB
    status = Column(String(50))

class Section(Base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String(255), nullable=False)
    order_index = Column(Integer, nullable=False)

class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    section_id = Column(Integer, ForeignKey('sections.id'), nullable=False)
    lesson_type = Column(String(50))
    url_content = Column(String(500))

# ==========================================
# 3. THI CỬ & TRẮC NGHIỆM
# ==========================================
class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    time_limit = Column(Integer, nullable=False)
    pass_score = Column(Float, nullable=False)

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    content = Column(String(500), nullable=False)
    point = Column(Float, nullable=False)

class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    option_text = Column(String(255), nullable=False)
    is_correct = Column(Boolean, nullable=False)

# ==========================================
# 4. TIẾN ĐỘ & KẾT QUẢ
# ==========================================
class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.datetime.now)
    status = Column(String(50))

class CourseProgress(Base):
    __tablename__ = "course_progress"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    lesson_id = Column(Integer, ForeignKey('lessons.id'), nullable=False)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime)

class QuizResult(Base):
    __tablename__ = "quiz_results"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    quiz_id = Column(Integer, ForeignKey('quizzes.id'), nullable=False)
    total_score = Column(Float, nullable=False)
    status = Column(String(50))
    attempt_count = Column(Integer)

# ==========================================
# 5. TÀI CHÍNH & TƯƠNG TÁC
# ==========================================
class Payment(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    amount = Column(Numeric(18, 2), nullable=False) # Đã đổi thành Numeric cho khớp Decimal
    payment_method = Column(String(100))
    transaction_id = Column(String(100), nullable=False)

class Coupon(Base):
    __tablename__ = "coupons"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    code = Column(String(50), nullable=False)
    discount_val = Column(Integer, nullable=False)
    expiry_date = Column(DateTime, nullable=False)
    usage_limit = Column(Integer, nullable=False)

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Integer)
    comment = Column(String(500))
    created_at = Column(DateTime)
from flask import current_app as app, jsonify
from app.models import Post


@app.route('/')
@app.route('/index')
def index():
    # 'title': 'EAT | Home'
    posts = Post.query.order_by(Post.date_created.desc()).all()
    
    return jsonify([p.to_dict() for p in posts])

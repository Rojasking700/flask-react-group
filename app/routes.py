from flask import current_app as app
from app.models import Post


@app.route('/')
@app.route('/index')
def index():
    context = {
        'title': 'EAT | Home',
        'posts': Post.query.order_by(Post.date_created.desc()).all()
    }
    return jsonify(context)

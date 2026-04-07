from flask import Flask, jsonify, session
from models import db, Article

app = Flask(__name__)

app.secret_key = "secret-key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# ✅ CREATE TABLE + SEED DATA
with app.app_context():
    db.create_all()

    if Article.query.count() == 0:
        db.session.add_all([
            Article(author="Author 1", title="First Article", content="Content 1"),
            Article(author="Author 2", title="Second Article", content="Content 2"),
            Article(author="Author 3", title="Third Article", content="Content 3"),
            Article(author="Author 4", title="Fourth Article", content="Content 4"),
        ])
        db.session.commit()


@app.route('/articles/<int:id>', methods=['GET'])
def get_article(id):

    # Initialize session
    if 'page_views' not in session:
        session['page_views'] = 0

    # Increment views
    session['page_views'] += 1

    # ✅ PAYWALL (MATCH TEST EXACTLY)
    if session['page_views'] > 3:
        return jsonify({
            "message": "Maximum pageview limit reached"
        }), 401

    # Get article
    article = Article.query.filter_by(id=id).first()

    if article is None:
        return jsonify({"message": "Article not found"}), 404

    # ✅ INCLUDE author (REQUIRED BY TEST)
    return jsonify({
        "id": article.id,
        "author": article.author,
        "title": article.title,
        "content": article.content
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
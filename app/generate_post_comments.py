from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from app import db
from app.models import User, Post, Comment

def post_comments():
    fake = Faker()
    user_count = User.query.count()
    post_count = Post.query.count()
    for i in range(1,post_count+1):
        p = Post.query.get(i)
        for i in range(randint(10,15)):
            u = User.query.offset(randint(0, user_count - 1)).first()
            comment = Comment(
                        body=fake.text(),
                        date_created=fake.past_date(),
                        author=u,
                        post=p)
            db.session.add(comment)
    db.session.commit()
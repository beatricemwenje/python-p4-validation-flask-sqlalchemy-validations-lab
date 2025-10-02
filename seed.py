#!/usr/bin/env python3
from random import choice as rc
from faker import Faker

from app import app
from models import db, Author, Post

fake = Faker()

with app.app_context():
    print("Deleting old data...")
    Author.query.delete()
    Post.query.delete()

    print("Creating authors...")
    authors = []
    for _ in range(10):
        author = Author(
            name=fake.name(),
            phone_number=fake.msisdn()[:10]  # ensures 10 digits
        )
        authors.append(author)
    db.session.add_all(authors)

    print("Creating posts...")
    posts = []
    for _ in range(20):
        post = Post(
            title=fake.sentence(nb_words=4),
            content=fake.text(max_nb_chars=300) * 2,
            category=rc(["Fiction", "Non-Fiction"]),
            summary=fake.sentence(nb_words=10),
            author=rc(authors)
        )
        posts.append(post)
    db.session.add_all(posts)

    db.session.commit()
    print("Seeding done!")

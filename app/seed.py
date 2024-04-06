import sys
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
import random

# Add the project's root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import your models here
from app import db, app
from models import Hero, Power, HeroPower

# Create an application context
with app.app_context():

    # Seeding powers
    powers_data = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"},
    ]

    powers = [Power(**data) for data in powers_data]
    db.session.bulk_save_objects(powers)
    db.session.commit()

    # Seeding heroes
    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"},
    ]

    heroes = [Hero(**data) for data in heroes_data]
    db.session.bulk_save_objects(heroes)
    db.session.commit()

    # Adding powers to heroes
    strengths = ["Strong", "Weak", "Average"]
    for hero in heroes:
        for _ in range(random.randint(1, 3)):
            power = random.choice(powers)
            hero_power = HeroPower(hero=hero, power=power, strength=random.choice(strengths))
            db.session.add(hero_power)

    db.session.commit()

    print("🦸‍♀️ Done seeding!")


#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify 
from flask_restful import Resource, Api
from flask_migrate import Migrate

from models import db, Hero, Power, HeroPower

import os 

abs_path=os.getcwd()
db_path=f'sqlite:///{abs_path}/db/app.db'

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return 'Superheroes'

class Heroes(Resource):
    def get(self):
        heroes =[]
        for hero in Hero.query.all():
            hero_dict = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name
            }
            heroes.append(hero_dict)
        return make_response(jsonify(heroes), 200)

class HeroesId(Resource):
    
    def get(self, id):
        hero = Hero.query.filter(Hero.id == id).first()
        
        if hero:
            hero_dict = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": []
            }

            for hero_power in hero.hero_power:
                power_dict = {
                    "id": hero_power.power.id,
                    "name": hero_power.power.name,
                    "description": hero_power.power.description
                }
                hero_dict["powers"].append(power_dict)

            return make_response(jsonify(hero_dict), 200)
        else:
            return make_response(jsonify({"error": "Hero not found"}), 404)
        
class Powers(Resource):
    
    def get(self):
        powers =[]
        
        for power in Power.query.all():
            power_dict = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            powers.append(power_dict)
        return make_response(jsonify(powers), 200)
    
class PowersId(Resource):
    
    def get(self, id):
        power =  Power.query.filter(Power.id == id).first()
        
        if power:
            power_dict = {
                "id": power.id, 
                "name": power.name, 
                "description": power.description 
            }
            return make_response(jsonify(power_dict), 200)
        else:
            return make_response(jsonify({"error": "Power not found"}), 404)
    
    def patch(self, id):
        
        try:
            power =  Power.query.filter(Power.id == id).first()
            for attr in request.form:
                setattr(power, attr, request.form.get(attr))
                
            db.session.add(power)
            db.session.commit()
            
            power_dict = {
                "id": power.id, 
                "name": power.name, 
                "description": power.description 
            }
            
            return make_response(jsonify(power_dict), 200)
        except ValueError as e:
            return make_response({"error": e.args}, 200)

class HeroPower(Resource):
    
    def post(self):
        data = request.get_json()
        new_hero_power = HeroPower(
            strength = data.get('strength'),
            power_id = data.get('power_id'),
            hero_id = data.get('hero_id')
        )
        db.session.add(new_hero_power)
        db.session.commit()
        
        if new_hero_power:
            return make_response(jsonify(new_hero_power.to_dict), 200)
        else:
            return make_response(jsonify({"errors": ["validation errors"]}), 404)

api.add_resource(Heroes, '/heroes')
api.add_resource(HeroesId, '/heroes/<int:id>')
api.add_resource(Powers, '/powers')
api.add_resource(PowersId, '/powers/<int:id>')
if __name__ == '__main__':
    app.run(port=5555)
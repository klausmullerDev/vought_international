from . import db
from datetime import datetime
import pytz

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    powers = db.Column(db.Text, nullable=False)
    strength_level = db.Column(db.Integer, default=50)
    popularity = db.Column(db.Integer, default=50)
    status = db.Column(db.String(20), default="Active")
    battle_history = db.Column(db.Text, nullable=True)

    crimes = db.relationship('Crime', backref='hero', lazy=True)

    def update_status(self):
        if self.popularity < 20:
            self.status = "Banished"
        elif self.popularity < 50:
            self.status = "Inactive"
        else:
            self.status = "Active"

    def save(self):
        """Ensure strength_level and popularity are within bounds before saving."""
        self.strength_level = max(0, min(100, self.strength_level))
        self.popularity = max(0, min(100, self.popularity))
        db.session.add(self)
        db.session.commit()

class Crime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    severity = db.Column(db.Integer, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    hidden = db.Column(db.Boolean, default=False)  # Novo atributo

    @staticmethod
    def adjust_popularity(entity, severity):
        entity.popularity -= severity
        if isinstance(entity, Hero):
            entity.update_status()
        elif isinstance(entity, Villain):
            entity.update_status()

class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    assigned_heroes = db.Column(db.Text, nullable=False)
    result = db.Column(db.String(20), nullable=True)
    reward_strength = db.Column(db.Integer, default=0)  # Adicione se não existir
    reward_popularity = db.Column(db.Integer, default=0)  # Adicione se não existir
    status = db.Column(db.String(20), default="Pendente")



class Villain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    evil_plan = db.Column(db.Text, nullable=False)
    strength_level = db.Column(db.Integer, default=50)
    popularity = db.Column(db.Integer, default=50)
    


class Battle(db.Model):
    __tablename__ = 'battle'
    id = db.Column(db.Integer, primary_key=True)
    hero1_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    hero2_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(pytz.timezone('America/Sao_Paulo')))

    hero1 = db.relationship('Hero', foreign_keys=[hero1_id])
    hero2 = db.relationship('Hero', foreign_keys=[hero2_id])
    winner = db.relationship('Hero', foreign_keys=[winner_id])



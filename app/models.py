from . import db

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

class Crime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    severity = db.Column(db.Integer, nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    hidden = db.Column(db.Boolean, default=False)  # Novo atributo

    @staticmethod
    def adjust_hero_popularity(hero, severity):
        hero.popularity -= severity
        hero.update_status()

class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    assigned_heroes = db.Column(db.Text, nullable=False)  # IDs dos heróis em uma string
    result = db.Column(db.String(20), nullable=True)
    reward_strength = db.Column(db.Integer, default=0)  # Recompensa de força
    reward_popularity = db.Column(db.Integer, default=0)  # Recompensa de popularidade

class Villain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    evil_plan = db.Column(db.Text, nullable=False)
    strength_level = db.Column(db.Integer, default=50)
    popularity = db.Column(db.Integer, default=50)
    
    
    
    


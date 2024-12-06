
from app import db
from app.models import Hero, Villain, Crime, Mission

# Populando Heróis
heroes = [
    Hero(name='Homelander', age=40, gender='Male', powers='Super força, voo, visão a laser', strength_level=95, popularity=90),
    Hero(name='Queen Maeve', age=35, gender='Female', powers='Super força, resistência', strength_level=85, popularity=70),
    Hero(name='A-Train', age=28, gender='Male', powers='Super velocidade', strength_level=80, popularity=65),
    Hero(name='The Deep', age=32, gender='Male', powers='Comunicação com animais aquáticos', strength_level=70, popularity=50),
    Hero(name='Starlight', age=25, gender='Female', powers='Manipulação de luz', strength_level=75, popularity=80),
]

# Populando Vilões
villains = [
    Villain(name='Stormfront', evil_plan='Dominação mundial', strength_level=90, popularity=80),
    Villain(name='Black Noir (Rebel)', evil_plan='Eliminar os heróis', strength_level=95, popularity=50),
    Villain(name='Soldier Boy', evil_plan='Retomar sua glória', strength_level=88, popularity=60),
]

# Populando Missões
missions = [
    Mission(name='Resgate de Reféns', description='Salvar civis sequestrados por vilões.', difficulty=80, assigned_heroes='1,2', reward_strength=10, reward_popularity=15),
    Mission(name='Proteção de Dignitários', description='Proteger líderes mundiais em cúpula de paz.', difficulty=70, assigned_heroes='3,4', reward_strength=5, reward_popularity=10),
]

# Inserindo dados no banco de dados
with app_context():
    db.session.add_all(heroes)
    db.session.add_all(villains)
    db.session.add_all(missions)
    db.session.commit()
    print("Banco de dados populado com sucesso!")

    # Verificar missões existentes
    missions = Mission.query.all()
    for mission in missions:
        print(f"Missão: {mission.name} - Status: {mission.status}")

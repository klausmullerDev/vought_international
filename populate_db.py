from app import create_app, db
from app.models import Hero, Villain, Crime, Mission
from datetime import datetime

# Criar o app para acessar o contexto
app = create_app()

# Populando Heróis
heroes = [
    Hero(name='Homelander', age=40, gender='Male', strength_level=95, popularity=90, powers="Super força, voo, visão laser"),
    Hero(name='Queen Maeve', age=35, gender='Female', strength_level=85, popularity=70, powers="Super força, durabilidade"),
    Hero(name='A-Train', age=28, gender='Male', strength_level=80, popularity=65, powers="Super velocidade"),
    Hero(name='The Deep', age=32, gender='Male', strength_level=70, popularity=50, powers="Respiração aquática, comunicação com animais marinhos"),
    Hero(name='Starlight', age=25, gender='Female', strength_level=75, popularity=80, powers="Controle de luz, super força"),
    Hero(name='Black Noir', age=33, gender='Male', strength_level=90, popularity=60, powers="Habilidades furtivas, super força"),
    Hero(name='Billy Butcher', age=38, gender='Male', strength_level=88, popularity=55, powers="Habilidades táticas, liderança"),
    Hero(name='Hughie Campbell', age=30, gender='Male', strength_level=65, popularity=45, powers="Inteligência, coragem")
]

# Populando Vilões
villains = [
    Villain(name='Stormfront', evil_plan='Dominar o mundo com ideologia neonazista', strength_level=90, popularity=80),
    Villain(name='Black Noir (Rebel)', evil_plan='Eliminar todos os membros dos The Seven', strength_level=95, popularity=50),
    Villain(name='Soldier Boy', evil_plan='Retomar seu posto como o maior herói da América', strength_level=88, popularity=60),
    Villain(name='Tek Knight', evil_plan='Acabar com qualquer herói que atrapalhe seus planos', strength_level=78, popularity=40),
    Villain(name='Lamplighter', evil_plan='Aumentar a destruição e sua fama ao mesmo tempo', strength_level=75, popularity=55)
]

# Populando Crimes
crimes = [
    Crime(hero_id=1, name="Homicídio de um civil", description='Homicídio de um civil inocente durante operação', 
          date=datetime(2024, 12, 1), severity=85),
    Crime(hero_id=2, name="Roubo de armas", description='Colaboração com criminosos para roubo de armas', 
          date=datetime(2024, 11, 20), severity=60),
    Crime(hero_id=3, name="Acidente em alta velocidade", description='Uso excessivo de velocidade causando acidentes', 
          date=datetime(2024, 11, 15), severity=70),
    Crime(hero_id=4, name="Poluição ambiental", description='Poluição ambiental por negligência', 
          date=datetime(2024, 10, 30), severity=50),
    Crime(hero_id=5, name="Promoção pessoal indevida", description='Uso indevido de poderes para promoção pessoal', 
          date=datetime(2024, 10, 25), severity=40),
    Crime(hero_id=6, name="Ataque urbano", description='Ataque não autorizado em área urbana', 
          date=datetime(2024, 10, 20), severity=75),
    Crime(hero_id=7, name="Assassinato de super-herói", description='Assassinato de um super-herói rival', 
          date=datetime(2024, 9, 15), severity=95),
    Crime(hero_id=8, name="Roubo de tecnologia", description='Roubo de tecnologia da Vought', 
          date=datetime(2024, 9, 10), severity=65)
]

# Populando Missões
missions = [
    Mission(name='Resgate de Reféns', description='Libertar civis mantidos como reféns por vilões armados.', 
            difficulty=80, assigned_heroes='1,2,5', reward_strength=10, reward_popularity=15),
    Mission(name='Prevenção de Catástrofe', description='Evitar a explosão de uma usina nuclear sequestrada.', 
            difficulty=90, assigned_heroes='1,6', reward_strength=20, reward_popularity=25),
    Mission(name='Investigação de Conspiração', description='Descobrir o envolvimento da Vought em um ataque terrorista.', 
            difficulty=70, assigned_heroes='7,8', reward_strength=15, reward_popularity=10),
    Mission(name='Proteção de Dignitários', description='Proteger líderes mundiais em uma cúpula de paz.', 
            difficulty=60, assigned_heroes='2,5', reward_strength=10, reward_popularity=20),
    Mission(name='Caça ao Vilão', description='Capturar Stormfront antes que ela inicie um novo ataque.', 
            difficulty=95, assigned_heroes='1,3,4', reward_strength=25, reward_popularity=30)
]

# Inserindo no Banco de Dados
with app.app_context():
    # Apagar dados antigos (se necessário)
    db.drop_all()
    db.create_all()

    # Inserir dados
    db.session.add_all(heroes)
    db.session.add_all(villains)
    db.session.add_all(crimes)
    db.session.add_all(missions)

    # Confirmar alterações
    db.session.commit()

    print("Banco de dados populado com sucesso!")

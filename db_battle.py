from app import create_app, db
from app.models import Battle

app = create_app()

with app.app_context():
    battles = Battle.query.all()
    for battle in battles:
        print(f"Data: {battle.timestamp}, Hero1: {battle.hero1.name if battle.hero1 else 'Desconhecido'}, "
              f"Hero2: {battle.hero2.name if battle.hero2 else 'Desconhecido'}, "
              f"Winner: {battle.winner.name if battle.winner else 'Empate'}")

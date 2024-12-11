# Populando Batalhas
from random import choice, randint
from datetime import timedelta
from app import create_app
from datetime import datetime, timedelta
import pytz

from app.models import Hero, Battle, db

app = create_app()


def generate_battles(heroes, num_battles=20):
    """Gera batalhas aleatórias entre heróis."""
    battles = []
    for _ in range(num_battles):
        # Seleciona dois heróis aleatoriamente para batalhar
        hero1, hero2 = choice(heroes), choice(heroes)
        while hero1["id"] == hero2["id"]:
            hero2 = choice(heroes)  # Evitar que sejam o mesmo herói

        # Determina o vencedor ou empate
        winner_id = None if randint(0, 4) == 0 else choice([hero1["id"], hero2["id"]])

        # Cria a data aleatória para a batalha
        timestamp = datetime.now(pytz.timezone('America/Sao_Paulo')) - timedelta(days=randint(1, 365))

        # Adiciona a batalha à lista
        battles.append({
            "hero1_id": hero1["id"],
            "hero2_id": hero2["id"],
            "winner_id": winner_id,
            "timestamp": timestamp
        })
    return battles


with app.app_context():
    # Carregar heróis para usar nos registros
    heroes = [{"id": h.id, "name": h.name} for h in Hero.query.all()]
    battles = generate_battles(heroes)

    # Inserir batalhas no banco de dados
    for battle in battles:
        existing = Battle.query.filter_by(
            hero1_id=battle["hero1_id"],
            hero2_id=battle["hero2_id"],
            timestamp=battle["timestamp"]
        ).first()
        if not existing:
            db.session.add(Battle(**battle))
    db.session.commit()

    # Exibir status das batalhas
    all_battles = Battle.query.all()
    for b in all_battles:
        winner = b.winner.name if b.winner else "Empate"
        print(f"Batalha: {b.hero1.name} VS {b.hero2.name} - Vencedor: {winner}")

    print("Batalhas adicionadas com sucesso!")

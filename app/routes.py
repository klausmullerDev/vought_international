from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import Hero, Crime, Mission, Villain
from . import db
from datetime import datetime
import random  # Certifique-se de importar random

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    heroes = Hero.query.all()
    return render_template('index.html', heroes=heroes)

@bp.route('/add_hero', methods=['POST'])
def add_hero():
    data = request.form
    new_hero = Hero(
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        powers=data['powers']
    )
    db.session.add(new_hero)
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.route('/simulate_battle', methods=['POST'])
def simulate_battle():
    hero1_id = int(request.form['hero1_id'])
    hero2_id = int(request.form['hero2_id'])

    hero1 = Hero.query.get(hero1_id)
    hero2 = Hero.query.get(hero2_id)

    if not hero1 or not hero2:
        return jsonify({"error": "Invalid heroes"}), 400

    # Cálculo do resultado
    hero1_score = hero1.strength_level + hero1.popularity + random.randint(-10, 10)
    hero2_score = hero2.strength_level + hero2.popularity + random.randint(-10, 10)

    if hero1_score > hero2_score:
        hero1.battle_history = f"{hero1.battle_history}W" if hero1.battle_history else "W"
        hero2.battle_history = f"{hero2.battle_history}L" if hero2.battle_history else "L"
        winner = hero1
    else:
        hero2.battle_history = f"{hero2.battle_history}W" if hero2.battle_history else "W"
        hero1.battle_history = f"{hero1.battle_history}L" if hero1.battle_history else "L"
        winner = hero2

    db.session.commit()
    return jsonify({"winner": winner.name})

@bp.route('/add_crime', methods=['POST'])
def add_crime():
    data = request.form
    hero = Hero.query.get(data['hero_id'])
    if hero:
        new_crime = Crime(
            name=data['name'],
            description=data['description'],
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            severity=int(data['severity']),
            hero_id=hero.id
        )
        # Ajuste da popularidade do herói com base na severidade do crime
        hero.popularity -= int(data['severity'])
        if hero.popularity < 20:
            hero.status = "Banished"
        elif hero.popularity < 50:
            hero.status = "Inactive"
        else:
            hero.status = "Active"

        db.session.add(new_crime)
        db.session.commit()
    return redirect(url_for('main.index'))

@bp.route('/view_crimes/<int:hero_id>')
def view_crimes(hero_id):
    hero = Hero.query.get(hero_id)  # Busca o herói com base no ID
    if not hero:
        return jsonify({"error": "Herói não encontrado"}), 404

    crimes = Crime.query.filter_by(hero_id=hero_id).all()
    return render_template('crimes.html', hero=hero, crimes=crimes)

@bp.route('/add_mission', methods=['POST'])
def add_mission():
    data = request.form
    assigned_heroes = ','.join(data.getlist('hero_ids'))
    new_mission = Mission(
        name=data['name'],
        description=data['description'],
        difficulty=int(data['difficulty']),
        assigned_heroes=assigned_heroes
    )
    db.session.add(new_mission)
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.route('/view_missions')
def view_missions():
    missions = Mission.query.all()
    return render_template('missions.html', missions=missions)


@bp.route('/battle', methods=['GET', 'POST'])
def battle():
    if request.method == 'GET':
        # Obter todos os heróis e vilões para seleção
        heroes = Hero.query.all()
        villains = Villain.query.all()
        return render_template('battle.html', heroes=heroes, villains=villains)

    elif request.method == 'POST':
        # Obter IDs dos combatentes
        hero_id = int(request.form['hero_id'])
        opponent_type = request.form['opponent_type']
        opponent_id = int(request.form['opponent_id'])

        # Obter o herói e o oponente (herói ou vilão)
        hero = Hero.query.get(hero_id)
        opponent = None
        if opponent_type == 'hero':
            opponent = Hero.query.get(opponent_id)
        elif opponent_type == 'villain':
            opponent = Villain.query.get(opponent_id)

        if not hero or not opponent:
            return jsonify({"error": "Invalid combatants selected"}), 400

        # Calcular resultado
        result = simulate_battle(hero, opponent)
        return render_template('battle_result.html', hero=hero, opponent=opponent, result=result)

import random

def simulate_battle(hero, opponent):
    # Calcular os atributos de cada combatente
    hero_score = hero.strength_level + hero.popularity + random.randint(-10, 10)
    opponent_score = opponent.strength_level + opponent.popularity + random.randint(-10, 10)

    # Determinar o vencedor
    if hero_score > opponent_score:
        winner = hero
        loser = opponent
        result = f"{hero.name} venceu {opponent.name}!"
        if isinstance(opponent, Hero):
            opponent.battle_history = f"{opponent.battle_history}L" if opponent.battle_history else "L"
        hero.battle_history = f"{hero.battle_history}W" if hero.battle_history else "W"
    else:
        winner = opponent
        loser = hero
        result = f"{opponent.name} venceu {hero.name}!"
        if isinstance(hero, Hero):
            hero.battle_history = f"{hero.battle_history}L" if hero.battle_history else "L"
        if isinstance(opponent, Hero):
            opponent.battle_history = f"{opponent.battle_history}W" if opponent.battle_history else "W"

    # Atualizar popularidade dos combatentes
    winner.popularity += 5
    loser.popularity -= 5

    db.session.commit()
    return result


# Adicionar Rota para Remover Herói
@bp.route('/delete_hero/<int:hero_id>', methods=['POST'])
def delete_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if hero:
        db.session.delete(hero)
        db.session.commit()
        return redirect(url_for('main.index'))
    return jsonify({"error": "Herói não encontrado"}), 404

# Adicionar Rota para Modificar Herói
@bp.route('/edit_hero/<int:hero_id>', methods=['GET', 'POST'])
def edit_hero(hero_id):
    hero = Hero.query.get(hero_id)
    if not hero:
        return jsonify({"error": "Herói não encontrado"}), 404

    if request.method == 'POST':
        data = request.form
        hero.name = data['name']
        hero.age = data['age']
        hero.gender = data['gender']
        hero.powers = data['powers']
        hero.strength_level = int(data['strength_level'])
        hero.popularity = int(data['popularity'])
        hero.update_status()
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('edit_hero.html', hero=hero)

# Consultar Heróis por Nome, Status ou Popularidade
@bp.route('/search_heroes', methods=['GET'])
def search_heroes():
    query = request.args.get('query', '')
    filter_by = request.args.get('filter_by', 'name')

    if filter_by == 'name':
        heroes = Hero.query.filter(Hero.name.ilike(f"%{query}%")).all()
    elif filter_by == 'status':
        heroes = Hero.query.filter_by(status=query).all()
    elif filter_by == 'popularity':
        try:
            popularity = int(query)
            heroes = Hero.query.filter(Hero.popularity >= popularity).all()
        except ValueError:
            heroes = []
    else:
        heroes = []

    return render_template('search_heroes.html', heroes=heroes)

# Ocultar Crime
@bp.route('/hide_crime/<int:crime_id>', methods=['POST'])
def hide_crime(crime_id):
    crime = Crime.query.get(crime_id)
    if crime:
        crime.hidden = True
        db.session.commit()
        return redirect(url_for('main.view_crimes', hero_id=crime.hero_id))
    return jsonify({"error": "Crime não encontrado"}), 404

# Exibir Crimes Ocultos
@bp.route('/hidden_crimes')
def hidden_crimes():
    crimes = Crime.query.filter_by(hidden=True).all()
    return render_template('hidden_crimes.html', crimes=crimes)

@bp.route('/complete_mission/<int:mission_id>', methods=['POST'])
def complete_mission(mission_id):
    mission = Mission.query.get(mission_id)
    if not mission:
        return jsonify({"error": "Missão não encontrada"}), 404

    result = request.form['result']
    mission.result = result

    hero_ids = [int(id) for id in mission.assigned_heroes.split(',')]
    for hero_id in hero_ids:
        hero = Hero.query.get(hero_id)
        if result == 'Sucesso':
            hero.strength_level += mission.reward_strength
            hero.popularity += mission.reward_popularity
        elif result == 'Fracasso':
            hero.strength_level -= 5
            hero.popularity -= 10
        hero.update_status()

    db.session.commit()
    return redirect(url_for('main.view_missions'))


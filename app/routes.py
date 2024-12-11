from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from .models import Hero, Crime, Mission, Villain, Battle
from . import db
from datetime import datetime
import random  
import pytz

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
def simulate_battle(hero, opponent):
    log = []
    hero_hp = 100
    opponent_hp = 100

    while hero_hp > 0 and opponent_hp > 0:
        # Turno do herói
        hero_roll = roll_dice() + (hero.popularity / 10)
        opponent_roll = roll_dice() + (opponent.popularity / 10)

        if hero_roll > opponent_roll:
            damage = roll_dice(sides=10)
            opponent_hp = max(0, opponent_hp - damage)  # Evitar valores negativos
            log.append(
                f"{hero.name} atacou {opponent.name}. Jogada: {hero_roll:.1f} > {opponent_roll:.1f}. Causou {damage} de dano."
            )
        else:
            log.append(
                f"{hero.name} atacou {opponent.name}. Jogada: {hero_roll:.1f} <= {opponent_roll:.1f}. Ataque falhou."
            )

        if opponent_hp <= 0:
            log.append(f"{opponent.name} foi derrotado!")
            break

        # Turno do oponente
        opponent_roll = roll_dice() + (opponent.popularity / 10)
        hero_roll = roll_dice() + (hero.popularity / 10)

        if opponent_roll > hero_roll:
            damage = roll_dice(sides=10)
            hero_hp = max(0, hero_hp - damage)  # Evitar valores negativos
            log.append(
                f"{opponent.name} atacou {hero.name}. Jogada: {opponent_roll:.1f} > {hero_roll:.1f}. Causou {damage} de dano."
            )
        else:
            log.append(
                f"{opponent.name} atacou {hero.name}. Jogada: {opponent_roll:.1f} <= {hero_roll:.1f}. Ataque falhou."
            )

        if hero_hp <= 0:
            log.append(f"{hero.name} foi derrotado!")
            break

    # Determinar o vencedor
    winner = hero if hero_hp > 0 else opponent

    # Registrar batalha no banco de dados
    try:
        battle = Battle(
            hero1_id=hero.id,
            hero2_id=opponent.id,
            winner_id=winner.id if winner else None,
            timestamp=datetime.now(pytz.timezone('America/Sao_Paulo'))  # Garantir fuso horário correto
        )
        db.session.add(battle)
        db.session.commit()
    except Exception as e:
        log.append(f"Erro ao salvar a batalha: {e}")
        db.session.rollback()
        return None, log

    return winner, log



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

@bp.route('/crimes', methods=['GET', 'POST'])
def crimes():
    if request.method == 'POST':
        # Adicionar crime
        data = request.form
        hero_id = data.get('hero_id')
        hero = Hero.query.get(hero_id)
        if hero:
            new_crime = Crime(
                name=data['name'],
                description=data['description'],
                date=datetime.strptime(data['date'], '%Y-%m-%d'),
                severity=int(data['severity']),
                hero_id=hero_id
            )
            # Atualizar popularidade do herói
            hero.popularity -= int(data['severity'])
            hero.update_status()
            db.session.add(new_crime)
            db.session.commit()
    crimes = Crime.query.all()
    heroes = Hero.query.all()
    return render_template('crimes.html', crimes=crimes, heroes=heroes)


@bp.route('/unhide_crime/<int:crime_id>', methods=['POST'])
def unhide_crime(crime_id):
    # Buscar o crime pelo ID
    crime = Crime.query.get(crime_id)
    if crime:
        # Alterar o status para "não oculto"
        crime.hidden = False
        db.session.commit()
        return redirect(url_for('main.view_crimes', hero_id=crime.hero_id))
    return jsonify({"error": "Crime não encontrado"}), 404



@bp.route('/delete_crime/<int:crime_id>', methods=['POST'])
def delete_crime(crime_id):
    crime = Crime.query.get(crime_id)
    if crime:
        db.session.delete(crime)
        db.session.commit()
        return redirect(url_for('main.crimes'))
    return jsonify({"error": "Crime não encontrado"}), 404


def simulate_battle(hero, opponent):
    hero_score = hero.strength_level + hero.popularity + random.randint(-10, 10)
    opponent_score = opponent.strength_level + opponent.popularity + random.randint(-10, 10)

    if hero_score > opponent_score:
        winner = hero
        loser = opponent
        result = f"{hero.name} venceu {opponent.name}!"
    else:
        winner = opponent
        loser = hero
        result = f"{opponent.name} venceu {hero.name}!"

    # Atualizar popularidade
    winner.popularity = min(winner.popularity + 5, 100)
    loser.popularity = max(loser.popularity - 5, 0)

    # Registrar batalha
    battle = Battle(
    hero1_id=hero.id,
    hero2_id=opponent.id,
    winner_id=winner.id if winner else None,
    timestamp=datetime.utcnow()
    )
    db.session.add(battle)
    db.session.commit()



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

        # Validar força e popularidade
        hero.strength_level = max(0, min(100, int(data['strength_level'])))
        hero.popularity = max(0, min(100, int(data['popularity'])))
        
        hero.update_status()
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('edit_hero.html', hero=hero)


# Consultar Heróis por Nome, Status ou Popularidade
@bp.route('/search_heroes', methods=['GET'])
def search_heroes():
    query = request.args.get('query', '').strip()
    filter_by = request.args.get('filter_by', 'name')
    order = request.args.get('order', 'asc')  # Padrão para ordem crescente

    heroes = None

    # Filtragem de acordo com o campo escolhido
    if not query:
        heroes = Hero.query
    else:
        if filter_by == 'name':
            heroes = Hero.query.filter(Hero.name.ilike(f"%{query}%"))
        elif filter_by == 'status':
            heroes = Hero.query.filter_by(status=query)
        elif filter_by == 'popularity':
            try:
                popularity = int(query)
                heroes = Hero.query.filter(Hero.popularity >= popularity)
            except ValueError:
                heroes = Hero.query.filter_by()  # Sem correspondência
        else:
            heroes = Hero.query

    # Ordenação
    if heroes is not None:
        if filter_by == 'popularity':
            if order == 'desc':
                heroes = heroes.order_by(Hero.popularity.desc())
            else:
                heroes = heroes.order_by(Hero.popularity.asc())
        else:
            heroes = heroes.order_by(Hero.name.asc())

    heroes = heroes.all()
    return render_template(
        'search_heroes.html', 
        heroes=heroes, 
        query=query, 
        filter_by=filter_by, 
        order=order
    )




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

@bp.route('/battle_log')
def battle_log():
    battles = Battle.query.order_by(Battle.timestamp.desc()).all()
    heroes = Hero.query.all()  # Para o modal de adicionar batalhas
    return render_template('battle_log.html', battles=battles, heroes=heroes)


@bp.route('/add_battle', methods=['POST'])
def add_battle():
    data = request.form
    hero1_id = data.get('hero1_id')
    hero2_id = data.get('hero2_id')
    winner_id = data.get('winner_id') if data.get('winner_id') else None

    hero1 = Hero.query.get(hero1_id)
    hero2 = Hero.query.get(hero2_id)
    winner = Hero.query.get(winner_id) if winner_id else None

    if hero1 and hero2:
        battle = Battle(
            hero1_id=hero1.id,
            hero2_id=hero2.id,
            winner_id=winner.id if winner else None,
            timestamp=datetime.now(pytz.timezone('America/Sao_Paulo'))
        )
        db.session.add(battle)
        db.session.commit()
        return redirect(url_for('main.battle_log'))
    return jsonify({"error": "Heróis inválidos"}), 400

@bp.route('/delete_battle/<int:battle_id>', methods=['POST'])
def delete_battle(battle_id):
    battle = Battle.query.get(battle_id)
    if battle:
        db.session.delete(battle)
        db.session.commit()
        return redirect(url_for('main.battle_log'))
    return jsonify({"error": "Batalha não encontrada"}), 404



@bp.route('/add_mission', methods=['POST', 'GET'])
def add_mission():
    
    if request.method == 'GET':
        heroes = Hero.query.order_by(Hero.name).all()  # Ordena os heróis por nome
        return render_template('add_mission.html', heroes=heroes)
    elif request.method == 'POST':
        data = request.form
        assigned_heroes = ','.join(data.getlist('hero_ids'))
        new_mission = Mission(
            name=data['name'],
            description=data['description'],
            difficulty=int(data['difficulty']),
            assigned_heroes=assigned_heroes,
            reward_strength=int(data['reward_strength']),
            reward_popularity=int(data['reward_popularity']),
            status="Pendente"
        )
        db.session.add(new_mission)
        db.session.commit()
        return redirect(url_for('main.view_missions'))


@bp.route('/view_missions')
def view_missions():
    """Lista todas as missões."""
    missions = Mission.query.all()
    return render_template('missions.html', missions=missions)


@bp.route('/edit_mission/<int:mission_id>', methods=['GET', 'POST'])
def edit_mission(mission_id):
    mission = Mission.query.get(mission_id)
    if not mission:
        return jsonify({"error": "Missão não encontrada"}), 404

    if request.method == 'POST':
        data = request.form
        mission.name = data['name']
        mission.description = data['description']
        mission.difficulty = int(data['difficulty'])
        mission.assigned_heroes = ','.join(data.getlist('hero_ids'))
        db.session.commit()
        return redirect(url_for('main.view_missions'))

    heroes = Hero.query.order_by(Hero.name).all()
    return render_template('edit_mission.html', mission=mission, heroes=heroes)



@bp.route('/execute_mission/<int:mission_id>', methods=['POST'])
def execute_mission(mission_id):
    """Executa uma missão e calcula o resultado."""
    mission = Mission.query.get(mission_id)
    if not mission:
        return jsonify({"error": "Missão não encontrada"}), 404

    hero_ids = [int(hero_id) for hero_id in mission.assigned_heroes.split(',')]
    heroes = [Hero.query.get(hero_id) for hero_id in hero_ids]

    # Calcular força total da equipe
    team_strength = sum(hero.strength_level for hero in heroes)
    success_threshold = mission.difficulty + random.randint(-10, 10)

    if team_strength >= success_threshold:
        mission.status = "Concluída"
        result = "Sucesso"
        for hero in heroes:
            hero.strength_level = min(hero.strength_level + mission.reward_strength, 100)
            hero.popularity = min(hero.popularity + mission.reward_popularity, 100)
    else:
        mission.status = "Falhada"
        result = "Fracasso"
        for hero in heroes:
            hero.strength_level = max(hero.strength_level - 5, 0)
            hero.popularity = max(hero.popularity - 10, 0)

    db.session.commit()
    return render_template('mission_result.html', mission=mission, result=result, heroes=heroes)

@bp.route('/delete_mission/<int:mission_id>', methods=['POST'])
def delete_mission(mission_id):
    mission = Mission.query.get(mission_id)
    if not mission:
        return jsonify({"error": "Missão não encontrada"}), 404

    db.session.delete(mission)
    db.session.commit()
    return redirect(url_for('main.view_missions'))

@bp.route('/battle', methods=['GET', 'POST'])
def battle():
    if request.method == 'GET':
        heroes = Hero.query.all()
        villains = Villain.query.all()
        return render_template('battle.html', heroes=heroes, villains=villains)

    elif request.method == 'POST':
        hero_id = int(request.form['hero_id'])
        opponent_type = request.form['opponent_type']
        opponent_id = int(request.form['opponent_id'])

        hero = Hero.query.get(hero_id)
        opponent = None

        if opponent_type == 'hero':
            opponent = Hero.query.get(opponent_id)
        elif opponent_type == 'villain':
            opponent = Villain.query.get(opponent_id)

        if not hero or not opponent:
            return jsonify({"error": "Herói ou oponente inválido"}), 400

        winner, log = simulate_battle(hero, opponent)

        if winner is None:
            return jsonify({"error": "Erro ao salvar batalha"}), 500

        return render_template('battle_result.html', winner=winner, log=log)



def simulate_battle(hero, opponent):
    """Simula uma batalha entre um herói e um oponente."""
    log = []
    hero_hp = 100
    opponent_hp = 100

    while hero_hp > 0 and opponent_hp > 0:
        # Turno do herói
        hero_roll = roll_dice() + (hero.popularity / 10)
        opponent_roll = roll_dice() + (opponent.popularity / 10)
        
        if hero_roll > opponent_roll:
            damage = roll_dice(sides=10)
            opponent_hp -= damage
            log.append(f"{hero.name} atacou {opponent.name}. Jogada: {hero_roll:.1f} > {opponent_roll:.1f}. Causou {damage} de dano.")
        else:
            log.append(f"{hero.name} atacou {opponent.name}. Jogada: {hero_roll:.1f} <= {opponent_roll:.1f}. Ataque falhou.")

        if opponent_hp <= 0:
            log.append(f"{opponent.name} foi derrotado!")
            break

        # Turno do oponente
        opponent_roll = roll_dice() + (opponent.popularity / 10)
        hero_roll = roll_dice() + (hero.popularity / 10)
        
        if opponent_roll > hero_roll:
            damage = roll_dice(sides=10)
            hero_hp -= damage
            log.append(f"{opponent.name} atacou {hero.name}. Jogada: {opponent_roll:.1f} > {hero_roll:.1f}. Causou {damage} de dano.")
        else:
            log.append(f"{opponent.name} atacou {hero.name}. Jogada: {opponent_roll:.1f} <= {hero_roll:.1f}. Ataque falhou.")

        if hero_hp <= 0:
            log.append(f"{hero.name} foi derrotado!")
            break

    # Determinar o vencedor
    winner = hero if hero_hp > 0 else opponent

    # Registrar batalha
    try:
        battle = Battle(
            hero1_id=hero.id,
            hero2_id=opponent.id,
            winner_id=winner.id if winner else None,
            timestamp = datetime.now(pytz.timezone('America/Sao_Paulo'))
        )
        db.session.add(battle)
        db.session.commit()
    except Exception as e:
        print(f"Erro ao salvar batalha: {e}")
        db.session.rollback()
        return None, log

    return winner, log


def roll_dice(sides=20):
    """Simula uma rolagem de dado."""
    import random
    return random.randint(1, sides)
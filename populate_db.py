from datetime import datetime
from app import db, create_app
from app.models import Hero, Villain, Crime, Mission

# Criar o contexto da aplicação
app = create_app()

# Função para adicionar registros, evitando duplicatas
def add_if_not_exists(model, data_list):
    for data in data_list:
        existing = model.query.filter_by(name=data['name']).first()
        if not existing:
            db.session.add(model(**data))
        else:
            print(f"{model.__name__} '{data['name']}' já existe no banco de dados.")

# Função para converter strings de data em objetos datetime
def convert_date(data_list, date_field):
    for data in data_list:
        if isinstance(data[date_field], str):  # Verifica se o campo de data é uma string
            data[date_field] = datetime.strptime(data[date_field], '%Y-%m-%d')  # Converte para datetime

# Executar o script dentro do contexto da aplicação
with app.app_context():
    # Populando Heróis
    heroes = [
        {"name": "Homelander", "age": 40, "gender": "Male", "powers": "Super força, voo, visão a laser", "strength_level": 95, "popularity": 90},
        {"name": "Queen Maeve", "age": 35, "gender": "Female", "powers": "Super força, resistência", "strength_level": 85, "popularity": 70},
        {"name": "A-Train", "age": 28, "gender": "Male", "powers": "Super velocidade", "strength_level": 80, "popularity": 65},
        {"name": "The Deep", "age": 32, "gender": "Male", "powers": "Comunicação com animais aquáticos", "strength_level": 70, "popularity": 50},
        {"name": "Starlight", "age": 25, "gender": "Female", "powers": "Manipulação de luz", "strength_level": 75, "popularity": 80},
        {"name": "Black Noir", "age": 35, "gender": "Male", "powers": "Agilidade, força sobre-humana, combate corpo a corpo", "strength_level": 90, "popularity": 60},
        {"name": "Stormfront", "age": 101, "gender": "Female", "powers": "Eletricidade, voo, super força", "strength_level": 85, "popularity": 75},
        {"name": "Billy Butcher", "age": 45, "gender": "Male", "powers": "Sem poderes naturais (mas usa o Composto V temporário)", "strength_level": 70, "popularity": 40},
        {"name": "Hughie Campbell", "age": 30, "gender": "Male", "powers": "Sem poderes naturais (usa o Composto V temporário)", "strength_level": 65, "popularity": 50},
        {"name": "Soldier Boy", "age": 102, "gender": "Male", "powers": "Super força, durabilidade, explosões de energia", "strength_level": 88, "popularity": 60},
    ]
    add_if_not_exists(Hero, heroes)

    # Populando Vilões
    villains = [
        {"name": "Stormfront", "evil_plan": "Dominação mundial", "strength_level": 90, "popularity": 80},
        {"name": "Black Noir (Rebel)", "evil_plan": "Eliminar os heróis", "strength_level": 95, "popularity": 50},
        {"name": "Soldier Boy", "evil_plan": "Retomar sua glória", "strength_level": 88, "popularity": 60},
        {"name": "Victoria Neuman", "evil_plan": "Eliminar super-heróis enquanto acumula poder político", "strength_level": 75, "popularity": 85},
        {"name": "The Crimson Countess", "evil_plan": "Vingar a destruição de seus aliados do Payback", "strength_level": 78, "popularity": 45},
        {"name": "Mindstorm", "evil_plan": "Usar manipulação mental para destruir super-heróis", "strength_level": 85, "popularity": 55},
    ]
    add_if_not_exists(Villain, villains)

    # Populando Missões
    missions = [
    {
        "name": "Resgate de Reféns",
        "description": "Salvar civis sequestrados por vilões em um prédio cheio de explosivos.",
        "difficulty": 80,
        "assigned_heroes": "1,2",  # Homelander, Queen Maeve
        "reward_strength": 10,
        "reward_popularity": 15
    },
    {
        "name": "Proteção de Dignitários",
        "description": "Proteger líderes mundiais durante uma cúpula de paz ameaçada por vilões.",
        "difficulty": 70,
        "assigned_heroes": "3,4",  # A-Train, The Deep
        "reward_strength": 5,
        "reward_popularity": 10
    },
    {
        "name": "Investigação de Infiltração",
        "description": "Identificar quem está vazando informações confidenciais da Vought.",
        "difficulty": 60,
        "assigned_heroes": "5,1",  # Starlight, Homelander
        "reward_strength": 8,
        "reward_popularity": 12
    },
    {
        "name": "Combate a Soldier Boy",
        "description": "Capturar Soldier Boy após um ataque a uma cidade.",
        "difficulty": 90,
        "assigned_heroes": "2,5",  # Queen Maeve, Starlight
        "reward_strength": 15,
        "reward_popularity": 20
    },
    {
        "name": "Evacuação de Civis",
        "description": "Evacuar civis presos em uma área sob ataque de supervilões.",
        "difficulty": 75,
        "assigned_heroes": "4,3",  # The Deep, A-Train
        "reward_strength": 10,
        "reward_popularity": 18
    },
    {
        "name": "Rebelião na Prisão",
        "description": "Conter uma rebelião em uma prisão de segurança máxima para supervilões.",
        "difficulty": 85,
        "assigned_heroes": "1,3",  # Homelander, A-Train
        "reward_strength": 12,
        "reward_popularity": 5
    },
    {
        "name": "Neutralizar Lamplighter",
        "description": "Impedir Lamplighter de incendiar um prédio cheio de reféns.",
        "difficulty": 65,
        "assigned_heroes": "2,4",  # Queen Maeve, The Deep
        "reward_strength": 7,
        "reward_popularity": 10
    },
    {
        "name": "Confronto com Mindstorm",
        "description": "Derrotar Mindstorm e impedir sua manipulação mental em massa.",
        "difficulty": 85,
        "assigned_heroes": "1,6",  # Homelander, Black Noir
        "reward_strength": 20,
        "reward_popularity": 10
    },
    {
        "name": "Missão Humanitária",
        "description": "Entregar suprimentos médicos a uma região afetada por um ataque vilão.",
        "difficulty": 50,
        "assigned_heroes": "5,4",  # Starlight, The Deep
        "reward_strength": 5,
        "reward_popularity": 15
    },
    {
        "name": "Caça à Crimson Countess",
        "description": "Capturar a Crimson Countess após seus ataques terroristas.",
        "difficulty": 80,
        "assigned_heroes": "5,1",  # Starlight, Homelander
        "reward_strength": 12,
        "reward_popularity": 20
    },{
        "name": "Defesa da Torre da Vought",
        "description": "Proteger a Torre da Vought durante um ataque surpresa de vilões.",
        "difficulty": 95,
        "assigned_heroes": "1,6",  # Homelander, Black Noir
        "reward_strength": 15,
        "reward_popularity": 25
    },
    {
        "name": "Interceptação de Contrabando",
        "description": "Impedir o transporte ilegal de Composto V em um navio.",
        "difficulty": 70,
        "assigned_heroes": "3,4",  # A-Train, The Deep
        "reward_strength": 10,
        "reward_popularity": 10
    },
    {
        "name": "Operação Resgate no Ártico",
        "description": "Salvar cientistas presos em uma base no Ártico após um ataque.",
        "difficulty": 80,
        "assigned_heroes": "2,5",  # Queen Maeve, Starlight
        "reward_strength": 12,
        "reward_popularity": 18
    },
    {
        "name": "Caçada ao Stormfront",
        "description": "Localizar Stormfront após sua fuga e impedir mais ataques.",
        "difficulty": 90,
        "assigned_heroes": "1,7",  # Homelander, Queen Maeve
        "reward_strength": 20,
        "reward_popularity": 15
    },
    {
        "name": "Sabotagem de Base Vilã",
        "description": "Infiltrar-se em uma base de vilões para desativar armas nucleares.",
        "difficulty": 85,
        "assigned_heroes": "6,8",  # Black Noir, Billy Butcher
        "reward_strength": 15,
        "reward_popularity": 10
    },
    {
        "name": "Neutralizar Explosão Química",
        "description": "Desativar um laboratório químico prestes a explodir.",
        "difficulty": 75,
        "assigned_heroes": "5,9",  # Starlight, Hughie Campbell
        "reward_strength": 10,
        "reward_popularity": 12
    },
    {
        "name": "Proteção de Evento Global",
        "description": "Garantir a segurança de uma conferência global ameaçada.",
        "difficulty": 65,
        "assigned_heroes": "4,3",  # The Deep, A-Train
        "reward_strength": 8,
        "reward_popularity": 10
    },
    {
        "name": "Rebelião em Base Subterrânea",
        "description": "Conter uma rebelião em uma base subterrânea controlada por vilões.",
        "difficulty": 85,
        "assigned_heroes": "2,6",  # Queen Maeve, Black Noir
        "reward_strength": 15,
        "reward_popularity": 10
    },
    {
        "name": "Missão de Diplomacia",
        "description": "Negociar um tratado de paz com uma facção vilã para evitar um confronto.",
        "difficulty": 50,
        "assigned_heroes": "5,10",  # Starlight, Soldier Boy
        "reward_strength": 5,
        "reward_popularity": 20
    },
    {
        "name": "Recuperação de Composto V",
        "description": "Recuperar um lote roubado de Composto V antes que seja usado.",
        "difficulty": 80,
        "assigned_heroes": "8,9",  # Billy Butcher, Hughie Campbell
        "reward_strength": 12,
        "reward_popularity": 15
    },
    {
        "name": "Defesa de Ponto Estratégico",
        "description": "Proteger um laboratório estratégico da Vought durante um ataque.",
        "difficulty": 90,
        "assigned_heroes": "1,2",  # Homelander, Queen Maeve
        "reward_strength": 15,
        "reward_popularity": 20
    },
    {
        "name": "Treinamento de Novos Heróis",
        "description": "Treinar recrutas da Vought em situações de combate simuladas.",
        "difficulty": 40,
        "assigned_heroes": "5,3",  # Starlight, A-Train
        "reward_strength": 5,
        "reward_popularity": 10
    },
    {
        "name": "Conflito em Cidade Pequena",
        "description": "Impedir que vilões destruam uma pequena cidade em retaliação.",
        "difficulty": 75,
        "assigned_heroes": "2,4",  # Queen Maeve, The Deep
        "reward_strength": 10,
        "reward_popularity": 18
    },
    {
        "name": "Vigilância de Alto Risco",
        "description": "Monitorar uma operação vilã sem ser detectado.",
        "difficulty": 60,
        "assigned_heroes": "6,7",  # Black Noir, Stormfront
        "reward_strength": 8,
        "reward_popularity": 10
    },
    {
        "name": "Resgate no Deserto",
        "description": "Salvar um comboio de civis preso em um deserto dominado por vilões.",
        "difficulty": 85,
        "assigned_heroes": "1,9",  # Homelander, Hughie Campbell
        "reward_strength": 15,
        "reward_popularity": 20
    },
    {
        "name": "Confronto na Área Costeira",
        "description": "Impedir um ataque vilão em um porto estratégico.",
        "difficulty": 70,
        "assigned_heroes": "4,10",  # The Deep, Soldier Boy
        "reward_strength": 10,
        "reward_popularity": 12
    },
    {
        "name": "Operação de Resgate Internacional",
        "description": "Resgatar diplomatas sequestrados em território hostil.",
        "difficulty": 90,
        "assigned_heroes": "2,8",  # Queen Maeve, Billy Butcher
        "reward_strength": 20,
        "reward_popularity": 25
    },
    {
        "name": "Combate ao Villain X",
        "description": "Derrotar um novo vilão que ameaça a segurança global.",
        "difficulty": 95,
        "assigned_heroes": "1,10",  # Homelander, Soldier Boy
        "reward_strength": 25,
        "reward_popularity": 20
    },
    {
        "name": "Rebelião no Espaço",
        "description": "Conter uma rebelião de vilões em uma estação espacial.",
        "difficulty": 100,
        "assigned_heroes": "1,5",  # Homelander, Starlight
        "reward_strength": 30,
        "reward_popularity": 30
    }
]

    add_if_not_exists(Mission, missions)

    # Populando Crimes
    crimes = [
        {"name": "Acidente do Voo 37", "description": "Permitiu que o avião caísse para manipular a opinião pública.", "date": "2020-08-15", "severity": 100, "hero_id": 1, "hidden": True},
    {"name": "Massacre em uma aldeia na Síria", "description": "Homelander matou dezenas durante uma operação militar.", "date": "2021-03-12", "severity": 85, "hero_id": 1, "hidden": True},
    {"name": "Destruição de prédio corporativo", "description": "Explodiu um prédio para eliminar um inimigo da Vought.", "date": "2021-09-25", "severity": 90, "hero_id": 1, "hidden": True},
    {"name": "Execução em público", "description": "Matou um manifestante com laser durante um comício ao vivo.", "date": "2022-04-10", "severity": 95, "hero_id": 1, "hidden": True},
    {"name": "Ameaça a político", "description": "Coagiu um senador para apoiar a Vought.", "date": "2022-07-15", "severity": 70, "hero_id": 1, "hidden": False},
    {"name": "Conivência no Voo 37", "description": "Permitiu a queda do avião junto com Homelander.", "date": "2020-08-15", "severity": 70, "hero_id": 2, "hidden": True},
    {"name": "Destruição de ponte", "description": "Colapsou uma ponte durante uma operação mal planejada.", "date": "2021-06-30", "severity": 55, "hero_id": 2, "hidden": True},
    {"name": "Agressão a civis", "description": "Atacou ativistas ambientais sem razão aparente.", "date": "2022-03-12", "severity": 60, "hero_id": 2, "hidden": False},
    {"name": "Uso excessivo de força", "description": "Machucou gravemente um criminoso rendido.", "date": "2023-02-15", "severity": 75, "hero_id": 2, "hidden": True},
    {"name": "Homicídio culposo", "description": "Matou Robin ao correr descontroladamente.", "date": "2019-07-03", "severity": 90, "hero_id": 3, "hidden": True},
    {"name": "Distribuição de drogas", "description": "Vendeu Composto V no mercado negro.", "date": "2020-04-21", "severity": 70, "hero_id": 3, "hidden": True},
    {"name": "Corrida ilegal", "description": "Participou de corridas clandestinas para lucrar.", "date": "2021-08-10", "severity": 50, "hero_id": 3, "hidden": False},
    {"name": "Negligência criminosa", "description": "Ignorou civis feridos durante uma perseguição.", "date": "2022-11-05", "severity": 60, "hero_id": 3, "hidden": True},
    {"name": "Assédio sexual", "description": "Coagiu uma nova integrante da equipe.", "date": "2019-12-20", "severity": 80, "hero_id": 4, "hidden": True},
    {"name": "Maus-tratos a animais", "description": "Usou golfinhos em situações perigosas.", "date": "2020-05-15", "severity": 50, "hero_id": 4, "hidden": False},
    {"name": "Destruição de barco", "description": "Afundou um barco durante um confronto.", "date": "2021-09-30", "severity": 70, "hero_id": 4, "hidden": True},
    {"name": "Uso não autorizado de Composto V", "description": "Utilizou o Composto V sem permissão.", "date": "2021-07-12", "severity": 60, "hero_id": 5, "hidden": False},
    {"name": "Negligência em resgate", "description": "Deixou civis para trás durante uma operação de resgate.", "date": "2022-06-15", "severity": 40, "hero_id": 5, "hidden": False},
    {"name": "Manipulação de mídia", "description": "Vazou informações sigilosas para desacreditar Homelander.", "date": "2023-04-01", "severity": 80, "hero_id": 5, "hidden": True},
    {"name": "Execução silenciosa", "description": "Assassinou um informante da Vought.", "date": "2021-10-12", "severity": 90, "hero_id": 6, "hidden": True},
    {"name": "Ataque desnecessário", "description": "Matou civis durante uma operação descontrolada.", "date": "2022-05-18", "severity": 85, "hero_id": 6, "hidden": True},
    {"name": "Propaganda fascista", "description": "Promoveu ideias fascistas publicamente.", "date": "2020-04-10", "severity": 70, "hero_id": 7, "hidden": True},
    {"name": "Massacre de civis", "description": "Matou dezenas de pessoas em um ataque ao vivo.", "date": "2021-02-15", "severity": 95, "hero_id": 7, "hidden": True},
     {"name": "Ataque a hospital", "description": "Destruiu um hospital infantil para demonstrar poder.", "date": "2023-07-20", "severity": 100, "hero_id": 1, "hidden": True},
    {"name": "Assassinato em massa no comício", "description": "Matou dezenas durante um discurso ao vivo.", "date": "2022-11-30", "severity": 95, "hero_id": 1, "hidden": True},
    {"name": "Dano colateral em combate", "description": "Destruiu uma estação de trem ao enfrentar vilões.", "date": "2021-09-11", "severity": 70, "hero_id": 2, "hidden": False},
    {"name": "Ataque a jornalista", "description": "Ameaçou um jornalista para impedir uma publicação.", "date": "2023-03-18", "severity": 65, "hero_id": 2, "hidden": True},
    {"name": "Corrida sobre civis", "description": "Atropelou um grupo de pedestres durante uma exibição pública.", "date": "2021-12-22", "severity": 90, "hero_id": 3, "hidden": True},
    {"name": "Invasão a propriedade privada", "description": "Quebrou a segurança de um banco para competir com outros heróis.", "date": "2020-08-25", "severity": 70, "hero_id": 3, "hidden": False},
    {"name": "Abandono de civis no mar", "description": "Deixou sobreviventes de um naufrágio à própria sorte.", "date": "2021-05-14", "severity": 75, "hero_id": 4, "hidden": True},
    {"name": "Vandalismo subaquático", "description": "Derrubou equipamentos de pesquisa científica no oceano.", "date": "2022-10-06", "severity": 50, "hero_id": 4, "hidden": False},
    {"name": "Negligência em combate", "description": "Falhou em proteger civis durante uma batalha com vilões.", "date": "2022-01-10", "severity": 55, "hero_id": 5, "hidden": False},
    {"name": "Explosão acidental", "description": "Causou uma explosão ao usar seus poderes incorretamente.", "date": "2023-06-22", "severity": 65, "hero_id": 5, "hidden": True},
    {"name": "Execução de reféns", "description": "Eliminou civis rendidos para completar sua missão.", "date": "2021-08-15", "severity": 90, "hero_id": 6, "hidden": True},
    {"name": "Sabotagem de infraestrutura", "description": "Destruiu uma usina elétrica durante uma missão secreta.", "date": "2022-12-01", "severity": 80, "hero_id": 6, "hidden": True},
    {"name": "Manipulação de campanha política", "description": "Espalhou desinformação para influenciar uma eleição.", "date": "2021-03-05", "severity": 85, "hero_id": 7, "hidden": True},
    {"name": "Conspiração global", "description": "Organizou uma operação secreta para derrubar governos estrangeiros.", "date": "2020-11-11", "severity": 95, "hero_id": 7, "hidden": True},
    {"name": "Roubo de armas biológicas", "description": "Roubou amostras do Composto V para desenvolver um antídoto.", "date": "2023-03-02", "severity": 70, "hero_id": 8, "hidden": True},
    {"name": "Infiltração em instalações militares", "description": "Invadiu uma base da Vought para obter informações confidenciais.", "date": "2022-06-20", "severity": 85, "hero_id": 8, "hidden": True},
    {"name": "Explosão de laboratório", "description": "Causou a destruição de um laboratório ao usar o Composto V.", "date": "2023-02-14", "severity": 65, "hero_id": 9, "hidden": True},
    {"name": "Dano colateral em combate", "description": "Destruiu uma praça pública durante uma batalha.", "date": "2022-04-08", "severity": 50, "hero_id": 9, "hidden": False},
    {"name": "Ataque descontrolado", "description": "Causou uma explosão nuclear em uma cidade pequena.", "date": "2021-07-19", "severity": 100, "hero_id": 10, "hidden": True},
    {"name": "Retaliação contra aliados", "description": "Atacou membros do próprio time após um desentendimento.", "date": "2020-12-12", "severity": 85, "hero_id": 10, "hidden": True},
    {"name": "Destruição de monumento histórico", "description": "Demoliu um marco histórico durante um ataque descontrolado.", "date": "2023-09-15", "severity": 90, "hero_id": 1, "hidden": True},
    {"name": "Uso de força contra manifestantes", "description": "Atacou manifestantes pacíficos em uma marcha.", "date": "2022-03-12", "severity": 75, "hero_id": 1, "hidden": True},
    {"name": "Combate com danos colaterais", "description": "Destruiu uma escola durante uma luta com vilões.", "date": "2021-06-20", "severity": 85, "hero_id": 2, "hidden": False},
    {"name": "Intimidação pública", "description": "Usou sua força para ameaçar uma multidão.", "date": "2023-02-10", "severity": 60, "hero_id": 2, "hidden": True},
    {"name": "Explosão durante corrida", "description": "Provocou uma explosão ao exceder os limites de velocidade.", "date": "2023-08-12", "severity": 75, "hero_id": 3, "hidden": False},
    {"name": "Roubo de tecnologia avançada", "description": "Invadiu um laboratório da Vought para roubar equipamentos.", "date": "2022-07-05", "severity": 80, "hero_id": 3, "hidden": True},
    {"name": "Abandono de operação", "description": "Deixou uma missão de resgate pela metade para salvar peixes.", "date": "2023-04-21", "severity": 65, "hero_id": 4, "hidden": True},
    {"name": "Ataque a pesquisa ambiental", "description": "Destruiu barcos de pesquisadores por acidente.", "date": "2021-12-02", "severity": 55, "hero_id": 4, "hidden": False},
    {"name": "Ruptura elétrica em cidade", "description": "Causou apagão ao tentar salvar civis.", "date": "2023-06-18", "severity": 70, "hero_id": 5, "hidden": False},
    {"name": "Destruição de infraestrutura pública", "description": "Causou danos ao usar seus poderes em combate.", "date": "2022-11-14", "severity": 60, "hero_id": 5, "hidden": True},
    {"name": "Execução de vilão rendido", "description": "Matou um vilão que já havia se rendido.", "date": "2023-01-27", "severity": 85, "hero_id": 6, "hidden": True},
    {"name": "Infiltração em prédio governamental", "description": "Entrou em um prédio governamental sem permissão.", "date": "2022-08-05", "severity": 75, "hero_id": 6, "hidden": True},
    {"name": "Propaganda enganosa", "description": "Manipulou vídeos para desacreditar oponentes.", "date": "2022-02-12", "severity": 80, "hero_id": 7, "hidden": True},
    {"name": "Conspiração para derrubar heróis", "description": "Planejou uma série de ataques para enfraquecer The Seven.", "date": "2023-03-22", "severity": 95, "hero_id": 7, "hidden": True},
    {"name": "Furto de documentos secretos", "description": "Roubou informações sigilosas da Vought.", "date": "2023-09-09", "severity": 70, "hero_id": 8, "hidden": True},
    {"name": "Dano a instalações de treinamento", "description": "Destruiu um centro de treinamento da Vought.", "date": "2021-11-16", "severity": 80, "hero_id": 8, "hidden": True},
    {"name": "Acidente com civis", "description": "Causou ferimentos em civis durante um combate.", "date": "2023-08-30", "severity": 55, "hero_id": 9, "hidden": False},
    {"name": "Combate com superpoder descontrolado", "description": "Causou destruição ao usar o Composto V.", "date": "2023-05-04", "severity": 70, "hero_id": 9, "hidden": True},
    {"name": "Explosão nuclear acidental", "description": "Causou uma explosão nuclear ao perder o controle.", "date": "2023-10-12", "severity": 100, "hero_id": 10, "hidden": True},
    {"name": "Combate destrutivo em área residencial", "description": "Destruiu várias casas durante uma luta com vilões.", "date": "2023-07-29", "severity": 90, "hero_id": 10, "hidden": True}
    ]
    # Converte datas antes de inserir
    convert_date(crimes, "date")
    add_if_not_exists(Crime, crimes)

    # Commit das mudanças
    db.session.commit()

    # Exibir status das missões
    missions = Mission.query.all()
    for mission in missions:
        print(f"Missão: {mission.name} - Status: {mission.status}")

    print("Banco de dados populado com sucesso!")

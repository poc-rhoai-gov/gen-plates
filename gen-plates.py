# %%
import pandas as pd
import numpy as np
import random
import uuid
import datetime
import argparse
from faker import Faker

def parse_args():
    """Configura e processa os argumentos de linha de comando"""
    parser = argparse.ArgumentParser(
        description='Gerador de dados de placas de veículos para o Distrito Federal',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    # Configurações principais
    parser.add_argument('--seed', type=int, default=42,
                        help='Seed para garantir reprodutibilidade dos dados')
    parser.add_argument('--num-records', type=int, default=1000,
                        help='Número de registros a serem gerados')
    parser.add_argument('--output', type=str, default="dados_placas_df.csv",
                        help='Nome do arquivo de saída')
    
    # Configurações de intervalo de datas
    parser.add_argument('--dias-passados', type=int, default=30,
                        help='Número de dias no passado para a geração de timestamps')
    
    # Configurações de coordenadas
    parser.add_argument('--lat-min', type=float, default=-16.0,
                        help='Latitude mínima para o Distrito Federal')
    parser.add_argument('--lat-max', type=float, default=-15.5,
                        help='Latitude máxima para o Distrito Federal')
    parser.add_argument('--long-min', type=float, default=-48.3,
                        help='Longitude mínima para o Distrito Federal')
    parser.add_argument('--long-max', type=float, default=-47.3,
                        help='Longitude máxima para o Distrito Federal')
    
    # Configurações de temperatura
    parser.add_argument('--temp-min', type=float, default=15.0,
                        help='Temperatura mínima em °C')
    parser.add_argument('--temp-max', type=float, default=30.0,
                        help='Temperatura máxima em °C')
    
    # Configurações de velocidade
    parser.add_argument('--velocidade-min', type=int, default=0,
                        help='Velocidade mínima em km/h')
    parser.add_argument('--velocidade-max', type=int, default=120,
                        help='Velocidade máxima em km/h')
    
    # Configurações de ano dos veículos
    parser.add_argument('--ano-min', type=int, default=2010,
                        help='Ano mínimo dos veículos')
    parser.add_argument('--ano-max', type=int, default=2023,
                        help='Ano máximo dos veículos')
    
    # Configurações de exibição
    parser.add_argument('--show-sample', action='store_true',
                        help='Mostrar amostra dos dados gerados')
    parser.add_argument('--show-stats', action='store_true',
                        help='Mostrar estatísticas dos dados gerados')
    
    # Parâmetros de locale
    parser.add_argument('--locale', type=str, default='pt_BR',
                        help='Configuração regional para a faker')
    
    return parser.parse_args()

def generate_license_plate():
    """Gera um número de placa brasileira aleatório"""
    formats = [
        # Traditional Brazilian format: 3 letters + 4 numbers (e.g., ABC1234)
        lambda: ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3)) + ''.join(random.choices('0123456789', k=4)),
        
        # Mercosur format: 3 letters + 1 number + 1 letter + 2 numbers (e.g., ABC1D23)
        lambda: ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3)) + 
                random.choice('0123456789') + 
                random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') + 
                ''.join(random.choices('0123456789', k=2)),
    ]
    return random.choice(formats)()

# Função para gerar UUIDs determinísticos baseados em seed
def generate_deterministic_uuid(seed, index):
    """Gera UUIDs determinísticos baseados em seed e índice"""
    # Criar um gerador de números aleatórios com a seed específica para cada índice
    r = random.Random(f"{seed}-{index}")
    # Gerar 16 bytes aleatórios (128 bits) para o UUID
    random_bytes = bytes([r.randint(0, 255) for _ in range(16)])
    # Criar UUID a partir dos bytes, ajustando a versão (version 4) e variante (DCE 1.1)
    random_bytes = bytearray(random_bytes)
    random_bytes[6] = (random_bytes[6] & 0x0F) | 0x40  # versão 4
    random_bytes[8] = (random_bytes[8] & 0x3F) | 0x80  # variante DCE 1.1
    return str(uuid.UUID(bytes=bytes(random_bytes)))

def determinar_infracao(velocidade, limite_velocidade, condicao_estrada, condicao_clima, tipo_veiculo, ano_veiculo):
    """Determina se houve alguma infração de trânsito com base nos dados do veículo e condições"""
    
    # Lista de possíveis infrações baseadas na legislação brasileira de trânsito
    infracoes = {
        # Infrações de velocidade
        "excesso_velocidade_leve": "Excesso de velocidade até 20% acima do limite",
        "excesso_velocidade_media": "Excesso de velocidade entre 20% e 50% acima do limite",
        "excesso_velocidade_grave": "Excesso de velocidade mais de 50% acima do limite",
        
        # Infrações de conduta
        "sem_licenciamento": "Veículo sem licenciamento atualizado",
        "veiculo_irregular": "Veículo em condições irregulares",
        "estacionamento_proibido": "Estacionamento em local proibido",
        "parada_proibida": "Parada em local proibido",
        "transitar_calcada": "Transitar na calçada ou passeio",
        
        # Infrações de equipamentos
        "equipamento_obrigatorio": "Falta de equipamento obrigatório",
        "farol_apagado": "Conduzir sem farol aceso em rodovia",
        
        # Infrações específicas
        "transito_faixa_exclusiva": "Transitar em faixa exclusiva",
        "avanco_sinal": "Avanço de sinal vermelho",
        "contramao": "Trafegar na contramão",
        "uso_celular": "Dirigir utilizando celular", 
        
        # Infrações de condições climáticas e via
        "velocidade_incompativel": "Velocidade incompatível com condições da via",
        
        # Sem infração
        "sem_infracao": "Sem infração detectada"
    }
    
    # Probabilidades de infrações específicas
    prob_sem_licenciamento = 0.03  # 3% de chance para veículos mais antigos 
    prob_equipamento = 0.04  # 4% de chance
    prob_avanco_sinal = 0.05  # 5% de chance
    prob_contramao = 0.02  # 2% de chance
    prob_uso_celular = 0.07  # 7% de chance
    prob_faixa_exclusiva = 0.04  # 4% de chance
    prob_farol_apagado = 0.06  # 6% de chance (apenas rodovias)
    
    # Lista para armazenar as possíveis infrações deste caso
    possiveis_infracoes = []
    
    # Verifica excesso de velocidade
    limite_velocidade_ajustado = limite_velocidade
    
    # Ajusta o limite de velocidade com base nas condições da via
    if condicao_estrada in ["Molhada", "Alagada"]:
        limite_velocidade_ajustado = 0.8 * limite_velocidade  # Reduz 20% em vias molhadas
    elif condicao_estrada in ["Em Obras", "Com Buracos"]:
        limite_velocidade_ajustado = 0.7 * limite_velocidade  # Reduz 30% em obras
    
    # Ajusta ainda mais com base nas condições climáticas
    if condicao_clima in ["Chuvoso", "Tempestuoso"]:
        limite_velocidade_ajustado = 0.9 * limite_velocidade_ajustado  # Reduz mais 10%
    
    if velocidade > limite_velocidade_ajustado:
        percentual_excesso = (velocidade - limite_velocidade_ajustado) / limite_velocidade_ajustado * 100
        
        if percentual_excesso <= 20:
            possiveis_infracoes.append(infracoes["excesso_velocidade_leve"])
        elif percentual_excesso <= 50:
            possiveis_infracoes.append(infracoes["excesso_velocidade_media"])
        else:
            possiveis_infracoes.append(infracoes["excesso_velocidade_grave"])
    
    # Veículos mais antigos têm maior probabilidade de estar sem licenciamento
    idade_veiculo = datetime.datetime.now().year - ano_veiculo
    if idade_veiculo > 10 and random.random() < prob_sem_licenciamento * (idade_veiculo / 10):
        possiveis_infracoes.append(infracoes["sem_licenciamento"])
    
    # Veículos mais antigos têm maior probabilidade de falta de equipamento obrigatório
    if idade_veiculo > 8 and random.random() < prob_equipamento * (idade_veiculo / 8):
        possiveis_infracoes.append(infracoes["equipamento_obrigatorio"])
    
    # Infrações aleatórias baseadas em probabilidade
    if random.random() < prob_avanco_sinal:
        possiveis_infracoes.append(infracoes["avanco_sinal"])
    
    if random.random() < prob_contramao:
        possiveis_infracoes.append(infracoes["contramao"])
    
    if random.random() < prob_uso_celular:
        possiveis_infracoes.append(infracoes["uso_celular"])
    
    if random.random() < prob_faixa_exclusiva and tipo_veiculo not in ["Ônibus"]:
        possiveis_infracoes.append(infracoes["transito_faixa_exclusiva"])
    
    if random.random() < prob_farol_apagado:
        possiveis_infracoes.append(infracoes["farol_apagado"])
    
    # Velocidade incompatível com condições da via
    if (condicao_estrada in ["Molhada", "Alagada", "Em Obras"] or 
        condicao_clima in ["Chuvoso", "Tempestuoso", "Baixa Visibilidade"]) and velocidade > 0.7 * limite_velocidade:
        possiveis_infracoes.append(infracoes["velocidade_incompativel"])

    # Se não foi detectada nenhuma infração, retornar "Sem infração"
    if not possiveis_infracoes:
        return infracoes["sem_infracao"]
    
    # Retorna uma das infrações detectadas (se houver mais de uma)
    return random.choice(possiveis_infracoes)

def generate_plate_data(args):
    """Gera um conjunto completo de registros de placas de veículos para o Distrito Federal, Brasil"""
    
    # Administrative regions of Distrito Federal
    df_regions = [
        "Brasília (Plano Piloto)", "Samambaia", "Taguatinga", "Águas Claras", "Guará", 
        "Ceilândia", "Gama", "Sobradinho", "Planaltina", "Santa Maria", 
        "Recanto das Emas", "Riacho Fundo", "São Sebastião", "Paranoá", "Núcleo Bandeirante", 
        "Lago Sul", "Lago Norte", "Brazlândia", "Candangolândia", "Cruzeiro", 
        "Itapoã", "Jardim Botânico", "SIA", "Sudoeste/Octogonal", "Varjão", 
        "Vicente Pires", "Fercal", "Estrutural", "Sobradinho II", "Park Way"
    ]
    
    # Plate types
    tipos_placa = ["Padrão", "Comercial", "Temporária", "Oficial", "Diplomática", "Colecionador"]
    
    # Vehicle types with their corresponding makes and models
    # This structure ensures realistic combinations of vehicle types, makes and models
    tipos_veiculo_dados = {
        "Carro": {
            "marcas": [
                "Volkswagen", "Fiat", "Chevrolet", "Toyota", "Hyundai", 
                "Renault", "Honda", "Ford", "Nissan", "Citroën", 
                "Peugeot", "BMW", "Mercedes-Benz", "Audi", "Kia"
            ],
            "modelos": {
                "Volkswagen": ["Gol", "Polo", "Virtus", "Jetta", "Nivus", "Fox", "Voyage", "Up"],
                "Fiat": ["Argo", "Mobi", "Uno", "Cronos", "Siena", "Palio", "Grand Siena", "Linea"],
                "Chevrolet": ["Onix", "Cruze", "Joy", "Cobalt", "Prisma", "Spin", "Malibu"],
                "Toyota": ["Corolla", "Yaris", "Etios", "Prius", "Camry"],
                "Hyundai": ["HB20", "i30", "Elantra", "Azera", "Sonata", "HB20S"],
                "Renault": ["Kwid", "Sandero", "Logan", "Fluence", "Symbol", "Megane"],
                "Honda": ["Civic", "City", "Fit", "Accord", "WR-V"],
                "Ford": ["Ka", "Focus", "Fusion", "Fiesta"],
                "Nissan": ["Versa", "Sentra", "March", "Leaf"],
                "Citroën": ["C3", "C4", "C4 Lounge", "C4 Picasso"],
                "Peugeot": ["208", "308", "408", "508"],
                "BMW": ["Série 1", "Série 3", "Série 5", "Série 7", "320i", "118i"],
                "Mercedes-Benz": ["Classe A", "Classe C", "Classe E", "Classe S"],
                "Audi": ["A3", "A4", "A5", "A6", "A7"],
                "Kia": ["Cerato", "Optima", "Rio", "Cadenza"]
            }
        },
        "SUV": {
            "marcas": [
                "Jeep", "Toyota", "Hyundai", "Volkswagen", "Chevrolet", 
                "Ford", "Honda", "Nissan", "Mitsubishi", "Renault",
                "BMW", "Mercedes-Benz", "Audi", "Kia", "Fiat"
            ],
            "modelos": {
                "Jeep": ["Renegade", "Compass", "Commander", "Cherokee", "Wrangler"],
                "Toyota": ["SW4", "RAV4", "Corolla Cross", "Hilux SW4", "Land Cruiser"],
                "Hyundai": ["Creta", "Tucson", "Santa Fe", "ix35", "Kona"],
                "Volkswagen": ["T-Cross", "Taos", "Tiguan", "Tiguan Allspace"],
                "Chevrolet": ["Tracker", "Equinox", "Trailblazer", "Captiva"],
                "Ford": ["EcoSport", "Territory", "Bronco", "Edge"],
                "Honda": ["HR-V", "CR-V", "WR-V"],
                "Nissan": ["Kicks", "X-Trail", "Murano"],
                "Mitsubishi": ["ASX", "Outlander", "Eclipse Cross", "Pajero Sport"],
                "Renault": ["Duster", "Captur", "Koleos"],
                "BMW": ["X1", "X3", "X5", "X6", "X7"],
                "Mercedes-Benz": ["GLA", "GLC", "GLE", "GLB", "GLS"],
                "Audi": ["Q3", "Q5", "Q7", "Q8"],
                "Kia": ["Sportage", "Sorento", "Stonic"],
                "Fiat": ["Pulse", "Fastback", "Toro"]
            }
        },
        "Caminhão": {
            "marcas": [
                "Mercedes-Benz", "Volkswagen", "Volvo", "Scania", "Iveco", 
                "Ford", "DAF", "MAN", "Hyundai"
            ],
            "modelos": {
                "Mercedes-Benz": ["Actros", "Atego", "Axor", "Accelo"],
                "Volkswagen": ["Constellation", "Delivery", "Worker", "Meteor"],
                "Volvo": ["FH", "FM", "FMX", "VM"],
                "Scania": ["R", "G", "P", "S"],
                "Iveco": ["Daily", "Tector", "Stralis", "Hi-Way"],
                "Ford": ["Cargo", "F-MAX"],
                "DAF": ["XF", "CF", "LF"],
                "MAN": ["TGX", "TGS", "TGL", "TGM"],
                "Hyundai": ["HD78", "HD80", "Mighty"]
            }
        },
        "Motocicleta": {
            "marcas": [
                "Honda", "Yamaha", "Suzuki", "Kawasaki", "Harley-Davidson",
                "BMW", "Ducati", "Triumph", "KTM", "Royal Enfield"
            ],
            "modelos": {
                "Honda": ["CG 160", "Biz", "CB 300", "CB 500", "XRE 300", "Pop 110", "Bros 160", "PCX"],
                "Yamaha": ["Factor 150", "Fazer 250", "MT-03", "MT-07", "MT-09", "Lander", "Crosser", "NMAX"],
                "Suzuki": ["GSX-S750", "V-Strom 650", "Intruder 125", "Hayabusa", "Burgman"],
                "Kawasaki": ["Ninja 300", "Ninja 400", "Z400", "Versys 650", "Vulcan"],
                "Harley-Davidson": ["Street 750", "Iron 883", "Sportster", "Fat Boy", "Road King"],
                "BMW": ["G 310", "F 750 GS", "F 850 GS", "R 1250 GS", "S 1000 RR"],
                "Ducati": ["Monster", "Panigale", "Scrambler", "Multistrada", "Diavel"],
                "Triumph": ["Street Twin", "Bonneville", "Tiger", "Trident", "Speed Triple"],
                "KTM": ["Duke 200", "Duke 390", "Adventure 390", "RC 390"],
                "Royal Enfield": ["Himalayan", "Meteor", "Classic 350", "Interceptor 650"]
            }
        },
        "Ônibus": {
            "marcas": [
                "Mercedes-Benz", "Volkswagen", "Volvo", "Scania", "Marcopolo",
                "Comil", "Caio", "Neobus", "Busscar"
            ],
            "modelos": {
                "Mercedes-Benz": ["O-500", "O-500 RS", "OF-1721", "OF-1519", "Citaro"],
                "Volkswagen": ["Volksbus 15.190 OD", "Volksbus 17.230 OD", "Volksbus 18.280 OT", "Volksbus 9.160 OD"],
                "Volvo": ["B270F", "B340R", "B380R", "B450R", "B8R"],
                "Scania": ["K360", "K400", "K410", "K440", "F250"],
                "Marcopolo": ["Paradiso", "Viaggio", "Audace", "Torino", "Senior"],
                "Comil": ["Campione", "Versatile", "Invictus", "Svelto"],
                "Caio": ["Apache", "Millennium", "Solar", "Foz"],
                "Neobus": ["New Road", "Mega", "Thunder", "Spectrum"],
                "Busscar": ["Urbanuss", "Vissta", "El Buss", "Jum Buss"]
            }
        },
        "Van": {
            "marcas": [
                "Mercedes-Benz", "Fiat", "Renault", "Iveco", "Peugeot",
                "Citroën", "Volkswagen", "Ford", "Hyundai"
            ],
            "modelos": {
                "Mercedes-Benz": ["Sprinter", "Vito", "Vito Tourer", "V-Class"],
                "Fiat": ["Ducato", "Fiorino", "Doblò", "Scudo"],
                "Renault": ["Master", "Trafic", "Kangoo"],
                "Iveco": ["Daily", "Daily Minibus", "Daily City"],
                "Peugeot": ["Expert", "Boxer", "Partner"],
                "Citroën": ["Jumper", "Jumpy", "Berlingo"],
                "Volkswagen": ["Kombi", "Transporter", "Crafter", "Delivery"],
                "Ford": ["Transit", "Transit Custom"],
                "Hyundai": ["HR", "H100", "Starex"]
            }
        }
    }
    
    # Vehicle colors
    cores_veiculo = ["Preto", "Branco", "Prata", "Cinza", "Vermelho", "Azul", "Verde", "Amarelo", "Marrom", "Laranja"]
    
    # Camera IDs (using Distrito Federal highway and avenue designations)
    ids_camera = [
        "EPIA-001", "EPNB-001", "EPTG-001", "EPCT-001", "EPNA-001", 
        "EPCL-001", "EPPR-001", "EPAR-001", "W3-001", "L2-001", 
        "L4-001", "ESPM-001", "EPIG-001", "EPDB-001", "DF-001", 
        "DF-002", "DF-003", "DF-004", "DF-005", "DF-085", 
        "DF-095", "DF-075", "DF-079", "DF-150", "DF-140", 
        "BR-020", "BR-040", "BR-060", "BR-070", "BR-251"
    ]
    
    # Weather conditions (relevant to Distrito Federal)
    condicoes_clima = ["Ensolarado", "Nublado", "Chuvoso", "Parcialmente Nublado", "Limpo", "Tempestuoso", "Ventoso"]
    
    # Visibility conditions
    condicoes_visibilidade = ["Dia", "Noite", "Pôr do Sol", "Amanhecer", "Baixa Visibilidade"]
    
    # Road conditions
    condicoes_estrada = ["Seca", "Molhada", "Alagada", "Em Obras", "Com Buracos", "Boa Condição"]
    
    # Traffic conditions
    condicoes_trafego = ["Leve", "Moderado", "Intenso", "Congestionado", "Parado"]
    
    # Direction of travel (using Distrito Federal common directions)
    direcoes = ["Plano Norte", "Plano Sul", "Asa Leste", "Asa Oeste", "Lago Norte", "Lago Sul", "Sentido Cidades Satélites", "Sentido Área Central"]
    
    # Popular locations in Distrito Federal
    locais = [
        "Congresso Nacional", "Esplanada dos Ministérios", "Ponte JK", 
        "Rodoviária do Plano Piloto", "Estádio Mané Garrincha", 
        "Praça dos Três Poderes", "Catedral Metropolitana", 
        "Parque da Cidade", "Memorial JK", "Torre de TV", 
        "Universidade de Brasília", "Aeroporto Internacional", 
        "Setor Comercial Sul", "Setor Bancário Sul", "Setor Hoteleiro Norte",
        "Setor de Embaixadas Sul", "Shopping Conjunto Nacional", 
        "ParkShopping", "Taguatinga Shopping", "Pátio Brasil",
        "Gilberto Salomão", "Lago Paranoá", "Pontão do Lago Sul"
    ]
    
    # Limites de velocidade por tipo de local (km/h)
    limites_velocidade = {
        "Congresso Nacional": 40,
        "Esplanada dos Ministérios": 60,
        "Ponte JK": 60,
        "Rodoviária do Plano Piloto": 40,
        "Estádio Mané Garrincha": 40,
        "Praça dos Três Poderes": 40,
        "Catedral Metropolitana": 40,
        "Parque da Cidade": 30,
        "Memorial JK": 40,
        "Torre de TV": 40,
        "Universidade de Brasília": 40,
        "Aeroporto Internacional": 60,
        "Setor Comercial Sul": 40,
        "Setor Bancário Sul": 40,
        "Setor Hoteleiro Norte": 40,
        "Setor de Embaixadas Sul": 60,
        "Shopping Conjunto Nacional": 40,
        "ParkShopping": 60,
        "Taguatinga Shopping": 60,
        "Pátio Brasil": 40,
        "Gilberto Salomão": 60,
        "Lago Paranoá": 60,
        "Pontão do Lago Sul": 40
    }
    
    # Criar listas vazias para armazenar os dados dos veículos
    tipos_veiculos = []
    marcas_veiculos = []
    modelos_veiculos = []
    
    # Gerar combinações realistas de tipo, marca e modelo
    for _ in range(args.num_records):
        # Escolher um tipo de veículo aleatório
        tipo_veiculo = random.choice(list(tipos_veiculo_dados.keys()))
        tipos_veiculos.append(tipo_veiculo)
        
        # Escolher uma marca compatível com o tipo de veículo
        marca_veiculo = random.choice(tipos_veiculo_dados[tipo_veiculo]["marcas"])
        marcas_veiculos.append(marca_veiculo)
        
        # Escolher um modelo compatível com a marca e tipo de veículo
        modelo_veiculo = random.choice(tipos_veiculo_dados[tipo_veiculo]["modelos"][marca_veiculo])
        modelos_veiculos.append(modelo_veiculo)
    
    # Generate data
    data = {
        # Usar UUIDs determinísticos para garantir reprodutibilidade completa
        "id_registro": [generate_deterministic_uuid(args.seed, i) for i in range(args.num_records)],
        "numero_placa": [generate_license_plate() for _ in range(args.num_records)],
        "regiao_administrativa": [random.choice(df_regions) for _ in range(args.num_records)],
        "tipo_placa": [random.choice(tipos_placa) for _ in range(args.num_records)],
        
        # Vehicle attributes with realistic combinations
        "tipo_veiculo": tipos_veiculos,
        "marca_veiculo": marcas_veiculos,
        "modelo_veiculo": modelos_veiculos,
    }
    
    # Add location information
    locais_gerados = [random.choice(locais) for _ in range(args.num_records)]
    data["local"] = locais_gerados
    
    # Continue with remaining fields
    data.update({
        "cor_veiculo": [random.choice(cores_veiculo) for _ in range(args.num_records)],
        "ano_veiculo": [random.randint(args.ano_min, args.ano_max) for _ in range(args.num_records)],
        
        # Generate timestamps over the last N days
        "data_hora": [
            (datetime.datetime.now() - datetime.timedelta(
                days=random.randint(0, args.dias_passados),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )).strftime("%Y-%m-%d %H:%M:%S") 
            for _ in range(args.num_records)
        ],
    })
    
    # Generate realistic latitude and longitude for Distrito Federal
    data.update({
        "latitude": [round(random.uniform(args.lat_min, args.lat_max), 6) for _ in range(args.num_records)],
        "longitude": [round(random.uniform(args.long_min, args.long_max), 6) for _ in range(args.num_records)],
        "id_camera": [random.choice(ids_camera) for _ in range(args.num_records)],
        "caminho_imagem": [f"/imagens/captura_{i:04d}.jpg" for i in range(args.num_records)],
        "confianca_ocr": [round(random.uniform(0.70, 1.0), 2) for _ in range(args.num_records)],
        
        # Environmental data (adjusted for Distrito Federal's climate)
        "condicao_clima": [random.choice(condicoes_clima) for _ in range(args.num_records)],
        # Distrito Federal has a specific climate with dry and wet seasons
        "temperatura": [round(random.uniform(args.temp_min, args.temp_max), 1) for _ in range(args.num_records)], # Celsius, specific to DF
        "visibilidade": [random.choice(condicoes_visibilidade) for _ in range(args.num_records)],
        "condicao_estrada": [random.choice(condicoes_estrada) for _ in range(args.num_records)],
        "condicao_trafego": [random.choice(condicoes_trafego) for _ in range(args.num_records)],
        
        # Additional fields
        "velocidade": [random.randint(args.velocidade_min, args.velocidade_max) for _ in range(args.num_records)], # km/h
        "direcao_deslocamento": [random.choice(direcoes) for _ in range(args.num_records)],
    })
    
    # Gerar dados de infração
    infracoes = []
    for i in range(args.num_records):
        local = locais_gerados[i]
        limite_velocidade = limites_velocidade.get(local, 60)  # Padrão 60 km/h se não especificado
        
        infracao = determinar_infracao(
            data["velocidade"][i], 
            limite_velocidade, 
            data["condicao_estrada"][i], 
            data["condicao_clima"][i],
            data["tipo_veiculo"][i],
            data["ano_veiculo"][i]
        )
        infracoes.append(infracao)
    
    # Adicionar a coluna de infrações ao dicionário de dados
    data["infracao"] = infracoes
    data["limite_velocidade"] = [limites_velocidade.get(local, 60) for local in locais_gerados]
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Add derived fields
    df["data_hora"] = pd.to_datetime(df["data_hora"])
    df["dia_semana"] = df["data_hora"].dt.day_name().map({
        'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira',
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    })
    df["hora_dia"] = df["data_hora"].dt.hour
    df["semana"] = df["data_hora"].dt.isocalendar().week
    df["mes"] = df["data_hora"].dt.month
    df["ano"] = df["data_hora"].dt.year
    
    # Convert back to string for CSV output
    df["data_hora"] = df["data_hora"].dt.strftime("%Y-%m-%d %H:%M:%S")
    
    return df

def main():
    # Processar argumentos da linha de comando
    args = parse_args()
    
    # Configurar seeds para reprodutibilidade
    np.random.seed(args.seed)
    random.seed(args.seed)
    fake = Faker(args.locale)
    Faker.seed(args.seed)
    
    print(f"Configurações:")
    print(f"  Seed: {args.seed}")
    print(f"  Registros: {args.num_records}")
    print(f"  Arquivo de saída: {args.output}")
    
    # Gerar os dados
    dados_placas = generate_plate_data(args)
    
    # Salvar para CSV
    dados_placas.to_csv(args.output, index=False)
    
    print(f"Gerados {len(dados_placas)} registros de placas para o Distrito Federal e salvos em {args.output}")
    
    # Mostrar amostra dos dados se solicitado
    if args.show_sample:
        print("\nAmostra de dados:")
        print(dados_placas.head())
    
    # Mostrar estatísticas se solicitado
    if args.show_stats:
        print("\nEstatísticas dos dados:")
        print(dados_placas.describe(include='all').T)

if __name__ == "__main__":
    main()




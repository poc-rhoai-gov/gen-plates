# Gerador de Dados de Placas de Veículos do Distrito Federal

Este script gera dados sintéticos de placas de veículos para o Distrito Federal (DF), Brasil, simulando registros de detecção de placas por câmeras de tráfego.

## Características

- Gera dados realistas de placas de veículos baseados na geografia do DF
- Inclui combinações realistas de tipos de veículos, marcas e modelos
- Cria timestamps distribuídos ao longo de um período configurável
- Fornece dados contextuais como condições climáticas e de tráfego
- Detecta e classifica possíveis infrações de trânsito com base nas condições
- Totalmente configurável via argumentos de linha de comando ou arquivo de configuração
- Suporte para exportação direta para banco de dados MySQL
- Garante reprodutibilidade completa quando a mesma seed é utilizada

## Campos de Dados Gerados

### Informações Principais do Veículo e Placa
- `id_registro`: Identificador único para o registro de detecção
- `numero_placa`: Número da placa do veículo (formatos padrão e Mercosul)
- `regiao_administrativa`: Região administrativa do DF
- `tipo_placa`: Tipo da placa (Padrão, Comercial, Oficial, etc.)

### Atributos do Veículo
- `tipo_veiculo`: Tipo do veículo (Carro, SUV, Caminhão, etc.)
- `marca_veiculo`: Fabricante do veículo
- `modelo_veiculo`: Modelo específico do veículo
- `cor_veiculo`: Cor do veículo
- `ano_veiculo`: Ano de fabricação do veículo

### Detalhes de Detecção e Captura
- `data_hora`: Data e hora da detecção
- `id_camera`: Identificador do dispositivo de câmera
- `caminho_imagem`: Caminho para a imagem capturada
- `confianca_ocr`: Pontuação de confiança do OCR (0.7-1.0)
- `local`: Local onde a placa foi detectada
- `latitude`: Coordenada de latitude
- `longitude`: Coordenada de longitude

### Dados Ambientais e Contextuais
- `condicao_clima`: Condições climáticas no momento da detecção
- `temperatura`: Temperatura em graus Celsius
- `visibilidade`: Condições de visibilidade e iluminação
- `condicao_estrada`: Estado da estrada
- `condicao_trafego`: Condições de tráfego
- `velocidade`: Velocidade estimada do veículo (km/h)
- `direcao_deslocamento`: Direção de deslocamento do veículo
- `limite_velocidade`: Limite de velocidade do local da detecção (km/h)

### Dados de Infrações
- `infracao`: Possível infração detectada (ex: excesso de velocidade, avanço de sinal, dirigir utilizando celular)

### Campos Derivados
- `dia_semana`: Dia da semana da detecção
- `hora_dia`: Hora do dia (0-23)
- `semana`: Número da semana do ano
- `mes`: Mês da detecção
- `ano`: Ano da detecção

## Configuração e Uso

Há duas maneiras de configurar o script:
1. **Via argumentos de linha de comando** - para execuções únicas ou testes rápidos
2. **Via arquivo de configuração JSON** - para configurações complexas ou reutilizáveis

### Armazenamento de Dados

Os dados gerados podem ser armazenados de duas formas:
1. **Arquivo CSV** - formato padrão para fácil compartilhamento e uso em diversas ferramentas
2. **Banco de dados MySQL** - para integração com sistemas e aplicações

### Arquivo de Configuração

Você pode usar um arquivo de configuração JSON para definir os parâmetros do script. Isso é especialmente útil para:
- Salvar configurações para uso posterior
- Compartilhar configurações com outros usuários
- Automatizar a geração de dados com parâmetros complexos

**Uso básico**:
```bash
# Carregar configurações a partir de um arquivo
python gen-plates.py --config config_exemplo.json

# Salvar as configurações atuais em um arquivo
python gen-plates.py --seed 123 --num-records 500 --save-config minha_config.json
```

O script inclui vários arquivos de configuração de exemplo:
- `config_exemplo.json` - Configuração geral de exemplo
- `config_infracoes_velocidade.json` - Configurado para gerar mais infrações de velocidade
- `config_veiculos_antigos.json` - Configurado para gerar dados de veículos mais antigos
- `config_mysql.json` - Configurado para salvar dados em banco MySQL

**Prioridade de configurações**:
1. Argumentos explícitos de linha de comando (maior prioridade)
2. Configurações do arquivo JSON
3. Valores padrão do script (menor prioridade)

### Opções de Linha de Comando

O script suporta vários argumentos de linha de comando para configurar a geração de dados:

```bash
python gen-plates.py [opções]
```

#### Opções de Configuração
- `--config ARQUIVO`: Carregar configurações a partir de um arquivo JSON
- `--save-config ARQUIVO`: Salvar as configurações atuais em um arquivo JSON

#### Configurações Principais
- `--seed SEED`: Define a seed para garantir reprodutibilidade dos dados (padrão: 42)
- `--num-records NUM`: Número de registros a serem gerados (padrão: 1000)
- `--output ARQUIVO`: Nome do arquivo de saída (padrão: dados_placas_df.csv)
- `--locale LOCALE`: Configuração regional para o Faker (padrão: pt_BR)

#### Configurações de Intervalo de Datas
- `--dias-passados DIAS`: Número de dias no passado para geração de timestamps (padrão: 30)

#### Configurações de Coordenadas
- `--lat-min MIN`: Latitude mínima para o Distrito Federal (padrão: -16.0)
- `--lat-max MAX`: Latitude máxima para o Distrito Federal (padrão: -15.5)
- `--long-min MIN`: Longitude mínima para o Distrito Federal (padrão: -48.3)
- `--long-max MAX`: Longitude máxima para o Distrito Federal (padrão: -47.3)

#### Configurações de Temperatura
- `--temp-min MIN`: Temperatura mínima em °C (padrão: 15.0)
- `--temp-max MAX`: Temperatura máxima em °C (padrão: 30.0)

#### Configurações de Velocidade
- `--velocidade-min MIN`: Velocidade mínima em km/h (padrão: 0)
- `--velocidade-max MAX`: Velocidade máxima em km/h (padrão: 120)

#### Configurações de Ano dos Veículos
- `--ano-min MIN`: Ano mínimo dos veículos (padrão: 2010)
- `--ano-max MAX`: Ano máximo dos veículos (padrão: 2023)

#### Configurações de Exibição
- `--show-sample`: Mostrar amostra dos dados gerados
- `--show-stats`: Mostrar estatísticas dos dados gerados

#### Configurações de Banco de Dados MySQL
- `--mysql`: Ativar armazenamento em banco de dados MySQL
- `--mysql-host HOST`: Host do servidor MySQL (padrão: localhost)
- `--mysql-port PORT`: Porta do servidor MySQL (padrão: 3306)
- `--mysql-user USER`: Usuário MySQL (padrão: root)
- `--mysql-password PASS`: Senha MySQL (se não fornecida, será solicitada interativamente)
- `--mysql-db DB`: Nome do banco de dados (padrão: placas_veiculos)
- `--mysql-table TABLE`: Nome da tabela (padrão: dados_placas)
- `--mysql-if-exists {fail,replace,append}`: Ação caso a tabela já exista (padrão: replace)

### Reprodutibilidade

Uma característica importante deste script é a capacidade de gerar conjuntos de dados idênticos quando a mesma seed é utilizada. Isso é fundamental para:

- Testes repetíveis e consistentes
- Comparação precisa entre diferentes execuções
- Compartilhamento de dados específicos com colegas
- Replicação de resultados em ambientes de desenvolvimento, teste e produção

Exemplo de uso para garantir reprodutibilidade:
```bash
# Ambos comandos gerarão exatamente os mesmos dados
python gen-plates.py --seed 123 --num-records 500
python gen-plates.py --seed 123 --num-records 500

# O mesmo resultado usando arquivo de configuração
python gen-plates.py --config config_com_seed_123.json
```

### Exemplos de Uso

Gerar 1000 registros com seed padrão:
```bash
python gen-plates.py
```

Gerar 500 registros com seed personalizada:
```bash
python gen-plates.py --num-records 500 --seed 123
```

Gerar dados para um período mais longo (90 dias) com nome de arquivo personalizado:
```bash
python gen-plates.py --dias-passados 90 --output dados_3meses.csv
```

Gerar dados com temperatura mais alta e mostrar estatísticas:
```bash
python gen-plates.py --temp-min 20 --temp-max 35 --show-stats
```

Gerar dados com veículos mais novos:
```bash
python gen-plates.py --ano-min 2018 --ano-max 2023
```

Gerar dados com intervalo de velocidade específico:
```bash
python gen-plates.py --velocidade-min 30 --velocidade-max 150
```

Usar um arquivo de configuração para gerar dados com foco em infrações de velocidade:
```bash
python gen-plates.py --config config_infracoes_velocidade.json
```

Usar linha de comando para sobrescrever parâmetros do arquivo de configuração:
```bash
python gen-plates.py --config config_exemplo.json --seed 789 --output novo_arquivo.csv
```

Gerar dados e salvar em um banco de dados MySQL:
```bash
python gen-plates.py --num-records 200 --mysql --mysql-db placas_veiculos --mysql-user usuario
```

Usar arquivo de configuração para conexão MySQL:
```bash
python gen-plates.py --config config_mysql.json
```

### Integração com MySQL

Para utilizar a funcionalidade de armazenamento em MySQL, você precisará:

1. **Instalar as dependências adicionais**:
```bash
pip install pymysql sqlalchemy
```

2. **Criar o banco de dados**:
```sql
CREATE DATABASE placas_veiculos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

3. **Configurar o acesso**:
A senha pode ser fornecida via parâmetro `--mysql-password` ou será solicitada interativamente durante a execução (mais seguro).

4. **Opções de tratamento de tabelas existentes**:
- `fail`: Falha se a tabela já existir
- `replace`: Substitui a tabela se já existir (padrão)
- `append`: Adiciona novos registros à tabela existente

## Sistema de Infrações

O script inclui um sistema inteligente para detecção de possíveis infrações de trânsito, considerando:

1. **Limite de velocidade do local**: Cada local tem um limite de velocidade predefinido (30-60 km/h)
2. **Condições ambientais**: O limite é automaticamente ajustado com base em:
   - Condição da estrada (redução de 20% em vias molhadas, 30% em obras)
   - Condição climática (redução adicional de 10% em condições chuvosas)
3. **Idade do veículo**: Veículos mais antigos têm maior probabilidade de certas infrações

### Tipos de Infrações Detectadas

- **Infrações de velocidade**:
  - Excesso leve (até 20% acima do limite)
  - Excesso médio (entre 20% e 50% acima do limite)
  - Excesso grave (mais de 50% acima do limite)

- **Infrações de documentação e condições**:
  - Veículo sem licenciamento atualizado
  - Veículo em condições irregulares
  - Falta de equipamento obrigatório

- **Infrações de comportamento**:
  - Avanço de sinal vermelho
  - Trafegar na contramão
  - Dirigir utilizando celular
  - Transitar em faixa exclusiva
  - Conduzir sem farol aceso em rodovia
  - Estacionamento ou parada em local proibido

- **Infrações por condições da via**:
  - Velocidade incompatível com as condições da via

## Combinações Realistas

O script garante combinações realistas entre:

1. Tipos de veículos e suas marcas correspondentes
2. Marcas de veículos e seus modelos correspondentes

Por exemplo, um veículo do tipo "Motocicleta" será associado apenas a marcas como Honda, Yamaha, ou Suzuki (e nunca a marcas como Volkswagen ou Fiat). Da mesma forma, uma marca específica (como "Honda") terá apenas modelos compatíveis com essa marca.

## Personalização

Para personalizar ainda mais:

- Adicione novas regiões administrativas, marcas/modelos de veículos, etc.
- Modifique as funções de geração para criar padrões diferentes
- Ajuste os parâmetros de linha de comando para cenários específicos
- Adicione novos tipos de infrações ou modifique as probabilidades das existentes
- Crie seus próprios arquivos de configuração JSON para casos de uso específicos
- Configure a integração com outros bancos de dados além do MySQL

## Requisitos

### Básicos
- Python 3.6+
- pandas
- numpy
- faker

### Para Funcionalidade MySQL (opcionais)
- pymysql
- sqlalchemy

Instale todas as dependências com:
```bash
pip install pandas numpy faker pymysql sqlalchemy
```

## Detalhes Sobre Combinações de Veículos

O script garante combinações realistas entre tipos de veículos, marcas e modelos:

1. **Carros**: Marcas como Volkswagen, Fiat, Chevrolet com modelos apropriados (Gol, Argo, Onix)
2. **SUVs**: Marcas como Jeep, Toyota, Hyundai com modelos como Renegade, RAV4, Creta
3. **Caminhões**: Marcas como Mercedes-Benz, Volvo, Scania com modelos como Actros, FH, R
4. **Motocicletas**: Marcas como Honda, Yamaha, Kawasaki com modelos como CG 160, Factor 150, Ninja 300
5. **Ônibus**: Marcas como Mercedes-Benz, Marcopolo, Comil com modelos como O-500, Paradiso, Campione
6. **Vans**: Marcas como Mercedes-Benz, Fiat, Renault com modelos como Sprinter, Ducato, Master 
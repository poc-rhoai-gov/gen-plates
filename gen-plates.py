# %%
import pandas as pd
import numpy as np
import random
import uuid
import datetime
from faker import Faker

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker('pt_BR')  # Using Brazilian Portuguese locale
Faker.seed(42)

# Set number of records to generate
num_records = 1000

def generate_license_plate():
    """Generate a random Brazilian license plate number"""
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

def generate_plate_data():
    """Generate a complete dataset of license plate records for Brazil"""
    
    # Brazilian states
    states = [
        "Acre", "Alagoas", "Amapá", "Amazonas", "Bahia", "Ceará", 
        "Distrito Federal", "Espírito Santo", "Goiás", "Maranhão", 
        "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Pará", 
        "Paraíba", "Paraná", "Pernambuco", "Piauí", "Rio de Janeiro", 
        "Rio Grande do Norte", "Rio Grande do Sul", "Rondônia", 
        "Roraima", "Santa Catarina", "São Paulo", "Sergipe", "Tocantins"
    ]
    
    # Plate types
    plate_types = ["Standard", "Commercial", "Temporary", "Official", "Diplomatic", "Collector"]
    
    # Vehicle types
    vehicle_types = ["Car", "Truck", "SUV", "Motorcycle", "Bus", "Van"]
    
    # Vehicle makes popular in Brazil
    vehicle_makes = [
        "Volkswagen", "Fiat", "Chevrolet", "Toyota", "Hyundai", 
        "Renault", "Honda", "Ford", "Jeep", "Nissan", "Mitsubishi", 
        "Citroën", "Peugeot", "BMW", "Mercedes-Benz", "Audi", "Kia"
    ]
    
    # Vehicle models popular in Brazil
    vehicle_models = {
        "Volkswagen": ["Gol", "Polo", "T-Cross", "Virtus", "Nivus", "Jetta", "Amarok", "Saveiro", "Taos"],
        "Fiat": ["Argo", "Mobi", "Uno", "Toro", "Strada", "Pulse", "Cronos", "Fastback", "Fiorino"],
        "Chevrolet": ["Onix", "Tracker", "Cruze", "S10", "Spin", "Montana", "Equinox", "Joy"],
        "Toyota": ["Corolla", "Hilux", "SW4", "Yaris", "Corolla Cross", "RAV4", "Etios"],
        "Hyundai": ["HB20", "Creta", "Tucson", "i30", "HB20S", "Santa Fe", "Elantra"],
        "Renault": ["Kwid", "Sandero", "Duster", "Logan", "Captur", "Stepway", "Oroch"],
        "Honda": ["Civic", "HR-V", "Fit", "City", "WR-V", "CR-V", "Accord"],
        "Ford": ["Ka", "EcoSport", "Ranger", "Territory", "Bronco", "Maverick"],
        "Jeep": ["Renegade", "Compass", "Commander", "Wrangler", "Cherokee"],
        "Nissan": ["Kicks", "Versa", "Frontier", "Sentra", "March", "Leaf"],
        "Mitsubishi": ["L200", "Pajero", "ASX", "Eclipse Cross", "Outlander"],
        "Citroën": ["C3", "C4 Cactus", "Aircross", "Jumpy", "Berlingo"],
        "Peugeot": ["208", "2008", "3008", "Partner", "Expert"],
        "BMW": ["320i", "X1", "X3", "X5", "118i", "530i"],
        "Mercedes-Benz": ["Classe A", "Classe C", "GLA", "GLC", "Classe E"],
        "Audi": ["A3", "Q3", "A4", "Q5", "A5"],
        "Kia": ["Sportage", "Cerato", "Sorento", "Stonic", "Rio"]
    }
    
    # Vehicle colors
    vehicle_colors = ["Black", "White", "Silver", "Gray", "Red", "Blue", "Green", "Yellow", "Brown", "Orange"]
    
    # Camera IDs (using Brazilian highway designations)
    camera_ids = [f"BR-{i:03d}" for i in range(101, 131)]
    
    # Weather conditions (relevant to Brazil)
    weather_conditions = ["Sunny", "Cloudy", "Rainy", "Foggy", "Partly Cloudy", "Clear", "Stormy"]
    
    # Visibility conditions
    visibility_conditions = ["Daytime", "Nighttime", "Dusk", "Dawn", "Low Visibility"]
    
    # Road conditions
    road_conditions = ["Dry", "Wet", "Flooded", "Construction", "Potholes", "Good Condition"]
    
    # Traffic conditions
    traffic_conditions = ["Light", "Moderate", "Heavy", "Congested", "Standstill"]
    
    # Event types
    event_types = ["Entry", "Exit", "Speeding", "Parking Violation", "Red Light", "Stop Sign", "Regular Scan"]
    
    # Direction of travel
    directions = ["Northbound", "Southbound", "Eastbound", "Westbound", "Northeast", "Northwest", "Southeast", "Southwest"]
    
    # Brazilian cities (major ones)
    cities = [
        "São Paulo", "Rio de Janeiro", "Brasília", "Salvador", "Fortaleza", 
        "Belo Horizonte", "Manaus", "Curitiba", "Recife", "Porto Alegre", 
        "Belém", "Goiânia", "Guarulhos", "Campinas", "São Luís", 
        "São Gonçalo", "Maceió", "Duque de Caxias", "Campo Grande", "Natal"
    ]
    
    # Generate data
    data = {
        "record_id": [str(uuid.uuid4()) for _ in range(num_records)],
        "license_plate_number": [generate_license_plate() for _ in range(num_records)],
        "plate_state_region": [random.choice(states) for _ in range(num_records)],
        "plate_type": [random.choice(plate_types) for _ in range(num_records)],
        
        # Vehicle attributes
        "vehicle_type": [random.choice(vehicle_types) for _ in range(num_records)],
        "vehicle_make": [random.choice(vehicle_makes) for _ in range(num_records)],
    }
    
    # Add vehicle models that match the makes
    data["vehicle_model"] = [random.choice(vehicle_models[data["vehicle_make"][i]]) for i in range(num_records)]
    
    # Add city information
    data["city"] = [random.choice(cities) for _ in range(num_records)]
    
    # Continue with remaining fields
    data.update({
        "vehicle_color": [random.choice(vehicle_colors) for _ in range(num_records)],
        "vehicle_year": [random.randint(2010, 2023) for _ in range(num_records)],
        
        # Generate timestamps over the last 30 days
        "timestamp": [
            (datetime.datetime.now() - datetime.timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            )).strftime("%Y-%m-%d %H:%M:%S") 
            for _ in range(num_records)
        ],
    })
    
    # Generate realistic latitude and longitude for Brazil
    # Brazil's latitude ranges from approximately 5.2 N to 33.7 S
    # Brazil's longitude ranges from approximately 35.3 W to 73.9 W
    data.update({
        "latitude": [round(random.uniform(-33.7, 5.2), 6) for _ in range(num_records)],
        "longitude": [round(random.uniform(-73.9, -35.3), 6) for _ in range(num_records)],
        "camera_device_id": [random.choice(camera_ids) for _ in range(num_records)],
        "image_path": [f"/images/capture_{i:04d}.jpg" for i in range(num_records)],
        "ocr_confidence_score": [round(random.uniform(0.70, 1.0), 2) for _ in range(num_records)],
        
        # Environmental data (adjusted for Brazil's climate)
        "weather_conditions": [random.choice(weather_conditions) for _ in range(num_records)],
        "temperature": [round(random.uniform(15.0, 40.0), 1) for _ in range(num_records)], # Celsius, warmer for Brazil
        "visibility_lighting": [random.choice(visibility_conditions) for _ in range(num_records)],
        "road_conditions": [random.choice(road_conditions) for _ in range(num_records)],
        "traffic_conditions": [random.choice(traffic_conditions) for _ in range(num_records)],
        
        # Additional fields
        "speed": [random.randint(0, 120) for _ in range(num_records)], # km/h
        "direction_of_travel": [random.choice(directions) for _ in range(num_records)],
        "event_type": [random.choice(event_types) for _ in range(num_records)],
        "error_codes_remarks": [fake.sentence() if random.random() < 0.2 else "" for _ in range(num_records)],
    })
    
    # Convert to DataFrame
    df = pd.DataFrame(data)
    
    # Add derived fields
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["day_of_week"] = df["timestamp"].dt.day_name()
    df["hour_of_day"] = df["timestamp"].dt.hour
    df["week"] = df["timestamp"].dt.isocalendar().week
    df["month"] = df["timestamp"].dt.month
    df["year"] = df["timestamp"].dt.year
    
    # Convert back to string for CSV output
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    
    return df

# Generate the data
plate_data = generate_plate_data()

# Save to CSV
output_file = "license_plate_data_brazil.csv"
plate_data.to_csv(output_file, index=False)

print(f"Generated {len(plate_data)} Brazilian license plate records and saved to {output_file}")

# Display sample of the data
print("\nSample data:")
print(plate_data.head())

# %%
# Display data statistics
print("\nData statistics:")
print(plate_data.describe(include='all').T)




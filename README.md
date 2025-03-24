# Brazilian License Plate Data Generator

This script generates synthetic Brazilian license plate data with various attributes for testing and development purposes.

## Features

- Generates realistic Brazilian license plate numbers in traditional and Mercosur formats
- Creates comprehensive vehicle data with makes and models popular in Brazil
- Includes Brazilian cities, states, and geographical coordinates
- Provides environmental and contextual data relevant to Brazil
- Adds derived fields for analytics (day of week, hour, etc.)
- Outputs data to a CSV file

## Generated Data Fields

### Core Vehicle and Plate Information
- Record ID: A unique identifier for each record
- License Plate Number: Brazilian license plate formats (traditional: ABC1234, Mercosur: ABC1D23)
- Plate State/Region: Brazilian states and Federal District
- Plate Type: Standard, Commercial, Temporary, Official, Diplomatic, Collector
- City: Major Brazilian cities

### Vehicle Attributes
- Vehicle Type: Car, truck, motorcycle, bus, etc.
- Vehicle Make: Manufacturers popular in Brazil (Volkswagen, Fiat, Chevrolet, etc.)
- Vehicle Model: Brazilian market models for each make
- Vehicle Color: Color of the vehicle
- Vehicle Year: Manufacturing year

### Detection and Capture Details
- Timestamp: Date and time of the record
- Location: GPS coordinates within Brazil's geographical boundaries
- Camera/Device ID: Using Brazilian highway designations (BR-101, BR-102, etc.)
- Image Path/URL: Reference to the stored image
- OCR Confidence Score: Confidence level of plate recognition

### Environmental and Contextual Data
- Weather Conditions: Weather patterns typical for Brazil
- Temperature: Ambient temperature (15-40°C, typical for Brazilian climate)
- Visibility/Lighting: Daytime, nighttime, etc.
- Road Conditions: Dry, wet, flooded, construction, potholes, etc.
- Traffic Conditions: Traffic density levels

### Additional Fields
- Speed: Vehicle speed in km/h
- Direction of Travel: Northbound, southbound, etc.
- Event Type: Entry, exit, violation, etc.
- Error Codes/Remarks: Issues or additional notes in Brazilian Portuguese

### Derived Fields
- Day of Week
- Hour of Day
- Week/Month/Year

## Setup and Usage

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the script:
   ```
   python gen-plates.py
   ```

3. The generated data will be saved to `license_plate_data_brazil.csv` in the current directory.

## Customization

You can modify the script to:
- Change the number of records generated (adjust `num_records` variable)
- Customize the range of values for fields
- Add or remove fields as needed
- Change the output file format or location
- Adjust specific regions or cities of Brazil

## Requirements

- Python 3.6+
- pandas
- numpy
- faker (with pt_BR locale)
- uuid 
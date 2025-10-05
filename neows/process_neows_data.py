import json
from pathlib import Path


def validate_neows_structure(input_file='neowsdata.json'):
    """Validate and display the structure of neowsdata.json"""
    with open(input_file, 'r') as f:
        data = json.load(f)

    print("Data type of root:", type(data))

    if isinstance(data, list):
        print(f"Root is a list with {len(data)} items")
        if len(data) > 0:
            print("First item type:", type(data[0]))
            if isinstance(data[0], dict):
                print("First item keys:", list(data[0].keys()))
                print("\nFirst item sample:")
                print(json.dumps(data[0], indent=2)[:800])
    elif isinstance(data, dict):
        print("Root keys:", list(data.keys()))
        for key, value in data.items():
            print(f"\nKey '{key}': type = {type(value)}")
            if isinstance(value, list):
                print(f"  - List length: {len(value)}")
                if len(value) > 0:
                    print(f"  - First item type: {type(value[0])}")
                    if isinstance(value[0], dict):
                        print(f"  - First item keys: {list(value[0].keys())}")
            elif isinstance(value, dict):
                print(f"  - Dict keys: {list(value.keys())[:5]}...")


def extract_name_limited(full_name):
    """Extract the limited name from the full asteroid name."""
    if '(' in full_name:
        before_paren = full_name.split('(')[0].strip()
        parts = before_paren.split()
        return parts[-1] if len(parts) > 1 else parts[0]
    return full_name


def process_neows_data(input_file='neowsdata.json', output_file='asteroids.json'):
    """Process NeoWs data and create simplified asteroid JSON."""

    with open(input_file, 'r') as f:
        data = json.load(f)

    asteroids = []
    asteroid_list = []

    # Case 1: Root is a list of asteroids
    if isinstance(data, list):
        asteroid_list = data
        print(f"Processing list of {len(data)} items")
    # Case 2: Root is a dict
    elif isinstance(data, dict):
        if 'near_earth_objects' in data:
            neo_data = data['near_earth_objects']
            if isinstance(neo_data, list):
                asteroid_list = neo_data
            elif isinstance(neo_data, dict):
                for date, date_asteroids in neo_data.items():
                    asteroid_list.extend(date_asteroids)
        elif 'id' in data and 'name' in data:
            asteroid_list = [data]
        else:
            for key, value in data.items():
                if isinstance(value, list):
                    asteroid_list.extend(value)

    print(f"Found {len(asteroid_list)} potential asteroids to process")

    for idx, asteroid in enumerate(asteroid_list):
        try:
            # Skip if not a dict or missing required fields
            if not isinstance(asteroid, dict):
                print(f"Item {idx} is not a dict, skipping")
                continue

            if 'id' not in asteroid or 'name' not in asteroid:
                print(f"Item {idx} missing id or name, skipping")
                continue

            # Extract year from close approach data
            year = None
            velocity_km_s = None
            closest_approach_distance_km = None

            if asteroid.get('close_approach_data') and len(asteroid['close_approach_data']) > 0:
                close_approach = asteroid['close_approach_data'][0]
                year = int(close_approach['close_approach_date'].split('-')[0])
                velocity_km_s = float(close_approach['relative_velocity']['kilometers_per_second'])
                closest_approach_distance_km = float(close_approach['miss_distance']['kilometers'])

            # Calculate average size in km
            size_km = (
                asteroid['estimated_diameter']['kilometers']['estimated_diameter_min'] +
                asteroid['estimated_diameter']['kilometers']['estimated_diameter_max']
            ) / 2

            asteroid_data = {
                'id': asteroid['id'],
                'name': asteroid['name'],
                'name_limited': extract_name_limited(asteroid['name']),
                'size_km': round(size_km, 3),
                'is_potentially_hazardous_asteroid': asteroid['is_potentially_hazardous_asteroid'],
                'velocity_km_s': round(velocity_km_s, 3) if velocity_km_s else None,
                'closest_approach_distance_km': round(closest_approach_distance_km, 3) if closest_approach_distance_km else None,
                'year': year
            }

            asteroids.append(asteroid_data)
        except (KeyError, TypeError, IndexError) as e:
            print(f"Error processing item {idx} (id: {asteroid.get('id', 'unknown')}): {e}")
            continue

    # Create output structure
    output_data = {'asteroids': asteroids}

    # Write to output file
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"Successfully processed {len(asteroids)} asteroids and saved to {output_file}")


if __name__ == '__main__':
    print("=== Validating neowsdata.json structure ===")
    validate_neows_structure()
    print("\n=== Processing data ===")
    process_neows_data()
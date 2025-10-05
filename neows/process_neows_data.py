import json
from pathlib import Path


def extract_name_limited(full_name):
    """Extract the limited name from the full asteroid name."""
    # Remove ID number and parenthetical designation
    # Example: "433 Eros (A898 PA)" -> "Eros"
    if '(' in full_name:
        # Get the part before the parenthesis
        before_paren = full_name.split('(')[0].strip()
        # Remove leading numbers and spaces
        parts = before_paren.split()
        # Return the last part which is typically the name
        return parts[-1] if len(parts) > 1 else parts[0]
    return full_name


def process_neows_data(input_file='neowsdata.json', output_file='asteroids.json'):
    """Process NeoWs data and create simplified asteroid JSON."""

    # Read the input JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    asteroids = []

    # Handle case where near_earth_objects is a list
    if 'near_earth_objects' in data:
        neo_data = data['near_earth_objects']

        # Check if it's a list or dictionary
        if isinstance(neo_data, list):
            asteroid_list = neo_data
        elif isinstance(neo_data, dict):
            # If it's a dictionary, flatten all asteroids from all dates
            asteroid_list = []
            for date, date_asteroids in neo_data.items():
                asteroid_list.extend(date_asteroids)
        else:
            asteroid_list = []

        for asteroid in asteroid_list:
            # Extract year from close approach data
            year = None
            velocity_km_s = None
            closest_approach_distance_km = None

            if asteroid.get('close_approach_data'):
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
                'closest_approach_distance_km': round(closest_approach_distance_km,
                                                      3) if closest_approach_distance_km else None,
                'year': year
            }

            asteroids.append(asteroid_data)

    # Create output structure
    output_data = {'asteroids': asteroids}

    # Write to output file
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)

    print(f"Processed {len(asteroids)} asteroids and saved to {output_file}")


if __name__ == '__main__':
    process_neows_data()

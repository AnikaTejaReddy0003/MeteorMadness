import json

# --- Step 1: Load JSON file ---
with open("asteroids.json", "r") as f:
    data = json.load(f)

# The JSON structure is:
# {
#   "asteroid": [ {...}, {...}, {...} ]
# }
asteroids = data["asteroids"]

# --- Step 2: Build fast lookup dictionaries ---
index_by_id = {a["id"]: a for a in asteroids}
index_by_name = {a["name_limited"].lower(): a for a in asteroids}


# --- Step 3: Search Functions ---
def search_by_id(asteroid_id: str):
    """O(1) lookup by unique asteroid id"""
    return index_by_id.get(asteroid_id)


def search_by_name(name: str):
    """Case-insensitive lookup by limited name"""
    return index_by_name.get(name.lower())


# --- Step 4: Example usage ---
if __name__ == "__main__":
    # Search by id
    print("Search by ID:")
    result = search_by_id("2000433")
    print(json.dumps(result, indent=2), "\n")

    # Search by name
    print("Search by name:")
    result = search_by_name("Eros")
    print(json.dumps(result, indent=2), "\n")

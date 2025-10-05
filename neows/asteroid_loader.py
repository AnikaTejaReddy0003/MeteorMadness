import json
from typing import Dict, List


class AsteroidData:
    """Singleton class to hold asteroid data"""
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.asteroids: List[Dict] = []
            self.index_by_id: Dict[str, Dict] = {}
            self.index_by_name: Dict[str, Dict] = {}
            AsteroidData._initialized = True

    def load_data(self, filepath="asteroids.json"):
        """Load asteroid data from JSON file"""
        if self.asteroids:  # Already loaded
            return

        with open(filepath, "r") as f:
            data = json.load(f)

        self.asteroids = data["asteroids"]
        self.index_by_id = {a["id"]: a for a in self.asteroids}
        self.index_by_name = {a["name_limited"].lower(): a for a in self.asteroids}

        print(f"Loaded {len(self.asteroids)} asteroids into memory")

    def get_all_asteroids(self) -> List[Dict]:
        """Return all loaded asteroids"""
        return self.asteroids

    def search_by_id(self, asteroid_id: str):
        """O(1) lookup by unique asteroid id"""
        return self.index_by_id.get(asteroid_id)

    def search_by_name(self, name: str):
        """Case-insensitive lookup by limited name"""
        return self.index_by_name.get(name.lower())


# Singleton instance
asteroid_data = AsteroidData()

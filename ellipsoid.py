import math

class Ellipsoid:
    ellipsoids = {
        "WGS84": {
            "name": "World Geodetic System 1984",
            "a": 6378137.0,       # Demi-grand axe (m)
            "f": 1 / 298.257223563 # Aplatissement
        },
        "Clarke1880": {
            "name": "Clarke 1880 (Maroc)",
            "a": 6378249.145,     # Demi-grand axe (m)
            "f": 1 / 293.465      # Aplatissement
        },
        # Systèmes UTM avec différentes zones (28, 29, 30)
        "UTM28": {
            "name": "UTM Zone 28",
            "a": 6378137.0,       # WGS84
            "f": 1 / 298.257223563,
            "lambda0": -15.0      # Longitude centrale pour UTM 28
        },
        "UTM29": {
            "name": "UTM Zone 29",
            "a": 6378137.0,       # WGS84
            "f": 1 / 298.257223563,
            "lambda0": -9.0       # Longitude centrale pour UTM 29
        },
        "UTM30": {
            "name": "UTM Zone 30",
            "a": 6378137.0,       # WGS84
            "f": 1 / 298.257223563,
            "lambda0": -3.0       # Longitude centrale pour UTM 30
        },
        # Projections Conique Conforme de Lambert (zones I, II, III, IV)
        "LambertI": {
            "name": "Lambert Zone I",
            "a": 6378249.145,     # Clarke 1880 pour le Maroc
            "f": 1 / 293.465,
            "phi0": 37.0,         # Latitude origine
            "lambda0": -6.0       # Longitude origine
        },
        "LambertII": {
            "name": "Lambert Zone II",
            "a": 6378249.145,     # Clarke 1880 pour le Maroc
            "f": 1 / 293.465,
            "phi0": 33.0,         # Latitude origine
            "lambda0": -6.0       # Longitude origine
        },
        "LambertIII": {
            "name": "Lambert Zone III",
            "a": 6378249.145,     # Clarke 1880 pour le Maroc
            "f": 1 / 293.465,
            "phi0": 29.0,         # Latitude origine
            "lambda0": -6.0       # Longitude origine
        },
        "LambertIV": {
            "name": "Lambert Zone IV",
            "a": 6378249.145,     # Clarke 1880 pour le Maroc
            "f": 1 / 293.465,
            "phi0": 25.0,         # Latitude origine
            "lambda0": -6.0       # Longitude origine
        }
    }

    def __init__(self, ellipsoid_name):
        """
        Initialise un ellipsoïde selon son nom
        :param ellipsoid_name: Nom de l'ellipsoïde (clé dans le dictionnaire ellipsoids)
        """
        ellipsoid_data = self.ellipsoids.get(ellipsoid_name)
        if not ellipsoid_data:
            raise ValueError(f"L'ellipsoïde {ellipsoid_name} n'est pas supporté.")
        
        self.name = ellipsoid_data["name"]
        self.a = ellipsoid_data["a"]  # Demi-grand axe
        self.f = ellipsoid_data["f"]  # Aplatissement
        self.b = self.a * (1 - self.f)  # Demi-petit axe
        self.e2 = 1 - (self.b**2 / self.a**2)  # Excentricité au carré
        self.lambda0 = ellipsoid_data.get("lambda0", None)  # Longitude centrale (pour UTM)
        self.phi0 = ellipsoid_data.get("phi0", None)        # Latitude origine (pour Lambert)

    def get_parameters(self):
        """
        Retourne les paramètres de l'ellipsoïde sous forme de dictionnaire
        """
        return {
            "Demi-grand axe (a)": self.a,
            "Demi-petit axe (b)": self.b,
            "Aplatissement (f)": self.f,
            "Excentricité au carré (e^2)": self.e2,
            "Longitude centrale (λ0)": self.lambda0,
            "Latitude origine (φ0)": self.phi0
        }

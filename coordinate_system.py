import math
from tkinter import messagebox

class CoordinateSystem:
    def __init__(self, ellipsoid):
        self.ellipsoid = ellipsoid
        self.history = []  # Pour stocker l'historique des transformations

    def geodetic_to_cartesian(self, lat, lon, h):
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        N = self.ellipsoid.a / math.sqrt(1 - self.ellipsoid.e2 * math.sin(lat_rad)**2)
        X = (N + h) * math.cos(lat_rad) * math.cos(lon_rad)
        Y = (N + h) * math.cos(lat_rad) * math.sin(lon_rad)
        Z = (N * (1 - self.ellipsoid.e2) + h) * math.sin(lat_rad)
        return X, Y, Z

    def cartesian_to_geodetic(self, X, Y, Z, tol=1e-9):
        lon = math.degrees(math.atan2(Y, X))
        r = math.sqrt(X**2 + Y**2)
        lat = math.degrees(math.atan2(Z, r))
        lat_rad = math.radians(lat)
        h = 0
        N = self.ellipsoid.a / math.sqrt(1 - self.ellipsoid.e2 * math.sin(lat_rad)**2)
        lat_old = 0
        while abs(lat - lat_old) > tol:
            lat_old = lat
            N = self.ellipsoid.a / math.sqrt(1 - self.ellipsoid.e2 * math.sin(lat_rad)**2)
            h = r / math.cos(lat_rad) - N
            lat_rad = math.atan2(Z + self.ellipsoid.e2 * N * math.sin(lat_rad), r)
            lat = math.degrees(lat_rad)
        return lat, lon, h

    def validate_coordinates_lambert(self, lat, lon, system_name):
        """
        Valide les coordonnées géodésiques pour les systèmes Lambert en fonction de la zone.
        """
        if system_name == "LambertI":
            # Zone Lambert I (par exemple) couvre latitudes de 36°N à 42°N et longitudes de -7°E à 0°E
            if not (36 <= lat <= 42 and -7 <= lon <= 0):
                messagebox.showerror("Erreur", "Les coordonnées ne sont pas valides pour la zone Lambert I")
                return False
        elif system_name == "LambertII":
            if not (32 <= lat <= 36 and -7 <= lon <= 0):
                messagebox.showerror("Erreur", "Les coordonnées ne sont pas valides pour la zone Lambert II")
                return False
        elif system_name == "LambertIII":
            if not (28 <= lat <= 32 and -7 <= lon <= 0):
                messagebox.showerror("Erreur", "Les coordonnées ne sont pas valides pour la zone Lambert III")
                return False
        elif system_name == "LambertIV":
            if not (24 <= lat <= 28 and -7 <= lon <= 0):
                messagebox.showerror("Erreur", "Les coordonnées ne sont pas valides pour la zone Lambert IV")
                return False
        return True

    def transform_to_utm_or_lambert(self, lat, lon, h, system_name):
        """
        Transforme des coordonnées géodésiques en coordonnées UTM ou Lambert.
        Ajout de la validation pour les zones Lambert.
        """
        # Valider les coordonnées pour Lambert
        if "Lambert" in system_name:
            if not self.validate_coordinates_lambert(lat, lon, system_name):
                return None, None

        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        if "UTM" in system_name:
            lambda0 = math.radians(self.ellipsoid.lambda0)
            k0 = 0.9996  # Facteur d'échelle UTM
        elif "Lambert" in system_name:
            phi0 = math.radians(self.ellipsoid.phi0)
            lambda0 = math.radians(self.ellipsoid.lambda0)
            k0 = 1.0  # Facteur d'échelle Lambert

        N = self.ellipsoid.a / math.sqrt(1 - self.ellipsoid.e2 * math.sin(lat_rad)**2)
        T = math.tan(lat_rad) ** 2
        C = (self.ellipsoid.e2 / (1 - self.ellipsoid.e2)) * math.cos(lat_rad) ** 2
        A = (lon_rad - lambda0) * math.cos(lat_rad)

        M = self.ellipsoid.a * ((1 - self.ellipsoid.e2 / 4 - 3 * self.ellipsoid.e2**2 / 64) * lat_rad -
                                (3 * self.ellipsoid.e2 / 8 + 3 * self.ellipsoid.e2**2 / 32) * math.sin(2 * lat_rad) +
                                (15 * self.ellipsoid.e2**2 / 256) * math.sin(4 * lat_rad))

        X = k0 * N * (A + (1 - T + C) * A**3 / 6)
        Y = k0 * (M + N * math.tan(lat_rad) * (A**2 / 2 + (5 - T + 9 * C + 4 * C**2) * A**4 / 24))
        return X, Y

    def transform_to_geo_from_utm_or_lambert(self, X, Y, system_name):
        # Transformer les coordonnées UTM ou Lambert en géodésiques
        pass  # Implémenter cette méthode si nécessaire

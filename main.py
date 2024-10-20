import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
from ellipsoid import Ellipsoid
from coordinate_system import CoordinateSystem
from datetime import datetime

class CoordinateTransformationApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Transformation de Coordonnées")
        self.geometry("800x600")
        
        # Choix du système de coordonnées
        self.ellipsoid_label = ctk.CTkLabel(self, text="Système de coordonnées")
        self.ellipsoid_label.pack(pady=10)

        # Ajouter UTM et Lambert dans la liste déroulante
        self.ellipsoid_var = tk.StringVar(value="WGS84")
        self.ellipsoid_dropdown = ctk.CTkComboBox(
            self, 
            values=["WGS84", "Clarke1880", "UTM28", "UTM29", "UTM30", "LambertI", "LambertII", "LambertIII", "LambertIV"], 
            variable=self.ellipsoid_var
        )
        self.ellipsoid_dropdown.pack(pady=10)

        # Champs d'entrée pour les coordonnées géographiques
        self.geo_label = ctk.CTkLabel(self, text="Coordonnées Géographiques (Lat, Lon, Alt)")
        self.geo_label.pack(pady=10)

        self.geo_entry = ctk.CTkEntry(self, width=400)
        self.geo_entry.pack(pady=10)

        # Champs d'entrée pour les coordonnées cartésiennes
        self.cartesian_label = ctk.CTkLabel(self, text="Coordonnées Cartésiennes (X, Y, Z)")
        self.cartesian_label.pack(pady=10)

        self.cartesian_entry = ctk.CTkEntry(self, width=400)
        self.cartesian_entry.pack(pady=10)

        # Bouton pour effectuer la transformation
        self.transform_button = ctk.CTkButton(self, text="Transformer", command=self.transform_coordinates)
        self.transform_button.pack(pady=10)

        # Historique des transformations (tableau)
        self.history_table = ttk.Treeview(self, columns=("Systeme", "Date", "Coord Entree", "Coord Sortie", "Sens"), show='headings')
        self.history_table.heading("Systeme", text="Système Utilisé")
        self.history_table.heading("Date", text="Date et Heure")
        self.history_table.heading("Coord Entree", text="Coordonnées d'Entrée")
        self.history_table.heading("Coord Sortie", text="Coordonnées de Sortie")
        self.history_table.heading("Sens", text="Sens de Transformation")
        self.history_table.pack(pady=20, fill="x")

        # Variables pour stocker les systèmes et l'historique
        self.coord_system = None
        self.history = []

        # Mise à jour du système de coordonnées en fonction du choix de l'utilisateur
        self.update_coord_system()

    def update_coord_system(self):
        ellipsoid_name = self.ellipsoid_var.get()
        ellipsoid = Ellipsoid(ellipsoid_name)
        self.coord_system = CoordinateSystem(ellipsoid)

    # Fonction pour nettoyer les coordonnées
    def clean_coordinates(self, coords):
        # Remplacer le signe moins Unicode par le signe moins standard
        cleaned = coords.replace('\u2212', '-').strip()
        # Supprimer les espaces et sauts de ligne supplémentaires
        return cleaned

    # Définition de la méthode transform_coordinates ici
    def transform_coordinates(self):
        # Récupérer les coordonnées entrées par l'utilisateur
        geo_coords = self.geo_entry.get().strip()
        cartesian_coords = self.cartesian_entry.get().strip()

        # Nettoyage des coordonnées
        geo_coords = self.clean_coordinates(geo_coords)
        cartesian_coords = self.clean_coordinates(cartesian_coords)

        # Système utilisé
        ellipsoid_name = self.ellipsoid_var.get()

        try:
            if geo_coords:
                # Transformer les coordonnées géographiques en cartésiennes
                lat, lon, h = map(float, geo_coords.split(","))
                if "UTM" in ellipsoid_name or "Lambert" in ellipsoid_name:
                    X, Y = self.coord_system.transform_to_utm_or_lambert(lat, lon, h, ellipsoid_name)
                    if X is None and Y is None:
                        # Si la transformation est annulée à cause d'une erreur, arrêter
                        return
                    self.cartesian_entry.delete(0, tk.END)
                    self.cartesian_entry.insert(0, f"{X:.3f}, {Y:.3f}")
                    sens = "Geo -> UTM/Lambert"
                else:
                    X, Y, Z = self.coord_system.geodetic_to_cartesian(lat, lon, h)
                    self.cartesian_entry.delete(0, tk.END)
                    self.cartesian_entry.insert(0, f"{X:.3f}, {Y:.3f}, {Z:.3f}")
                    sens = "Geo -> Cart"
                coord_entree = geo_coords
                coord_sortie = f"{X:.3f}, {Y:.3f}"
            elif cartesian_coords:
                # Transformer les coordonnées cartésiennes en géodésiques
                X, Y = map(float, cartesian_coords.split(","))
                if "UTM" in ellipsoid_name or "Lambert" in ellipsoid_name:
                    lat, lon = self.coord_system.transform_to_geo_from_utm_or_lambert(X, Y, ellipsoid_name)
                    self.geo_entry.delete(0, tk.END)
                    self.geo_entry.insert(0, f"{lat:.6f}, {lon:.6f}")
                    sens = "UTM/Lambert -> Geo"
                else:
                    X, Y, Z = map(float, cartesian_coords.split(","))
                    lat, lon, h = self.coord_system.cartesian_to_geodetic(X, Y, Z)
                    self.geo_entry.delete(0, tk.END)
                    self.geo_entry.insert(0, f"{lat:.6f}, {lon:.6f}, {h:.3f}")
                    sens = "Cart -> Geo"
                coord_entree = cartesian_coords
                coord_sortie = f"{lat:.6f}, {lon:.6f}"
        except ValueError:
            messagebox.showerror("Erreur", "Coordonnées invalides. Assurez-vous que les valeurs sont au format correct.")

        # Enregistrer la transformation dans l'historique
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append((ellipsoid_name, date_time, coord_entree, coord_sortie, sens))

        # Ajouter à la table d'historique
        self.history_table.insert("", tk.END, values=(ellipsoid_name, date_time, coord_entree, coord_sortie, sens))


if __name__ == "__main__":
    app = CoordinateTransformationApp()
    app.mainloop()

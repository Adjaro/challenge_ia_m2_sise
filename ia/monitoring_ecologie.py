class EnvironmentMetrics:
    """Classe pour gérer les métriques environnementales"""

    def __init__(self):
        self.gwp = 0.0
        self.energy_usage = 0.0

    def update_metrics(self, new_gwp: float, new_energy: float):
        """Met à jour les métriques environnementales"""
        self.gwp += new_gwp
        self.energy_usage += new_energy

    def reset_metrics(self):
        """Réinitialise les métriques"""
        self.gwp = 0.0
        self.energy_usage = 0.0

    def get_metrics(self):
        """Renvoie les métriques"""
        return self.gwp, self.energy_usage


# Créer une instance unique
# monitoring_environnement = EnvironmentMetrics()

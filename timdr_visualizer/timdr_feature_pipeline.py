import json
import math
import numpy as np

class TIMDRFeaturePipeline:
    def __init__(self, ontology_path="theory/timdr_ontology.json"):
        # Próba załadowania sztywnych reguł ontologii
        try:
            with open(ontology_path, "r", encoding="utf-8") as f:
                self.ontology = json.load(f)
        except FileNotFoundError:
            # Fallback w przypadku braku pliku (wartości domyślne)
            self.ontology = {"operators": {"Tau": {"canonical_angles": [36.0, 30.0, 5.625, 720.0]}}}

    def generate_ai_training_tensor(self, steps=100):
        """Generuje ustrukturyzowaną macierz cech (Feature Matrix) optymalną dla uczenia maszynowego."""
        t_values = np.linspace(0, 4 * np.pi, steps) # Pełne 720 stopni
        
        # Przygotowanie tablicy cech: [Kąt, Amplituda_Skrętu, Teoretyczna_Delta_S]
        feature_matrix = []
        
        for t in t_values:
            angle = np.degrees(t)
            # Operator skrętu J - modelowany jako interferencja Tetroidy na Torusie
            twist_j = np.cos(3 * t) * np.sin(2 * t)
            # Równanie dywergencji z uwzględnieniem kompresji
            delta_s = twist_j - 0.25 * (t / (2 * np.pi))
            
            feature_matrix.append([angle, twist_j, delta_s])
            
        return np.array(feature_matrix)

if __name__ == "__main__":
    pipeline = TIMDRFeaturePipeline()
    features = pipeline.generate_ai_training_tensor(steps=5)
    print("=== POTOK CECH AI (TIMDR FEATURE STORE) ===")
    print("Wygenerowana próbka tensora wejściowego dla sieci neuronowej [Kąt, Skręt_J, Delta_S]:")
    print(features)

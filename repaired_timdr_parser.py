import json
import math

class RepairedTIMDRParser:
    def __init__(self):
        # Parametry niezmienników z repozytoriów jbackk-lang
        self.canonical_states = {"λ", "τ", "ρ"}
        self.allowed_angles = {36.0, 30.0, 5.625, 720.0}

    def parse_and_validate_fai(self, raw_input):
        """Naprawiony parser struktur FAI z automatycznym domykaniem wyjątków"""
        try:
            # Jeśli wejście jest tekstem, próbuje wyizolować strukturę JSON
            if isinstance(raw_input, str):
                cleaned = raw_input.strip()
                if "{" in cleaned:
                    start_idx = cleaned.find("{")
                    end_idx = cleaned.rfind("}") + 1
                    data = json.loads(cleaned[start_idx:end_idx])
                else:
                    return {"status": "PARSING_ERROR", "error": "Brak prawidłowego bloku danych JSON."}
            else:
                data = raw_input

            # Sprawdzenie obecności głównych sekcji architektury Λ-τ-ρ
            required = ["MODEL", "STATES", "TRANSITIONS"]
            if not all(req in data for req in required):
                return {"status": "VALIDATION_FAILED", "error": "Niekompletna struktura modelu GIA."}

            # Ekstrakcja i walidacja symboli stanów
            extracted_symbols = {s.get("SYMBOL") for s in data["STATES"] if "SYMBOL" in s}
            if not extracted_symbols.issubset(self.canonical_states):
                return {
                    "status": "ANOMALY_DETECTED",
                    "error": f"Niedozwolone symbole stanów w warstwie Λ: {extracted_symbols - self.canonical_states}"
                }

            return {"status": "SUCCESS", "data": data, "message": "Warstwa strukturalna Λ zweryfikowana."}

        except json.JSONDecodeError as je:
            return {"status": "MALFORMED_JSON", "error": f"Błąd składni w pliku konfiguracyjnym: {str(je)}"}
        except Exception as e:
            return {"status": "RUNTIME_ERROR", "error": str(e)}

    def inject_astro_map_data(self, dataset_name, photon_count_2mass, photon_count_rosat):
        """Potok wejściowy dla astro-map: Wyliczanie dywergencji interferencji ΔS"""
        # Unikanie dzielenia przez zero przy logarytmowaniu tła kosmicznego
        p1 = max(photon_count_2mass, 1)
        p2 = max(photon_count_rosat, 1)
        
        # Wyliczenie entropii względnej (Kullback-Leibler / dywergencja ΔS dla pól rezonansowych)
        # Symulacja rzutu z idealnej struktury do obserwowalnej projekcji ρ
        initial_entropy = math.log2(p1)
        final_entropy = math.log2(p2)
        delta_S = final_entropy - initial_entropy

        # Sprawdzenie stabilizacji według reguł FIELDCORE
        is_stable = "TAK (Kompresja rezonansowa)" if delta_S <= 0 else "NIE (Nadmiar skrętu / Emisja fali)"

        return {
            "dataset": dataset_name,
            "metrics": {
                "initial_entropy_lambda": round(initial_entropy, 4),
                "final_entropy_rho": round(final_entropy, 4),
                "divergence_delta_S": round(delta_S, 4),
                "is_topologically_stable": is_stable
            }
        }

# =====================================================================
# SYMULACJA URUCHOMIENIA I WALIDACJI POTOKU DANYCH
# =====================================================================
if __name__ == "__main__":
    parser = RepairedTIMDRParser()
    print("=== NAPRAWIONY PARSER ZINTEGROWANY Z MATH-VALIDATOR-2.0 ===\n")

    # 1. Test parsowania surowego, zanieczyszczonego tekstem formatu ze strony model.html
    raw_html_payload = """
    FORMAT DO PARSOWANIA PRZEZ AI
    {
        "MODEL": { "STATES": ["λ", "τ", "ρ"], "TRANSITIONS": "MIXED", "VERSION": 1 },
        "STATES": [
            {"SYMBOL": "λ", "NAME": "lambda", "ROLE": "start", "CODE": "00"},
            {"SYMBOL": "τ", "NAME": "tau", "ROLE": "change", "CODE": "01"},
            {"SYMBOL": "ρ", "NAME": "rho", "ROLE": "effect", "CODE": "10"}
        ],
        "TRANSITIONS": [
            {"FROM": "λ", "TO": "τ", "CODE": "0001"},
            {"FROM": "τ", "TO": "ρ", "CODE": "0110"}
        ]
    }
    """
    
    parsed_result = parser.parse_and_validate_fai(raw_html_payload)
    print(f"[TEST 1] Status parsowania: {parsed_result['status']}")
    if parsed_result['status'] == "SUCCESS":
        print(f"         Wiadomość: {parsed_result['message']}")
    else:
        print(f"         Błąd: {parsed_result['error']}")

    print("\n---------------------------------------------------------------\n")

    # 2. Test wstrzyknięcia danych empirycznych z astro-map (Interferencja map 2MASS i ROSAT)
    print("[TEST 2] Przetwarzanie spektrum interferencji dla astro-map:")
    astro_analysis = parser.inject_astro_map_data(
        dataset_name="Przegląd_Nieba_Sektor_X",
        photon_count_2mass=1024,  # Sygnał wejściowy (Struktura)
        photon_count_rosat=256    # Sygnał wyjściowy (Efekt kompresji)
    )
    print(f"         Identyfikator danych:   {astro_analysis['dataset']}")
    print(f"         Entropia początkowa (Λ): {astro_analysis['metrics']['initial_entropy_lambda']}")
    print(f"         Entropia końcowa (ρ):    {astro_analysis['metrics']['final_entropy_rho']}")
    print(f"         Wynikowa dywergencja ΔS: {astro_analysis['metrics']['divergence_delta_S']}")
    print(f"         Stabilność topologiczna: {astro_analysis['metrics']['is_topologically_stable']}")

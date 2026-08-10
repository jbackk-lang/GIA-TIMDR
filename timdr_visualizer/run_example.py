from analyzer import analyze_text, detect_twists
from visualizer import plot_analysis

text = """
Czarna dziura jest lokalnym maksimum pola spektralnego.
Gdy koherencja fazowa rośnie, struktura staje się bardziej stabilna.
Następnie pojawia się punkt skrętu, który zmienia topologię.
To prowadzi do projekcji Möbiusa.
"""

analyses = analyze_text(text)
twists = detect_twists(analyses)
plot_analysis(analyses, twists)

import re
import numpy as np

class SentenceAnalysis:
    def __init__(self, sentence, lam, tau, rho):
        self.sentence = sentence
        self.lam = lam
        self.tau = tau
        self.rho = rho

def split_sentences(text):
    return re.split(r'(?<=[.!?]) +', text)

def lambda_score(sentence):
    logic_words = ["jeśli", "bo", "ponieważ", "dlatego", "gdy", "kiedy", "ale", "jednak"]
    return sum(sentence.lower().count(w) for w in logic_words)

def tau_score(sentence):
    time_words = ["potem", "następnie", "wcześniej", "później", "gdy", "kiedy"]
    return sum(sentence.lower().count(w) for w in time_words)

def rho_score(sentence):
    return len([w for w in sentence.split() if len(w) > 7])

def normalize(values):
    arr = np.array(values, dtype=float)
    if arr.max() == 0:
        return arr
    return arr / arr.max()

def analyze_text(text):
    sentences = split_sentences(text)
    lam_list = [lambda_score(s) for s in sentences]
    tau_list = [tau_score(s) for s in sentences]
    rho_list = [rho_score(s) for s in sentences]

    lam_norm = normalize(lam_list)
    tau_norm = normalize(tau_list)
    rho_norm = normalize(rho_list)

    return [
        SentenceAnalysis(s, lam_norm[i], tau_norm[i], rho_norm[i])
        for i, s in enumerate(sentences)
    ]

def detect_twists(analyses, threshold=0.4):
    twists = []
    for i in range(1, len(analyses)):
        prev = analyses[i-1]
        curr = analyses[i]
        delta = abs(curr.lam - prev.lam) + abs(curr.tau - prev.tau) + abs(curr.rho - prev.rho)
        if delta > threshold:
            twists.append(i)
    return twists

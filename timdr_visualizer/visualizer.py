import matplotlib.pyplot as plt

def plot_analysis(analyses, twists):
    x = list(range(len(analyses)))
    lam = [a.lam for a in analyses]
    tau = [a.tau for a in analyses]
    rho = [a.rho for a in analyses]

    plt.figure(figsize=(10,5))
    plt.plot(x, lam, label="Λ (lambda)")
    plt.plot(x, tau, label="τ (tau)")
    plt.plot(x, rho, label="ρ (rho)")

    for t in twists:
        plt.axvline(t, color='red', linestyle='--', alpha=0.5)

    plt.legend()
    plt.title("TIMDR — analiza struktury informacji")
    plt.xlabel("Zdanie")
    plt.ylabel("Wartość znormalizowana")
    plt.tight_layout()
    plt.show()

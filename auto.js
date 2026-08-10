async function fetchMarkdown(path) {
    const url = `https://raw.githubusercontent.com/jbackk-lang/TIMDR/main/${path}`;
    const res = await fetch(url);
    return await res.text();
}

async function autoAnalyze() {
    const files = ["README.md", "TIMDR.md", "topologia.md"]; // dodasz swoje
    let combined = "";

    for (const f of files) {
        try {
            const text = await fetchMarkdown(f);
            combined += "\n" + text;
        } catch(e) {
            console.log("Brak pliku:", f);
        }
    }

    document.getElementById("inputText").value = combined;
    analyze();
}

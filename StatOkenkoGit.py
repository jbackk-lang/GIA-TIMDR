"""GitHub traffic: live colored window, no snapshots or files written."""
TOKEN = "Wklej Token"  # Możesz wkleić token tutaj albo w oknie programu.
USERNAME = "Twój login"
DNI = 14  # Dostępne okresy: 3, 7, 14 dni.

import json
import queue
import threading
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timezone, timedelta
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote
import webbrowser


class GithubError(Exception):
    def __init__(self, message, fatal=False):
        super().__init__(message)
        self.fatal = fatal


def github_get(path, token, params=None):
    url = "https://api.github.com" + path
    if params:
        url += "?" + urlencode(params)
    request = Request(url, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + token,
        "User-Agent": "GitHub-Traffic-Live-Table",
    })
    try:
        with urlopen(request, timeout=15) as response:
            return json.load(response)
    except HTTPError as error:
        try:
            message = json.loads(error.read()).get("message", "")
        except (ValueError, OSError):
            message = ""
        if error.code == 401:
            raise GithubError("401: token nieprawidłowy lub wygasł", fatal=True) from None
        if error.code == 429 or error.headers.get("X-RateLimit-Remaining") == "0":
            raise GithubError("Limit zapytań GitHub — odśwież później", fatal=True) from None
        if error.code == 403:
            raise GithubError("403: brak uprawnień do statystyk ruchu (Administration: read)") from None
        if error.code == 404:
            raise GithubError("404: repozytorium lub statystyki niedostępne dla tokena") from None
        raise GithubError(f"HTTP {error.code}: {message[:160]}") from None
    except (URLError, TimeoutError, OSError) as error:
        raise GithubError("Problem połączenia: " + str(error)[:160]) from None
    except ValueError:
        raise GithubError("GitHub zwrócił nieprawidłowy JSON") from None


def get_repos(username, token, stop=None):
    identity = github_get("/user", token)
    if not isinstance(identity, dict) or not identity.get("login"):
        raise GithubError("Nie udało się rozpoznać konta tokena", fatal=True)
    owner = quote(username, safe="")
    if identity["login"].casefold() == username.casefold():
        endpoint = "/user/repos"
        params = {"affiliation": "owner", "sort": "full_name", "direction": "asc"}
    else:
        account = github_get("/users/" + owner, token)
        if not isinstance(account, dict):
            raise GithubError("Nieprawidłowe dane konta", fatal=True)
        endpoint = "/orgs/" + owner + "/repos" if account.get("type") == "Organization" else "/users/" + owner + "/repos"
        params = {"type": "all" if account.get("type") == "Organization" else "owner"}
    repos, seen = [], set()
    page = 1
    while True:
        if stop is not None and stop.is_set():
            return repos
        data = github_get(endpoint, token, {**params, "per_page": 100, "page": page})
        if not isinstance(data, list):
            raise GithubError("Nieprawidłowa lista repozytoriów", fatal=True)
        for repo in data:
            if repo.get("full_name") and repo["full_name"] not in seen:
                seen.add(repo["full_name"])
                repos.append(repo)
        if len(data) < 100:
            return repos
        page += 1


def traffic_totals(payload, kind, days, today=None):
    if not isinstance(payload, dict):
        raise GithubError("Brak danych statystyk")
    def number(value):
        if type(value) is not int or value < 0:
            raise GithubError("Nieprawidłowe wartości statystyk")
        return value
    if days == 14:
        return number(payload.get("count")), number(payload.get("uniques"))
    rows = payload.get(kind)
    if not isinstance(rows, list):
        raise GithubError("Brak dziennego rozbicia statystyk")
    today = today or datetime.now(timezone.utc).date()
    since = today - timedelta(days=days - 1)
    count = uniques = 0
    for row in rows:
        try:
            day = datetime.fromisoformat(row["timestamp"].replace("Z", "+00:00")).astimezone(timezone.utc).date()
        except (KeyError, ValueError, TypeError, AttributeError):
            raise GithubError("Nieprawidłowa data statystyk") from None
        if since <= day <= today:
            count += number(row.get("count"))
            uniques += number(row.get("uniques"))
    return count, uniques


def fetch_repo(repo, token, days, stop):
    result = {"repo": repo["full_name"], "views": None, "unique_views": None,
              "clones": None, "unique_clones": None, "errors": []}
    endpoint = "/repos/" + "/".join(quote(part, safe="") for part in repo["full_name"].split("/")) + "/traffic/"
    for kind, unique_key in (("views", "unique_views"), ("clones", "unique_clones")):
        if stop.is_set():
            result["errors"].append("Zatrzymano pobieranie")
            break
        try:
            result[kind], result[unique_key] = traffic_totals(github_get(endpoint + kind, token), kind, days)
        except GithubError as error:
            result["errors"].append(kind + ": " + str(error))
            if error.fatal:
                stop.set()
                break
    return result


class TrafficWindow:
    def __init__(self, root):
        self.root = root
        root.title("GitHub — tabela ruchu na żywo")
        root.geometry("1230x740")
        root.minsize(900, 520)
        root.configure(bg="#0b1220")
        self.messages = queue.Queue()
        self.rows = {}
        self.stop = threading.Event()
        self.job = 0
        self.running = False
        self.total = 0
        self.period = DNI
        self.sort_key = "views"
        self.descending = False
        self.hidden_zero = tk.BooleanVar(value=True)
        style = ttk.Style(root)
        style.theme_use("clam")
        style.configure("Treeview", background="#111c30", fieldbackground="#111c30",
                        foreground="#e2e8f0", rowheight=29, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", background="#1e3a5f", foreground="white", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#2563eb")], foreground=[("selected", "white")])
        tk.Label(root, text="RUCH W REPOZYTORIACH", bg="#0b1220", fg="#7dd3fc",
                 font=("Segoe UI", 19, "bold")).pack(anchor="w", padx=20, pady=(16, 8))
        controls = tk.Frame(root, bg="#0b1220")
        controls.pack(fill="x", padx=20)
        tk.Label(controls, text="Konto:", bg="#0b1220", fg="white").pack(side="left")
        self.user = ttk.Entry(controls, width=20)
        self.user.insert(0, USERNAME)
        self.user.pack(side="left", padx=(6, 15))
        tk.Label(controls, text="Token:", bg="#0b1220", fg="white").pack(side="left")
        self.token = ttk.Entry(controls, show="*", width=28)
        if TOKEN and TOKEN != "WKLEJ TOKEN":
            self.token.insert(0, TOKEN)
        self.token.pack(side="left", padx=6)
        self.days = ttk.Combobox(controls, values=[3, 7, 14], state="readonly", width=4)
        self.days.set(str(DNI))
        self.days.pack(side="left", padx=(12, 4))
        tk.Label(controls, text="dni", bg="#0b1220", fg="white").pack(side="left")
        self.start_button = ttk.Button(controls, text="Pobierz / odśwież", command=self.start)
        self.start_button.pack(side="left", padx=12)
        ttk.Button(controls, text="Zatrzymaj", command=lambda: self.stop.set()).pack(side="left")
        tk.Checkbutton(root, text="Ukryj potwierdzone zera", variable=self.hidden_zero, command=self.render,
                       bg="#0b1220", fg="#cbd5e1", selectcolor="#17243a", activebackground="#0b1220",
                       activeforeground="white").pack(anchor="w", padx=16, pady=8)
        area = tk.Frame(root, bg="#0b1220")
        area.pack(fill="both", expand=True, padx=20)
        self.columns = ("repo", "views", "unique_views", "clones", "unique_clones", "status")
        self.tree = ttk.Treeview(area, columns=self.columns, show="headings")
        for key, title, width in zip(self.columns,
            ("Repozytorium", "Wyświetlenia", "Unikalni (14 dni)", "Klonowania", "Unikalni (14 dni)", "Stan"),
            (330, 105, 125, 105, 125, 280)):
            self.tree.heading(key, text=title, command=lambda name=key: self.change_sort(name))
            self.tree.column(key, width=width, minwidth=70, anchor="w" if key in ("repo", "status") else "e")
        self.tree.tag_configure("even", background="#152238")
        self.tree.tag_configure("odd", background="#101a2c")
        self.tree.tag_configure("active", foreground="#bbf7d0")
        self.tree.tag_configure("zero", foreground="#94a3b8")
        self.tree.tag_configure("error", foreground="#fecaca")
        self.tree.tag_configure("partial", foreground="#fde68a")
        vertical = ttk.Scrollbar(area, orient="vertical", command=self.tree.yview)
        horizontal = ttk.Scrollbar(area, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        area.rowconfigure(0, weight=1)
        area.columnconfigure(0, weight=1)
        self.tree.bind("<Double-1>", self.open_repo)
        self.summary = tk.Label(root, text="Suma wyświetleń: 0   |   Suma klonowań: 0", bg="#0b1220",
                                fg="#86efac", font=("Segoe UI", 14, "bold"), anchor="w")
        self.summary.pack(fill="x", padx=20, pady=(12, 4))
        self.status = tk.Label(root, text="Wklej token i kliknij Pobierz. Wyniki pojawiają się podczas pobierania.",
                               bg="#0b1220", fg="#cbd5e1", anchor="w", wraplength=1150)
        self.status.pack(fill="x", padx=20, pady=4)
        self.note = tk.Label(root, text="Dane pobierane bezpośrednio z GitHuba. Program nie zapisuje plików ani snapshotów.",
                             bg="#0b1220", fg="#94a3b8", anchor="w", wraplength=1150)
        self.note.pack(fill="x", padx=20, pady=(0, 14))
        root.protocol("WM_DELETE_WINDOW", self.close)
        root.after(100, self.poll)
        if self.token.get():
            root.after(200, self.start)

    def start(self):
        if self.running:
            return
        token = self.token.get().strip()
        username = self.user.get().strip()
        if not token or token == "WKLEJ TOKEN" or not username:
            self.status.config(text="Uzupełnij token i nazwę konta.", fg="#fca5a5")
            return
        self.job += 1
        job = self.job
        self.stop = threading.Event()
        stop = self.stop
        self.period = int(self.days.get())
        self.rows.clear()
        self.total = 0
        self.running = True
        self.start_button.config(state="disabled")
        unique = "Unikalni (14 dni)" if self.period == 14 else "Suma dziennych uniq."
        self.tree.heading("unique_views", text=unique)
        self.tree.heading("unique_clones", text=unique)
        self.note.config(text="14 dni: unikalni według API. Dla 3/7 dni: suma dziennych unikalnych, z możliwymi powtórzeniami osób. Dni liczone w UTC. Żadne pliki nie są zapisywane.")
        self.status.config(text="Pobieram listę repozytoriów…", fg="#7dd3fc")
        self.render()
        def coordinator():
            try:
                repos = get_repos(username, token, stop)
                self.messages.put((job, "total", len(repos)))
                work = queue.Queue()
                for repo in repos:
                    work.put(repo)
                def worker():
                    while not stop.is_set():
                        try:
                            repo = work.get_nowait()
                        except queue.Empty:
                            return
                        self.messages.put((job, "row", fetch_repo(repo, token, self.period, stop)))
                workers = [threading.Thread(target=worker, daemon=True) for _ in range(min(3, len(repos)))]
                for worker_thread in workers:
                    worker_thread.start()
                for worker_thread in workers:
                    worker_thread.join()
                self.messages.put((job, "done", stop.is_set()))
            except Exception as error:
                self.messages.put((job, "error", str(error)))
        threading.Thread(target=coordinator, daemon=True).start()

    def render(self):
        rows = list(self.rows.values())
        if self.hidden_zero.get():
            rows = [r for r in rows if r["errors"] or r["views"] != 0 or r["clones"] != 0]
        if self.sort_key in ("repo", "status"):
            rows.sort(key=lambda r: (r["repo"] if self.sort_key == "repo" else "; ".join(r["errors"])).casefold(), reverse=self.descending)
        else:
            known = [r for r in rows if r[self.sort_key] is not None]
            unknown = [r for r in rows if r[self.sort_key] is None]
            known.sort(key=lambda r: (r[self.sort_key], r["repo"].casefold()), reverse=self.descending)
            rows = known + unknown
        self.tree.delete(*self.tree.get_children())
        for index, row in enumerate(rows):
            color = "partial" if row["errors"] and (row["views"] is not None or row["clones"] is not None) else "error" if row["errors"] else "active" if row["views"] or row["clones"] else "zero"
            values = [row["repo"]] + ["N/D" if row[k] is None else f"{row[k]:,}".replace(",", " ") for k in self.columns[1:5]]
            self.tree.insert("", "end", values=values + ["; ".join(row["errors"]) or "OK"], tags=("even" if index % 2 == 0 else "odd", color))
        views = sum(r["views"] for r in self.rows.values() if r["views"] is not None)
        clones = sum(r["clones"] for r in self.rows.values() if r["clones"] is not None)
        errors = sum(bool(r["errors"]) for r in self.rows.values())
        self.summary.config(text=f"Suma wyświetleń: {views:,}   |   Suma klonowań: {clones:,}   |   Błędy/częściowe: {errors}".replace(",", " "))

    def change_sort(self, key):
        self.descending = not self.descending if self.sort_key == key else False
        self.sort_key = key
        self.render()

    def poll(self):
        changed = False
        while True:
            try:
                job, kind, payload = self.messages.get_nowait()
            except queue.Empty:
                break
            if job != self.job:
                continue
            if kind == "total":
                self.total = payload
            elif kind == "row":
                self.rows[payload["repo"]] = payload
                changed = True
                self.status.config(text=f"Pobrano {len(self.rows)}/{self.total} repozytoriów. Tabela jest na bieżąco sortowana.", fg="#7dd3fc")
            elif kind in ("done", "error"):
                self.running = False
                self.start_button.config(state="normal")
                text = "Błąd: " + payload if kind == "error" else f"{'Zatrzymano' if payload else 'Gotowe'}: {len(self.rows)}/{self.total} repozytoriów. Dwuklik otwiera repozytorium."
                self.status.config(text=text, fg="#fca5a5" if kind == "error" else "#86efac")
        if changed:
            self.render()
        self.root.after(100, self.poll)

    def open_repo(self, event):
        selected = self.tree.selection()
        if selected:
            name = self.tree.item(selected[0], "values")[0]
            webbrowser.open("https://github.com/" + name)

    def close(self):
        self.stop.set()
        self.root.destroy()


def main():
    root = tk.Tk()
    TrafficWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()


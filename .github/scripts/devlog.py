"""Escreve no README o que foi mexido por último nos projetos.

Roda pela Action, uma vez por dia — quem abre o perfil vê o que está vivo
agora, não em 2024. Só troca o miolo entre os marcadores DEVLOG; o resto do
README fica intacto.

Uso:  GITHUB_TOKEN=... python .github/scripts/devlog.py
"""
import json
import os
import pathlib
import urllib.error
import urllib.request
from datetime import datetime, timezone

# Lista curada, e não "repositórios com push mais recente": ordenar por push
# faz subir merge, ajuste de README e commit de manutenção — justamente o que
# ninguém quer ler num perfil.
ACOMPANHAR = [
    "Israel-Mendes-git/Guilda-da-Corrupcao",
    "Israel-Mendes-git/Roguelike",
    "Israel-Mendes-git/tower-defense",
    "Israel-Mendes-git/Dizido",
    "Israel-Mendes-git/Uikanban",
    "Israel-Mendes-git/Rapadura_filmes",
]
QUANTOS = 3
INICIO, FIM = "<!-- DEVLOG:INICIO -->", "<!-- DEVLOG:FIM -->"
README = pathlib.Path(__file__).resolve().parents[2] / "README.md"


def api(caminho: str):
    cabecalho = {"Accept": "application/vnd.github+json", "User-Agent": "devlog-perfil"}
    if os.environ.get("GITHUB_TOKEN"):
        cabecalho["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    req = urllib.request.Request(f"https://api.github.com{caminho}", headers=cabecalho)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def ha_quanto(iso: str) -> str:
    quando = datetime.fromisoformat(iso.replace("Z", "+00:00"))
    dias = (datetime.now(timezone.utc) - quando).days
    if dias <= 0:
        return "hoje"
    if dias == 1:
        return "ontem"
    if dias < 14:
        return f"há {dias} dias"
    if dias < 60:
        return f"há {dias // 7} semanas"
    return f"há {dias // 30} meses"


def primeira_linha(msg: str, limite: int = 90) -> str:
    linha = msg.strip().splitlines()[0].strip()
    return linha if len(linha) <= limite else linha[: limite - 1].rstrip() + "…"


def montar() -> str:
    achados = []
    for completo in ACOMPANHAR:
        try:
            commits = api(f"/repos/{completo}/commits?per_page=1")
        except urllib.error.HTTPError:
            continue  # privado, vazio ou renomeado — some em silêncio
        if not commits:
            continue
        c = commits[0]["commit"]
        achados.append(
            {
                "data": c["author"]["date"],
                "nome": completo.split("/")[-1],
                "url": f"https://github.com/{completo}",
                "msg": primeira_linha(c["message"]),
            }
        )

    achados.sort(key=lambda a: a["data"], reverse=True)
    if not achados:
        return "_Sem novidade por aqui._"

    # Dois espaços no fim da primeira linha forçam quebra dentro da citação.
    blocos = [
        f"> **[{a['nome']}]({a['url']})** · {ha_quanto(a['data'])}  \n> {a['msg']}"
        for a in achados[:QUANTOS]
    ]
    return "\n>\n".join(blocos)


texto = README.read_text(encoding="utf-8")
i, f = texto.index(INICIO) + len(INICIO), texto.index(FIM)
novo = texto[:i] + "\n" + montar() + "\n" + texto[f:]

if novo == texto:
    print("devlog sem mudança")
else:
    README.write_text(novo, encoding="utf-8")
    print("devlog atualizado")

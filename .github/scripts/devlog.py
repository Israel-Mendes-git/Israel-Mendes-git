"""Desenha em SVG o que foi mexido por último nos projetos.

Gera devlog.svg, que o README embute. Em SVG em vez de markdown porque no
markdown isso era três linhas de citação cinza — some no meio da página.

Roda pela Action, uma vez por dia. Lista curada, e não "repositórios com push
mais recente": ordenar por push faz subir merge, ajuste de README e commit de
manutenção — justamente o que ninguém quer ler num perfil.

Uso:  GITHUB_TOKEN=... python .github/scripts/devlog.py
"""
import json
import os
import pathlib
import urllib.error
import urllib.request
from datetime import datetime, timezone
from xml.sax.saxutils import escape

ACOMPANHAR = [
    ("Israel-Mendes-git/Guilda-da-Corrupcao", "#d99a3c"),
    ("Israel-Mendes-git/Roguelike", "#5fae52"),
    ("Israel-Mendes-git/tower-defense", "#d97a3c"),
    ("Israel-Mendes-git/Dizido", "#7b7bdd"),
    ("Israel-Mendes-git/Uikanban", "#4a94d8"),
    ("Israel-Mendes-git/Rapadura_filmes", "#9b6bd6"),
]
QUANTOS = 3
L, LINHA_H = 900, 46
SAIDA = pathlib.Path(__file__).resolve().parents[2] / "devlog.svg"


def api(caminho: str):
    cabecalho = {"Accept": "application/vnd.github+json", "User-Agent": "devlog-perfil"}
    if os.environ.get("GITHUB_TOKEN"):
        cabecalho["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    req = urllib.request.Request(f"https://api.github.com{caminho}", headers=cabecalho)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def ha_quanto(iso: str) -> str:
    dias = (datetime.now(timezone.utc) - datetime.fromisoformat(iso.replace("Z", "+00:00"))).days
    if dias <= 0:
        return "hoje"
    if dias == 1:
        return "ontem"
    if dias < 14:
        return f"há {dias} dias"
    if dias < 60:
        return f"há {dias // 7} semanas"
    return f"há {dias // 30} meses"


def encurta(msg: str, limite: int = 62) -> str:
    """SVG não quebra linha sozinho — corta no limite que cabe na largura."""
    linha = msg.strip().splitlines()[0].strip()
    return linha if len(linha) <= limite else linha[: limite - 1].rstrip() + "…"


def coletar():
    achados = []
    for completo, cor in ACOMPANHAR:
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
                "msg": encurta(c["message"]),
                "cor": cor,
            }
        )
    achados.sort(key=lambda a: a["data"], reverse=True)
    return achados[:QUANTOS]


def desenhar(itens) -> str:
    A = 78 + max(len(itens), 1) * LINHA_H

    if itens:
        linhas = "".join(
            f'''
    <g transform="translate(0, {70 + i * LINHA_H})">
      <rect x="28" y="-16" width="3" height="32" rx="1.5" fill="{it['cor']}"/>
      <text x="44" y="-1" fill="{it['cor']}" font-size="14" font-weight="700" class="t">{escape(it['nome'])}</text>
      <text x="{L-32}" y="-1" fill="#6f6a63" font-size="12" text-anchor="end" class="m">{escape(ha_quanto(it['data']))}</text>
      <text x="44" y="17" fill="#9d968c" font-size="12.5" class="m">{escape(it['msg'])}</text>
    </g>'''
            for i, it in enumerate(itens)
        )
    else:
        linhas = f'<text x="44" y="78" fill="#6f6a63" font-size="13" class="m">sem novidade por aqui</text>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {A}" width="{L}" height="{A}"
     role="img" aria-label="Últimos commits nos projetos">
  <title>No que estou mexendo</title>
  <defs>
    <clipPath id="corte"><rect width="{L}" height="{A}" rx="10"/></clipPath>
    <style>
      .t {{ font-family: "Segoe UI", Ubuntu, Helvetica, Arial, sans-serif; }}
      .m {{ font-family: ui-monospace, "DejaVu Sans Mono", Consolas, monospace; }}
    </style>
  </defs>
  <g clip-path="url(#corte)">
    <rect width="{L}" height="{A}" fill="#080a08"/>
    <rect width="{L}" height="{A}" fill="none" stroke="#22c55e" stroke-opacity="0.28" stroke-width="2" rx="10"/>

    <text x="28" y="34" fill="#22c55e" font-size="11" letter-spacing="4" class="m">NO QUE ESTOU MEXENDO</text>
    <line x1="28" y1="48" x2="{L-28}" y2="48" stroke="#22c55e" stroke-opacity="0.18"/>
    <text x="{L-28}" y="34" fill="#3f3b36" font-size="10" text-anchor="end" class="m">atualiza sozinho, todo dia</text>
    {linhas}

    <rect x="28" y="{A-20}" width="7" height="12" fill="#22c55e">
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>
'''


itens = coletar()
novo = desenhar(itens)
antigo = SAIDA.read_text(encoding="utf-8") if SAIDA.exists() else ""

if novo == antigo:
    print("devlog sem mudança")
else:
    SAIDA.write_text(novo, encoding="utf-8")
    print(f"devlog.svg atualizado com {len(itens)} itens")

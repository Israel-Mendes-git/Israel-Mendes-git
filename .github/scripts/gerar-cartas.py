"""Desenha os projetos como cartas de jogo em SVG.

Uma carta por projeto, porque SVG servido dentro de <img> não carrega link
interno: para cada carta ser clicável ela precisa ser um arquivo, envolvido
por um <a> no README.

Uso:  python .github/scripts/gerar-cartas.py
"""
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]
L, A = 240, 336  # 5:7, proporção de carta

VERDE, CLARO, ESCURO = "#22c55e", "#4ade80", "#0f2c1b"
TINTA, BRUMA = "#e6edf3", "#9ca3af"

# emblema: desenho simples em vez de emoji, que depende da fonte do sistema
EMBLEMAS = {
    "escudo": '<path d="M0,-34 L28,-22 C28,4 16,26 0,34 C-16,26 -28,4 -28,-22 Z" '
              'fill="none" stroke="{cor}" stroke-width="3"/>'
              '<path d="M0,-18 L0,18 M-14,0 L14,0" stroke="{cor}" stroke-width="3"/>',
    "arvore": '<path d="M0,-34 L22,-4 L12,-4 L30,22 L-30,22 L-12,-4 L-22,-4 Z" '
              'fill="none" stroke="{cor}" stroke-width="3"/>'
              '<path d="M0,22 L0,34" stroke="{cor}" stroke-width="4"/>',
    "play":   '<circle r="30" fill="none" stroke="{cor}" stroke-width="3"/>'
              '<path d="M-9,-15 L18,0 L-9,15 Z" fill="{cor}"/>',
}

CARTAS = [
    {
        "arquivo": "carta-guilda.svg",
        "nome": ["GUILDA DA", "CORRUPÇÃO"],
        "custo": "2026",
        "emblema": "escudo",
        "tipo": "Roguelike de cartas",
        "regra": ["Heróis morrem para sempre.", "A guilda vai cair — a questão", "é quão longe você chega."],
        "rodape": "Unity · C#",
        "selo": "EM OBRA",
    },
    {
        "arquivo": "carta-grito.svg",
        "nome": ["O GRITO", "DA MATA"],
        "custo": "2025",
        "emblema": "arvore",
        "tipo": "Roguelike procedural",
        "regra": ["Mapas gerados por grafos.", "Cada partida desenha", "um labirinto novo."],
        "rodape": "Unity · C#",
        "selo": "FINALIZADO",
    },
    {
        "arquivo": "carta-filmerama.svg",
        "nome": ["FILMERAMA"],
        "custo": "2026",
        "emblema": "play",
        "tipo": "Plataforma de streaming",
        "regra": ["No ar em filmerama.com,", "distribuindo o que o estúdio", "produz."],
        "rodape": "React · Node",
        "selo": "NO AR",
    },
]


# Posições fixas. Antes o layout descia junto com o título, então carta de
# duas linhas empurrava a linha de tipo por cima do texto de regra.
TITULO = {1: [95], 2: [83, 106]}
ARTE_Y, ARTE_H = 118, 78
TIPO_Y, REGRA_Y, RODAPE_Y = 218, 246, 316


def desenha(c: dict) -> str:
    bases = TITULO[len(c["nome"])]
    nome = "".join(
        f'<text x="{L/2}" y="{y}" fill="{TINTA}" font-size="18" font-weight="700" '
        f'text-anchor="middle" letter-spacing="1">{linha}</text>'
        for linha, y in zip(c["nome"], bases)
    )
    regra = "".join(
        f'<text x="20" y="{REGRA_Y + i*17}" fill="{BRUMA}" font-size="11">{linha}</text>'
        for i, linha in enumerate(c["regra"])
    )
    emblema = EMBLEMAS[c["emblema"]].format(cor=CLARO)

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {A}" width="{L}" height="{A}"
     role="img" aria-label="{' '.join(c['nome'])} — {c['tipo']}. {' '.join(c['regra'])}">
  <title>{' '.join(c['nome'])}</title>
  <defs>
    <clipPath id="borda"><rect width="{L}" height="{A}" rx="14"/></clipPath>
    <linearGradient id="brilho" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#fff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#fff" stop-opacity="0.10"/>
      <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <g clip-path="url(#borda)">
    <rect width="{L}" height="{A}" fill="#050505"/>
    <rect x="8" y="8" width="{L-16}" height="{A-16}" rx="10" fill="#000"
          stroke="{VERDE}" stroke-opacity="0.45"/>

    <circle cx="32" cy="34" r="15" fill="{ESCURO}" stroke="{VERDE}" stroke-opacity="0.6"/>
    <text x="32" y="38" fill="{CLARO}" font-size="10" font-weight="700"
          text-anchor="middle" font-family="ui-monospace, monospace">{c['custo']}</text>
    <text x="{L-20}" y="38" fill="{VERDE}" font-size="8" text-anchor="end"
          letter-spacing="2" font-family="ui-monospace, monospace">{c['selo']}</text>

    <g font-family="'Segoe UI', Ubuntu, Helvetica, Arial, sans-serif">{nome}</g>

    <rect x="20" y="{ARTE_Y}" width="{L-40}" height="{ARTE_H}" rx="8"
          fill="{ESCURO}" fill-opacity="0.35" stroke="{VERDE}" stroke-opacity="0.25"/>
    <g transform="translate({L/2}, {ARTE_Y + ARTE_H/2}) scale(0.82)">{emblema}</g>

    <text x="20" y="{TIPO_Y}" fill="{CLARO}" font-size="11" font-weight="600"
          font-family="'Segoe UI', Ubuntu, Helvetica, Arial, sans-serif">{c['tipo']}</text>
    <line x1="20" y1="{TIPO_Y + 9}" x2="{L-20}" y2="{TIPO_Y + 9}"
          stroke="{VERDE}" stroke-opacity="0.3"/>

    <g font-family="'Segoe UI', Ubuntu, Helvetica, Arial, sans-serif">{regra}</g>

    <line x1="20" y1="{RODAPE_Y - 20}" x2="{L-20}" y2="{RODAPE_Y - 20}"
          stroke="{VERDE}" stroke-opacity="0.3"/>
    <text x="20" y="{RODAPE_Y}" fill="{BRUMA}" font-size="11"
          font-family="ui-monospace, monospace">{c['rodape']}</text>

    <rect x="-90" y="0" width="70" height="{A}" fill="url(#brilho)" transform="skewX(-14)">
      <animate attributeName="x" values="-90;-90;{L+40};{L+40}"
               keyTimes="0;0.55;0.75;1" dur="6s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>
'''


for c in CARTAS:
    (RAIZ / c["arquivo"]).write_text(desenha(c), encoding="utf-8")
    print("escrita:", c["arquivo"])

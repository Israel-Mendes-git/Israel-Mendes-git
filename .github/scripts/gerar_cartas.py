"""Desenha os projetos como cartas de jogo em SVG.

Uma carta por arquivo, porque SVG servido dentro de <img> não carrega link
interno: para cada carta ser clicável ela precisa ser um arquivo, envolvido
por um <a> no README.

Cada carta tem a cor do seu projeto e moldura ornamentada — cantoneiras,
borda dupla e hachura de fundo. Acrescentar projeto é editar CARTAS.

Uso:  python .github/scripts/gerar_cartas.py
"""
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]
L, A = 240, 336  # 5:7, proporção de carta

TINTA, BRUMA = "#f0ece4", "#9d968c"

# Posições fixas: se o layout descesse junto com o título, carta de duas
# linhas jogaria a linha de tipo por cima do texto de regra.
TITULO = {1: [97], 2: [85, 108]}
ARTE_Y, ARTE_H = 120, 76
TIPO_Y, REGRA_Y, RODAPE_Y = 218, 246, 316

EMBLEMAS = {
    "escudo": '<path d="M0,-32 L26,-21 C26,3 15,24 0,32 C-15,24 -26,3 -26,-21 Z"/>'
              '<path d="M0,-16 L0,16 M-13,0 L13,0"/>',
    "arvore": '<path d="M0,-32 L20,-5 L11,-5 L27,20 L-27,20 L-11,-5 L-20,-5 Z"/>'
              '<path d="M0,20 L0,31"/>',
    "play":   '<circle r="27"/><path d="M-8,-13 L16,0 L-8,13 Z" class="cheio"/>',
    "atomo":  '<circle r="6" class="cheio"/><ellipse rx="28" ry="11"/>'
              '<ellipse rx="28" ry="11" transform="rotate(60)"/>'
              '<ellipse rx="28" ry="11" transform="rotate(-60)"/>',
    "balao":  '<path d="M-26,-20 H26 A5,5 0 0 1 31,-15 V10 A5,5 0 0 1 26,15 H-6 L-18,27 V15 H-26'
              ' A5,5 0 0 1 -31,10 V-15 A5,5 0 0 1 -26,-20 Z"/>'
              '<path d="M-16,-6 H12 M-16,4 H4"/>',
    "quadro": '<rect x="-30" y="-24" width="60" height="48" rx="4"/>'
              '<path d="M-10,-24 V24 M10,-24 V24"/>'
              '<rect x="-26" y="-18" width="12" height="9" class="cheio"/>'
              '<rect x="-6" y="-18" width="12" height="14" class="cheio"/>'
              '<rect x="14" y="-18" width="12" height="6" class="cheio"/>',
}

CARTAS = [
    {
        "arquivo": "carta-guilda.svg",
        "url": "https://github.com/Israel-Mendes-git/Guilda-da-Corrupcao",
        "nome": ["GUILDA DA", "CORRUPÇÃO"],
        "ano": "2026", "selo": "EM OBRA", "emblema": "escudo",
        "cor": "#d99a3c", "fundo": "#1a1208",
        "tipo": "Roguelike de cartas",
        "regra": ["Heróis morrem para sempre.", "A guilda vai cair — a questão", "é quão longe você chega."],
        "rodape": "Unity · C#",
    },
    {
        "arquivo": "carta-grito.svg",
        "url": "https://github.com/Israel-Mendes-git/Roguelike",
        "nome": ["O GRITO", "DA MATA"],
        "ano": "2025", "selo": "FINALIZADO", "emblema": "arvore",
        "cor": "#5fae52", "fundo": "#0c1a0c",
        "tipo": "Roguelike procedural",
        "regra": ["Mapas gerados por grafos.", "Cada partida desenha", "um labirinto novo."],
        "rodape": "Unity · C#",
    },
    {
        "arquivo": "carta-filmerama.svg",
        "url": "https://github.com/Israel-Mendes-git/Rapadura_filmes",
        "nome": ["FILMERAMA"],
        "ano": "2026", "selo": "NO AR", "emblema": "play",
        "cor": "#9b6bd6", "fundo": "#150e1f",
        "tipo": "Plataforma de streaming",
        "regra": ["No ar em filmerama.com,", "distribuindo o que o estúdio", "produz."],
        "rodape": "React · Node",
    },
    {
        "arquivo": "carta-nuclear.svg",
        "url": "https://github.com/Rapadura-Atomica/Nuclear",
        "nome": ["NUCLEAR"],
        "ano": "2026", "selo": "NO AR", "emblema": "atomo",
        "cor": "#3fb5ab", "fundo": "#08191a",
        "tipo": "Software de animação",
        "regra": ["Fork do Blender que anima", "as séries do estúdio.", "Sou o segundo dev."],
        "rodape": "C++ · Blender",
    },
    {
        "arquivo": "carta-dizido.svg",
        "url": "https://github.com/Israel-Mendes-git/Dizido",
        "nome": ["DIZIDO"],
        "ano": "2026", "selo": "EM OBRA", "emblema": "balao",
        "cor": "#7b7bdd", "fundo": "#0e0e1f",
        "tipo": "Chat de equipe",
        "regra": ["O que foi decidido não", "se perde no meio do", "histórico."],
        "rodape": ".NET · Blazor",
    },
    {
        "arquivo": "carta-kanban.svg",
        "url": "https://github.com/Israel-Mendes-git/Uikanban",
        "nome": ["UI KANBAN"],
        "ano": "2026", "selo": "NO AR", "emblema": "quadro",
        "cor": "#4a94d8", "fundo": "#08131f",
        "tipo": "Ferramenta interna",
        "regra": ["O quadro da equipe numa", "TV da sala de produção,", "com burndown."],
        "rodape": "Kotlin · Compose",
    },
]


def cantoneira(x, y, sx, sy, cor):
    """L de canto, espelhado pelos sinais de sx/sy."""
    return (
        f'<path d="M{x},{y + 14 * sy} L{x},{y} L{x + 14 * sx},{y}" '
        f'fill="none" stroke="{cor}" stroke-width="2" stroke-opacity="0.85"/>'
    )


def desenha(c: dict) -> str:
    cor, fundo = c["cor"], c["fundo"]
    bases = TITULO[len(c["nome"])]

    nome = "".join(
        f'<text x="{L/2}" y="{y}" fill="{TINTA}" font-size="18" font-weight="700" '
        f'text-anchor="middle" letter-spacing="1.5">{linha}</text>'
        for linha, y in zip(c["nome"], bases)
    )
    regra = "".join(
        f'<text x="22" y="{REGRA_Y + i*17}" fill="{BRUMA}" font-size="11">{linha}</text>'
        for i, linha in enumerate(c["regra"])
    )
    cantos = "".join(
        cantoneira(x, y, sx, sy, cor)
        for x, y, sx, sy in ((16, 16, 1, 1), (L - 16, 16, -1, 1), (16, A - 16, 1, -1), (L - 16, A - 16, -1, -1))
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {A}" width="{L}" height="{A}"
     role="img" aria-label="{' '.join(c['nome'])} — {c['tipo']}. {' '.join(c['regra'])}">
  <title>{' '.join(c['nome'])}</title>
  <defs>
    <clipPath id="corte"><rect width="{L}" height="{A}" rx="14"/></clipPath>
    <pattern id="hachura" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <line x1="0" y1="0" x2="0" y2="6" stroke="{cor}" stroke-width="1" stroke-opacity="0.10"/>
    </pattern>
    <radialGradient id="halo" cx="50%" cy="38%" r="60%">
      <stop offset="0%" stop-color="{cor}" stop-opacity="0.22"/>
      <stop offset="100%" stop-color="{cor}" stop-opacity="0"/>
    </radialGradient>
    <linearGradient id="brilho" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#fff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#fff" stop-opacity="0.13"/>
      <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <style>
      .emblema {{ fill: none; stroke: {cor}; stroke-width: 2.6; stroke-linejoin: round; }}
      .emblema .cheio {{ fill: {cor}; stroke: none; }}
      .rotulo {{ font-family: ui-monospace, "DejaVu Sans Mono", Consolas, monospace; }}
      .texto  {{ font-family: "Segoe UI", Ubuntu, Helvetica, Arial, sans-serif; }}
    </style>
  </defs>

  <g clip-path="url(#corte)">
    <rect width="{L}" height="{A}" fill="{fundo}"/>
    <rect width="{L}" height="{A}" fill="url(#hachura)"/>
    <rect width="{L}" height="{A}" fill="url(#halo)"/>

    <!-- borda dupla + cantoneiras -->
    <rect x="7" y="7" width="{L-14}" height="{A-14}" rx="11" fill="none"
          stroke="{cor}" stroke-opacity="0.55" stroke-width="2"/>
    <rect x="12" y="12" width="{L-24}" height="{A-24}" rx="8" fill="none"
          stroke="{cor}" stroke-opacity="0.22"/>
    {cantos}

    <!-- ano e selo -->
    <circle cx="36" cy="38" r="14" fill="{fundo}" stroke="{cor}" stroke-opacity="0.7"/>
    <text x="36" y="42" fill="{cor}" font-size="10" font-weight="700"
          text-anchor="middle" class="rotulo">{c['ano']}</text>
    <text x="{L-24}" y="42" fill="{cor}" font-size="8" text-anchor="end"
          letter-spacing="2" class="rotulo">{c['selo']}</text>

    <g class="texto">{nome}</g>

    <!-- quadro de arte, com o canto cortado -->
    <path d="M22,{ARTE_Y} H{L-32} L{L-22},{ARTE_Y+10} V{ARTE_Y+ARTE_H} H32 L22,{ARTE_Y+ARTE_H-10} Z"
          fill="{cor}" fill-opacity="0.07" stroke="{cor}" stroke-opacity="0.35"/>
    <g class="emblema" transform="translate({L/2}, {ARTE_Y + ARTE_H/2}) scale(0.78)">{EMBLEMAS[c['emblema']]}</g>

    <!-- linha de tipo, com regra dupla -->
    <text x="22" y="{TIPO_Y}" fill="{cor}" font-size="11" font-weight="600" class="texto">{c['tipo']}</text>
    <line x1="22" y1="{TIPO_Y + 8}" x2="{L-22}" y2="{TIPO_Y + 8}" stroke="{cor}" stroke-opacity="0.45"/>
    <line x1="22" y1="{TIPO_Y + 11}" x2="{L-22}" y2="{TIPO_Y + 11}" stroke="{cor}" stroke-opacity="0.18"/>

    <g class="texto">{regra}</g>

    <line x1="22" y1="{RODAPE_Y - 20}" x2="{L-22}" y2="{RODAPE_Y - 20}" stroke="{cor}" stroke-opacity="0.35"/>
    <text x="22" y="{RODAPE_Y}" fill="{BRUMA}" font-size="11" class="rotulo">{c['rodape']}</text>

    <!-- brilho atravessando, com espera longa entre as passadas -->
    <rect x="-90" y="0" width="70" height="{A}" fill="url(#brilho)" transform="skewX(-14)">
      <animate attributeName="x" values="-90;-90;{L+40};{L+40}"
               keyTimes="0;0.55;0.75;1" dur="7s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>
'''


if __name__ == "__main__":
    for c in CARTAS:
        (RAIZ / c["arquivo"]).write_text(desenha(c), encoding="utf-8")
        print("escrita:", c["arquivo"])

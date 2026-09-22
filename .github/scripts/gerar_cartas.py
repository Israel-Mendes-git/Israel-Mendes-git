"""Desenha os projetos como cartas em pixel art.

Uma carta por arquivo, porque SVG servido dentro de <img> não carrega link
interno: para cada carta ser clicável ela precisa ser um arquivo, envolvido
por um <a> no README.

Tudo é retângulo — título, sprite e moldura. Nenhuma curva, nenhuma fonte
externa, nada de anti-serrilhado. Acrescentar projeto é editar CARTAS.

Uso:  python .github/scripts/gerar_cartas.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from pixelfonte import largura_texto, sprite_svg, texto_svg  # noqa: E402

RAIZ = pathlib.Path(__file__).resolve().parents[2]

PX = 4  # lado do pixel da moldura
L, A = 240, 336  # 5:7, proporção de carta
TINTA, BRUMA = "#f0ece4", "#8d867c"

CARTAS = [
    {
        "arquivo": "carta-guilda.svg",
        "url": "https://github.com/Israel-Mendes-git/Guilda-da-Corrupcao",
        "nome": ["GUILDA DA", "CORRUPÇÃO"],
        "ano": "2026", "selo": "EM OBRA", "sprite": "escudo",
        "cor": "#e8a83e", "escura": "#6b4a12", "fundo": "#1a1206",
        "tipo": "DECKBUILDER",
        "regra": ["Heróis morrem para sempre.", "A guilda vai cair — a questão", "é quão longe você chega."],
        "rodape": "UNITY + C#",
    },
    {
        "arquivo": "carta-grito.svg",
        "url": "https://github.com/Israel-Mendes-git/Roguelike",
        "nome": ["O GRITO", "DA MATA"],
        "ano": "2025", "selo": "FINALIZADO", "sprite": "arvore",
        "cor": "#63c455", "escura": "#1d4a18", "fundo": "#0a180a",
        "tipo": "ROGUELIKE",
        "regra": ["Mapas gerados por grafos.", "Cada partida desenha", "um labirinto novo."],
        "rodape": "UNITY + C#",
    },
    {
        "arquivo": "carta-filmerama.svg",
        "url": "https://github.com/Israel-Mendes-git/Rapadura_filmes",
        "nome": ["FILMERAMA"],
        "ano": "2026", "selo": "NO AR", "sprite": "play",
        "cor": "#a674e8", "escura": "#40276b", "fundo": "#140d1f",
        "tipo": "STREAMING",
        "regra": ["No ar em filmerama.com,", "distribuindo o que o estúdio", "produz."],
        "rodape": "REACT + NODE",
    },
    {
        "arquivo": "carta-nuclear.svg",
        "url": "https://github.com/Rapadura-Atomica/Nuclear",
        "nome": ["NUCLEAR"],
        "ano": "2026", "selo": "NO AR", "sprite": "atomo",
        "cor": "#3fc7bb", "escura": "#12514c", "fundo": "#07191a",
        "tipo": "ANIMAÇÃO 2D",
        "regra": ["Fork do Blender que anima", "as séries do estúdio.", "Sou o segundo dev."],
        "rodape": "C++ + BLENDER",
    },
    {
        "arquivo": "carta-dizido.svg",
        "url": "https://github.com/Israel-Mendes-git/Dizido",
        "nome": ["DIZIDO"],
        "ano": "2026", "selo": "EM OBRA", "sprite": "balao",
        "cor": "#8a8aee", "escura": "#33336b", "fundo": "#0d0d1e",
        "tipo": "CHAT DE EQUIPE",
        "regra": ["O que foi decidido não", "se perde no meio do", "histórico."],
        "rodape": ".NET + BLAZOR",
    },
    {
        "arquivo": "carta-kanban.svg",
        "url": "https://github.com/Israel-Mendes-git/Uikanban",
        "nome": ["UI KANBAN"],
        "ano": "2026", "selo": "NO AR", "sprite": "quadro",
        "cor": "#4fa2ec", "escura": "#153f66", "fundo": "#07121f",
        "tipo": "FERRAMENTA",
        "regra": ["O quadro da equipe numa", "TV da sala de produção,", "com burndown."],
        "rodape": "KOTLIN + COMPOSE",
    },
]


def chanfro():
    """Canto cortado em degraus de um pixel — chanfro liso entregaria a curva."""
    p, l, a = PX, L, A
    return (
        f"M{2*p},0 H{l-2*p} V{p} H{l-p} V{2*p} H{l} "
        f"V{a-2*p} H{l-p} V{a-p} H{l-2*p} V{a} "
        f"H{2*p} V{a-p} H{p} V{a-2*p} H0 "
        f"V{2*p} H{p} V{p} H{2*p} Z"
    )


def desenha(c: dict) -> str:
    cor, escura, fundo = c["cor"], c["escura"], c["fundo"]

    # Título: uma ou duas linhas, centralizado, 3px por pixel.
    topo = 44 if len(c["nome"]) == 2 else 62
    titulo = "".join(
        texto_svg(linha, 0, topo + i * 40, 3, TINTA, centro_em=L / 2)
        for i, linha in enumerate(c["nome"])
    )

    arte_y = 126
    sprite = sprite_svg(c["sprite"], int(L / 2 - 6 * 5), arte_y + 6, 5, cor)

    regra = "".join(
        f'<text x="20" y="{248 + i*15}" fill="{BRUMA}" font-size="10.5" class="m">{linha}</text>'
        for i, linha in enumerate(c["regra"])
    )

    # Borda em blocos: dois anéis de 1 pixel, o de fora aceso.
    p = PX
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {L} {A}" width="{L}" height="{A}"
     shape-rendering="crispEdges" role="img"
     aria-label="{' '.join(c['nome'])} — {c['tipo'].title()}. {' '.join(c['regra'])}">
  <title>{' '.join(c['nome'])}</title>
  <defs>
    <clipPath id="corte"><path d="{chanfro()}"/></clipPath>
    <pattern id="tramado" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="2" height="2" fill="{cor}" fill-opacity="0.07"/>
      <rect x="2" y="2" width="2" height="2" fill="{cor}" fill-opacity="0.07"/>
    </pattern>
    <style>
      .m {{ font-family: ui-monospace, "DejaVu Sans Mono", Consolas, monospace; }}
    </style>
  </defs>

  <g clip-path="url(#corte)">
    <rect width="{L}" height="{A}" fill="{fundo}"/>
    <path d="{chanfro()}" fill="none" stroke="{cor}" stroke-width="{2*p}"/>
    <rect x="{2*p}" y="{2*p}" width="{L-4*p}" height="{A-4*p}" fill="none"
          stroke="{escura}" stroke-width="{p}"/>

    <!-- barra de cabeçalho -->
    <rect x="{2*p}" y="{2*p}" width="{L-4*p}" height="{7*p}" fill="{escura}"/>
    {texto_svg(c['ano'], 3*p + 2, 2*p + 4, 2, cor)}
    {texto_svg(c['selo'], L - 3*p - largura_texto(c['selo'], 2), 2*p + 4, 2, TINTA)}

    <g>{titulo}</g>

    <!-- quadro de arte, tramado por dentro -->
    <rect x="20" y="{arte_y}" width="{L-40}" height="72" fill="{escura}" fill-opacity="0.55"/>
    <rect x="20" y="{arte_y}" width="{L-40}" height="72" fill="url(#tramado)"/>
    <rect x="20" y="{arte_y}" width="{L-40}" height="72" fill="none" stroke="{cor}" stroke-width="{p/2}"/>
    {sprite}

    {texto_svg(c['tipo'], 20, 206, 2, cor)}

    <g>{regra}</g>

    <rect x="20" y="{A-48}" width="{L-40}" height="{p/2}" fill="{escura}"/>
    {texto_svg(c['rodape'], 20, A - 42, 2, BRUMA)}
  </g>
</svg>
'''


if __name__ == "__main__":
    for c in CARTAS:
        (RAIZ / c["arquivo"]).write_text(desenha(c), encoding="utf-8")
        print("escrita:", c["arquivo"])

"""Sorteia a mão de cartas do dia e escreve no README.

O baralho tem mais cartas do que cabem na tela, então a Action tira três por
dia. Quem volta ao perfil vê projetos diferentes, e os menos badalados
aparecem em vez de ficar sempre atrás dos mesmos três.

O sorteio usa a data como semente: dentro do mesmo dia o resultado é sempre o
mesmo, então rodar a Action duas vezes não gera commit à toa.

Uso:  python .github/scripts/baralho.py
"""
import pathlib
import random
import sys
from datetime import date

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gerar_cartas import CARTAS  # noqa: E402

NA_MAO = 3
INICIO, FIM = "<!-- BARALHO:INICIO -->", "<!-- BARALHO:FIM -->"
README = pathlib.Path(__file__).resolve().parents[2] / "README.md"


def mao_do_dia():
    sorteio = random.Random(date.today().toordinal())
    return sorteio.sample(CARTAS, min(NA_MAO, len(CARTAS)))


def montar() -> str:
    cartas = "\n".join(
        f'  <a href="{c["url"]}" title="{" ".join(c["nome"])}">'
        f'<img src="{c["arquivo"]}" width="31%" alt="{" ".join(c["nome"])} — {c["tipo"]}" /></a>'
        for c in mao_do_dia()
    )
    return f'<div align="center">\n{cartas}\n</div>'


texto = README.read_text(encoding="utf-8")
i, f = texto.index(INICIO) + len(INICIO), texto.index(FIM)
novo = texto[:i] + "\n" + montar() + "\n" + texto[f:]

if novo == texto:
    print("mão do dia sem mudança")
else:
    README.write_text(novo, encoding="utf-8")
    print("mão do dia:", ", ".join(" ".join(c["nome"]) for c in mao_do_dia()))

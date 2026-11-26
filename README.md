# stories-dradasmultas

Robô que monta e publica os stories diários do Instagram @dradasmultas.
**Guia de configuração em português simples: [GUIA.md](GUIA.md).**

| Arquivo | O que faz |
|---|---|
| `gerar_dia.py` | Busca notícias (Claude + busca na web), escreve a sequência do dia e desenha as artes |
| `arte_natural.py` | Desenha os stories com cara de celular (fontes livres, fotos do Unsplash) |
| `aprovacao.py` | Manda o lote para o Telegram e lê o "OK" |
| `publicar.py` | Publica pela API do Instagram o que está aprovado e na hora; anota em `registro.csv` |
| `conhecimento.md` | Única fonte de regras de trânsito que o robô pode afirmar |
| `fila.csv` | Fila: arquivo, data, hora, status, lote |
| `stories/destaques/` | Capas e sequências dos destaques (visual dos carrosséis) |
| `.github/workflows/` | Agendamentos: gerar (18:50 Cuiabá), publicar (a cada 30 min), renovar token (segunda) |

Testes (sem internet; Claude, Telegram e Meta simulados): `python3 -m unittest discover -s testes -v`
Conferir a fila sem publicar: `python3 publicar.py --teste`

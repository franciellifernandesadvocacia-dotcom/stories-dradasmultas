"""Estilo sóbrio (perfil @franciellifernandes.adv): foto escurecida em preto, sombra preta suave e
texto branco numa serifada clássica e fina (Cormorant Garamond), centralizado, sem caixas.
Inspirado nos stories de frase com café: calmo, elegante, orgânico."""
import os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

import arte_natural as A

W, H = A.W, A.H
BRANCO = (255, 255, 255)
CREME = (246, 236, 220)
DOURADO = (201, 164, 108)


def serif(tam, peso="Medium", italico=False):
    arq = "CormorantGaramond-Italic.ttf" if italico else "CormorantGaramond.ttf"
    f = ImageFont.truetype(os.path.join(A.AQUI, "fontes", arq), int(tam))
    f.set_variation_by_name(("%s Italic" % peso if peso != "Regular" else "Italic") if italico else peso)
    return f


def espacado(txt):
    return " ".join(txt.upper())


def foto_escura(nome, forca=0.5):
    """Foto em tela cheia, escurecida, com degradê preto em cima e embaixo (onde o Instagram põe os botões)."""
    if nome and nome.startswith("cor:"):
        return Image.new("RGB", (W, H), (14, 12, 11))
    ft = ImageOps.exif_transpose(Image.open(A.escolher_foto(nome or ""))).convert("RGB")
    ft = ImageOps.fit(ft, (W, H), centering=(0.5, 0.4))
    ft = ImageEnhance.Brightness(ft).enhance(forca)
    ft = ImageEnhance.Color(ft).enhance(0.85)
    grad = Image.new("L", (1, H))
    for y in range(H):
        t = y / H
        a = 170 * max(0, 1 - t / 0.22) + 200 * max(0, (t - 0.62) / 0.38)   # topo e base mais escuros
        grad.putpixel((0, y), int(min(230, a)))
    grad = grad.resize((W, H))
    return Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), ft, grad)


def texto_com_sombra(img, linhas, y, f, cor=BRANCO, entre=1.18, sombra=0.75):
    """Escreve linhas centralizadas com uma sombra preta difusa atrás (a 'sombra preta')."""
    asc, desc = f.getmetrics()
    passo = int((asc + desc) * entre)
    camada = Image.new("L", (W, H), 0)
    dc = ImageDraw.Draw(camada)
    for i, ln in enumerate(linhas):
        dc.text((W / 2, y + i * passo), ln, font=f, fill=255, anchor="ma")
    halo = camada.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(28))
    img.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), halo.point(lambda v: int(v * sombra)))
    d = ImageDraw.Draw(img)
    for i, ln in enumerate(linhas):
        d.text((W / 2, y + i * passo), ln, font=f, fill=cor, anchor="ma")
    return y + len(linhas) * passo


def assinatura(img):
    d = ImageDraw.Draw(img)
    logo = os.path.join(A.AQUI, "fontes", "simbolo-creme.png")
    y = A.BASE_SEGURA - 30
    if os.path.exists(logo):
        lg = Image.open(logo).convert("RGBA")
        lg.thumbnail((70, 70))
        img.paste(lg, (int(W / 2 - lg.width / 2), y - lg.height - 18), lg)
    d.text((W / 2, y), espacado(A.PERFIL["handle"].lstrip("@")), font=serif(24, "SemiBold"), fill=CREME, anchor="ma")


def rotulo(img, txt, y):
    if txt:
        d = ImageDraw.Draw(img)
        d.text((W / 2, y), espacado(txt), font=serif(28, "SemiBold"), fill=DOURADO, anchor="ma")
        d.line([(W / 2 - 40, y + 52), (W / 2 + 40, y + 52)], fill=DOURADO, width=2)


def posicao(alt):
    """Texto no terço de baixo (abaixo do rosto nas fotos), sem invadir a assinatura nem o topo."""
    y = int(H * 0.64 - alt / 2)
    return max(A.TOPO_SEGURO + 40, min(y, A.BASE_SEGURA - 230 - alt))


def desenhar(story, caminho):
    tipo = story.get("tipo", "dica")
    img = foto_escura(story.get("fundo", ""), 0.55 if tipo != "noticia" else 0.38)

    f_tit = serif(92, "Medium", italico=True)
    f_txt = serif(56, "Medium")
    largura = 860

    if tipo == "bom_dia":
        texto, ref = story["texto"], ""
        if " — " in texto:                       # versículo — referência
            texto, ref = texto.rsplit(" — ", 1)
        tl = A.quebrar(story.get("titulo") or "Bom dia", f_tit, largura)
        cl = A.quebrar(texto, f_txt, largura)
        alt = len(tl) * 110 + 50 + len(cl) * 66 + (70 if ref else 0)
        y = posicao(alt)
        y = texto_com_sombra(img, tl, y, f_tit, CREME) + 40
        y = texto_com_sombra(img, cl, y, f_txt)
        if ref:
            texto_com_sombra(img, [ref], y + 20, serif(40, "Medium", italico=True), DOURADO, sombra=0.6)
    else:
        rot = A.ROTULOS.get(tipo, "")
        if tipo == "noticia":
            rot = (story.get("fonte") or "notícia").split("·")[0].strip()
        tl = A.quebrar(story["titulo"], serif(80, "Medium", italico=True), largura)
        cl = A.quebrar(story["texto"], f_txt, largura)
        com = A.quebrar(story.get("comentario", ""), serif(48, "Medium", italico=True), largura - 60) if story.get("comentario") else []
        alt = ((100 if rot else 0) + len(tl) * 96 + 50 + len(cl) * 66 + (len(com) * 60 + 50 if com else 0)
               + (70 if tipo == "noticia" and story.get("fonte") else 0) + (80 if story.get("rodape") else 0))
        y = posicao(alt)
        if rot:
            rotulo(img, rot, y)
            y += 100
        y = texto_com_sombra(img, tl, y, serif(80, "Medium", italico=True), CREME) + 40
        y = texto_com_sombra(img, cl, y, f_txt)
        if tipo == "noticia" and story.get("fonte"):
            d = ImageDraw.Draw(img)
            d.text((W / 2, y + 20), story["fonte"], font=serif(32, "Medium", italico=True), fill=DOURADO, anchor="ma")
            y += 70
        if com:
            y = texto_com_sombra(img, com, y + 40, serif(48, "Medium", italico=True), CREME)
        if story.get("rodape"):
            texto_com_sombra(img, [story["rodape"]], y + 40, serif(38, "Medium", italico=True), DOURADO, sombra=0.6)
    assinatura(img)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    img.save(caminho, quality=88, optimize=True)
    return caminho

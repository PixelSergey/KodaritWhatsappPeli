import pygame
import sys
import random
from pygame.locals import *

# Alustaa pygamen
pygame.init()
pygame.font.init()
pygame.mixer.init()

koko = (400,600)  # Näytön koko on 1920x1080
ruutu = pygame.display.set_mode(koko)

# Lataus
pelaaja = pygame.image.load("auto.png")
este = pygame.image.load("juusto.png")
tausta = pygame.image.load("avaruus.png")

pelaaja = pygame.transform.scale(pelaaja, (42,64))
este = pygame.transform.scale(este, (32,32))
tausta = pygame.transform.scale(tausta, koko)

# Musa
pygame.mixer.music.load("burning_memory.mp3")
pygame.mixer.music.play(-1) # -1 on looppaus, 0 on vain kerran

vihellys = pygame.mixer.Sound("vihellys.mp3")
suru = pygame.mixer.Sound("sad.mp3")
wow = pygame.mixer.Sound("wow.mp3")


# Tekstit
pelifontti = pygame.font.SysFont("Algerian", 30)
loppufontti = pygame.font.SysFont("Impact", 40)
pelivari = (237,255,242)
loppuvari = (227,81,70)
voittovari = (143,255,135)

# Muuttujat
pelx = 200-32
pely = 500
pelnopeus = 7
vihunopeus = 5
hp = 5
on_tehty = False
ennatys = 0

vihut = [
    [100,100],
    [200,200],
    [300,300],
    [500,500],
    [100,400],
    ]

# Ennätyksen lukeminen
with open("ennatys","r") as tiedosto:
    luettu = tiedosto.read()
    ennatys = int(luettu)

# Aikajutut
kello = pygame.time.Clock()
FPS = 30
alkuaika = pygame.time.get_ticks()

# Käsittelee tapahtumia
def kasittelija():
    tapahtumat = pygame.event.get()
    for tapahtuma in tapahtumat:
        if tapahtuma.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


# Ohjaa pelaajia, vihollisia ja pistemäärää
def pelilogiikka():
    global pelx, pely, hp, ennatys, vihunopeus
    aika = pygame.time.get_ticks()-alkuaika

    # Pelaajan liikkuminen
    napit = pygame.key.get_pressed()
    if napit[pygame.K_d]:
        pelx += pelnopeus
    if napit[pygame.K_a]:
        pelx -= pelnopeus
    
    # Pysäytä pelaaja laitaan
    if pelx < 0:
        pelx = 0
    if pelx > 400-42:  # ruudun leveys miinus pelaajan leveys
        pelx = 400-42

    # Vihollisten kiihdyttäminen
    if (aika//1000) % 5 == 0: # onko jakojäännös nolla? tapahtuu joka 5 sekuntia
        vihunopeus += 0.05

    # Vihollisten liikkuminen
    for vihu in vihut:
        vihu[1] += vihunopeus
        if vihu[1] > 600:
            # Heittää viholliset ylös
            vihu[1] = -100
            vihu[0] = random.randint(10, 400-32-10) # mistä (vähäsen), mihin (leveys - vihun leveys - vähäsen)

    # Koskevatko viholliset pelaajaan?
    for vihu in vihut:
        if vihu[1]+32 > pely and vihu[1] < pely+64:  # 32 on vihun korkeus, 64 on pelaajan korkeus
            if vihu[0]+32 > pelx and vihu[0] < pelx+42:  # 32 on vihun leveys, 42 on pelaajan leveys
                # KOSKEE!
                vihellys.play()
                hp -= 1
                vihu[1] = -100
                vihu[0] = random.randint(10, 400-32-10)

    if aika > ennatys:
        ennatys = aika


# Piirtää asioita näytölle
def piirtaja():
    ruutu.blit(tausta, (0,0))  # Taustan piirto
    ruutu.blit(pelaaja, (pelx,pely))  # Pelaajan piirto

    # Vihollisten piirto
    for vihu in vihut:
        ruutu.blit(este, vihu)
    
    # Tekstin piirto
    hpteksti = pelifontti.render("Elämät: "+str(hp), True, pelivari)
    ruutu.blit(hpteksti, (30,30))

    aika = pygame.time.get_ticks()-alkuaika
    aikateksti = pelifontti.render("Aika: "+str(aika/1000), True, pelivari)
    ruutu.blit(aikateksti, (30,70))

    ennatysteksti = pelifontti.render("Ennätys: "+str(ennatys/1000), True, pelivari)
    ruutu.blit(ennatysteksti, (30,120))


# Häviö -näyttö
def gameover():
    global on_tehty

    # Tämä lohko suoriutuu vain kerran pelin loputtua
    if not on_tehty:
        on_tehty = True
        pygame.mixer.music.stop()  # Pysäytä musa
        suru.play()  # Soita loppuääni

        with open("ennatys","w") as tiedosto:
            tiedosto.write(str(ennatys))

    ruutu.fill(loppuvari) # Täyttö punaisella

    # Tekstin piirto
    teksti = loppufontti.render("WHATSAPP-AUTO", True, pelivari)
    ruutu.blit(teksti, (60,30))
    teksti = loppufontti.render("TÖRMÄSI JUUSTOON", True, pelivari)
    ruutu.blit(teksti, (50,70))
    teksti = loppufontti.render("BOTTOM TEXT", True, pelivari)
    ruutu.blit(teksti, (80,500))

    ennatysteksti = loppufontti.render("Ennätys: "+str(ennatys/1000), True, pelivari)
    ruutu.blit(ennatysteksti, (60,300))


# Voitto -näyttö
def voitto():
    global on_tehty

    # Tämä lohko suoriutuu vain kerran pelin loputtua
    if not on_tehty:
        on_tehty = True
        pygame.mixer.music.stop()  # Pysäytä musa
        wow.play()

        with open("ennatys","w") as tiedosto:
            tiedosto.write(str(ennatys))

    ruutu.fill(voittovari) # Täyttö vihreällä

    # Tekstin piirto
    teksti = loppufontti.render("WHATSAPP-AUTO", True, pelivari)
    ruutu.blit(teksti, (60,30))
    teksti = loppufontti.render("PYSYI ELOSSA", True, pelivari)
    ruutu.blit(teksti, (50,90))
    teksti = loppufontti.render("EPIC", True, pelivari)
    ruutu.blit(teksti, (100,550))


# Pelin silmukka
while True:
    kasittelija()
    aika = pygame.time.get_ticks()-alkuaika

    if hp <= 0:
        gameover()
    elif aika > 100000:
        voitto()
    else:
        pelilogiikka()
        piirtaja()

    pygame.display.flip()
    kello.tick(FPS)

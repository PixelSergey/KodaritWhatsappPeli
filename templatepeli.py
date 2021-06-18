import pygame
import sys
from pygame.locals import *

# Alustaa pygamen
pygame.init()

koko = (400,600)  # Ruudun koko on 1920x1080
ruutu = pygame.display.set_mode(koko)

taustavari = (82,32,12)
pallovari = (252,186,3)


# Käsittelee tapahtumia
def kasittelija():
    tapahtumat = pygame.event.get()
    for tapahtuma in tapahtumat:
        if tapahtuma.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


# Piirtää asioita näytölle
def piirtaja():
    napit = pygame.mouse.get_pressed()
    if not napit[0]:
        ruutu.fill(taustavari)
    paikka = pygame.mouse.get_pos()
    skoko = (5,5) 
    #pygame.draw.circle(ruutu, pallovari, paikka, 7)
    pygame.draw.rect(ruutu, pallovari, paikka+skoko)


# Pelin silmukka
while True:
    kasittelija()
    piirtaja()
    pygame.display.flip()
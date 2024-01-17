#Tervetuloa pelaamaan InsaneMoneyHoboRobo:ta pelin ideana on voittaa kapitalistiset rahaa ahmivat hirviöt kolikoikoiden keruussa
#Auta kadunmies robottia keräämään enemmän kolikoita.
#Näytetään kapitalisteille, että robotteja ohjaavat koodarit saavuttavat maailmanherruuden.

import pygame
from random import randint

#Robo, kolikko ja hirvio luokat esitellään ennen main-luokkaa, jotta niitä voidaan käyttää main-luokan. Tämä selkeyttää myös ohjelman laajentamista
#Tarkoitus on lisätä objektien toiminnallisuuksia jälkikäteen ja niiden käsittelyä metodien avulla. Koodia rakentaessa pyritty ajattelemaan myöhempää muokkaamista

class Robo:
    def __init__(self) -> None:
        self.robo = pygame.image.load("robo.png")
        self.x = 0
        self.y = 500 - self.robo.get_height()
        self.leveys = self.robo.get_width()
        self.korkeus = self.robo.get_height()

    def liikuta(self, suunta: str):
        #Tuodaan suunta parametri ja liikutetaan sen mukaan robottia
        if suunta == "vasen":
            self.x -= 2
        elif suunta == "oikea":
            self.x += 2
        elif suunta == "ylos":
            self.y -= 2
        elif suunta == "alas":
            self.y += 2

    
class Kolikko:
    def __init__(self) -> None:
        #Aloitetaan kolikon ilmestyminen y alempaa tekstien takia
        self.kolikko = pygame.image.load("kolikko.png")
        self.x = randint(0, 1000-self.kolikko.get_width())
        #Vähennetään y-koordinaatti max -35, jotta hirviot kattaa alueen
        self.y = randint(40, 500-self.kolikko.get_height()-35)
        #Vaikka kolikko on neliö, luodaan omat muuttujat korkeudelle ja leveydelle -> Jos muutetaan jälkikäteen kuvaa, ei koodi hajoa.
        self.leveys = self.kolikko.get_width()
        self.korkeus = self.kolikko.get_height()

class Hirvio:
    def __init__(self, x: int, y: int) -> None:
        self.hirvio = pygame.image.load("hirvio.png")
        self.x = x
        self.y = y
        self.vx = 2
        self.leveys = self.hirvio.get_width()
        self.korkeus = self.hirvio.get_height()

    def liikuta(self):
        if self.x + self.hirvio.get_width() == 1000:
            self.vx = -2
        elif self.x == 0:
            self.vx = 2
        self.x += self.vx

class InsaneMain:
    def __init__(self):
        #Alustetaan pygame
        pygame.init()
        pygame.display.set_caption("InsaneMoneyHoboRobo")
        #Alustetaan näyttö, kuvat ja fontti. Leveys/Korkeus omat muuttujat, jotta koodin muuttaminen jälkikäteen helpottuu.
        self.leveys = 1000
        self.korkeus = 500
        #Tehdään muuttujista suojattuja, niitä ei ole tarkoitussa muuttaa luokan ulkopuolelta. Korkeus ja leveys jätetään näkyviksi, sillä jatkossa niitä saatetaan haluta muuttaa
        self._naytto = pygame.display.set_mode((self.leveys, self.korkeus))
        self._kello = pygame.time.Clock()
        self.kuvat = {}
        self._pisteet = [0, 0]  

        self.__alusta_kuva_oliot()
        self.ohjelma()     

#Piilotetaan, mikään muu luokka tai asiakas ei tule tätä tarvitsemaan -> Luokkametodiksi? 
    def __alusta_kuva_oliot(self):
        #Otetaan jokaiselle liikkuvalle kuvalle oma luokkansa käyttöön, jotta niiden liikuttaminen koordinaatistossa helpottuu
        #Hirvioille luodaan lista, sillä niitä on useampi
        hirviot = []
        robo = Robo()
        kolikko = Kolikko()
        #Tässä olisi voitu käyttää myös rekursiivista algoritmia, mutta en nähnyt sille tarvetta. Palaute on tervetullutta on toteutus hyvä, kiitos!
        for i in range(5):
            #Lisätään y-koordinaattiin , jotta saadaan pudotettua tekstin alapuolelle -> iteroitu, jotta voidaan luoda eri koordinaatteihin
            hirvio = Hirvio(i*200, 50+i*75)
            hirviot.append(hirvio)
        self.kuvat["hirvio"] = hirviot
        self.kuvat["robo"] = robo
        self.kuvat["kolikko"] = kolikko

    #Metodi tarkistamaan osuuko hirviö tai robo kolikkoon, hirviot olioina...kolikot ja muut myös, oikeat tiedot???
    def __osuiko(self, hirviot: list, robo: Robo, kolikko: Kolikko) -> bool:
#KORJATTU! -> Käytetty aiemmin suoria kokoja. Jos ajan kanssa tarkkaan koodaisin ohjelmaa en välttämättä tekisi näin, saattaa jatkossa aiheuttaa virheellisen toiminnallisuuden mikäli kuvien koko muuttuu 
#Koot: Kolikko K40 L40, Robo K86 L50, Hirvio K70 L50
        #Ehto, jos kolikko osuu roboon Käytetty suoraan kuvien kokoa koodin selkeyttämiseksi   
        if kolikko.x in range(robo.x - (kolikko.leveys + 1), robo.x + 50 + (kolikko.leveys-1)):
            if kolikko.y in range(robo.y - kolikko.korkeus-1, robo.y + robo.korkeus + kolikko.korkeus-1):
                self._pisteet[1] += 1
                return True
        for hirvio in hirviot:
            if kolikko.x in range(hirvio.x - (kolikko.leveys + 1), hirvio.x + hirvio.leveys + (kolikko.leveys-1)):
                if kolikko.y in range(hirvio.y - kolikko.korkeus-1, hirvio.y + hirvio.korkeus + kolikko.korkeus-1):
                    self._pisteet[0] += 1
                    return True
    #Metodi start menu:lle               
    def __alku__naytto(self):
        #Luodaan muuttuja värille joka toistuu useasti
        #Teksteille voidaan käyttää myös listaa, nyt sama asia kirjoitetaan useaan kertaan
#Kaikille fonteille, teksteille, väreille yms. oma luokka ja metodit -> Nyt toistetaan samoja asioita monessa paikkaa, ei järkevää, mahdollisesti olisi voinut käyttää sanakirjaa
        punainen = (255, 0, 0)
        violetti = (255, 0, 255)
        self._naytto.fill((64, 64, 64))
        fontti_otsikko = pygame.font.SysFont("calibri", 40)
        fontti_leipa = pygame.font.SysFont("calibri", 28)
        tervetulo_teksti = fontti_otsikko.render("Insane Money HoboRobo", True, punainen)
        ohjeet = fontti_leipa.render("Voita katalat kapitalisti hirviöt keräämällä 25 kolikkoa ensin.", True, punainen)
        liike_ohje = fontti_leipa.render("Robotti liikkuu nuoli näppäimillä.", True, punainen)
        aloita_teksti = fontti_leipa.render("Space - aloita peli", True, violetti)
        restart_teksti = fontti_leipa.render("F2 - aloittaa uudestaan pelin", True, violetti)
        #Piirretään reunaviiva visuaalisuuden selkeyttämiseksi ja luettavuudelle
        pygame.draw.rect(self._naytto, (255, 0, 0), pygame.Rect(2, 2, self.leveys-4, self.korkeus-4), 2)
        self._naytto.blit(tervetulo_teksti, (self.leveys/2 - tervetulo_teksti.get_width()/2, 30))
        self._naytto.blit(ohjeet, (self.leveys/2 - ohjeet.get_width()/2, 120))
        self._naytto.blit(liike_ohje, (self.leveys/2 - liike_ohje.get_width()/2, 160))
        self._naytto.blit(aloita_teksti, (self.leveys/2-restart_teksti.get_width()/2, 250))
        self._naytto.blit(restart_teksti, (self.leveys/2-restart_teksti.get_width()/2, 290))

        pygame.display.flip()
        self._kello.tick(15)

    def ohjelma(self):
        #Hirvio olio tuodaan ennen looppia, muuten se alustetaan aina loopissa, eikä tämä toimi
        hirviot = self.kuvat.get("hirvio")
        robo = self.kuvat.get("robo")
        kolikko = self.kuvat.get("kolikko")
        fontti = pygame.font.SysFont("calibri", 30)

        #Alustetaan muuttujat robo:n liikkumiseen
        vasen = False
        oikea = False
        ylos = False
        alas = False

        peli_tila = False
    
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    exit()

                if tapahtuma.type == pygame.KEYDOWN:     
                    if tapahtuma.key == pygame.K_LEFT:
                        vasen = True
                    if tapahtuma.key == pygame.K_RIGHT:
                        oikea = True
                    if tapahtuma.key == pygame.K_UP:
                        ylos = True
                    if tapahtuma.key == pygame.K_DOWN:
                        alas = True
                    if tapahtuma.key == pygame.K_SPACE:
                        peli_tila = True
                    if tapahtuma.key == pygame.K_F2:
                        self._pisteet = [0, 0]

                if tapahtuma.type == pygame.KEYUP:
                    if tapahtuma.key == pygame.K_LEFT:
                        vasen = False
                    if tapahtuma.key == pygame.K_RIGHT:
                        oikea = False
                    if tapahtuma.key == pygame.K_UP:
                        ylos = False
                    if tapahtuma.key == pygame.K_DOWN:
                        alas = False
            if not peli_tila:
                self.__alku__naytto()
            if peli_tila:
                if self._pisteet[0] < 25 and self._pisteet[1] < 25:
#Olisin halunnut tehdä jokaiselle peli tilalle kokonaan oman metodinsa, en saanut tätä kuitenkaan toimimaan. Hirviöiden liike ei toiminut, epäilen, että siksi koska metodia kutsutaan kerta toisensa jälkeen eikä looppia ole koordinaattien muuttamiseen. 
#Tämän olisi varmasti saanut ajan kanssa ratkaistua, tekemällä oma metodi koordinaattien muutokselle. Ajankäytön takia päädyin nyt tähän. Jatkossa kehitän tämän vielä pidemmälle.
#Saanen vielä huomauttaa, että lopussa kun näyttö vain piirretään uudelleen päälle, jäävät vanhat objektit taustalla. Tämä ei ole hyvä ratkaisu ja kasvattaa turhaan ohjelman vaatimia prosesseja. 
#Tässä mittakaavassa ero ei vielä ole merkittävä, mutta laajempaa kokonaisuutta käsiteltäessä on hyvä kiinnittää huomiota tämän tyyppisiin tekijöihin.
                    #Näytön taustaväri
                    self._naytto.fill((102, 153, 102))
                    #Kuvien liikkuminen
                    for hirvio in hirviot:
                        hirvio.liikuta()
                    if vasen:
                        robo.liikuta("vasen")
                    if oikea:
                        robo.liikuta("oikea")
                    if ylos:
                        robo.liikuta("ylos")
                    if alas:
                        robo.liikuta("alas")
                    #Alustetaan tekstit
                    hirvio__pisteet = fontti.render(f"Kapitalistit: {self._pisteet[0]}", True, (51, 0, 51))
                    robo__pisteet = fontti.render(f"Robotit: {self._pisteet[1]}", True, (51, 0, 51))
                    #Tuodaan kuvat
                    for hirvio in hirviot:
                        self._naytto.blit(hirvio.hirvio, (hirvio.x, hirvio.y))
                    self._naytto.blit(robo.robo, (robo.x, robo.y))
                    self._naytto.blit(kolikko.kolikko, (kolikko.x, kolikko.y))
                    #Piirretään tekstit
                    self._naytto.blit(hirvio__pisteet, (10, 10))
                    self._naytto.blit(robo__pisteet, (200, 10))
                    #Osuuko kolikko parametri: hirvio_x:int, hirvio_y:int, robo_x: int, robo_y:int, kolikko_X: int, kolikko_y: int
                    if self.__osuiko(hirviot, robo, kolikko):
                        kolikko = Kolikko()   
                elif self._pisteet[0] == 25:
#Tee tästä synkkä ja murheellinen -> Kolikoita pomppimaan pitkin ruutua -> Laajenna animaatio
                    self._naytto.fill((0, 0, 0))
                    hirviot_voitti = fontti.render("Kapitalisti hirviöt voittivat, robotit jatkavat vallankumouksen suunnittelua!", True, (0, 255, 255))
                    uusi_peli = fontti.render("F2 - Uusi peli", True, (0, 255, 255))
                    self._naytto.blit(hirviot_voitti, (self.leveys/2-hirviot_voitti.get_width()/2, self.korkeus/2-hirviot_voitti.get_height()/2-50))
                    self._naytto.blit(uusi_peli, (self.leveys/2-uusi_peli.get_width()/2, self.korkeus/2-uusi_peli.get_height()/2))
                elif self._pisteet[1] == 25:
#Lisää satavia robotteja ja jotain muuta kivaa -> Tähän tullaan laajentamaan animaatio
                    self._naytto.fill((0, 0, 0))
                    robotit_voitti = fontti.render("Robotit voittivat. Koodarit saavuttavat maailmanherruuden!", True, (0, 255, 255))
                    uusi_peli = fontti.render("F2 - Uusi peli", True, (0, 255, 255))
                    self._naytto.blit(robotit_voitti, (self.leveys/2-robotit_voitti.get_width()/2, self.korkeus/2-robotit_voitti.get_height()/2-50))
                    self._naytto.blit(uusi_peli, (self.leveys/2-uusi_peli.get_width()/2, self.korkeus/2-uusi_peli.get_height()/2))

                pygame.display.flip()
                self._kello.tick(60)

if __name__ == "__main__":
    InsaneMain()


#Yleisiä huomautuksia koodiin liittyen:
#Koodista puuttuu tällä hetkellä virheiden käsittely kokonaan, en kokenut tälläisenään niitä tarpeeliseksi sillä mikään ulkopuolinen tekijä ei vaikuta,
#eikä koodissa ole sen tyyppisiä iterointi tapauksia, jotka tämän vaatisivat. Koodin laajentuessa on hyvä kuitenkin pohtia, jos näitä tarvitaan.

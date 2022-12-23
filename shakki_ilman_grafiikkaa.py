"""
COMP.CS.100 Ohjelmointi 1
Nimi: Taneli Rikala

Ohjelman kuvaus: Ideani oli toteuttaa edistyneeksi käyttöliittymäksi
shakkilauta, joka rakentuu Tkinterin napeista. Ensimmäisen version (tämä
ohjelma) oli tarkoitus olla toimiva shakkilauta ilman kuvien käyttöä,
ja suunnittelin lisääväni palautukseen vielä omat grafiikkani. Tämän version
täyteen toimimiseen meni kuitenkin sen verran aikaa, että päätin palauttaa sen
tällaisenaan. Tein tämän ohjelman parissa suurinta osaa asioita ensimmäistä
kertaa, joten sitä ei ole optimoitu juurikaan.

Peli antaa tehdä vain säännöissä sallittuja siirtoja ja korostaa punaisella
shakissa olevan kuninkaan. Pelin voittaa konkreettisesti vain syömällä
kuninkaan. Pelin suorittaminen pyörii pääpiirteittäin suunnittelemassani
silmukassa:
- Valmistele pelilauta
    -> lisää tyhjät ruudut
    -> aseta nappulat oikeisiin ruutuihin
    -> jaa vuorot
- Vuoro
    -> deaktivoi vastustajan nappulat
    -> aktivoi omat nappulat
- Nappuloiden painelu
    -> poista aiemmin näytetyt siirtonapit
    -> lisää painettua nappulaa vastaavat siirtonapit
- Siirtonapin painallus
    -> poista näytetyt siirtonapit
    -> päivitä tietorakenteet oikein
    -> aseta lauta uudelleen
"""


from tkinter import *


# Globaalina muuttujana lista shakkilaudan koordinaattikirjaimista
KIRJAIMET = ["a", "b", "c", "d", "e", "f", "g", "h"]


class Shakkilauta:
    def __init__(self):
        """
        Keskittyy käyttöliittymän rakentamiseen.
        """

        # Pelin ulkoasun muokkaamisen pitäisi olla helppoa tästä
        ikkunan_taustavari = "#424242"
        # shakkilaudan ruudut
        self.__tumma_ruutu = "#66452d"
        self.__vaalea_ruutu = "#c9a565"
        # fontit
        ikkunan_fontti = "Kozuka Gothic Pro B", 18, "bold"
        ikkunan_fontin_vari = "#ffffff"
        self.__pelilaudan_fontti = "Kozuka Gothic Pro B", 12

        # Määritetään pääikkunä
        self.__paaikkuna = Tk()
        self.__paaikkuna.overrideredirect(True)
        self.__paaikkuna.configure(bg=ikkunan_taustavari, relief="solid")
        self.__paaikkuna.resizable(width=False, height=False)
        self.__paaikkuna.title("Shakkilauta")
        # Ideana asettaa ikkuna hieman koko näyttöä pienemmäksi
        # ja keskelle näyttöä
        self.__ruudun_koko = self.__paaikkuna.winfo_screenheight() // 10
        self.__maksimileveys_tekstille = self.__ruudun_koko // 8
        ikkunan_leveys = str(self.__ruudun_koko * 8)
        ikkunan_korkeus = str(self.__ruudun_koko * 9)
        leveyden_keskikohta = str(self.__paaikkuna.winfo_screenwidth()//2
                                  - int(ikkunan_leveys)//2)
        self.__paaikkuna.geometry(ikkunan_leveys+"x"+ikkunan_korkeus
                                  + "+"+leveyden_keskikohta+"+"+"0")

        # Luodaan käyttöliittymään pelin lisäksi muutama muu toiminto
        # Koko näytölle asettaminen
        self.__koko_naytto = Button(self.__paaikkuna,
                                    bg=ikkunan_taustavari,
                                    relief="flat", overrelief="flat",
                                    text="Koko näyttö",
                                    font=ikkunan_fontti,
                                    fg=ikkunan_fontin_vari,
                                    command=self.koko_naytto)
        self.__koko_naytto.grid(row=0, column=6, columnspan=2, sticky="nsew",
                                ipadx=0, ipady=0, padx=0, pady=0)
        # Sulkeminen
        self.__sulje = Button(self.__paaikkuna,
                              bg=ikkunan_taustavari,
                              relief="flat", overrelief="flat",
                              text="Sulje pelilauta",
                              font=ikkunan_fontti, fg=ikkunan_fontin_vari,
                              command=self.__paaikkuna.destroy)
        self.__sulje.grid(row=0, column=0, columnspan=2, sticky="nsew",
                          ipadx=0, ipady=0, padx=0, pady=0)
        # Tilanneteksti
        self.__siirtonro = 1
        self.__tilanneteksti = Label(self.__paaikkuna,
                                     bg=ikkunan_taustavari,
                                     text="Siirto " + str(self.__siirtonro),
                                     font=ikkunan_fontti,
                                     fg=ikkunan_fontin_vari)
        self.__tilanneteksti.grid(row=0, column=2, columnspan=4, sticky="nsew",
                                  ipadx=0, ipady=0, padx=0, pady=0)

        # Pidetään kirjaa laudan varatuista ruuduista
        # Valkoisen asemat
        self.__valkoisen_sotilaat = ["a2", "b2", "c2", "d2",
                                     "e2", "f2", "g2", "h2"]
        self.__valkoisen_tornit = ["a1", "h1"]
        self.__valkoisen_ratsut = ["b1", "g1"]
        self.__valkoisen_lahetit = ["c1", "f1"]
        self.__valkoisen_kuningatar = ["d1"]
        self.__valkoisen_kuningas = ["e1"]
        # Peilataan mustalle
        self.__mustan_sotilaat = ["a7", "b7", "c7", "d7",
                                  "e7", "f7", "g7", "h7"]
        self.__mustan_tornit = ["a8", "h8"]
        self.__mustan_ratsut = ["b8", "g8"]
        self.__mustan_lahetit = ["c8", "f8"]
        self.__mustan_kuningatar = ["d8"]
        self.__mustan_kuningas = ["e8"]

        # Castlingia eli linnoitusta varten on pidettävä lukua kaikesta tästä
        self.__valkoisen_vasen_torni_liikkunut = False
        self.__valkoisen_oikea_torni_liikkunut = False
        self.__valkoisen_kuningas_liikkunut = False
        self.__mustan_vasen_torni_liikkunut = False
        self.__mustan_oikea_torni_liikkunut = False
        self.__mustan_kuningas_liikkunut = False
        self.__linnoittaminen = False

        # Lisäksi näitä tarvitaan myöhemmin ohjelmassa
        self.__valkoisen_kuningas_shakissa = False
        self.__mustan_kuningas_shakissa = False
        self.__valkoisen_asemat = []
        self.__mustan_asemat = []

        # Nyt lisätään käyttöliittymään itse shakkilauta
        # Luodaan ensin laudan jokaista ruutua varten nappi-attribuutti
        self.__ruudut_nappeina = []
        # shakkilauta on 8x8, range(64) on numerot 0-63
        for numero in range(64):
            self.__ruudut_nappeina.append(Button(self.__paaikkuna,
                                                 relief="flat",
                                                 overrelief="flat"))

        # Lisätään laudan jokainen attribuutti taulukkoon
        # Haluan ensimmäisen attribuutin olevan shakkilaudan koordinaateissa
        # a1, toisen a2 jne.
        # Napit täytetään alhaalta ylöspäin (taulukon riveille 1-8) ja
        # vasemmalta oikealle (sarakkeisiin 0-7).
        indeksi = 0
        for sarake in range(0, 8):
            for rivi in range(8, 0, -1):
                self.__ruudut_nappeina[indeksi].grid(row=rivi, column=sarake,
                                                     sticky="nsew",
                                                     columnspan=1,
                                                     ipadx=0, ipady=0,
                                                     padx=0, pady=0)
                indeksi += 1
        # Tässä voidaan muotoilla koko taulukkoa vielä enemmän
        for sarake in range(0, 8):
            self.__paaikkuna.grid_columnconfigure(index=sarake, pad=0,
                                                  minsize=self.__ruudun_koko)
        for rivi in range(0, 9):
            self.__paaikkuna.grid_rowconfigure(index=rivi, pad=0,
                                               minsize=self.__ruudun_koko)
        self.__paaikkuna.grid_anchor("n")

        # Käynnistä ohjelma
        self.paivita_asemat()
        self.laudan_pohja()
        self.aseta_nappulat()
        self.kumman_vuoro()

    def paivita_asemat(self):
        """
        Päivittää valkoisten ja mustien nappuloiden sijaintien listat.
        """

        # Päivitetään asemat tietorakenteisiin
        self.__valkoisen_asemat = self.__valkoisen_sotilaat \
            + self.__valkoisen_tornit + self.__valkoisen_ratsut \
            + self.__valkoisen_lahetit + self.__valkoisen_kuningatar \
            + self.__valkoisen_kuningas
        self.__mustan_asemat = self.__mustan_sotilaat + self.__mustan_tornit \
            + self.__mustan_ratsut + self.__mustan_lahetit \
            + self.__mustan_kuningatar + self.__mustan_kuningas

    def laudan_pohja(self):
        """
        Tyhjentää laudan napit sekä asettaa ruuduille oikeat taustavärit.
        """
        # Koonfiguroidaan napit silmukkana
        ehto = 0
        for ruutu in self.__ruudut_nappeina:
            # Aloitetaan tyhjistä napeista
            ruutu.configure(text="", command=NONE, state=DISABLED)
            # joka toinen ruutu on tumma ja joka toinen vaalea
            if ehto % 2 == 0:
                taustavari = self.__tumma_ruutu
            else:
                taustavari = self.__vaalea_ruutu
            ruutu.configure(bg=taustavari, activebackground=taustavari)
            ehto += 1
            # 8. ja 9. ruutu halutaan samanvärisiksi, sitten 16. ja 17. jne.
            if ehto in range(8, 64, 9):
                ehto += 1

    def aseta_nappulat(self):
        """
        Lisää nappuloille siirtomahdollisuudet näyttävät ja siirtämisen
        mahdollistavat napit. Tarkkailee myös shakkia ja merkkaa shakitetun
        kuninkaan punaisella.
        """

        # Oletetaan, että kuninkaat eivät ole shakissa
        self.__mustan_kuningas_shakissa = False
        self.__valkoisen_kuningas_shakissa = False
        oikea_vari = "White"
        for ruutu in self.__valkoisen_asemat:
            if ruutu in self.__valkoisen_sotilaat:
                oikea_teksti = "Sotilas"
                siirrot = self.valkoisen_sotilaan_liike(ruutu)
                if self.__mustan_kuningas[0] in siirrot:
                    self.__mustan_kuningas_shakissa = True
            elif ruutu in self.__valkoisen_tornit:
                oikea_teksti = "Torni"
                siirrot = self.tornin_liike(ruutu)
                if self.__mustan_kuningas[0] in siirrot:
                    self.__mustan_kuningas_shakissa = True
            elif ruutu in self.__valkoisen_ratsut:
                oikea_teksti = "Ratsu"
                siirrot = self.ratsun_liike(ruutu)
                if self.__mustan_kuningas[0] in siirrot:
                    self.__mustan_kuningas_shakissa = True
            elif ruutu in self.__valkoisen_lahetit:
                oikea_teksti = "Lähetti"
                siirrot = self.lahetin_liike(ruutu)
                if self.__mustan_kuningas[0] in siirrot:
                    self.__mustan_kuningas_shakissa = True
            elif ruutu in self.__valkoisen_kuningatar:
                oikea_teksti = "Kuningatar"
                siirrot = self.tornin_liike(ruutu) + self.lahetin_liike(ruutu)
                if self.__mustan_kuningas[0] in siirrot:
                    self.__mustan_kuningas_shakissa = True
            else:
                oikea_teksti = "Kuningas"
                siirrot = self.kuninkaan_liike(ruutu)
                if self.__mustan_kuningas[0] in siirrot:
                    self.__mustan_kuningas_shakissa = True
            self.nappi_koordinaatille(ruutu).configure(
                font=self.__pelilaudan_fontti, text=oikea_teksti,
                fg=oikea_vari, disabledforeground=oikea_vari,
                activeforeground=oikea_vari,
                command=lambda tieto1=ruutu, tieto2=siirrot:
                self.nayta_siirrot(tieto1, tieto2))

        oikea_vari = "Black"
        for ruutu in self.__mustan_asemat:
            if ruutu in self.__mustan_sotilaat:
                oikea_teksti = "Sotilas"
                siirrot = self.mustan_sotilaan_liike(ruutu)
                if self.__valkoisen_kuningas[0] in siirrot:
                    self.__valkoisen_kuningas_shakissa = True
            elif ruutu in self.__mustan_tornit:
                oikea_teksti = "Torni"
                siirrot = self.tornin_liike(ruutu)
                if self.__valkoisen_kuningas[0] in siirrot:
                    self.__valkoisen_kuningas_shakissa = True
            elif ruutu in self.__mustan_ratsut:
                oikea_teksti = "Ratsu"
                siirrot = self.ratsun_liike(ruutu)
                if self.__valkoisen_kuningas[0] in siirrot:
                    self.__valkoisen_kuningas_shakissa = True
            elif ruutu in self.__mustan_lahetit:
                oikea_teksti = "Lähetti"
                siirrot = self.lahetin_liike(ruutu)
                if self.__valkoisen_kuningas[0] in siirrot:
                    self.__valkoisen_kuningas_shakissa = True
            elif ruutu in self.__mustan_kuningatar:
                oikea_teksti = "Kuningatar"
                siirrot = self.tornin_liike(ruutu) + self.lahetin_liike(ruutu)
                if self.__valkoisen_kuningas[0] in siirrot:
                    self.__valkoisen_kuningas_shakissa = True
            else:
                oikea_teksti = "Kuningas"
                siirrot = self.kuninkaan_liike(ruutu)
                if self.__valkoisen_kuningas[0] in siirrot:
                    self.__valkoisen_kuningas_shakissa = True
            # Itse nappien muuttaminen tapahtuu tässä
            self.nappi_koordinaatille(ruutu).configure(
                font=self.__pelilaudan_fontti, text=oikea_teksti,
                fg=oikea_vari, disabledforeground=oikea_vari,
                activeforeground=oikea_vari,
                command=lambda tieto1=ruutu, tieto2=siirrot:
                self.nayta_siirrot(tieto1, tieto2))

        # Merkataan shakissa oleva kuningas punaisella
        if self.__mustan_kuningas_shakissa:
            self.nappi_koordinaatille(
                self.__mustan_kuningas[0]).configure(bg="Red",
                                                     activebackground="Red")
        if self.__valkoisen_kuningas_shakissa:
            self.nappi_koordinaatille(
                self.__mustan_kuningas[0]).configure(bg="Red",
                                                     activebackground="Red")

    def kumman_vuoro(self):
        """
        Tarkistaa ensin, onko toinen voittanut. Jos ei, jakaa vuoron oikealle
        puolelle yksinkertaisesti laskurin parillisuuteen perustuen.
        """

        # Tarkistetaan voitto
        if not self.__valkoisen_kuningas:
            # Musta on voittanut pelin
            self.__tilanneteksti.configure(text="Peli on päättynyt, "
                                                "musta voitti!")
            return
        if not self.__mustan_kuningas:
            # Valkoinen on voittanut pelin
            self.__tilanneteksti.configure(text="Peli on päättynyt, valkoinen "
                                                "voitti!")
            return

        if self.__siirtonro % 2 == 1:
            oma_puoli, vast_puoli = self.__valkoisen_asemat, \
                                    self.__mustan_asemat
        else:
            vast_puoli, oma_puoli = self.__valkoisen_asemat, \
                                    self.__mustan_asemat
        self.deaktivoi_merkkijonolistan_napit(vast_puoli)
        self.aktivoi_merkkijonolistan_napit(oma_puoli)
        self.__siirtonro += 1

    def nayta_siirrot(self, lahtoasema, siirrot):
        """
        Tämä komento ajetaan pelilaudan nappulaa vastaavaa nappia painettaessa.
        Tyhjentää laudan vanhentuneista siirtonapeista ja lisää laudalle
        nappulan siirtämisen mahdollistavat siirtonapit.

        :param lahtoasema: str, painetun napin lähtökoordinaatit merkkijonona.
        :param siirrot: [str, ...]; lista nappulan mahdollisista siirroista
                        koordinaattien merkkijoina.
        """

        # Poistetaan vanhentuneet siirtonapit lataamalla lauta uudestaan
        oma_puoli, vast_puoli = self.kummat_puolet(lahtoasema)
        self.laudan_pohja()
        self.aseta_nappulat()
        self.aktivoi_merkkijonolistan_napit(oma_puoli)

        for ruutu in siirrot:
            self.nappi_koordinaatille(ruutu).configure(
                state=NORMAL, text="Siirto", fg="grey",
                font=self.__pelilaudan_fontti,
                activeforeground="grey",
                command=lambda tieto1=lahtoasema, tieto2=ruutu:
                self.tee_siirto(tieto1, tieto2))

    def tee_siirto(self, sijainti, siirto):
        """
        Tämä komento ajetaan siirtonappia painettaessa. Se poistaa ensin
        siirtonapit laudalta. Sitten se siirtää nappulan valittuun paikkaan
        päivittämällä tietolistat ja laudan.

        :param sijainti: str, siirrettävän nappulan koordinaatit merkkijonona.
        :param siirto: str, siirryttävän ruudun koordinaatit merkkijonona.
        """

        # Poistetaan siirtonapit laudalta
        for ruutu in shakkilaudan_koordinaatit():
            if ruutu not in (self.__valkoisen_asemat + self.__mustan_asemat):
                self.nappi_koordinaatille(ruutu).configure(state=DISABLED,
                                                           text="",
                                                           command=NONE)

        # Kerätään tarvittavat muuttujat
        oma_puoli, vast_puoli = self.kummat_puolet(sijainti)
        kategoria = self.etsi_nappulan_tyyppi(sijainti)
        indeksi = kategoria.index(sijainti)

        # Nappulan syöminen tapahtuu tässä
        if siirto in vast_puoli:
            self.etsi_nappulan_tyyppi(siirto).remove(siirto)
            self.nappi_koordinaatille(siirto).configure(state=DISABLED,
                                                        text="", command=NONE)
        # Poistetaan tiedoista nappulan sijaintiruutu ja lisätään sen
        # paikalle annettu siirtoruutu
        kategoria.pop(indeksi)
        kategoria.insert(indeksi, siirto)

        # Tarkkaillaan seuraavien nappuloiden liikkeitä linnoittamista varten:
        if sijainti == "a1":
            self.__valkoisen_vasen_torni_liikkunut = True
        if sijainti == "a8":
            self.__mustan_vasen_torni_liikkunut = True
        if sijainti == "h1":
            self.__valkoisen_oikea_torni_liikkunut = True
        if sijainti == "h8":
            self.__mustan_oikea_torni_liikkunut = True
        if sijainti == "e1":
            self.__valkoisen_kuningas_liikkunut = True
        if sijainti == "e8":
            self.__mustan_kuningas_liikkunut = True
        # Jos linnoittaminen tapahtuu
        if self.__linnoittaminen:
            if siirto == "c1":
                self.__valkoisen_tornit.remove("a1")
                self.__valkoisen_tornit.append("d1")
            if siirto == "g1":
                self.__valkoisen_tornit.remove("h1")
                self.__valkoisen_tornit.append("f1")
            if siirto == "c8":
                self.__mustan_tornit.remove("a8")
                self.__mustan_tornit.append("d8")
            if siirto == "g8":
                self.__mustan_tornit.remove("h8")
                self.__mustan_tornit.append("f8")

        # Kuningattareksi nousu sotilaalle laudan päädyssä
        if kategoria == self.__valkoisen_sotilaat and siirto in \
                ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]:
            self.__valkoisen_sotilaat.remove(siirto)
            self.__valkoisen_kuningatar.append(siirto)
        if kategoria == self.__mustan_sotilaat and siirto in \
                ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]:
            self.__mustan_sotilaat.remove(siirto)
            self.__mustan_kuningatar.append(siirto)

        # Päivitä lauta
        self.paivita_asemat()
        self.laudan_pohja()
        # Jos peli ei jatku, älä aseta nappuloita uudestaan
        if self.__mustan_kuningas and self.__valkoisen_kuningas:
            self.aseta_nappulat()
        self.kumman_vuoro()

    def aktivoi_merkkijonolistan_napit(self, merkkijonolista):
        """
        Apufunktio, joka pistää annetun merkkijonolistan koordinaattien
        mukaiset napit päälle.

        :param merkkijonolista: [str, ...]; lista ruutujen koordinaateista
                                merkkijonoina
        """

        for ruutu in merkkijonolista:
            self.nappi_koordinaatille(ruutu).configure(state=NORMAL)

    def deaktivoi_merkkijonolistan_napit(self, merkkijonolista):
        """
        Apufunktio, joka pistää annetun merkkijonolistan koordinaattien
        mukaiset napit pois päältä.

        :param merkkijonolista: [str, ...]; lista ruutujen koordinaateista
               merkkijonoina
        """

        for ruutu in merkkijonolista:
            self.nappi_koordinaatille(ruutu).configure(state=DISABLED)

    def nappi_koordinaatille(self, merkkijono):
        """
        Kenties tärkein apufunktio, joka parittaa ruudun koordinaattiin
        käyttöliittymässä koordinaattia vastaavassa paikassa sijaitsevan napin.

        :param merkkijono: str, ruudun koordinaatti merkkijonona
        :return: Button-tyyppinen attribuutti
        """

        ruudut_merkkijonoina = shakkilaudan_koordinaatit()
        # Luodaan lista laudan ruuduista merkkijonoina, samaan järjestykseen
        # kuin self.__ruudut_nappeina eli a1, a2, ..., a8, b1 jne.
        # otetaan etsityn merkkijonon indeksi
        indeksi = ruudut_merkkijonoina.index(merkkijono)
        # palautetaan indeksiä vastaava attribuutti
        return self.__ruudut_nappeina[indeksi]

    def etsi_nappulan_tyyppi(self, asema):
        """
        Apufunktio, joka tutkii ja palauttaa kategorian, johon <asema>:ssa eli
        laudan ruudussa oleva kuuluu.

        :param asema: str, laudan ruudun koordinaatit
        :return: [str, ...]; lista, jossa on tallennettuina kaikki kategoriaan
                             kuuluvien nappuloiden koordinaatit
        """

        if asema in self.__valkoisen_sotilaat:
            return self.__valkoisen_sotilaat
        if asema in self.__valkoisen_tornit:
            return self.__valkoisen_tornit
        if asema in self.__valkoisen_ratsut:
            return self.__valkoisen_ratsut
        if asema in self.__valkoisen_lahetit:
            return self.__valkoisen_lahetit
        if asema in self.__valkoisen_kuningatar:
            return self.__valkoisen_kuningatar
        if asema in self.__valkoisen_kuningas:
            return self.__valkoisen_kuningas
        if asema in self.__mustan_sotilaat:
            return self.__mustan_sotilaat
        if asema in self.__mustan_tornit:
            return self.__mustan_tornit
        if asema in self.__mustan_ratsut:
            return self.__mustan_ratsut
        if asema in self.__mustan_lahetit:
            return self.__mustan_lahetit
        if asema in self.__mustan_kuningatar:
            return self.__mustan_kuningatar
        if asema in self.__mustan_kuningas:
            return self.__mustan_kuningas

    def kummat_puolet(self, asema):
        """
        Apufunktio, joka palauttaa asemien listat järjestyksessä omat asemat,
        vastustajan asemat.

        :param asema: str, ruudun koordinaatit, jossa on pelinappula.
        :return: [str, ...], [str, ...]; lista omista asemista ja
                 vastustajan asemista.
        """

        if asema in self.__valkoisen_asemat:
            return self.__valkoisen_asemat, self.__mustan_asemat
        return self.__mustan_asemat, self.__valkoisen_asemat

    def koko_naytto(self):
        """
        Asettaa ikkunan koko näytölle sekä muuttaa napin toiminnoksi palaamaan
        alkuperäiseen ikkunaan.
        """
        self.__paaikkuna.overrideredirect(False)
        self.__paaikkuna.attributes('-fullscreen', True)
        self.__koko_naytto.configure(text="Ikkunaksi",
                                     command=self.pois_koko_naytosta)

    def pois_koko_naytosta(self):
        """
        Asettaa ikkunan koko näytöltä takaisin alkuperäiseen kokoon sekä
        muuttaa napin toiminnoksi palaamaan koko näytölle.
        """
        self.__paaikkuna.overrideredirect(True)
        self.__paaikkuna.attributes('-fullscreen', False)
        self.__koko_naytto.configure(text="Koko näyttö",
                                     command=self.koko_naytto)

    def valkoisen_sotilaan_liike(self, asema):
        """
        Apufunktio, joka tutkii valkoisen sotilaan liikkumismahdollisuuksia
        annetusta <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Sotilaat voivat liikkua kaksi askelta eteen
        ensimmäisellä siirrollaan, sen jälkeen vain yhden. Sotilas voi myös
        syödä vastustajan pelinappulan yhden askeleen päästä viistottain.
        Koska nappulat siirtyvät eri väreillä eri suuntaan, ne on eroteltu
        omiksi metodeikseen.

        :param asema: str, ruudun koordinaatit, josta sotilas lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []
        aseman_kirjain = asema[0]
        aseman_numero = asema[1]
        # syömismahdollisuudet
        for kirjain in viereiset_kirjaimet(aseman_kirjain):
            if (kirjain + str(int(aseman_numero) + 1)) in self.__mustan_asemat:
                siirrot.append(kirjain + str(int(aseman_numero) + 1))
        # ei ole blokkausta
        if (aseman_kirjain + str(int(aseman_numero) + 1)) not in \
                (self.__mustan_asemat + self.__valkoisen_asemat):
            siirrot.append(aseman_kirjain + str(int(aseman_numero) + 1))
            # lähtöasemassa ja kahden askeleen päässä ei ole blokkausta
            if aseman_numero == "2" and (aseman_kirjain + "4") not in (
                    self.__mustan_asemat + self.__valkoisen_asemat):
                # kahden askeleen siirto on mahdollinen
                siirrot.append(aseman_kirjain + str(int(aseman_numero) + 2))
        return siirrot

    def mustan_sotilaan_liike(self, asema):
        """
        Apufunktio, joka tutkii mustan sotilaan liikkumismahdollisuuksia
        annetusta <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Sotilaat voivat liikkua kaksi askelta eteen
        ensimmäisellä siirrollaan, sen jälkeen vain yhden. Sotilas voi myös
        syödä vastustajan pelinappulan yhden askeleen päästä viistottain.

        :param asema: str, ruudun koordinaatit, josta sotilas lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []
        aseman_kirjain = asema[0]
        aseman_numero = asema[1]
        # syömismahdollisuudet
        for kirjain in viereiset_kirjaimet(aseman_kirjain):
            if (kirjain + str(int(aseman_numero) - 1)) in \
                    self.__valkoisen_asemat:
                siirrot.append(kirjain + str(int(aseman_numero) - 1))
        # ei ole blokkausta
        if (aseman_kirjain + str(int(aseman_numero) - 1)) not in \
                (self.__mustan_asemat + self.__valkoisen_asemat):
            siirrot.append(aseman_kirjain + str(int(aseman_numero) - 1))
        # lähtöasemassa ja kahden askeleen päässä ei ole blokkausta
        if aseman_numero == "7" and (aseman_kirjain + "5") not in (
                self.__mustan_asemat + self.__valkoisen_asemat):
            # kahden askeleen siirto on mahdollinen
            siirrot.append(aseman_kirjain + str(int(aseman_numero) - 2))
        return siirrot

    def tornin_liike(self, asema):
        """
        Apufunktio, joka tutkii tornin liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Torni voi liikkua suorasti niin pitkälle kuin
        vain mahdollista. Molemmille väreille voidaan soveltaa samaa
        liikkumista.

        :param asema: str, ruudun koordinaatit, josta torni lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []
        aseman_kirjain = asema[0]
        aseman_numero = asema[1]
        indeksi = KIRJAIMET.index(aseman_kirjain)
        oma_puoli, vast_puoli = self.kummat_puolet(asema)

        # Torni voi liikkua neljään suuntaan
        # ylös pääsee, alas pääsee, vasemmalle pääsee, oikealle pääsee
        paasylista = [True, True, True, True]
        for kerroin in range(1, 9):
            # tallennetaan kierroksen käsiteltävät ruudut listaan
            kasiteltavat_ruudut = []
            # ylöspäin, jos ei olla ylälaidassa tai blokattuna
            if int(aseman_numero) + kerroin <= 8 and paasylista[0]:
                kasiteltavat_ruudut.append(aseman_kirjain + str(int(
                    aseman_numero) + kerroin))
            else:
                kasiteltavat_ruudut.append("")
            # alaspäin, jos ei olla alalaidassa
            if int(aseman_numero) - kerroin >= 1 and paasylista[1]:
                kasiteltavat_ruudut.append(aseman_kirjain + str(int(
                    aseman_numero) - kerroin))
            else:
                kasiteltavat_ruudut.append("")
            # oikealle, jos ei olla oikeassa laidassa tai blokattuna
            if indeksi + kerroin <= 7 and paasylista[2]:
                kasiteltavat_ruudut.append(KIRJAIMET[indeksi + kerroin] +
                                           aseman_numero)
            else:
                kasiteltavat_ruudut.append("")
            # vasemmalle, jos ei olla vasemmassa laidassa tai blokattuna
            if indeksi - kerroin >= 0 and paasylista[3]:
                kasiteltavat_ruudut.append(KIRJAIMET[indeksi - kerroin] +
                                           aseman_numero)
            else:
                kasiteltavat_ruudut.append("")
            # käsitellään ruudut
            for ruutu in kasiteltavat_ruudut:
                ruudun_indeksi = kasiteltavat_ruudut.index(ruutu)
                if not ruutu or ruutu in oma_puoli:
                    paasylista[ruudun_indeksi] = False
                elif ruutu in vast_puoli:
                    paasylista[ruudun_indeksi] = False
                    siirrot.append(ruutu)
                else:
                    siirrot.append(ruutu)
        return siirrot

    def ratsun_liike(self, asema):
        """
        Apufunktio, joka tutkii ratsun liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Ratsu voi liikkua L-kirjaimen mukaisesti eli
        kaksi eteen, yhden sivulle. Molemmille väreille voidaan soveltaa samaa
        liikkumista.

        :param asema: str, ruudun koordinaatit, josta ratsu lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []
        aseman_kirjain = asema[0]
        aseman_numero = asema[1]
        indeksi = KIRJAIMET.index(aseman_kirjain)
        oma_puoli, vast_puoli = self.kummat_puolet(asema)
        # hevonen saattaa liikkua enintään kahdeksaan ruutuun
        # kaksi ruutua ylös
        if int(aseman_numero) <= 6:
            # ruutu vasempaan
            if indeksi >= 1:
                ruutu = KIRJAIMET[indeksi - 1] + str(int(aseman_numero) + 2)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
            # ruutu oikeaan
            if indeksi <= 6:
                ruutu = KIRJAIMET[indeksi + 1] + str(int(aseman_numero) + 2)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
        # kaksi ruutua alas
        if int(aseman_numero) >= 3:
            # ruutu vasempaan
            if indeksi >= 1:
                ruutu = KIRJAIMET[indeksi - 1] + str(int(aseman_numero) - 2)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
            # ruutu oikeaan
            if indeksi <= 6:
                ruutu = KIRJAIMET[indeksi + 1] + str(int(aseman_numero) - 2)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
        # kaksi ruutua vasempaan
        if indeksi >= 2:
            # ruutu ylös
            if int(aseman_numero) <= 7:
                ruutu = KIRJAIMET[indeksi - 2] + str(int(aseman_numero) + 1)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
            # ruutu alas
            if int(aseman_numero) >= 2:
                ruutu = KIRJAIMET[indeksi - 2] + str(int(aseman_numero) - 1)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
        # kaksi ruutua oikeaan
        if indeksi <= 5:
            # ruutu ylös
            if int(aseman_numero) <= 7:
                ruutu = KIRJAIMET[indeksi + 2] + str(int(aseman_numero) + 1)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
            # ruutu alas
            if int(aseman_numero) >= 2:
                ruutu = KIRJAIMET[indeksi + 2] + str(int(aseman_numero) - 1)
                if ruutu not in oma_puoli:
                    siirrot.append(ruutu)
        return siirrot

    def lahetin_liike(self, asema):
        """
        Apufunktio, joka tutkii lähetin liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Lähetti voi liikkua viistottain niin pitkälle
        kuin vain mahdollista. Molemmille väreille voidaan soveltaa samaa
        liikkumista.

        :param asema: str, ruudun koordinaatit, josta lähetti lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []
        aseman_kirjain = asema[0]
        aseman_numero = asema[1]
        oma_puoli, vast_puoli = self.kummat_puolet(asema)
        indeksi = KIRJAIMET.index(aseman_kirjain)
        # Lähetti saattaa liikkua enintään neljään suuntaan
        # ylös vasemmalle, ylös oikealle, alas vasemmalle, alas oikealle
        paasylista = [True, True, True, True]
        for kerroin in range(1, 9):
            # tallennetaan kierroksen käsiteltävät ruudut listaan
            kasiteltavat_ruudut = []
            # ylös ja vasemmalle, jos ei olla ylä- tai vasemmassa laidassa
            if indeksi - kerroin >= 0 and int(aseman_numero) + kerroin <= 8 \
                    and paasylista[0]:
                kasiteltavat_ruudut.append(KIRJAIMET[indeksi - kerroin]
                                           + str(int(aseman_numero) + kerroin))
            else:
                kasiteltavat_ruudut.append("")
            # ylös ja oikealle, jos ei olla ylä- tai oikeassa laidassa
            if indeksi + kerroin <= 7 and int(aseman_numero) + kerroin <= 8 \
                    and paasylista[1]:
                kasiteltavat_ruudut.append(KIRJAIMET[indeksi + kerroin]
                                           + str(int(aseman_numero) + kerroin))
            else:
                kasiteltavat_ruudut.append("")
            # alas ja vasemmalle, jos ei olla ala- tai vasemmassa laidassa
            if indeksi - kerroin >= 0 and int(aseman_numero) - kerroin >= 1 \
                    and paasylista[2]:
                kasiteltavat_ruudut.append(KIRJAIMET[indeksi - kerroin]
                                           + str(int(aseman_numero) - kerroin))
            else:
                kasiteltavat_ruudut.append("")
            # alas ja oikealle, jos ei olla ala- tai oikeassa laidassa
            if indeksi + kerroin <= 7 and int(aseman_numero) - kerroin >= 1 \
                    and paasylista[3]:
                kasiteltavat_ruudut.append(KIRJAIMET[indeksi + kerroin]
                                           + str(int(aseman_numero) - kerroin))
            else:
                kasiteltavat_ruudut.append("")
            # käsitellään ruudut
            for ruutu in kasiteltavat_ruudut:
                ruudun_indeksi = kasiteltavat_ruudut.index(ruutu)
                if not ruutu or ruutu in oma_puoli:
                    paasylista[ruudun_indeksi] = False
                elif ruutu in vast_puoli:
                    paasylista[ruudun_indeksi] = False
                    siirrot.append(ruutu)
                else:
                    siirrot.append(ruutu)
        return siirrot

    def kuninkaan_liike(self, asema):
        """
        Apufunktio, joka tutkii kuninkaan liikkumismahdollisuuksia annetusta
        <asema>:sta eli pelilaudan ruudusta. Palauttaa kaikki
        siirtomahdollisuudet. Kuningas voi liikkua yhden askeleen joka
        suuntaan laudalla. Molemmille väreille voidaan soveltaa samaa
        liikkumista.

        :param asema: str, ruudun koordinaatit, josta kuningas lähtee.
        :return: [str, ...]; lista mahdollisista siirryttävistä ruuduista.
        """

        siirrot = []
        aseman_kirjain = asema[0]
        aseman_numero = asema[1]
        oma_puoli, vast_puoli = self.kummat_puolet(asema)
        indeksi = KIRJAIMET.index(aseman_kirjain)
        # ylöspäin
        # jos ei olla jo ylälaidassa
        if int(aseman_numero) <= 7:
            # ruutu vasempaan
            if indeksi >= 1:
                ruutu = KIRJAIMET[indeksi - 1] + str(int(aseman_numero) + 1)
                siirrot.append(ruutu)
            # ruutu oikeaan
            if indeksi <= 6:
                ruutu = KIRJAIMET[indeksi + 1] + str(int(aseman_numero) + 1)
                siirrot.append(ruutu)
            # keskelle voi liikkua ilman lisärajoituksia
            ruutu = aseman_kirjain + str(int(aseman_numero) + 1)
            siirrot.append(ruutu)
        # alaspäin
        if int(aseman_numero) >= 2:
            # ruutu vasempaan
            if indeksi >= 1:
                ruutu = KIRJAIMET[indeksi - 1] + str(int(aseman_numero) - 1)
                siirrot.append(ruutu)
            # ruutu oikeaan
            if indeksi <= 6:
                ruutu = KIRJAIMET[indeksi + 1] + str(int(aseman_numero) - 1)
                siirrot.append(ruutu)
            ruutu = aseman_kirjain + str(int(aseman_numero) - 1)
            siirrot.append(ruutu)
        # vasemmalle tarvitsee lisätä vain yksi askel suoraan vasemmalle
        if indeksi >= 1:
            ruutu = KIRJAIMET[indeksi - 1] + aseman_numero
            siirrot.append(ruutu)
        # oikealle
        if indeksi <= 6:
            ruutu = KIRJAIMET[indeksi + 1] + aseman_numero
            siirrot.append(ruutu)
        # poistetaan vielä siirroista sellaiset ruudut,
        # jotka ovat varattuina omille nappuloille
        for ruutu in oma_puoli:
            if ruutu in siirrot:
                siirrot.remove(ruutu)

        # Linnoittaminen
        self.__linnoittaminen = False
        if not self.__valkoisen_kuningas_liikkunut and asema == "e1":
            if not self.__valkoisen_vasen_torni_liikkunut:
                # tornin ja kuninkaan väli on tyhjä
                if "b1" not in (oma_puoli + vast_puoli) \
                        and "c1" not in (oma_puoli + vast_puoli) \
                        and "d1" not in (oma_puoli + vast_puoli):
                    siirrot.append("c1")
                    self.__linnoittaminen = True
            if not self.__valkoisen_oikea_torni_liikkunut:
                # kuninkaan luo on mahdollista mennä
                if "f1" not in (oma_puoli + vast_puoli) \
                        and "g1" not in (oma_puoli + vast_puoli):
                    siirrot.append("g1")
                    self.__linnoittaminen = True
        if not self.__mustan_kuningas_liikkunut and asema == "e8":
            if not self.__mustan_vasen_torni_liikkunut:
                if "b8" not in (oma_puoli + vast_puoli) \
                        and "c8" not in (oma_puoli + vast_puoli) \
                        and "d8" not in (oma_puoli + vast_puoli):
                    siirrot.append("c8")
                    self.__linnoittaminen = True
            if not self.__mustan_oikea_torni_liikkunut:
                if "bg" not in (oma_puoli + vast_puoli) \
                        and "f8" not in (oma_puoli + vast_puoli):
                    siirrot.append("g8")
                    self.__linnoittaminen = True
        return siirrot

    def aloita(self):
        """
        Käynnistää pääikkunan silmukan, ts. käynnistää käyttöliittymän ikkunan.
        """

        self.__paaikkuna.mainloop()


def viereiset_kirjaimet(kirjain):
    """
    Apufunktio nappuloiden siirtomahdollisuuksien tutkimiseen. Palauttaa
    laudan koordinaattikirjaimen viereiset kirjaimet tai viereisen kirjaimen.

    :param kirjain: str, koordinaattikirjain.
    :return: str / str, str; viereiset koordinaattikirjaimet.
    """

    indeksi = KIRJAIMET.index(kirjain)
    if indeksi == 0:
        return KIRJAIMET[1]
    if indeksi == 7:
        return KIRJAIMET[6]
    return KIRJAIMET[indeksi-1], KIRJAIMET[indeksi+1]


def shakkilaudan_koordinaatit():
    """
    Apufunktio, joka palauttaa shakkilaudan ruudut listana a1, a2, ..., b1 jne.

    :return: [str, ...]; shakkilaudan ruudut.
    """

    ruudut = []
    for kirjain in KIRJAIMET:
        for numero in range(1, 9):
            ruudut.append(kirjain + str(numero))
    return ruudut


def main():
    # otetaan käyttöön Shakkilauta
    lauta = Shakkilauta()
    # käynnistetään grafiikka
    lauta.aloita()


if __name__ == "__main__":
    main()

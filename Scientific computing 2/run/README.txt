Ohjelman rk4.exe suoritus tapahtuu seuraavilla komentoriviargumenteilla:

./rk4.exe [inpufile] [outputfile] [aikajakso] [tallennustiheys] [aika-askel]

Inputfile ja outputfile kertovat mistä tiedostosta ohjelma lukee simuloitavien kappaleiden alkuperäiset ominaisuudet, ja mihin simuloitu data tallennetaan. Inputfilejä on valmiina neljä: aurinkokunta.txt, aurinko-jupiter.txt, aurinko-maa.txt ja maa-kuu.txt. Tiedostojen nimet kertovat minkä kaikkien kappaleiden tiedot tiedostoissa on.
Aikajakso on vuosissa se aika, joka halutaan simuloida. Tämä voi olla kokonaisluku tai desimaaliluku.
Tallennustiheys kertoo ohjelmalle kuinka monen aika-askeleen välein uudet lasketut paikat tallennetaan. Täytyy olla kokonaisluku. Mikäli tämä on 1, tallennetaan jokainen simuloitu paikka.
Aika-askel kertoo kuinka monen päivän välein ohjelma laskee uudet paikat. Voi olla kokonaisluku tai desimaaliluku. Eli jos tämä on 1, ohjelma laskee uudet paikat kerran päivässä. Jos tämä on 0.5, ohjelma laskee uudet paikat kaksi kertaa päivässä.

Esimerkki tästä:

./rk4.exe aurinkokunta.txt aurinkokunta_10v.dat 10 30 1


Piirtäjiä kutsutaan seuraavalla komennolla:

python piirtaja_[tyyppi].py [inpufile] [aikaväli]

Tässä tyyppi tarkoittaa sitä, millaista piirtäjää halutaan käyttää. Piirtäjiä on neljä: piirtaja_aurinkokunta.py, piirtaja_aurinko-jupiter.py, piirtaja_aurinko-maa.py ja piirtaja_maa-kuu.py. Nimet kertovat millaisten systeemien kuvantamiseen ne on tarkoitettu.
Inputfile kertoo mistä tiedostosta piirrettävä data katsotaan. Käytännössä sama kuin rk4:n outpufile.
Aikaväli kertoo kuinka monen päivän välein inputfilen paikat on tallennettu. Tätä käytetään ajanhetken kirjaamiseen kuviin. Voi olla kokonaisluku tai desimaaliluku. Käytännössä tämä on sama kuin rk4:n [tallennustiheys] * [aika-askel]. 

Esimerkki tästä:

python piirtaja_aurinkokunta.py aurinkokunta_10v.dat 30


Kasutajaliidese ehk *front-end*'i kood asub siin: https://github.com/helenasokk/Loputoo_front-end

**NB!** Enne tuleks läbi teha allpool välja toodud juhised ja alles siis suunduda kasutajaliidese juurde.
# Serveri tööks vajalikud failid:
* '21_lemmad_frq.txt' - lemmade sagedussõnastik.
* 'saveKerged.pickle' - kergete raskusgruppi kuuluvad võõrsõnad.
* 'saveKeskm.pickle' - keskmiste raskusgruppi kuuluvad võõrsõnad.
* 'saveRasked.pickle' - raskete gruppi kuuluvad võõrsõnad.
* 'savePaarid.pickle' - teise alammängu jaoks vajalikud sarnaste võõrsõnade paarid.
* 'saveSonastik.pickle' - fail, mis sisaldab võõrsõnade sõnastikku, milles on võtmeteks võõrsõnad ning vasteteks vihjed.
* 'saveLaused.pickle' - võõrsõnadele vastavaid lauseid sisaldav fail, igale võõrsõnale on kogutud 20 lauset.
# Eeltöötluse jaoks vajalikud failid:
* 'eeltootlus.py' - mängude jaoks vajalik eeltöötlus: võõrsõnade eraldamine võõrsõnade leksikonist koos vihjetega, võõrsõnade raskusastmetesse grupeerimine, sarnaste võõrsõnapaaride loomine.
* 'importLaused.py' - SketchEngine'ist võõrsõnu sisaldavate lausete pärimine ja pickle-failidesse salvestamine.
* 'mergeSonastikud.py' - Liidab mitmesse pickle-faili salvestatud sõnastikud üheks terveks (lauseid sisaldavad).
# Serveri tööks vajalikud moodulid koos käskudega:
```
pip install Flask
pip install estnltk==1.7
```
# Eeltöötlus
Kaustas 'Eeltootlus' on olemas kõik eelnevalt mainitud eeltöötluseks vajalikud failid. 
Eelnevalt on vaja läbi jooksutada fail 'eeltootlus.py', mis loob: 
* võõrsõnade sõnastiku ning salvestab selle faili 'saveSonastik.pickle'; 
* võõrsõnade raskusgrupid ning salvestab need failidesse 'saveKerged.pickle', 'saveKeskm.pickle' ja 'saveRasked.pickle'; 
* ning sarnaste võõrsõnade paarid ja salvestab need faili 'savePaarid.pickle'.

Kindlasti tuleks lugeda eeltöötluse failis olevaid kommentaare, sest enne sarnaste võõrsõnade paaride loomist tuleks eemaldada kõikidest raskusgruppide failidest ebasobivad sõnad, mis on välja toodud failis 'eemaldatud_sõnad.txt'.

**NB!** Projektis on kasutatud EKI Eesti keele ühendkorpuse 2021 lemmade ja sõnavormide sagedusloendit (sageduse järgi), mille litsents on leitav [siit](https://eki.ee/eki/litsents.html).

Kui sõnastik, raskusgrupid ja võõrsõnade paarid on olemas, tuleks järgmisena koguda kokku laused, mis päritakse SketchEngine'i API-st. Selleks on vaja SketchEngine'isse sisse logida ning failis 'importLaused.py' asendada muutujad USERNAME ja API_KEY vastavalt enda andmetega (neid on võimalik näha SketchEngine'isse sisse logides My account vaates). Lauseid saab koguda vastavalt soovile 500, 1000 jne kaupa, kuid kindlasti tuleb jälgida koodis olevaid kommentaare ja time.sleep() sisendeid, mis sobiksid kõige paremini. Sellest on täpsemalt juttu [siin](https://www.sketchengine.eu/fair-use-policy/#:~:text=The%20FUP%20limit%20applies%20to,exceeding%20any%20of%20these%20limits). 

Kui laused on kokku kogutud ja vastavatesse failidesse salvestatud (sõnastiku kujul), näiteks 'saveKergedLaused.pickle' jne, siis on võimalik jooksutada faili 'mergeSonastikud.py', mis salvestab kõik eraldi failidesse salvestatud laused ühte faili 'saveLaused.pickle'.

# Serveri töö
Kogu serveri töö toimub failis server.py, kuid selleks, et vajalikke mooduleid installeerida ning serverit tööle panna, on vaja luua virtuaalkeskkond. Liikudes terminaliaknas serverile mõeldud kausta (eeldusel, et selline kaust juba eksisteerib), sisesta käsk ```python -m venv env```, mis loob vastava virtuaalkeskkonna nimega **env**. Selleks, et env'i aktiveerida, sisesta käsk ```env\Scripts\activate```. Nüüd on võimalik vajalikke mooduleid installeerida, mille käsud on välja toodud lõigus "Serveri tööks vajalikud moodulid koos käskudega:". Selleks, et näha serveri väljundit, sisesta käsk ```python server.py```. Kui on korras, peaks tulema teade '* Running on http://127.0.0.1:5000' ning minnes oma veebibrauseris lehele http://127.0.0.1:5000/keskmmang1 peaks väljundiks olema esimese mängu jaoks vajalik sõnastik.

Kasutajaliidese kohta on täpsemad juhised ja failid [selles projektis](https://github.com/helenasokk/Loputoo_front-end).

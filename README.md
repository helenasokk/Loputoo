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
# Eeltöötlus
Kaustas 'Eeltootlus' on olemas kõik eelnevalt mainitud eeltöötluseks vajalikud failid. 
Eelnevalt on vaja läbi jooksutada fail 'eeltootlus.py', mis loob: 
* võõrsõnade sõnastiku ning salvestab selle faili 'saveSonastik.pickle'; 
* võõrsõnade raskusgrupid ning salvestab need failidesse 'saveKerged.pickle', 'saveKeskm.pickle' ja 'saveRasked.pickle'; 
* ning sarnaste võõrsõnade paarid ja salvestab need faili 'savePaarid.pickle'.

Kindlasti tuleks lugeda eeltöötluse failis olevaid kommentaare, sest enne sarnaste võõrsõnade paaride loomist tuleks eemaldada kõikidest raskusgruppide failidest ebasobivad sõnad, mis on välja toodud failis 'eemaldatud_sõnad.txt'.

Kui sõnastik, raskusgrupid ja võõrsõnade paarid on olemas, tuleks järgmisena koguda kokku laused, mis päritakse SketchEngine'i API-st. Selleks on vaja SketchEngine'isse sisse logida ning failis 'importLaused.py' asendada muutujad USERNAME ja API_KEY vastavalt enda andmetega (neid on võimalik näha SketchEngine'isse sisse logides My account vaates). Lauseid saab koguda vastavalt soovile 500, 1000 jne kaupa, kuid kindlasti tuleb jälgida koodis olevaid kommentaare ja time.sleep() sisendeid, mis sobiksid kõige paremini. Sellest on täpsemalt juttu siin: https://www.sketchengine.eu/fair-use-policy/#:~:text=The%20FUP%20limit%20applies%20to,exceeding%20any%20of%20these%20limits. 

Kui laused on kokku kogutud ja vastavatesse failidesse salvestatud (sõnastiku kujul), näiteks 'saveKergedLaused.pickle' jne, siis on võimalik jooksutada faili 'mergeSonastikud.py', mis salvestab kõik eraldi failidesse salvestatud laused ühte faili 'saveLaused.pickle'.

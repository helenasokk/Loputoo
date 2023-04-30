# Serveri tööks vajalikud failid:
'21_lemmad_frq.txt' - lemmade sagedussõnastik.
'saveKerged.pickle' - kergete raskusgruppi kuuluvad võõrsõnad.
'saveKeskm.pickle' - keskmiste raskusgruppi kuuluvad võõrsõnad.
'saveRasked.pickle' - raskete gruppi kuuluvad võõrsõnad.
'savePaarid.pickle' - teise alammängu jaoks vajalikud sarnaste võõrsõnade paarid.
'saveSonastik.pickle' - fail, mis sisaldab võõrsõnade sõnastikku, milles on võtmeteks võõrsõnad ning vasteteks vihjed.
'saveLaused.pickle' - võõrsõnadele vastavaid lauseid sisaldav fail, igale võõrsõnale on kogutud 20 lauset.
# Eeltöötluse jaoks vajalikud failid:
'eeltootlus.py' - mängude jaoks vajalik eeltöötlus: võõrsõnade eraldamine võõrsõnade leksikonist koos vihjetega, võõrsõnade raskusastmetesse grupeerimine, sarnaste võõrsõnapaaride loomine.
'importLaused.py' - SketchEngine'ist võõrsõnu sisaldavate lausete pärimine ja pickle-failidesse salvestamine.
'mergeSonastikud.py' - Liidab mitmesse pickle-faili salvestatud sõnastikud üheks terveks (lauseid sisaldavad).

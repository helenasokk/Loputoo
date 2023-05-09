# Sagedussõnastik
from bs4 import BeautifulSoup
import pickle
filename = "21_lemmad_frq.txt"
f = open(filename, encoding="utf-8")
sõnad = []
for rida in f.readlines():
  tulemus = rida.strip().split()
  if len(tulemus) != 0 and len(tulemus) == 3:
    sõnad.append([tulemus[0], [tulemus[1], tulemus[2]]])
  #sõnad.append([tulemus[0], [tulemus[1], tulemus[2]]])
sõnastik_frq = {sona: vaste for sona, vaste in sõnad}

# XML fail
# tsitaatsõnad tähisega 'zs' - need jätan välja, pole vajalikud
# allmärksõnad tähisega 'all' - neid pole ka vaja
# märksõna tähisega 'm' - siit saan kätte võõrsõna
# 'A' - artikkel - iga märksõna on eraldi artikli sees
# 'P' - Päis - see on vajalik, et eraldada märksõna allmärksõnast
# sisu tähistatud 'S' - kogu definitsioonide ja seletuste plokk on selle sees
# sõna seletus tähisega 'd' - siit saan kõik vajalikud võõrsõna seletused/definitsioonid
# 'v' tähis näitab sõna valdkonda - nt AJ on ajalugu, KEEM on keemia jne
tulemused = []
filename = "vsl_EKI_CCBY40.xml"
with open(filename, 'r', encoding="utf-8") as f:
    data = f.readlines()
for line in data:
  bs_line = BeautifulSoup(line, "xml")
  for line_A in bs_line.find_all('A'):
    if ((line_A.find('m').has_attr('zs')) == False) and (line_A.find('m').has_attr('liik') == False) and (len(line_A.find_all('d')) != 0):# Jätan välja kõik tsitaatsõnad ('zs' märgisega) ja ebavajalikud eesliited, muusikaga seotud sõnad jne ('liik' märgisega)
        #tulemused.append(line_A.find('m').text) # Avastasin ka seda, et neil on leksikonis noolega suunatud eestikeelse sõna juurde, seega sain seda kasutada sobivate sõnade otsimiseks
        vihjed = [] # kogu vihjete list, mis sisasldab endast vasteid (definitsioonid/tähendused) ja lisaks mida veel saaks kasutada
        valdkond = ''
        vastand = ''
        vorm = ''
        for line_P in line_A.find_all('P'):
          märksõna = line_P.find('m').text
          if len(line_P.find_all('sl')) != 0:
              vorm = line_P.find('sl').text
        for line_S in line_A.find_all('S'):
          if len(line_S.find_all('s')) == 0 and len(märksõna) > 3: # Jätan kõik vananenud, nõukogulikud, harva esinevad jne sõnad välja (lisaks pole vaja liiga lühikesi sõnu ka nt muusikas kasutatavad 'as')
            char_remove = ['&la;', '&ll;', '&supa;', '&supl;', '&suba;', '&subl;', '&ema;', '&eml;'] # panin tähele, et sellised tähised olid sisse jäänud, seega eemaldan need kohe, kui olen vaste leidnud
            if (len(line_S.find_all('v')) != 0):
              valdkond = line_S.find('v').text
            if (len(line_S.find_all('tvt1')) != 0 and line_S.find('tvt1').has_attr('tvtl1') == True): # Kui on olemas vastandsõna, lisan selle ka vihjete hulka
              if len(line_S.find_all(attrs={"tvtl1": "vast"})) != 0:
                vastand = line_S.find_all(attrs={"tvtl1": "vast"})[0].text
            if (len(line_S.find_all('tvt2')) != 0 and line_S.find('tvt2').has_attr('tvtl2') == True): # Kui on olemas vastandsõna, lisan selle ka vihjete hulka
              if len(line_S.find_all(attrs={"tvtl2": "Vast"})) != 0:
                vastand = line_S.find_all(attrs={"tvtl2": "Vast"})[0].text
                if vastand[-1] == '2':
                  vastand = vastand.replace('2', '')
            #if (len(line_S.find_all('s')) != 0):
            #  stiil = line_S.find('s').text
            if (len(line_S.find_all('d')) > 1):
              vasted = []
              for vaste in line_S.find_all('d'):
                tulemus = vaste.text
                for char in char_remove:
                  tulemus = tulemus.replace(char, '')
                tulemus = tulemus.replace(' v ', ' või ')
                tulemus = tulemus.replace(' e ', ' ehk ')
                vasted.append(tulemus)
              vihjed = [valdkond, vasted, vastand, vorm]
              tulemused.append([märksõna, vihjed])
            else:
              #print(märksõna)
              sona = line_S.find('d').text
              for char in char_remove:
                  sona = sona.replace(char, '')
              tulemused.append([märksõna, [valdkond, sona, vastand, vorm]])

sõnastik = {sona: vaste for sona, vaste in tulemused}
del sõnastik['ageeratum']
del sõnastik['abstruusne']

kerged = []
keskmised = []
rasked = []
for key in sõnastik.keys():
  if key in sõnastik_frq.keys():
    if float(sõnastik_frq[key][1]) >= 5.0: #Tundub, et alla 0.2 -> sobiksid raskemate/keerulisemate sõnade sekka. Keskmise raskusaste jaoks sobiks >= 0.2st ja < 5.0st
      kerged.append(key)
    elif float(sõnastik_frq[key][1]) < 5.0 and float(sõnastik_frq[key][1]) >= 0.2:
      keskmised.append(key)
    elif float(sõnastik_frq[key][1]) < 0.2:
      rasked.append(key)
print(len(kerged))
print(len(keskmised))
print(len(rasked))
def levenshtein(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1], distances[index1+1], newDistances[-1])))
        distances = newDistances
    return distances[-1]

with open('saveKerged.pickle', 'rb') as handle:
    kerged = pickle.load(handle)

with open('saveKeskm.pickle', 'rb') as handle:
    keskmised = pickle.load(handle)
    
with open('saveRasked.pickle', 'rb') as handle:
    rasked = pickle.load(handle)
    
with open('saveSonastik.pickle', 'rb') as handle:
    sõnastik = pickle.load(handle)

paarid = []
keys = kerged + keskmised + rasked
for idx, a in enumerate(keys):
  for b in keys[idx + 1:]:
    if len(keys[idx]) > 4 and len(b) > 4:
        if ((keys[idx][:3] == b[:3]) or (keys[idx][3:] == b[3:])) and sõnastik[keys[idx]][3] == sõnastik[b][3]:
          kaugus = levenshtein(keys[idx], b)
          if kaugus >= 1 and kaugus < 3: # #kui kaugus on 1, siis tuleb u 410 paari, kui kaugus väiksem 4st suurem või võrdne 1ga -> 4718 paari ja paljud nendest on päris ebaloogilised
            paarid.append([keys[idx], b])

'''with open('saveSonastik.pickle', 'wb') as handle:
    pickle.dump(sõnastik, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('saveKerged.pickle', 'wb') as handle:
    pickle.dump(kerged, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('saveKeskm.pickle', 'wb') as handle:
    pickle.dump(keskmised, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
with open('saveRasked.pickle', 'wb') as handle:
    pickle.dump(rasked, handle, protocol=pickle.HIGHEST_PROTOCOL)'''
    
with open('savePaarid.pickle', 'wb') as handle:
    pickle.dump(paarid, handle, protocol=pickle.HIGHEST_PROTOCOL)
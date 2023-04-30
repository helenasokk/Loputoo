import requests
import pickle
import time
USERNAME = '...'
headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)", "Referer": "http://example.com"}
API_KEY = '...'
data = {
 'corpname': 'preloaded/sonaveeb_2021',
 'struct_attr_stats': 1,
 'format': 'json',
 'lemma': 'adapteerima',
 'lpos': '-v',
}
sõnastik = {}
sõnad = [] #Otsin lauseid SketchEngine'ist vastavalt sellele, kas kuuluvad kergete, keskmiste või raskete hulka
# Selliselt ei saa limiit liiga kiiresti täis
failinimi = 'saveRasked.pickle'
with open(failinimi, 'rb') as handle:
    sõnad = pickle.load(handle)
with open('saveSonastik.pickle', 'rb') as handle:
    sõnastik = pickle.load(handle)
#print(len(sõnastik))
#print(len(sõnad))
pool = sõnad[7000:]
#pool = ['anomaalne']
#print(sõnad)
lausedKokku = []
oota = 0
#for sõna in sõnastik.keys():
for sõna in pool:
    # Teen päringuid ScketchEngine'isse vastavalt sõnastikust võetud võõrsõnale
    #print(sõna)
    base_url = 'https://api.sketchengine.eu/bonito/run.cgi/view?corpname=preloaded/elexis_ettenten21_fil2&q=q[lemma="'+sõna+'"]&viewmode=sen&pagesize=20&format=json'
    d = requests.get(base_url, auth=(USERNAME, API_KEY), headers=headers)
    d.raise_for_status()
    if d.status_code != 204:
        d = d.json()
    yheLaused = [] # Ühe võõrsõna laused
    for lause in d['Lines']:
        left = ''
        right = ''
        word = ''
        if len(lause['Left']) > 1:
            #print(lause['Left'][1]['str'])
            left = lause['Left'][1]['str']
        elif len(lause['Left']) != 0:
            #print(lause['Left'][0]['str'])
            left = lause['Left'][0]['str']
        if len(lause['Right']) != 0:
            #print(lause['Right'][0]['str'])
            right = lause['Right'][0]['str']
        word = str(lause['Kwic'][0]['str']).strip()
        yheLaused.append([left, right, word])
    lausedKokku.append([sõna, yheLaused])
    oota += 1
    if oota >= 100 and oota < 500:
        time.sleep(6)
    elif oota >= 500:
        time.sleep(60)

#1452
#5302
#7337
lausedSonastik = {sona: laused for sona, laused in lausedKokku}
with open('saveLausedRasked7337.pickle', 'wb') as handle:
    pickle.dump(lausedSonastik, handle, protocol=pickle.HIGHEST_PROTOCOL)
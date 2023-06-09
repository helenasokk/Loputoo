from flask import Flask
import random
import pickle
from estnltk import Text
from estnltk.vabamorf.morf import synthesize

app = Flask(__name__)

# sõnastik, milles on võõrsõnad koos vihjetega
sõnastik = {}
with open('saveSonastik.pickle', 'rb') as handle:
    sõnastik = pickle.load(handle)
kerged = []# kergete võõrsõnade grupp
with open('saveKerged.pickle', 'rb') as handle:
    kerged = pickle.load(handle)
keskmised = []# keskmiste võõrsõnade grupp
with open('saveKeskm.pickle', 'rb') as handle:
    keskmised = pickle.load(handle)
rasked = []
with open('saveRasked.pickle', 'rb') as handle:
    rasked = pickle.load(handle)
# laen laused pickle-failist sisse
# kasutan ainult kergeid ja keskmisi võõrsõnu
laused = {}
with open('saveLaused.pickle', 'rb') as handle:
    laused = pickle.load(handle)

paarid = []# sarnaste võõrsõnade paarid, mis on vajalikud teise mängu jaoks
with open('savePaarid.pickle', 'rb') as handle:
    paarid = pickle.load(handle)

# funktsioon võõrsõna õige vormi leidmiseks
def leiaVorm(vasak, parem, sona):
    tulemus = ""
    # Moodustan lause
    tekst = Text(str(vasak + " " + sona + " " + parem))
    lemmad = tekst.tag_layer().morph_analysis.lemma
    sonaLemmana = Text(sona).tag_layer().morph_analysis.lemma[0][0]
    vormid = tekst.tag_layer().morph_analysis.form # leian lause kõikide sõnade vormid
    i = 0
    for i in range(len(vormid) - 1):
        if (lemmad[i][0] == sonaLemmana):
            tulemus = vormid[i][0]
        i += 1
    return tulemus

# Funktsioon võõrsõna valdkonna leidmiseks
def leiaValdkond(valdkond):
    # Kõik eksisteerivad valdkonnad ühes sõnastikus
    valdkonnad = {'aiand': 'aiandus', 'aj': 'ajalugu', 'anat': 'anatoomia', 'antr': 'antropoloogia',
                  'arheol': 'arheoloogia', 'arhit': 'arhitektuur','astr': 'astronoomia', 'bibl': 'bibliograafia',
                  'biol': 'bioloogia', 'bot': 'botaanika', 'dipl': 'diplomaatia', 'eh': 'ehitus', 'el': 'elektroonika',
                  'etn': 'etnoloogia', 'farm': 'farmaatsia', 'fil': 'filosoofia', 'film': 'filmindus', 'folkl': 'folkloor',
                  'fot': 'fotograafia', 'füsiol': 'füsioloogia', 'füüs': 'füüsika', 'geod': 'geodeesia', 'geogr': 'geograafia',
                  'geol': 'geoloogia', 'hüdrol': 'hüdroloogia', 'info': 'informaatika', 'jur': 'juriidika', 'keem': 'keemia',
                  'kirj': 'kirjandus', 'kok': 'kokandus', 'kunst': 'kunst', 'lenn': 'lennundus', 'lgv': 'lingvistika', 'loog': 'loogika',
                  'maj': 'majandus', 'mat': 'matemaatika', 'med': 'meditsiin', 'mer': 'merendus', 'meteor': 'meteoroloogia',
                  'mets': 'metsandus', 'miner': 'mineraloogia', 'muus': 'muusika', 'mäend': 'mäendus', 'müt': 'mütoloogia',
                  'paleont': 'paleonoloogia', 'ped': 'pedagoogika', 'pol': 'poliitika', 'psühh': 'psühholoogia', 'põll': 'põllumajandus',
                  'relig': 'religioon', 'sotsiol': 'sotsioloogia', 'sport': 'sport', 'stat': 'statistika', 'sõj': 'sõjandus', 'zool': 'zoologia',
                  'tants': 'tants', 'teater': 'teater', 'tehn': 'tehnika', 'tekst': 'tekstiil', 'trük': 'trükindus', 'vet': 'veterinaaria', 'ökol': 'ökoloogia'}
    return valdkonnad[valdkond]

# leiame sõnastikust õigele võõrsõnale vastavad laused ja valime nendest suvalise
def leiaLause(sõna):
    if sõna not in laused.keys():
        return ("","")
    lauseOsad = laused[sõna][random.randint(0, len(laused[sõna]) - 1)]
    # Tagastan lause, kus võõrsõna koht on tühjaks jäetud
    return (lauseOsad[0] + " __ " + lauseOsad[1], lauseOsad[-1])

# Funktsioon, mis tagastab võõrsõnale vastavad vihjed
def leiaVihjed(sõna):
    sonavormid = {'S': 'nimisõnaga', 'V': 'tegusõnaga', 'A': 'omadussõnaga', 'P': 'asesõnaga', 'N': 'põhiarvsõnaga', 
                  'I': 'hüüdsõnaga', 'J': 'sidesõnaga', 'G': 'omastavalise täiendiga', 'D': 'määrsõnaga'}
    # Lisan kõik vihjed eraldi nimekirja ja leian kui palju vihjeid on kokku
    nimekiri = []
    # Esimese vihjena antakse ette, mis on selle võõrsõna vorm ning millisesse valdkonda kuulub
    if sõnastik[sõna][0] != "" and sõnastik[sõna][3] != "":
        nimekiri.append("Selle sõna valdkond on "+ leiaValdkond(sõnastik[sõna][0])+". " + "Tegemist on "+ sonavormid[sõnastik[sõna][3]]+".\n")
    # Teise vihjena antakse võõrsõna definitsioon(id)
    # Kui definitsioone on mitu, siis kuvatakse vihjed üksteise alla
    if type(sõnastik[sõna][1]) is list:
        tulemuse = "Selle võõrsõna definitsioonid on:\n"
        for t in sõnastik[sõna][1]:
            t = t.replace(" vm ", " või muu ")
            t = t.replace(" a-ni ", " aastani ")
            t = t.replace(" kasut ", " kasutatakse ")
            t = t.replace(" hrl ", " harilikult ")
            t = t.replace(" v ", " või ")
            tulemuse += " *" + t + "\n"
        nimekiri.append(tulemuse)
    # Kui definitsioone on ainult üks, siis kuvatakse ühe lausena
    elif type(sõnastik[sõna][1]) is str:
        sõnastik[sõna][1] = sõnastik[sõna][1].replace(" vm ", " või muu ")
        sõnastik[sõna][1] = sõnastik[sõna][1].replace(" a-ni ", " aastani ")
        sõnastik[sõna][1] = sõnastik[sõna][1].replace(" kasut ", " kasutatakse ")
        sõnastik[sõna][1] = sõnastik[sõna][1].replace(" hrl ", " harilikult ")
        sõnastik[sõna][1] = sõnastik[sõna][1].replace(" v ", " või ")
        nimekiri.append("Selle võõrsõna definitsioon on: "+sõnastik[sõna][1]+".\n")
    # Kui sõnastikus on olemas vastandsõna, siis lisatakse ka see vihjete hulka
    if sõnastik[sõna][2] != "":
        nimekiri.append("Selle sõna vastandsõna on "+ sõnastik[sõna][2]+".\n")
    # Lisan vihjena ka sõna algustähe
    nimekiri.append("See sõna algab "+sõna[0].upper()+" tähega.\n")
    # Lisan vihjena ka sõna pikkuse
    nimekiri.append("Selle võõrsõna pikkus on "+ str(len(sõna))+ " tähte.\n")
    # Viimasena lisan ühe näidislause
    lause, oigesKaandes = leiaLause(sõna)
    nimekiri.append("Mul on sulle üks näidislause:\n" + lause + "\n")
    return (oigesKaandes, nimekiri)

# Esimese mängu jaoks vajalikud andmed küsitakse siit
@app.route("/keskmmang1")
def mang1():
    # Võtan sõnastikust välja 5 kerget sõna ja nendega seotud vihjet testimiseks
    sonad = []
    kogutud = []
    for i in range(5):
        while True:
            sona = kerged[random.randint(0, len(kerged) - 1)]
            oigesKaandes, vihjed = leiaVihjed(sona)
            if sona not in kogutud and oigesKaandes != "" and vihjed != "":
                kogutud.append(sona)
                break
        lisa = {"sõna": [sona, oigesKaandes], "raskus": "kerge", "vihjeteNkr": vihjed}
        sonad.append(lisa)
        i+=1
    # Võtan sõnastikust välja 5 keskmist sõna ja nendega seotud vihjet testimiseks
    kogutud2 = []
    for j in range(5):
        while True:
            sona = keskmised[random.randint(0, len(keskmised) - 1)]
            oigesKaandes, vihjed = leiaVihjed(sona)
            if sona not in kogutud2 and oigesKaandes != "" and vihjed != "":
                kogutud2.append(sona)
                break
        lisa = {"sõna": [sona, oigesKaandes], "raskus": "keskmine", "vihjeteNkr": vihjed}
        sonad.append(lisa)
        j+=1
    return sonad

# Teise mängu jaoks vajalikud andmed küsitakse siit
@app.route("/keskmmang2")
def mang2():
    sonad = []
    for i in range(10):
        while True:
            paar = paarid[random.randint(0, len(paarid) - 1)]
            if ((paar[0] in kerged or paar[0] in keskmised) and (paar[1] in kerged or paar[1] in keskmised)):
                print("Leidsin!")
                break
        # asendus: paar[0], leitav: paar[1]
        lauseOsad = laused[paar[1]][random.randint(0, len(laused[paar[1]]) - 1)]
        lauseOsad[0] = lauseOsad[0].replace("<p>", "")
        lauseOsad[1] = lauseOsad[1].replace("</p>", "")
        vorm = leiaVorm(lauseOsad[0], lauseOsad[1], lauseOsad[-1])#igaks juhuks võtan viimase elemendi, sest mõne puhul on lauselõpupunkt eraldi
        asendus = synthesize(paar[0], vorm)
        if len(asendus) == 0:
            while True:
                lauseOsad = laused[paar[1]][random.randint(0, len(laused[paar[1]]) - 1)]
                lauseOsad[0] = lauseOsad[0].replace("<p>", "")
                lauseOsad[1] = lauseOsad[1].replace("</p>", "")
                vorm = leiaVorm(lauseOsad[0], lauseOsad[1], lauseOsad[-1])#igaks juhuks võtan viimase elemendi, sest mõne puhul on lauselõpupunkt eraldi
                asendus = synthesize(paar[0], vorm)
                if len(asendus) != 0:
                    break
        if type(asendus) is list:
            asendus = asendus[0]
        asenduseAsendus = ""
        if lauseOsad[-1][0].isupper():
            asenduseAsendus = asendus[0].upper() + asendus[1:]
        if asenduseAsendus == "":
            asenduseAsendus = asendus
        # lauseOsad[-1] -> mõnel sõnal võib olla mõttekriips lõpus või mõni muu üleliigne kirjavahemärk juures
        lisa = {"õige": [paar[1], lauseOsad[-1]], "vasak": lauseOsad[0], "parem": lauseOsad[1], "asendus": asenduseAsendus}
        sonad.append(lisa)
        i += 1
    # Tagastan sõnastikuna, et saaks kuvada õige info kasutajale
    # õige: vastus, mille kasutaja peab sisestama [lemma, õiges vormis]
    # vasak: lause vasak pool
    # parem: lause parem pool
    # asendus: õiges vormis asendatud sõna, mis on vale (õige võõrsõna asemel)
    return sonad

# lisafunktsioon selleks, et leida kõik ühest valdkonnast pärit võõrsõnad
# vajalik kolmanda mängu jaoks
def leiaSamastValdkonnast(valdkond):
    kokku = []
    # hetkel jätan kõik raskete grupi sõnad välja
    yhendatud = kerged + keskmised
    for key in yhendatud:
        if sõnastik[key][0] == valdkond:
            kokku.append(key)
    return kokku

# Kolmanda mängu jaoks vajalikud andmed küsitakse siit
@app.route("/keskmmang3")
def mang3():
    # Kolmanda mängu jaoks on vaja valida üks valdkond
    # Valin neli suvalist lauset ja kuus võõrsõna
    valdkonnad = ['aiand', 'aj', 'anat', 'antr', 'arheol', 'arhit', 'astr', 'bibl', 'biol', 'bot', 'dipl', 
                  'eh', 'el', 'etn', 'farm', 'fil', 'film', 'folkl', 'fot', 'füsiol', 'füüs', 'geod', 
                  'geogr', 'geol', 'hüdrol', 'info', 'jur', 'keem', 'kirj', 'kok', 'lenn', 'lgv', 'loog', 
                  'maj', 'mat', 'med', 'mer', 'kunst,' 'meteor', 'mets', 'miner', 'muus', 'mäend', 'müt', 'paleont', 
                  'ped', 'pol', 'psühh', 'põll', 'relig', 'sotsiol', 'stat', 'sõj', 'sport', 'zool', 'tants', 'tehn', 'tekst', 
                  'trük', 'vet', 'ökol']
    while True:
        valdkond = valdkonnad[random.randint(0, len(valdkonnad)-1)]
        sobivadSõnad = leiaSamastValdkonnast(valdkond)
        if len(sobivadSõnad) > 6:# valdkond sobib ainult siis, kui sõnu sellest valdkonnast on vähemalt 6
            break
    sõnad = []
    vastus = []
    sõna = sobivadSõnad[random.randint(0, len(sobivadSõnad)-1)]
    sõnad.append(sõna)
    for i in range(5):
        while True:
            sõna = sobivadSõnad[random.randint(0, len(sobivadSõnad)-1)]
            if sõna not in sõnad:
                sõnad.append(sõna)
                break
        lauseOsad = laused[sõna][random.randint(0, len(laused[sõna]) - 1)]
        lauseOsad[0] = lauseOsad[0].replace("<p>", "")
        lauseOsad[1] = lauseOsad[1].replace("</p>", "")
        lauseOsad[-1] = lauseOsad[-1].replace("-", "")
        lause = {"sõna": [sõna, lauseOsad[-1]], "vasak": lauseOsad[0], "parem": lauseOsad[1], "sõnad": sõnad}
        vastus.append(lause)
        i+=1
    return vastus

if __name__ == "__main__":
    app.run(debug=True)
import pickle
import yaml

keskm = []
kerged = []
rasked = []

# Kõigepealt salvestan yaml failidena, et saaks käsitsi üle vaadata
# ja seejärel salvestan pickle failidena lõppversiooni
with open('saveKerged.pickle', 'rb') as handle:
    kerged = pickle.load(handle)
with open('kerged.yaml', 'w') as file:
    yaml.dump(kerged, file)

with open('saveKeskm.pickle', 'rb') as handle:
    keskm = pickle.load(handle)
with open('keskmised.yaml', 'w') as file:
    yaml.dump(keskm, file)

with open('saveRasked.pickle', 'rb') as handle:
    rasked = pickle.load(handle)
with open('rasked.yaml', 'w') as file:
    yaml.dump(rasked, file)

# Alumise osa võiks välja kommenteerida, et saaks yaml failid salvestada
# seejärel vaata üle, mis sõnad eemaldada ning kommenteeri ülemine osa välja
# ja jooksuta alumine osa, et salvestada tagasi pickle failid
with open('kerged.yaml', 'r') as file:
    kerged = yaml.safe_load(file)
with open('keskmised.yaml', 'r') as file:
    keskm = yaml.safe_load(file)
with open('rasked.yaml', 'r') as file:
    rasked = yaml.safe_load(file)
with open('saveKerged.pickle', 'wb') as handle:
    pickle.dump(kerged, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('saveKeskm.pickle', 'wb') as handle:
    pickle.dump(keskm, handle, protocol=pickle.HIGHEST_PROTOCOL)    
with open('saveRasked.pickle', 'wb') as handle:
    pickle.dump(rasked, handle, protocol=pickle.HIGHEST_PROTOCOL)

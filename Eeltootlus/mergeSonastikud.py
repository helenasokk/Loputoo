import pickle

sõnastik1 = {}
with open('saveLausedKerged500.pickle', 'rb') as handle:
    sõnastik1 = pickle.load(handle)

sõnastikud = ['saveLausedKerged1000.pickle', 'saveLausedKerged1452.pickle',
             'saveLausedKeskm500.pickle', 'saveLausedKeskm1000.pickle', 'saveLausedKeskm1500.pickle',
             'saveLausedKeskm2000.pickle', 'saveLausedKeskm2500.pickle', 'saveLausedKeskm3000.pickle',
             'saveLausedKeskm3500.pickle', 'saveLausedKeskm4000.pickle', 'saveLausedKeskm4500.pickle',
             'saveLausedKeskm5000.pickle', 'saveLausedKeskm5302.pickle', 'saveLausedRasked500.pickle', 'saveLausedRasked1000.pickle', 'saveLausedRasked1500.pickle',
             'saveLausedRasked2000.pickle', 'saveLausedRasked2500.pickle', 'saveLausedRasked3000.pickle',
             'saveLausedRasked3500.pickle', 'saveLausedRasked4000.pickle', 'saveLausedRasked4500.pickle',
             'saveLausedRasked5000.pickle', 'saveLausedRasked5500.pickle', 'saveLausedRasked6000.pickle',
             'saveLausedRasked6500.pickle', 'saveLausedRasked7000.pickle', 'saveLausedRasked7337.pickle']
for fail in sõnastikud:
    with open(fail, 'rb') as handle:
        sõnastik2 = pickle.load(handle)
        sõnastik1.update(sõnastik2)

with open('saveLaused.pickle', 'wb') as handle:
    pickle.dump(sõnastik1, handle, protocol=pickle.HIGHEST_PROTOCOL)
from nltk import download

models = ['punkt', 'averaged_perceptron_tagger']
corpora = ['words']

for e in models + corpora:
    download(e)


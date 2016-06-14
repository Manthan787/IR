from pycorenlp import StanfordCoreNLP
import nltk
from nltk.tokenize import word_tokenize


def parse(text):
    nlp = StanfordCoreNLP('http://localhost:9000')
    #
    # text = "Document will identify acquisition by the U.S. Army of specified advanced weapons systems."
    # text1 = "Document will report actual studies, or even unsubstantiated concerns about the safety to manufacturing employees and installation workers of fine-diameter fibers used in insulation and other products."
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,pos,depparse',
        'outputFormat': 'json'
    })

    dg = output['sentences'][0]['basic-dependencies']
    avoid = []
    for dep in dg:
        if dep['dep'] == 'ROOT':
            avoid.append(dep['dependentGloss'])

        if dep['dep'] == 'amod':
            avoid.append(dep['dependentGloss'])

        # if dep['dep'] == 'nmod':
        #     avoid.append(dep['dependentGloss'])

        if dep['dep'] == 'advmod':
            avoid.append(dep['dependentGloss'])

        if dep['dep'] == 'compound':
             avoid.append(dep['dependentGloss'])

    return avoid



# tags = nltk.pos_tag(tokens)
#
# final = []
#
# avoid = ['VBZ', 'DT', 'IN', 'CD', 'WDT', 'MD']
#
# for tag in tags:
#     if not tag[1] in avoid:
#         final.append(tag[0])
#
# print final

#Tutorial -  https://nlpforhackers.io/wordnet-sentence-similarity/
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')

def penn_to_wn(tag):
    """ Convert between a Penn Treebank tag to a simplified Wordnet tag """
    if tag.startswith('N'):
        return 'n'
 
    if tag.startswith('V'):
        return 'v'
 
    if tag.startswith('J'):
        return 'a'
 
    if tag.startswith('R'):
        return 'r'
 
    return None
 
def tagged_to_synset(word, tag):
    wn_tag = penn_to_wn(tag)
    if wn_tag is None:
        return None
 
    try:
        return wn.synsets(word, wn_tag)[0]
    except:
        return None
 
def sentence_similarity(sentence1, sentence2):
    """ compute the sentence similarity using Wordnet """
    # Tokenize and tag
    sentence1 = pos_tag(word_tokenize(sentence1))
    sentence2 = pos_tag(word_tokenize(sentence2))
 
    # Get the synsets for the tagged words
    synsets1 = [tagged_to_synset(*tagged_word) for tagged_word in sentence1]
    synsets2 = [tagged_to_synset(*tagged_word) for tagged_word in sentence2]
 
    # Filter out the Nones
    synsets1 = [ss for ss in synsets1 if ss]
    synsets2 = [ss for ss in synsets2 if ss]
 
    score, count = 0.0, 0
    arr_simi_score = []

    for syn1 in synsets1:
      for syn2 in synsets2:
        simi_score = syn1.path_similarity(syn2)
        if simi_score is not None:
          arr_simi_score.append(simi_score)
          best = max(arr_simi_score)
          score += best
          count += 1


    # # For each word in the first sentence
    # for synset in synsets1:
    #     # Get the similarity value of the most similar word in the other sentence
    #     best_score = max([synset.wup_similarity(ss) for ss in synsets2])
 
    #     # Check that the similarity could have been computed
    #     if best_score is not None:
    #         score += best_score
    #         count += 1
 
    # Average the values
    score /= count
    return score
 
sentences = [
    "Dogs are awesome.",
    "Some gorgeous creatures are felines.",
    "Dolphins are swimming mammals.",
    "Cats are beautiful animals.",
]

focus_sentence = "Cats are beautiful animals."
 
for sentence in sentences:
    print("Similarity(\"%s\", \"%s\") = %s" % (focus_sentence, sentence, sentence_similarity(focus_sentence, sentence)))
    print("Similarity(\"%s\", \"%s\") = %s" % (sentence, focus_sentence, sentence_similarity(sentence, focus_sentence)))
    print() 
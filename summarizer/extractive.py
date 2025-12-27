import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

nlp = spacy.load("en_core_web_sm")

def extractive_summary_nlp(text, ratio=0.3):
    doc = nlp(text)

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in STOP_WORDS and word.text not in punctuation:
            word_frequencies[word.text.lower()] = word_frequencies.get(word.text.lower(), 0) + 1

    max_freq = max(word_frequencies.values()) if word_frequencies else 1
    for word in word_frequencies:
        word_frequencies[word] /= max_freq

    sentence_scores = {}
    for sent in doc.sents:
        for word in sent:
            if word.text.lower() in word_frequencies:
                sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word.text.lower()]

    select_len = max(1, int(len(sentence_scores) * ratio))
    top_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:select_len]

    summary = " ".join([str(s).strip() for s in top_sentences])
    return summary

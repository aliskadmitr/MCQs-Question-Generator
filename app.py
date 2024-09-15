import spacy
import random
from collections import Counter


nlp = spacy.load("en_core_web_sm")

def generate_mcqs(text, num_questions=5):
    if text is None:
        return []

    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]
    num_questions = min(num_questions, len(sentences))
    selected_sentences = random.sample(sentences, num_questions)

    mcqs = []

    for sentence in selected_sentences:
        sent_doc = nlp(sentence)
        nouns = [token.text for token in sent_doc if token.pos_ == "NOUN"]

        if len(nouns) < 2:
            continue

        noun_counts = Counter(nouns)

        if noun_counts:
            subject = noun_counts.most_common(1)[0][0]
            question_stem = sentence.replace(subject, "______")
            answer_choices = [subject]
            distractors = list(set(nouns) - {subject})

            while len(distractors) < 3:
                distractors.append("[Distractor]")  

            random.shuffle(distractors)
            for distractor in distractors[:3]:
                answer_choices.append(distractor)

            random.shuffle(answer_choices)

            correct_answer = chr(64 + answer_choices.index(subject) + 1) 
            mcqs.append((question_stem, answer_choices, correct_answer))

    return mcqs
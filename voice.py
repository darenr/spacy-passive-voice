import spacy, json
from spacy.matcher import Matcher


class Voice:
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')
        self.matcher = Matcher(self.nlp.vocab)
        self.matcher.add('passive-voice', None, [
            {'DEP': 'nsubjpass'},
            {'DEP': 'aux', 'OP': '*'},
            {'DEP': 'auxpass'},
            {'TAG': 'VBN'}
        ])

    def passive(self, text):
        for sent in self.nlp(text).sents:
            if self.matcher(sent):
                for (_, start, end) in self.matcher(sent):
                    span = sent[start:end]
                    yield (sent, span)

if __name__ == '__main__':
    
    v = Voice()

    with open('test-data/data.json', 'r') as f:
        docs = json.loads(f.read())
        passive_text = ' '.join(docs['passive_sentences'])
        active_text = ' '.join(docs['active_sentences'])

        print("\n\nActive sentences:")
        for sentence, passive_span in v.passive(active_text):
            print(f'passive span: "{passive_span}"')

        print("\n\nPassive sentences:")
        for sentence, passive_span in v.passive(passive_text):
            print(f'passive span: "{passive_span}"')

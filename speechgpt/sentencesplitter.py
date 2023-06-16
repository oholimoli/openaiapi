import re

class SentenceSplitter:
    def __init__(self, text):
        self.sentences = re.findall(r'(?ms)(?:^|\.\s)(.*?)(?=(?:\.\s|$))', text)

    def pop_sentence(self):
        if self.sentences:
            return self.sentences.pop(0)
        else:
            return None

    @property
    def sentence_list(self):
        return self.sentences
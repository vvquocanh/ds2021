import re
from collections import defaultdict

def tokenize(message):
    message = message.lower()
    all_words = re.findall("[a-z0-9']+", message)
    return set(all_words)

def wc_mapper(document):
    for word in tokenize(document):
        yield(word, 1)

def wc_reducer(word, counts):
    yield (word, sum(counts))

def word_count(documents):
    collector = defaultdict(list)
    for document in documents:
        for word, count in wc_mapper(document):
            collector[word].append(count)
    return [output
           for word, counts in collector.items()
           for output in wc_reducer(word, counts)]

docs = ["In as name to here them deny wise this. As rapid woody my he me which. Men but they fail shew just wish next put. Led all visitor musical calling nor her. Within coming figure sex things are. Pretended concluded did repulsive education smallness yet yet described. Had country man his pressed shewing. No gate dare rose he. Eyes year if miss he as upon."]

word_count(docs)
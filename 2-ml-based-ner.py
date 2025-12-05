import spacy

# Add a  example text from Harry Potter books
text = """
Mr. Dusley was a big, beefy man with hardly any neck, although he did have a very large mustache. He was what is known in the trade as a big beefy man. 
Mrs Dusley was thin and blonde and had nearly twice the usual amount of neck, which came in very useful as she spent so much of her time craning over garden fences,
spying on the neighbors. The Dusleys had a small son called Dudley and in their opinion there was no finer boy anywhere.
The Dursleys lived at number four, Privet Drive, which was in a small town in England. They were proud to say that they were perfectly normal, thank you very much.
They were the last people you'd expect to be involved in anything strange or mysterious, because they just didn't hold with such nonsense.
"""

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
for doc in doc.ents:
    print(f"Found Characters: {doc.text} - Type: {doc.label_}")
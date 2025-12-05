import spacy
from spacy.lang.en import English
import json


def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def save_data(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def generate_better_characters(file):
    data = load_data(file)
    print(len(data))
    new_characters=[]
    for item in data:
        new_characters.append(item)
    for item in data:
        item=item.replace("The", "").replace("the", "").replace("And", "").replace("and", "")
        names = item.split(" ")
        for name in names:
            name = name.strip()
            new_characters.append(name)
        if "(" in item:
            names = item.split("(")
            for name in names:
                name = name.replace(")", "").strip()
                new_characters.append(name)
        if "," in item:
            names = item.split(",")
            for name in names:
                name = name.replace("and", "").strip()
                if " " in name:
                    new_names = name.split(" ")
                    for n in new_names:
                        n = n.strip()   
                        new_characters.append(n)
                new_characters.append(name)  
    final_characters=[]
    titles = ["Mr.", "Mrs.", "Miss", "Ms.", "Dr.", "Sir", "Lady", "Lord", "Aunt", "Uncle", "Professor"]
    for character in new_characters:
        if "" in character or len(character)<=0:
            final_characters.append(character)
            for title in titles:
                titled_chars = f"{title} {character}"
                final_characters.append(titled_chars)
            
    print(len(final_characters))   
    final_characters = list(set(final_characters))  
    print(len(final_characters))    
    return final_characters
                        

def create_training_data(file, type):
    data = generate_better_characters(file)
    patterns = []
    for item in data:
        pattern = {"label": type, "pattern": item} 
        patterns.append(pattern)  
    return patterns 


def generate_rules(patterns):
    nlp = English()
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns)
    nlp.to_disk("hp_ner_model")    
    
def test_model(model, text):
    doc = nlp(text)
    results=[]
    for ent in doc.ents:
        results.append(ent.text)    
    return results
 
#To create the model, uncomment the following lines and run the script                       
#patterns=create_training_data('data/hp_characters.json', 'PERSON')
#generate_rules(patterns)

nlp = spacy.load("hp_ner_model")
ie_data={}
with open('data/hp.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    
    chapters = text.split('CHAPTER')[1:]
    for chapter in chapters:
        chapter_num, chapter_text = chapter.strip().split('\n\n')[0:2]
        chapter_num = chapter_num.strip()
        segments = chapter.split('\n\n')[2:]
        hits=[]
        for segment in segments:
            segment = segment.strip()
            segment = segment.replace('\n', ' ')
            results = test_model(nlp, segment)
            for result in results:
                hits.append(result)
        ie_data[chapter_num] = list(set(hits))
        
save_data('data/hp_ie_data.json', ie_data)
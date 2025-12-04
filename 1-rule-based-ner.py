import json

with open('data/hp.txt', 'r', encoding='utf-8') as f:
    text = f.read().split('\n\n')[1:5]
    #print(text)
    
characters_name=[]
with open('data/hp_characters.json', 'r', encoding='utf-8') as f:
    characters = json.load(f)
    for character in characters:
        names = character.split(" ")
        for name in names:
            if "and" != name and "the" != name and "The" != name:
                name= name.replace(",", "").strip()
                characters_name.append(name)
    
for segment in text:
    segment = segment.strip()
    segment = segment.replace('\n', ' ')
    
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    for ele in segment:
        if ele in punc:
            segment = segment.replace(ele, "")
    
    words = segment.split(" ")
    
    i=0
    for word in words:
        if word in characters_name:
            if words[i-1][0].isupper():
                print(f"Found Characters: {words[i-1]} {word}")
            else:
                print(f"Found Characters: {word}")
        i+=1
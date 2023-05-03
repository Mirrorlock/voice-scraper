import os

from fasttext import load_model

m = load_model(os.getenv('MODEL', "action.bin"))

def get_label_text(label):
    label_sub = '__label__'
    return label.replace(label_sub, '')

sentences = """
    What will the weather be like today?
    Will it be sunny today?
    Will it rain today?
    Will it be windy today?
    Should I bring an umbrella?
    Should I wear an umbrella?
    How hot will it be?
    Will I be hot?

    What is the time in Turgistan
    What is the time here?
    What time is it in New York?
    What time is it in Budapest?
    What is the time in Austria?

    Why not laugh a little
    Tell me a joke.
    Tell me something funny
    What jokes do you know?
    I'm sad

    Which is the highest peek in the world?
    Who is the best swimmer?
    When was Shawn Menedes born?
    How to tie a knot?
    What is required for a nice campfire?

    Tell me the news today?
    Read me the news.
    What is happening in the world today?
    Give me the news today?
    What's new?
"""
for sentence in sentences.split("\n"): 
    if(sentence != ""):
        sentence = sentence.strip()
        print(sentence)   
        labels, probs = m.predict(sentence)
        for l, p in zip(labels, probs):
            print("Label: ", get_label_text(l))
            print("Probability: ", p)
            print()
    else:
        print("-"*20, "\n")
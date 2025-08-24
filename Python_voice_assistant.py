import pyttsx3

import wikipedia

assistant = pyttsx3.init()

SearchBar = input("Search here: ")

SearchResult = wikipedia.summary(SearchBar, sentences = 4)
print(SearchResult)

assistant.say(SearchResult)

assistant.runAndWait()



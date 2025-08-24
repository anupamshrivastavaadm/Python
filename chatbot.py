import pyttsx3
import wikipediaapi

# Initialize text-to-speech
assistant = pyttsx3.init()

# Create Wikipedia object with user agent
wiki = wikipediaapi.Wikipedia(
    language="en",
    user_agent="MyWikipediaChatbot/1.0 (https://example.com)"
)

print("🤖 Wikipedia Assistant (type 'exit' to quit)\n")

while True:
    SearchBar = input("Search here: ")

    if SearchBar.lower() in ["exit", "quit", "bye"]:
        print("Goodbye! 👋")
        assistant.say("Goodbye! Have a nice day.")
        assistant.runAndWait()
        break

    page = wiki.page(SearchBar)

    if page.exists():
        info = page.text[:5000]  # first 5000 characters
        print(f"\n{info}\n")
        assistant.say(info)
        assistant.runAndWait()
    else:
        print("\nNo data found, try again.\n")
        assistant.say("No data found, try again.")
        assistant.runAndWait()

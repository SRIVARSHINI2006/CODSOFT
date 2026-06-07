import datetime

print("=== SmartBot ===")
print("Type 'bye' to exit")

while True:
    user = input("You: ").lower()

    if user in ["hi", "hello", "hey"]:
        print("Bot: Hello! How can I help you?")

    elif "name" in user:
        print("Bot: My name is SmartBot.")

    elif "time" in user:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print("Bot: Current time is", current_time)

    elif "date" in user:
        current_date = datetime.datetime.now().strftime("%d-%m-%Y")
        print("Bot: Today's date is", current_date)

    elif "help" in user:
        print("Bot: I can answer greetings, date, time and name related questions.")

    elif user in ["bye", "exit", "quit"]:
        print("Bot: Goodbye!")
        break

    else:
        print("Bot: Sorry, I don't understand that.")
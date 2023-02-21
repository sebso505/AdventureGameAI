import openai
import random

# Setting the OpenAI API key
openai.api_key = "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"

# Prompt for the name
name = "Johnny"
book = "Harry Potter"

text_prompt = f"I want you to act as if you are a classic text adventure game and we are playing.Do not break character, or refer to yourself in any way.The setting of this text-based game will be in {book} in which myself is the main character {name}.Each room or location should have at least 3 sentence descriptions."

#CREATE A INTRO

intro = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"{text_prompt} + Begin by describing the first room or location.",
    max_tokens=1000,
    n=1,
    stop=None,
    temperature=0.5,
).get("choices")[0].text


plot = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"{text_prompt} + {intro}. Create the plot of the game.",
    max_tokens=1000,
    n=1,
    stop=None,
    temperature=0.5,
).get("choices")[0].text
print(plot)


choices = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"{text_prompt} + {intro} + {plot}. Generate 3 choices for me to choose. One is always bad and ends the game",
    max_tokens=1000,
    n=1,
    stop=None,
    temperature=0.5,
).get("choices")[0].text.split("\n")

for i,choice in enumerate(choices):
    print(f"{choice}")

choice_num = input("Please choose the number of your choice: ")
choice = choices[int(choice_num) - 1]

text_prompt_second = f"I want you to act as if you are a classic text adventure game and we are playing.Do not break character, or refer to yourself in any way.The setting of this text-based game will be in {book} in which myself is the main character {name}.Each room or location should have at least 3 sentence descriptions. A choice has been made. The choice is {choices}. Continue the story based on that choice"

outcome = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"{text_prompt_second} + {choice}. Continue the story.",
    max_tokens=1000,
    n=1,
    stop=None,
    temperature=0.5,
).get("choices")[0].text
print(outcome)

while True:
    text_prompt_second = f"I want you to act as if you are a classic text adventure game and we are playing.Do not break character, or refer to yourself in any way.The setting of this text-based game will be in {book} in which myself is the main character {name}.Each room or location should have at least 3 sentence descriptions. A choice has been made. The choice is {choices}. Continue the story based on that choice"

    choices = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{text_prompt_second} + {outcome}. Generate 3 choices for me to choose. One is always bad and ends the game",
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    ).get("choices")[0].text.split("\n")
    print("Choose one of the following: ")

    for i, choice in enumerate(choices):
        print(f"{choice}")

    choice_num = input("Please choose the number of your choice: ")
    choice = choices[int(choice_num) - 1]



    outcome_continue = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{text_prompt_second} + {choice}. Continue the story.",
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.5,
    ).get("choices")[0].text
    print(outcome_continue)

    # Check if the outcome results in the character's death
    if "game over" in outcome.lower():
        print("You have died. Game over.")
        break
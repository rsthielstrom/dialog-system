from character_class import Character
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

print("Sitting in front of you on a lilypad is a toad. What would you like to say to it?")

str = ""
while str!="goodbye":
    str = input(">")
    llm_model = ChatOllama(
            model="llama3.1",
            temperature=0,
        )
    toad = Character(llm_model, 'toad')
    answer = toad.address(str)
    print(answer)
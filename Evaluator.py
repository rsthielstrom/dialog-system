from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

'''Semantic interpreter class for converting incoming text to semantics.'''
class Evaluator:

    def __init__(self, llm_model):
        # Define the prompt template for the LLM
        prompt = PromptTemplate(
            template="""
            Character information:
            {personal}  
            Context:
            {world}
            {speaker}
            Respond in character to the input below in a way that attempts to fulfill your personal goals.
            If the Interpretation notes there is missing information needed, respond in a way that solicits that missing information.
            Use two sentences maximum and keep the sentences short:
            Input: {question}
            Next action:
            """,
            input_variables=["question","personal","world","speaker"],
        )

        llm = llm_model
        # Create a chain combining the prompt template and LLM
        self.rag_chain = prompt | llm | StrOutputParser()

    def plan(self, input, interpretation, speaker, personal, world):
    
        answer = self.rag_chain.invoke({"question":input,"interpretation":interpretation,"speaker":speaker,"personal":personal,"world":world})
        return answer
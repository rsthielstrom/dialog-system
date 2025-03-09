from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

'''Semantic interpreter class for converting incoming text to semantics.'''
class Interpreter:

    def __init__(self, llm_model):
        # Define the prompt template for the LLM
        interpret_prompt = PromptTemplate(
            template="""You are an assistant for tasks in which semantic meaning is extracted from textual input.
            Classify the input as one or more of these three categories: Information Request, Action Request, Emotional Expression, Informational Statement.
            Then use the Context to determine the speaker's intent. Use two sentences maximum:
            Context: {context}
            Input: {question}
            Classification and Intent:
            """,
            input_variables=["question","context"],
        )
        inforequest_prompt = PromptTemplate(
            template="""
            Can the answer to the speaker's question be found or inferred from the following Context? If not, identify what information is missing.
            Use two sentences maximum:
            Context: 
            {speaker_context}
            {self_context}
            {world_context}
            Question: {question}
            Answer:
            """,
            input_variables=["question","speaker_context","self_context","world_context"],
        )
        actionrequest_prompt = PromptTemplate(
            template="""You are an informational assistant. Determine what action would fulfill the following Action Request. Use two sentences maximum:
            Speaker Context: {speaker_context}
            Self Context: {self_context}
            World Context: {world_context}
            Information Request: {question}
            Answer:
            """,
            input_variables=["question","speaker_context","self_context","world_context"],
        )
        stmt_prompt = PromptTemplate(
            template="""You are an informational assistant. Are there any pieces of information in the following Contexts that would contradict the information in the Supplied Statement? Use two sentences maximum:
            Speaker Context: {speaker_context}
            Self Context: {self_context}
            World Context: {world_context}
            Supplied Statement: {question}
            Answer:
            """,
            input_variables=["question","speaker_context","self_context","world_context"],
        )

        llm = llm_model
        # Create a chain combining the prompt template and LLM
        self.interpret_chain = interpret_prompt | llm | StrOutputParser()
        self.inforequest_chain = inforequest_prompt | llm | StrOutputParser()
        self.actionrequest_chain = actionrequest_prompt | llm | StrOutputParser()
        self.stmt_chain = stmt_prompt | llm | StrOutputParser()


    def interpret(self, input, speaker_context, self_context, world_context):
        #interpret question, command, or statement
        answer = self.interpret_chain.invoke({"question": input,"context": speaker_context})
        print(answer)
        intentindex = answer.index("**Intent:**")
        categoryindex = answer.index("**Classification:**")+20 
        print(categoryindex,intentindex)
        category = answer[categoryindex:intentindex]
        if categoryindex!=None:
            intent = answer[intentindex:len(answer)]
        print(category)
        if category.strip()=="Information Request":
            answer = self.inforequest_chain.invoke({"question": input,"speaker_context": speaker_context, "self_context": self_context, "world_context": world_context})
        if category.strip()=="Action Request":
            answer = self.actionrequest_chain.invoke({"question": input,"speaker_context": speaker_context, "self_context": self_context, "world_context": world_context})
        if category.strip()=="Informational Statement":
            answer = self.stmt_chain.invoke({"question": input,"speaker_context": speaker_context, "self_context": self_context, "world_context": world_context})
        return answer

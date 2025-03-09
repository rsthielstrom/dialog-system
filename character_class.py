from Interpreter import Interpreter
from Evaluator import Evaluator

class Character:
    
    def __init__(self, llm_model, name):
        #set up llm
        self.llm = llm_model

        #set up database
        self.speaker_model = self.read_from_file(name+'/speaker.txt')
        self.self_model = self.read_from_file(name+'/self.txt')
        self.world_model = self.read_from_file(name+'/world.txt')
        print(self.speaker_model)

        self.interpreter = Interpreter(llm_model)
        self.evaluator = Evaluator(llm_model)

    def read_from_file(self,filepath):
        """
        Loads the content of a text file into a string.
            filepath: The path to the text file.

        Returns a string, or None if an error occurs.
        """
        try:
            with open(filepath, 'r') as file:
                file_content = file.read()
            return file_content
        except FileNotFoundError:
            print(f"Error: File not found at {filepath}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    def address(self,input):
        interpretation = self.interpreter.interpret(input,self.speaker_model,self.self_model,self.world_model)
        print(f"Interpretation: {interpretation}")
        return self.evaluator.plan(input,interpretation,self.speaker_model,self.self_model,self.world_model)
    

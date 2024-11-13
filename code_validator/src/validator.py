from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import subprocess

class CodeValidator:
    def __init__(self, vector_store):
        self.vector_store = vector_store
        self.llm = Ollama(model="mistral")
        
        self.validation_prompt = PromptTemplate(
            input_variables=["original_code", "modified_code", "context"],
            template="""
            You are a C code validation expert. Analyze the following code change:
            
            Original Code:
            {original_code}
            
            Modified Code:
            {modified_code}
            
            Similar code examples from the codebase:
            {context}
            
            Determine if the modification is valid based on:
            1. Syntactic correctness
            2. Semantic similarity to existing patterns
            3. Preservation of core functionality
            
            Provide your analysis and verdict (valid/invalid) with explanation.
            """
        )
        
        self.chain = LLMChain(llm=self.llm, prompt=self.validation_prompt)
    
    def check_syntax(self, code):
        with open('temp.c', 'w') as f:
            f.write(code)
        try:
            subprocess.run(['gcc', '-fsyntax-only', 'temp.c'], 
                         check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def validate_change(self, original_code, modified_code):
        # Get relevant context from vector store
        docs = self.vector_store.similarity_search(modified_code, k=3)
        context = "\n".join([doc.page_content for doc in docs])
        
        # First check syntax
        if not self.check_syntax(modified_code):
            return {
                "is_valid": False,
                "explanation": "Syntax error in modified code"
            }
        
        # Get LLM analysis
        result = self.chain.run({
            "original_code": original_code,
            "modified_code": modified_code,
            "context": context
        })
        
        return result

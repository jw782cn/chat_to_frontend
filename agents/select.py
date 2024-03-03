from agents.state import *


select_template = """
You are building a frontend using components selected from shadcn library.
Generate a list of needed components based on the context and query. 

Instructions:
- include as many components as needed.
- include at least 3 components, no more than 10 components.
- only select from provided components.

---

Follow the following format.

Question: a query to build a frontend using components selected from shadcn library

Components: a list of components in shadcn library

Reasoning: Let's think step by step in order to ${{produce the needed_components}}. We ...

Needed Components: a full list of needed components name, rememeber to include .tsx, separated by comma, only output name, no verbose!

---

Question: {question}

Components: {components}

Reasoning: Let's think step by step in order to"""

class SelectAgent:
    """Select the needed components based on the question and components."""
    
    def __init__(self, components: str, model: str = "gpt-3.5-turbo-0125"):
        self.components = components
        self.model = model

    def select_parser(self, result: str):
        # only need the last part of the result
        result = result.split("Needed Components:")[-1]
        file_names = [name.strip() for name in result.split(",") if name.strip()]
        return file_names

    def select(self, state: AgentState):
        question = state["question"]
        prompt = PromptTemplate(
            template=select_template, input_variables=["question"], partial_variables={"components": self.components}
        )
        llm = ChatOpenAI(temperature=0.1, max_tokens=1024, model=self.model)
        parser = StrOutputParser()
        llm_chain = (
            prompt 
            | llm 
            | parser
            )
        result = llm_chain.invoke({"question": question})
        file_names = self.select_parser(result)
        state["file_names"] = file_names
        return state

    def run(self, state: AgentState):
        return self.select(state)
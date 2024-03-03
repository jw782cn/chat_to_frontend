from agents.state import *

outline_template = """
You are building a frontend using components selected from shadcn library.
Generate a frontend outline based on provided components and user question.

Instructions:
- Use the components selected.
- Use bullet points to describe the structure.
- Include detailed instructions for your colleague to follow. You need to describe ideally what this frontend will look like

---

Follow the following format.

Question: a query to build a frontend using components selected from shadcn library

Components Selected: a list of components that can need to be used.

Components: nessary components in shadcn library

Reasoning: Let's think step by step in order to ${{produce the frontend_outline}}. We ...

Frontend Outline: a frontend outline based on the retrieved components and query, use bullet points to describe the structure

---

Question: {question}

Components Selected: {selected_components}

Components: {components}

Reasoning: Let's think step by step in order to"""


class OutlineAgent:
    
    def __init__(self, df, model: str = "gpt-3.5-turbo-0125"):
        self.model = model
        self.df = df

    def outline_parser(self, result: str):
        # only need the last part of the result
        result = result.split("Frontend Outline:")[-1]
        return result
    
    def retrieve_components(self, state: AgentState):
        file_names = state["file_names"]
        combined_contexts = get_combined_contexts(self.df, file_names)
        components = contexts_to_string(combined_contexts)
        return components

    def outline(self, state: AgentState):
        question = state["question"]
        components = self.retrieve_components(state)
        file_names = state["file_names"]
        selected_components = ", ".join(file_names)
        prompt = PromptTemplate(
            template=outline_template, input_variables=["question"], partial_variables={"components": components, "selected_components": selected_components}
        )
        llm = ChatOpenAI(temperature=0.1, max_tokens=1024, model=self.model)
        parser = StrOutputParser()
        llm_chain = (
            prompt 
            | llm 
            | parser
            )
        result = llm_chain.invoke({"question": question})
        result = self.outline_parser(result)
        state["frontend_outline"] = result
        return state

    def run(self, state: AgentState):
        return self.outline(state)
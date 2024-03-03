from agents.state import *

code_template = """
Generate a frontend code based on the shadcn components, query and frontend outline. Choose from the components in shadcn library. 
Follow the frontend outline step by step.
1. Use tailwind to make grid and layout.
2. Use components to make the structure. But you don't have to use all the components. Choose the components that fit the best.
3. Refer to the description to import the components.
4. always generate whole page.tsx.
5. dont use fake image.
6. assume that the components are already imported.
I will tip you 1000$ for complete the whole code without skipping any codes!!!!

---

Follow the following format.

Question: a query to build a frontend using components selected from shadcn library

Components: nessary components in shadcn library

Frontend Outline: a frontend outline based on the retrieved components and query, use bullet points to describe the structure

Reasoning: Let's think step by step in order to ${{produce the frontend_code}}. We ...

Frontend Code: a frontend code. Only output the code, no verbose!

---
{example_code}
---

Question: {question}

Components: {components}

Frontend Outline: {frontend_outline}

Reasoning: Let's think step by step in order to"""


class CodeAgent:
    
    def __init__(self, df, model: str = "gpt-4-turbo-preview"):
        self.model = model
        self.df = df

    def code_parser(self, result: str):
        result = result.split("Frontend Code:")[-1]
        # only need code snippet between ```tsx and ```
        result = result.split("```tsx")[1].split("```")[0]
        return result
    
    def retrieve_components(self, state: AgentState):
        file_names = state["file_names"]
        combined_contexts = get_combined_contexts(self.df, file_names)
        components = contexts_to_string(combined_contexts)
        return components

    def coding(self, state: AgentState):
        question = state["question"]
        components = self.retrieve_components(state)
        file_names = state["file_names"]
        selected_components = ", ".join(file_names)
        frontend_outline = state["frontend_outline"]
        prompt = PromptTemplate(
            template=code_template, input_variables=["question"], partial_variables={"components": components, "frontend_outline": frontend_outline, "example_code": example_code}
        )
        llm = ChatOpenAI(temperature=0.1, max_tokens=1024, model=self.model)
        parser = StrOutputParser()
        llm_chain = (
            prompt 
            | llm 
            | parser
            )
        result = llm_chain.invoke({"question": question})
        result = self.code_parser(result)
        state["codes"] = result
        return state

    def run(self, state: AgentState):
        return self.coding(state)
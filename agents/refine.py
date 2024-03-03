from agents.state import *

refine_template = """
You are very strict about tsx coding!
Refine a code based on the shadcn components, query and frontend outline.
- Use tailwind to make grid and layout.
- Refer to the description to import the components.
- always generate whole page.tsx.
- dont use fake image.
- expand any placeholder in the code.
- remember this is not a component but a page.tsx.
- output the whole codes.
- make this code as real as possible, add necessary texts, fake data to make it look real.
- choose black, gray and white as the main color.
- add more details please.

I will tip you 1000$ for complete the whole code without skipping any codes!!!!

---

Follow the following format.

Question: a query to build a frontend using components selected from shadcn library

Components: nessary components in shadcn library

Reasoning: Let's think step by step in order to ${{produce the frontend_code}}. We ...

Frontend Code: a frontend code. Only output the code, no verbose!

---

Question: {question}

Components Example: {components}

Reasoning: Let's think step by step in order to"""


class RefineAgent:
    
    def __init__(self, df, model: str = "gpt-4-turbo-preview"):
        self.model = model
        self.df = df

    def output_parser(self, result: str):
        result = result.split("Frontend Code:")[-1]
        # only need code snippet between ```tsx and ```
        result = result.split("```tsx")[1].split("```")[0]
        # add "use client" if not exist at the front
        if "use client" not in result:
            result = "\"use client\"\n" + result
        return result
    
    def retrieve_components(self, state: AgentState):
        file_names = state["file_names"]
        combined_contexts = get_combined_contexts(self.df, file_names)
        components = contexts_to_string(combined_contexts)
        return components

    def coding(self, state: AgentState):
        question = state["question"]
        components = self.retrieve_components(state)
        prompt = PromptTemplate(
            template=refine_template, input_variables=["question"], partial_variables={"components": components}
        )
        llm = ChatOpenAI(temperature=0.1, max_tokens=2048, model=self.model)
        parser = StrOutputParser()
        llm_chain = (
            prompt 
            | llm 
            | parser
            )
        result = llm_chain.invoke({"question": question})
        result = self.output_parser(result)
        state["codes"] = result
        return state

    def run(self, state: AgentState):
        return self.coding(state)
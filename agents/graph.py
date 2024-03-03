from agents.state import *
from agents.refine import RefineAgent
from agents.code import CodeAgent
from agents.outline import OutlineAgent
from agents.select import SelectAgent
from langgraph.graph import StateGraph, END


class FrontendAgent:
    def __init__(self, data_path: str = "..\data\shadcn.csv", refine_nums: int = 1):
        self.df = pd.read_csv(data_path, index_col=False)
        self.components = read_combined_file(data_path)
        self.refine_nums = refine_nums
        self.set_app()
    
    def set_app(self):
        selectAgent = SelectAgent(components=self.components)
        outlineAgent = OutlineAgent(df=self.df)
        codeAgent = CodeAgent(df=self.df)
        refineAgent = RefineAgent(df=self.df)

        # Define a new graph
        workflow = StateGraph(AgentState)

        # Define the two nodes we will cycle between
        workflow.add_node("select", selectAgent.run)
        workflow.add_node("outline", outlineAgent.run)
        workflow.add_node("code", codeAgent.run)
        workflow.add_node("refine", refineAgent.run)

        # Define the edges between the nodes
        workflow.add_edge("select", "outline")
        workflow.add_edge("outline", "code")
        workflow.add_edge("code", "refine")
        workflow.add_edge("refine", END)

        # Set the entrypoint as `select`
        # This means that this node is the first one called
        workflow.set_entry_point("select")
        self.app = workflow.compile()
    
    def run(self, question: str):
        inputs = {"question": question}

        # streaming output from the graph, yielding the output of each node
        for output in self.app.stream(inputs):
            # stream() yields dictionaries with output keyed by node name
            for key, value in output.items():
                # select -> file_names
                # outline -> frontend_outline
                # code -> codes
                # refine -> codes
                # different output from different node
                if key == "select":
                    yield {"node": key, "output": value["file_names"]}
                elif key == "outline":
                    yield {"node": key, "output": value["frontend_outline"]}
                elif key == "code":
                    yield {"node": key, "output": value["codes"]}
                elif key == "refine":
                    yield {"node": key, "output": value["codes"]}
        yield {"node": "end", "output": "end"}
        return
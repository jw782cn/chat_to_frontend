from typing import TypedDict, List

from langchain.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers.json import SimpleJsonOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

from agents.utils import *
from agents.example import example_code


class AgentState(TypedDict):
    question: str
    file_names: List[str]
    frontend_outline: str
    codes: str


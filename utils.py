import tiktoken
import pandas as pd

def num_tokens_from_string(string: str, model="gpt-3.5-turbo-0613") -> int:
    """Returns the number of tokens in a text string based on the specified model's encoding."""
    try:
        encoding = tiktoken.encoding_for_model(model)  # Attempt to get encoding for the specified model
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")  # Fallback encoding if model's encoding not found

    num_tokens = len(encoding.encode(string))  # Calculate number of tokens based on encoding
    return num_tokens


def retrieve_component_from_df(df, file_name):
    # only return json object
    data_entry = df[df['file_name'] == file_name]
    # return the first one
    # if not exist, return empty json object
    if data_entry.empty:
        return {}
    return data_entry.to_dict(orient='records')[0]

def get_combined_context_string(data_entry):
    # include file_name, description, usage_example, file_content
    # use mdx description instead
    context = f"----- START OF {data_entry['file_name']} -----\
    {data_entry['mdx_description']}\
    ----- END OF {data_entry['file_name']} -----\n\n"
    
    return {"context": context, "token": num_tokens_from_string(context)}

def get_combined_contexts(df, file_names):
    # list of file_names -> list of combined context strings, also count token of each context
    combined_contexts = {}
    for file_name in file_names:
        data_entry = retrieve_component_from_df(df, file_name)
        if data_entry:
            combined_contexts[file_name] = get_combined_context_string(data_entry)
    return combined_contexts

def contexts_to_string(combined_contexts):
    return "".join([combined_contexts[file_name]["context"] for file_name in combined_contexts])

def get_combined_meta_string(data_entry):
    return f"----- START OF {data_entry['file_name']} -----\n{data_entry['description']}\n----- END OF {data_entry['file_name']} -----\n\n"

def read_combined_file(data_path):
    # data_path is the csv file path of df
    df = pd.read_csv(data_path)
    combined_list = [get_combined_meta_string(data_entry) for data_entry in df.to_dict(orient='records')]
    # get combined string
    combined_string = "".join(combined_list)
    return combined_string
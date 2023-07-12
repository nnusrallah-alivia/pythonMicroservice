import openai
import os
os.environ["OPENAI_API_KEY"] = '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'
from typing import List, Dict, Union
from pydantic import BaseModel


class InputData(BaseModel):
    table_name: str
    input_data: Union[Dict[str, str], List[Dict[str, str]]]


class Service:
    def __init__(self):

        prefix_prompt_path = r"src/static/prefix_prompt.txt"
        postfix_prompt_path = r"src/static/postfix_prompt.txt"
        self.prefix_prompt = self.open_text_file(prefix_prompt_path)
        self.postfix_prompt = self.open_text_file(postfix_prompt_path)

    def open_text_file(self, file_path):
        with open(file_path) as f:
            return f.read()

    def get_table_schema(self, table_name: str):
        schema_path = r"src/static/{}.txt".format(table_name)
        table_schema = self.open_text_file(file_path=schema_path)
        return table_schema

    def build_context(self, schema_details: str, table_name):
        context_prompt = self.prefix_prompt.format(table_name=table_name) + schema_details + self.postfix_prompt
        return context_prompt

    def build_query_prompt(self, schema_details, query):
        input_str = f"""
        {schema_details}
        {query}
        """
        return input_str

    def get_initial_messages(self, final_query):
        return

    def create_openapi_completion(self, messages):
        response = openai.ChatCompletion.create(
            model="gpt-4-32k",
            messages=messages,
            temperature=0,
            max_tokens=16000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        sql_response = response.choices[0].message.content
        return sql_response

    def run_sql_query_builder(self, input_data: InputData):
        table_name = input_data.table_name
        table_schema = self.get_table_schema(table_name=table_name)
        schema_prompt = self.build_context(schema_details=table_schema,
                                           table_name=table_name)
        chat = input_data.input_data
        final_query = self.build_query_prompt(schema_details=schema_prompt,
                                              query=chat[0]["question"])

        messages = [
            {"role": "system",
             "content": "I would like you to be my data anlayst and generate accurate microsft sql query for the question given."},
        ]
        messages.append({"role": "user", "content": final_query})

        if len(chat) > 1:
            for record in chat[1:]:
                if "question" in record:
                    messages.append({"role": "user", "content": record["question"]})
                else:
                    messages.append({"role": "assistant", "content": record["response"]})

        sql_response = self.create_openapi_completion(messages=messages)

        print(sql_response)
        return sql_response

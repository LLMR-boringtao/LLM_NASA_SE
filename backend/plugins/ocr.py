import os

from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

from dotenv import load_dotenv
load_dotenv()


class OCRAgent:
    def __init__(self, request):
        self.request = request
        self.parser = LlamaParse(
            result_type="markdown", 
            language="ch_sim",
            gpt4o_mode=True,
            gpt4o_api_key=os.getenv("OPENAI_API_KEY")
        )

    def actor(self):
        file_extractor = {".pdf": self.parser, ".docx": self.parser, ".doc": self.parser, ".txt": self.parser}
        documents = SimpleDirectoryReader(input_dir=self.request, file_extractor=file_extractor).load_data()
        result = documents[0].text
    
        return result
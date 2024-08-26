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
        file_extractor = {".pdf": self.parser}
        result = SimpleDirectoryReader(input_dir=self.request, file_extractor=file_extractor).load_data()

        # convert the result to a string
        result = str(result)
        # save the result to a file
        with open("backend/data/market/market.txt", "w") as f:
            f.write(result)
    
        return result
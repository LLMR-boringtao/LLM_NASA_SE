# bring in our LLAMA_CLOUD_API_KEY
from dotenv import load_dotenv
load_dotenv()
import os

# bring in deps
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

# set up parser
parser = LlamaParse(
    result_type="text", 
    language="ch_sim",
    gpt4o_mode=True,
    gpt4o_api_key=os.getenv("OPENAI_API_KEY")

)

# use SimpleDirectoryReader to parse our file
file_extractor = {".pdf": parser}
documents = SimpleDirectoryReader(input_dir="data/market", file_extractor=file_extractor).load_data()
print(documents[0].text)

# save the parsed text to a file
with open('data/market/数据.md', 'w') as f:
    f.write(documents[0].text)

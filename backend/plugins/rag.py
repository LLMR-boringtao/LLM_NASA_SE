from copy import deepcopy
from dotenv import load_dotenv
import os
import nest_asyncio

from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.schema import TextNode
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.core import SimpleDirectoryReader
from llama_parse import LlamaParse
from llama_index.postprocessor.flag_embedding_reranker import (
    FlagEmbeddingReranker,
)

from backend.plugins.ocr import OCRAgent

load_dotenv()
nest_asyncio.apply()

def get_page_nodes(docs, separator="\n---\n"):
    nodes = []
    for doc in docs:
        doc_chunks = doc.text.split(separator)
        for doc_chunk in doc_chunks:
            node = TextNode(
                text=doc_chunk,
                metadata=deepcopy(doc.metadata),
            )
            nodes.append(node)

    return nodes

class RAGAgent:
    def __init__(self, request):
        self.request = request
        self.parser = LlamaParse(
            result_type="markdown", 
            gpt4o_mode=True,
            gpt4o_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.openai_embedding = OpenAIEmbedding(api_key=os.getenv("OPENAI_API_KEY"))

    def perceiver(self):
        file_extractor = {".pdf": self.parser, ".png": self.parser}
        query = SimpleDirectoryReader(input_dir=self.request, file_extractor=file_extractor).load_data()
        return query

    def actor(self):
        query = self.perceiver()
        page_nodes = get_page_nodes(query)
        node_parser = MarkdownElementNodeParser(
            llm=OpenAI(model="gpt-3.5-turbo-0125"), num_workers=8
        )

        nodes = node_parser.get_nodes_from_documents(query)
        base_nodes, objects = node_parser.get_nodes_and_objects(nodes)
        recursive_index = VectorStoreIndex(nodes=base_nodes + objects + page_nodes)
        result = base_nodes

        reranker = FlagEmbeddingReranker(
            top_n=5,
            model="BAAI/bge-reranker-large",
        )

        recursive_query_engine = recursive_index.as_query_engine(
            similarity_top_k=5, node_postprocessors=[reranker], verbose=True
        )

        raw_index = VectorStoreIndex.from_documents(query)
        raw_query_engine = raw_index.as_query_engine(
            similarity_top_k=5, node_postprocessors=[reranker]
        )

        question = "System engineering's definition？"
        response_1 = raw_query_engine.query(question)
        print("\n***********Basic Query Engine***********")
        print(response_1)

        response_2 = recursive_query_engine.query(question)
        print("\n***********New LlamaParse+ Recursive Retriever Query Engine***********")
        print(response_2)
        
        return result


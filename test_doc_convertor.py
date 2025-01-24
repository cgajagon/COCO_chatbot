from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.question_gen.prompts import (
    DEFAULT_SUB_QUESTION_PROMPT_TMPL,
)
from llama_index.core.question_gen import LLMQuestionGenerator
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.core.extractors import (
    SummaryExtractor,
    QuestionsAnsweredExtractor,
    TitleExtractor,
    KeywordExtractor,
    BaseExtractor,
)
import nest_asyncio

import os
import openai

from llama_index.llms.openai import OpenAI
from llama_index.core.schema import MetadataMode
from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import (
    VectorStoreIndex, SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage
)
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata

nest_asyncio.apply()

OPENAI_API_KEY = "sk-svcacct-mlAMZX4r64ayLNpkYgPH_Sbskaj_mio53Vgtppof8d4EWIc_97MLRPLYsuTMKOInST3BlbkFJZxxJ-0crSTV18xBUmw4lkPOUmcvwSJwVLYJcAsf9RnrIBzJJE4K6sduQWpDb_krAA"

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

model = "gpt-3.5-turbo"
llm = OpenAI(temperature=0.1, model=model, max_tokens=512)


text_splitter = TokenTextSplitter(
    separator=" ", chunk_size=512, chunk_overlap=128
)


class CustomExtractor(BaseExtractor):
    def extract(self, nodes):
        metadata_list = [
            {
                "custom": (
                    node.metadata["document_title"]
                    + "\n"
                    + node.metadata["excerpt_keywords"]
                )
            }
            for node in nodes
        ]
        return metadata_list


extractors = [
    TitleExtractor(nodes=5, llm=llm),
    QuestionsAnsweredExtractor(questions=3, llm=llm),
    SummaryExtractor(summaries=["prev", "self"], llm=llm),
    KeywordExtractor(keywords=10, llm=llm),
    # CustomExtractor()
]

transformations = [text_splitter] + extractors

pipeline = IngestionPipeline(transformations=transformations)

try:
    storage_context = StorageContext.from_defaults(
        persist_dir="./storage/uber_lift_context"
    )
    index = load_index_from_storage(storage_context)

    index_loaded = True
except:
    index_loaded = False

if not index_loaded:

    lyft_docs = SimpleDirectoryReader(
        input_files=["data/test/lyft.pdf"]).load_data()
    uber_docs = SimpleDirectoryReader(
        input_files=["data/test/uber.pdf"]).load_data()

    # reader = SimpleWebPageReader(html_to_text=True)
    # docs = reader.load_data(urls=["https://eugeneyan.com/writing/llm-patterns/"])
    # nodes = pipeline.run(documents=docs)

    uber_nodes = pipeline.run(documents=uber_docs)
    lyft_nodes = pipeline.run(documents=lyft_docs)

    nodes = uber_nodes + lyft_nodes

    # build index
    index = VectorStoreIndex(
        nodes=nodes
    )

    # persist index
    index.storage_context.persist(
        persist_dir="./storage/uber_lift_context")

question_gen = LLMQuestionGenerator.from_defaults(
    llm=llm,
    prompt_template_str="""
        Follow the example, but instead of giving a question, always prefix the question
        with: 'By first identifying and quoting the most relevant sources, '.
        """
    + DEFAULT_SUB_QUESTION_PROMPT_TMPL,
)

engine = index.as_query_engine(similarity_top_k=10, llm=OpenAI(model="gpt-4"))

final_engine = SubQuestionQueryEngine.from_defaults(
    query_engine_tools=[
        QueryEngineTool(
            query_engine=engine,
            metadata=ToolMetadata(
                name="sec_filing_documents",
                description="financial information on companies.",
            ),
        )
    ],
    question_gen=question_gen,
    use_async=True,
)

# response = final_engine.query(
#    """
#    What was the cost due to research and development v.s. sales and marketing for uber and lyft in 2019 in millions of USD?
#    Give your answer as a JSON.
#    """
# )
# print(response.response)
# Correct answer:
# {"Uber": {"Research and Development": 4836, "Sales and Marketing": 4626},
#  "Lyft": {"Research and Development": 1505.6, "Sales and Marketing": 814 }}

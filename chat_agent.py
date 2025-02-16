from llama_index.core.extractors import (
    SummaryExtractor,
    QuestionsAnsweredExtractor,
)
from llama_index.core.schema import MetadataMode
from llama_index.core.node_parser import TokenTextSplitter
from llama_index.agent.openai import OpenAIAgent
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from llama_index.core.query_engine import TransformQueryEngine
from llama_index.core.indices.query.query_transform import HyDEQueryTransform
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.core.memory import ChatMemoryBuffer

import streamlit as st

api_key = st.secrets["OPENAI_API_KEY"]
is_prod = True

if is_prod is True:
    directory = "./data/prod"
else:
    directory = "./data/dev"

# Define input files and base descriptions
input_files = {
    "agm_sgm_legal_info_sheet": {
        "filename": "AGM-Legal-Info-Sheet-EN-2019.pdf",
        "engine_metadata": (
            "This engine provides an in-depth overview of the legal requirements governing Annual General Meetings and Special General Meetings for non-profit organizations, emphasizing their critical role in member engagement and organizational sustainability. "
            "Use a detailed plain text question as input to the tool."
        ),
    },
    "amalgamation": {
        "filename": "Amalgamation-2012-EN.pdf",
        "engine_metadata": (
            "This engine delivers essential legal guidance on the amalgamation process for non-profit organizations, outlining the core regulatory framework applicable to both provincially and federally incorporated entities while highlighting the flexibility available for customizing organizational structures. "
            "Use a detailed plain text question as input to the tool."
        ),
    },
    "charitable_status": {
        "filename": "Applying-Charitable-Status-August-2018-.pdf",
        "engine_metadata": (
            "This engine offers comprehensive insights into achieving and maintaining charitable status for non-profit organizations, detailing eligibility criteria, the benefits and drawbacks, and the overall application process. "
            "Use a detailed plain text question as input to the tool."
        ),
    },
    "board_liability": {
        "filename": "Board-Liablity_modified2012_0.pdf",
        "engine_metadata": (
            "This engine clarifies the legal liabilities and responsibilities of board members in non-profit organizations, outlining their statutory duties and potential risks to ensure sound governance and risk management. "
            "Use a detailed plain text question as input to the tool."
        ),
    },
    "branching_out": {
        "filename": "Branching-Out-2012-EN.pdf",
        "engine_metadata": (
            "This engine provides strategic and legal insights for non-profit organizations considering expansion, detailing the requirements and considerations for branching out into new activities, services, or programs. "
            "Use a detailed plain text question as input to the tool."
        ),
    },
    "bod_roles_responsibilities": {
        "filename": "COCo-BoardOfDirectors-3-1.pdf",
        "engine_metadata": (
            "This engine offers detailed guidance on the roles, responsibilities, and legal obligations of board members in non-profit organizations, including best practices for board structure, policy development, fundraising, and overall financial support. "
            "Use a detailed plain text question as input to the tool."
        ),
    },
    "cooperatives": {
        "filename": "Co-op-infosheet-EN-modified2012_0.pdf",
        "engine_metadata": (
            "This engine outlines the key legal requirements and operational considerations for forming and managing cooperatives within the non-profit sector, ensuring a clear understanding of cooperative governance and structure. "
            "Use a detailed plain text question as input to the tool."
        ),
    },
    "conflict_of_interest": {
        "filename": "conflict-of-interest-final-nov-2010.pdf",
        "engine_metadata": (
            "This engine provides robust guidance on identifying and managing conflicts of interest among board members in non-profit organizations. It explains how to maintain transparency, impartial decision-making, and proper disclosure practices, while also offering recommendations for developing clear bylaws regarding board remuneration. "
            "Use a detailed plain text question as input to the tool."
        ),
    },
    "dissolution": {
        "filename": "Dissolution-EN-modified2012.pdf",
        "engine_metadata": (
            "This engine explains the legal procedures for the dissolution of non-profit organizations, covering both voluntary and forced dissolution. It details the necessary steps, such as obtaining member approval, settling debts, and filing appropriate declarations, while emphasizing the importance of regulatory compliance. "
            "Use a detailed plain text question as input to the tool."
        ),
    },
    "incorporation": {
        "filename": "incorporation-new-info-sheet-May-2018-draft.pdf",
        "engine_metadata": (
            "This engine offers comprehensive guidance on incorporating a non-profit organization in Quebec. It contrasts incorporation with charitable status, clarifies legal obligations—including governance and compliance—and explains the key differences between provincial and federal incorporation structures. "
            "Use a detailed plain text question as input to the tool."
        ),
    },
    "key_questions_incorporation": {
        "filename": "Key-things-before-inc-EN-modified-20121.pdf",
        "engine_metadata": (
            "This engine serves as an essential guide, outlining critical questions and considerations before incorporating a non-profit organization. It examines the viability of incorporation, explores alternative structures and funding strategies, and assesses long-term commitments to empower informed decision-making. "
            "Use a detailed plain text question as input to the tool."
        ),
    },
    "key_questions_bylaws": {
        "filename": "Key-things-to-think-about-bylaws.pdf",
        "engine_metadata": (
            "This engine delivers a comprehensive overview of bylaws for non-profit organizations, detailing their purpose in ensuring fairness, transparency, and consistency. It also offers best practices for drafting, revising, and implementing clear and inclusive bylaws. "
            "Use a detailed plain text question as input to the tool."
        ),
    },
    "accounting": {
        "filename": "nonprof_accounting_infosheet.pdf",
        "engine_metadata": (
            "This engine provides a detailed guide to Generally Accepted Accounting Principles (GAAP) for small non-profit organizations. It outlines essential accounting practices—including accrual accounting and double-entry bookkeeping—and emphasizes the importance of internal controls and regulatory compliance. "
            "Use a detailed plain text question as input to the tool."
        ),
    },
    "political_activities": {
        "filename": "Political-Activities-Aug-2018.pdf",
        "engine_metadata": (
            "This engine outlines the legal framework governing political activities for registered charities in Canada. It explains the limitations on non-partisan activities under the '10% Rule,' differentiates between non-profit incorporation and charitable status, and details the regulatory requirements for maintaining compliance. "
            "Use a detailed plain text question as input to the tool."
        ),
    },
}

# Define metadata extractors
metadata_extractor_llm = OpenAI(
    temperature=0.1, model="gpt-3.5-turbo", max_tokens=512
)

text_splitter = TokenTextSplitter(
    separator=" ", chunk_size=256, chunk_overlap=128
)

summary_extractor = SummaryExtractor(summaries=["prev", "self", "next"],
                                     llm=metadata_extractor_llm)

qa_extractor = QuestionsAnsweredExtractor(
    questions=3, llm=metadata_extractor_llm, metadata_mode=MetadataMode.EMBED
)

# Setup Multi-Document HyDE Query Engine Tools
query_engine_tools = []
hyde = HyDEQueryTransform(include_original=True)

for key, value in input_files.items():

    storage_directory = f"{directory}/storage/{key}"

    # Load or create each query index
    try:
        storage_context = StorageContext.from_defaults(
            persist_dir=storage_directory
        )
        index = globals()[f"{key}_index"] = load_index_from_storage(
            storage_context
        )

    except:
        # Load the data
        documents = globals()[f"{key}_doc"] = SimpleDirectoryReader(
            input_files=[f"{directory}/docs/{value["filename"]}"]).load_data()

        # Build the index
        index = globals()[f"{key}_index"] = VectorStoreIndex.from_documents(
            documents,
            transformations=[text_splitter, summary_extractor, qa_extractor]
        )

        # Persist the index
        globals()[f"{key}_index"].storage_context.persist(
            persist_dir=storage_directory)

    # Setup the base query engine (using semantic search)
    engine = globals()[f"{key}_engine"] = index.as_query_engine(
        similarity_top_k=3
    )
    # Enhance the engine with HyDE query transformation for improved context mapping.
    hyde_query_engine = TransformQueryEngine(
        engine, hyde
    )

    query_engine_tools.append(
        QueryEngineTool(
            query_engine=hyde_query_engine,
            metadata=ToolMetadata(
                name=f"{key}",
                description=(value["engine_metadata"])
            ),
        )
    )

# Set up tools for agent
tools = query_engine_tools

# Setup memory
memory = ChatMemoryBuffer.from_defaults(token_limit=1500)

# Setup agent
agent_llm = OpenAI(model="gpt-4", api_key=api_key)

agent = OpenAIAgent.from_tools(
    tools=tools,
    memory=memory,
    llm=agent_llm,
    system_prompt=(
        "You are a helpful chatbot called Flor with access to files containing legal information for Non-Profit Organizations in Quebec."
        "You can discuss ONLY details from those documents and hold normal, friendly conversations."
        "Keep your answers concise."
        "If you lack sufficient information to provide an accurate answer, acknowledge this and share any relevant context you do have."
        "When the user decides that the conversation is complete, close with a friendly message on a new line line. Only the user can end the conversation."
        "The closing message must contain the words 'Have a great day!' to end the conversation and the emoji '🌻' for a friendly touch."
    ),
    verbose=True,
)

# Stream data from the agent


def stream_data(prompt):
    streaming_response = agent.stream_chat(prompt)
    for word in streaming_response.response_gen:
        yield word

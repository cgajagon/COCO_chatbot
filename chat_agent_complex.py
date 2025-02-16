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

# Setup Multi Doc HyDE Query Engine / Tool
try:
    storage_context = StorageContext.from_defaults(
        persist_dir=f"{directory}/storage/agm_sgm_legal_info_sheet"
    )

    storage_context = StorageContext.from_defaults(
        persist_dir=f"{directory}/storage/amalgamation"
    )

    storage_context = StorageContext.from_defaults(
        persist_dir=f"{directory}/storage/charitable-status"
    )

    storage_context = StorageContext.from_defaults(
        persist_dir=f"{directory}/storage/board-liability"
    )

    storage_context = StorageContext.from_defaults(
        persist_dir=f"{directory}/storage/branching-out"
    )

    storage_context = StorageContext.from_defaults(
        persist_dir=f"{directory}/storage/bod_roles_responsibilities"
    )

    storage_context = StorageContext.from_defaults(
        persist_dir=f"{directory}/storage/cooperatives"
    )

    storage_context = StorageContext.from_defaults(
        persist_dir=f"{directory}/storage/conflict_of_interest"
    )
    storage_context = StorageContext.from_defaults(
        persist_dir=f"{directory}/storage/dissolution"
    )
    storage_context = StorageContext.from_defaults(
        persist_dir=f"{directory}/storage/incorporation"
    )
    storage_context = StorageContext.from_defaults(
        persist_dir=f"{directory}/storage/key_questions_incorporation"
    )
    storage_context = StorageContext.from_defaults(
        persist_dir=f"{directory}/storage/key_questions_bylaws"
    )
    storage_context = StorageContext.from_defaults(
        persist_dir=f"{directory}/storage/accounting"
    )
    storage_context = StorageContext.from_defaults(
        persist_dir=f"{directory}/storage/political_activities"
    )

    agm_sgm_legal_index = load_index_from_storage(storage_context)
    amalgamation_index = load_index_from_storage(storage_context)
    charitable_status_index = load_index_from_storage(storage_context)
    board_liability_index = load_index_from_storage(storage_context)
    branching_out_index = load_index_from_storage(storage_context)
    bod_roles_responsibilities_index = load_index_from_storage(storage_context)
    cooperatives_index = load_index_from_storage(storage_context)
    conflict_of_interest_index = load_index_from_storage(storage_context)
    dissolution_index = load_index_from_storage(storage_context)
    incorporation_index = load_index_from_storage(storage_context)
    key_questions_incorporation_index = load_index_from_storage(
        storage_context)
    key_questions_bylaws_index = load_index_from_storage(storage_context)
    accounting_index = load_index_from_storage(storage_context)
    political_activities_index = load_index_from_storage(storage_context)

    index_loaded = True
except:
    index_loaded = False

if not index_loaded:
    # load data
    agm_sgm_legal_docs = SimpleDirectoryReader(
        input_files=[f"{directory}/docs/AGM-Legal-Info-Sheet-EN-2019.pdf"]
    ).load_data()
    amalgamation_docs = SimpleDirectoryReader(
        input_files=[f"{directory}/docs/Amalgamation-2012-EN.pdf"]
    ).load_data()
    charitable_status_docs = SimpleDirectoryReader(
        input_files=[
            f"{directory}/docs/Applying-Charitable-Status-August-2018-.pdf"]
    ).load_data()
    board_liability_docs = SimpleDirectoryReader(
        input_files=[f"{directory}/docs/Board-Liablity_modified2012_0.pdf"]
    ).load_data()
    branching_out_docs = SimpleDirectoryReader(
        input_files=[f"{directory}/docs/Branching-Out-2012-EN.pdf"]
    ).load_data()
    bod_roles_responsibilities_docs = SimpleDirectoryReader(
        input_files=[f"{directory}/docs/COCo-BoardOfDirectors-3-1.pdf"]
    ).load_data()
    cooperatives_docs = SimpleDirectoryReader(
        input_files=[f"{directory}/docs/Co-op-infosheet-EN-modified2012_0.pdf"]
    ).load_data()
    conflict_of_interest_docs = SimpleDirectoryReader(
        input_files=[
            f"{directory}/docs/conflict-of-interest-final-nov-2010.pdf"]
    ).load_data()
    dissolution_docs = SimpleDirectoryReader(
        input_files=[f"{directory}/docs/Dissolution-EN-modified2012.pdf"]
    ).load_data()
    incorporation_docs = SimpleDirectoryReader(
        input_files=[
            f"{directory}/docs/incorporation-new-info-sheet-May-2018-draft.pdf"]
    ).load_data()
    key_questions_incorporation_docs = SimpleDirectoryReader(
        input_files=[
            f"{directory}/docs/Key-things-before-inc-EN-modified-20121.pdf"]
    ).load_data()
    key_questions_bylaws_docs = SimpleDirectoryReader(
        input_files=[
            f"{directory}/docs/Key-things-to-think-about-bylaws.pdf"]
    ).load_data()
    accounting_docs = SimpleDirectoryReader(
        input_files=[
            f"{directory}/docs/nonprof_accounting_infosheet.pdf"]
    ).load_data()
    political_activities_docs = SimpleDirectoryReader(
        input_files=[
            f"{directory}/docs/Political-Activities-Aug-2018.pdf"]
    ).load_data()

    # build index
    agm_sgm_legal_index = VectorStoreIndex.from_documents(agm_sgm_legal_docs)
    amalgamation_index = VectorStoreIndex.from_documents(amalgamation_docs)
    charitable_status_index = VectorStoreIndex.from_documents(
        charitable_status_docs)
    board_liability_index = VectorStoreIndex.from_documents(
        board_liability_docs)
    branching_out_index = VectorStoreIndex.from_documents(branching_out_docs)
    bod_roles_responsibilities_index = VectorStoreIndex.from_documents(
        bod_roles_responsibilities_docs)
    cooperatives_index = VectorStoreIndex.from_documents(cooperatives_docs)
    conflict_of_interest_index = VectorStoreIndex.from_documents(
        conflict_of_interest_docs)
    dissolution_index = VectorStoreIndex.from_documents(dissolution_docs)
    incorporation_index = VectorStoreIndex.from_documents(incorporation_docs)
    key_questions_incorporation_index = VectorStoreIndex.from_documents(
        key_questions_incorporation_docs)
    key_questions_bylaws_index = VectorStoreIndex.from_documents(
        key_questions_bylaws_docs)
    accounting_index = VectorStoreIndex.from_documents(accounting_docs)
    political_activities_index = VectorStoreIndex.from_documents(
        political_activities_docs)

    # persist index
    agm_sgm_legal_index.storage_context.persist(
        persist_dir=f"{directory}/storage/agm_sgm_legal_info_sheet")
    amalgamation_index.storage_context.persist(
        persist_dir=f"{directory}/storage/amalgamation")
    charitable_status_index.storage_context.persist(
        persist_dir=f"{directory}/storage/charitable-status")
    board_liability_index.storage_context.persist(
        persist_dir=f"{directory}/storage/board-liability")
    branching_out_index.storage_context.persist(
        persist_dir=f"{directory}/storage/branching-out")
    bod_roles_responsibilities_index.storage_context.persist(
        persist_dir=f"{directory}/storage/bod_roles_responsibilities")
    cooperatives_index.storage_context.persist(
        persist_dir=f"{directory}/storage/cooperatives")
    conflict_of_interest_index.storage_context.persist(
        persist_dir=f"{directory}/storage/conflict_of_interest")
    dissolution_index.storage_context.persist(
        persist_dir=f"{directory}/storage/dissolution")
    incorporation_index.storage_context.persist(
        persist_dir=f"{directory}/storage/incorporation")
    key_questions_incorporation_index.storage_context.persist(
        persist_dir=f"{directory}/storage/key_questions_incorporation")
    key_questions_bylaws_index.storage_context.persist(
        persist_dir=f"{directory}/storage/key_questions_bylaws")
    accounting_index.storage_context.persist(
        persist_dir=f"{directory}/storage/accounting")
    political_activities_index.storage_context.persist(
        persist_dir=f"{directory}/storage/political_activities")

# Setup query engines
agm_sgm_legal_engine = agm_sgm_legal_index.as_query_engine(
    similarity_top_k=3)
amalgamation_engine = amalgamation_index.as_query_engine(
    similarity_top_k=3)
charitable_status_engine = charitable_status_index.as_query_engine(
    similarity_top_k=3)
board_liability_engine = board_liability_index.as_query_engine(
    similarity_top_k=3)
branching_out_engine = branching_out_index.as_query_engine(
    similarity_top_k=3)
bod_roles_responsibilities_engine = bod_roles_responsibilities_index.as_query_engine(
    similarity_top_k=3)
cooperatives_engine = cooperatives_index.as_query_engine(
    similarity_top_k=3)
conflict_of_interest_engine = conflict_of_interest_index.as_query_engine(
    similarity_top_k=3)
dissolution_engine = dissolution_index.as_query_engine(
    similarity_top_k=3)
incorporation_engine = incorporation_index.as_query_engine(
    similarity_top_k=3)
key_questions_incorporation_engine = key_questions_incorporation_index.as_query_engine(
    similarity_top_k=3)
key_questions_bylaws_engine = key_questions_bylaws_index.as_query_engine(
    similarity_top_k=3)
accounting_engine = accounting_index.as_query_engine(
    similarity_top_k=3)
political_activities_engine = political_activities_index.as_query_engine(
    similarity_top_k=3)

# Setup HyDE query engines
hyde = HyDEQueryTransform(include_original=True)

agm_sgm_legal_hyde_query_engine = TransformQueryEngine(
    agm_sgm_legal_engine, hyde)
amalgamation_hyde_query_engine = TransformQueryEngine(
    amalgamation_engine, hyde)
charitable_status_hyde_query_engine = TransformQueryEngine(
    charitable_status_engine, hyde)
board_liability_hyde_query_engine = TransformQueryEngine(
    board_liability_engine, hyde)
branching_out_hyde_query_engine = TransformQueryEngine(
    branching_out_engine, hyde)
bod_roles_responsibilities_hyde_query_engine = TransformQueryEngine(
    bod_roles_responsibilities_engine, hyde)
cooperatives_hyde_query_engine = TransformQueryEngine(
    cooperatives_engine, hyde)
conflict_of_interest_hyde_query_engine = TransformQueryEngine(
    conflict_of_interest_engine, hyde)
dissolution_hyde_query_engine = TransformQueryEngine(
    dissolution_engine, hyde)
incorporation_hyde_query_engine = TransformQueryEngine(
    incorporation_engine, hyde)
key_questions_incorporation_hyde_query_engine = TransformQueryEngine(
    key_questions_incorporation_engine, hyde)
key_questions_bylaws_hyde_query_engine = TransformQueryEngine(
    key_questions_bylaws_engine, hyde)
accounting_hyde_query_engine = TransformQueryEngine(
    accounting_engine, hyde)
political_activities_hyde_query_engine = TransformQueryEngine(
    political_activities_engine, hyde)

query_engine_tools = [
    QueryEngineTool(
        query_engine=agm_sgm_legal_hyde_query_engine,
        metadata=ToolMetadata(
            name="agm_sgm_legal_info_sheet",
            description=(
                "Provides detailed information on the legal requirements for Annual General Meetings and Special General Meetings of non-profit organizations."
                "Explains their importance in member engagement and sustaining organizational health."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=amalgamation_hyde_query_engine,
        metadata=ToolMetadata(
            name="amalgamation",
            description=(
                "Provides legal information for non-profit organizations (NPO) seeking to merge with one or several other NPOs."
                "The information provided here sets out the basic rules that apply to provincially and federally incorporated organizations."
                "However, organizations should be aware that they can tailor their organizational structure to suit their needs,"
                "preferences and goals as long as certain basic rules are followed."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=charitable_status_hyde_query_engine,
        metadata=ToolMetadata(
            name="charitable_status",
            description=(
                "Provides information on charitable status for non-profit organizations, who can apply for it, pros and cons, and the process of applying for and maintaining it."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=board_liability_hyde_query_engine,
        metadata=ToolMetadata(
            name="board_liability",
            description=(
                "Provides information on the liability of board members of non-profit organizations, including the legal duties and responsibilities of board members."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=branching_out_hyde_query_engine,
        metadata=ToolMetadata(
            name="branching_out",
            description=(
                "Provides information on branching out for non-profit organizations, including the legal requirements and considerations for expanding the organization's activities, services, or programs."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=bod_roles_responsibilities_hyde_query_engine,
        metadata=ToolMetadata(
            name="bod_roles_responsibilities",
            description=(
                "Provides information on the roles and responsibilities of board members of non-profit organizations, including the legal duties and obligations of board members."
                "Also includes information on the structure and functioning of the board of directors, as well as how to make policies, organize fundraising events and financially support the organization in general."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=cooperatives_hyde_query_engine,
        metadata=ToolMetadata(
            name="cooperatives",
            description=(
                "Provides information on cooperatives for non-profit organizations, including the legal requirements and considerations for forming and operating a cooperative."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=conflict_of_interest_hyde_query_engine,
        metadata=ToolMetadata(
            name="conflict_of_interest",
            description=(
                "Provide guidance on identifying and managing conflicts of interest for board members in nonprofit organizations."
                "It defines conflicts of interest as situations where personal or professional interests may compromise impartiality and stresses the importance of transparency, honesty, and acting in the organization’s best interests."
                "It also advises about disclosing conflicts, abstaining from decision-making when necessary, and maintaining thorough records."
                "It also addresses board member remuneration, recommending clear bylaws to discourage payment for board duties while allowing reimbursement for expenses or engagement in contracts under strict transparency protocols."
                "Ultimately, it emphasizes fostering a culture of accountability and dialogue, with legal consultation recommended for specific organizational needs."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=dissolution_hyde_query_engine,
        metadata=ToolMetadata(
            name="dissolution",
            description=(
                "Provides the process for the dissolution of nonprofit organizations, emphasizing that dissolution is a natural part of an organization's lifecycle."
                "Describes both voluntary and forced dissolution, including the necessary legal steps, such as obtaining member approval, settling debts, and filing declarations with the Registrar."
                "Explains for voluntary dissolution, organizations must pass a board resolution, settle financial obligations, and distribute remaining assets according to bylaws or donor intentions."
                "Explains how forced dissolution often occurs due to non-compliance, such as failing to file required reports."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=incorporation_hyde_query_engine,
        metadata=ToolMetadata(
            name="incorporation",
            description=(
                "Provides guidance for incorporating a nonprofit organization in Quebec."
                "Explains whether incorporation is necessary, highlighting alternative options and considerations before proceeding."
                "Explains the distinction between incorporation and charitable status, emphasizing that incorporation provides a legal structure for the organization to operate independently, while charitable status entails tax benefits and additional requirements."
                "Provides guidance on the incorporation process, detailing the legal obligations for provincially incorporated nonprofits, including governance, bylaws, annual meetings, and compliance with filing requirements."
                "Compares provincial and federal incorporation, discussing key differences such as board member requirements, financial obligations, and dual registration for federally incorporated nonprofits operating in Quebec."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=key_questions_incorporation_hyde_query_engine,
        metadata=ToolMetadata(
            name="key_questions_incorporation",
            description=(
                "An informational guide that outlines key considerations before incorporating a nonprofit organization."
                "Explains the necessity and sustainability of incorporation, exploring alternative structures, identifying funding sources, creating a development plan, and understanding long-term commitments."
                "Provides resources for incorporation and charitable status applications while highlighting situations where incorporation may not be the best option."
                "Assist individuals or groups in making informed decisions about forming a nonprofit."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=key_questions_bylaws_hyde_query_engine,
        metadata=ToolMetadata(
            name="key_questions_bylaws",
            description=(
                "Provides an overview of bylaws for nonprofit organizations."
                "Explains the purpose of bylaws as guiding rules that govern organizational operations, ensuring fairness, transparency, and consistency."
                "Provides recommendations for drafting clear and inclusive bylaws, avoiding ambiguity, and involving multiple contributors in the process."
                "Explains the process for modifying bylaws at general meetings, and the distinction between bylaws and letters patent."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=accounting_hyde_query_engine,
        metadata=ToolMetadata(
            name="accounting",
            description=(
                "Provides a guide to Generally Accepted Accounting Principles (GAAP) for small nonprofit organizations."
                "Explains accounting practices, including documenting all financial transactions, using accrual accounting, implementing double-entry bookkeeping, and maintaining a detailed chart of accounts."
                "Explains the importance of producing financial statements, recognizing revenue appropriately, recording capital assets, and adhering to government regulations."
                "Provides recommendations about internal controls such as budgeting, segregation of financial duties, and policies for petty cash management."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=political_activities_hyde_query_engine,
        metadata=ToolMetadata(
            name="political_activities",
            description=(
                "Explains rules governing political activities."
                "Provides guidance on the legal limitations regarding political activities for registered charities in Canada."
                "Explains the distinction between nonprofit incorporation and charitable status, highlights the benefits of being a registered charity, and outlines the compliance requirements to maintain charitable status."
                "Explains that only non-partisan activities directly tied to a charity's purpose are allowed within specific resource limits (commonly referred to as the '10% Rule')."
                "Explains exceptions, advocacy activities considered charitable, and criticisms of political activity limitations."
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
]

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

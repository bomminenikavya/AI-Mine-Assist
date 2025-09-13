

import os

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
import os


from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os

from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters.character import CharacterTextSplitter

os.environ["GROQ_API_KEY"] = "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"

chat = ChatGroq(
    temperature=0,
    groq_api_key=os.environ.get("GROQ_API_KEY"),
    model_name="mixtral-8x7b-32768",
    streaming=True,
)


def execute(question):
    os.environ["OPENAI_API_KEY"] = "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"
    embeddings = OpenAIEmbeddings()

    ### INDEXING INITIALLY ###

    #
    # loader = PyPDFLoader("theminesact1952.pdf")
    #
    # documents = loader.load()
    # print("started indexing")
    # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    # docs = text_splitter.split_documents(documents)
    #
    # db = FAISS.from_documents(docs, embeddings)
    #
    # db.save_local("mine-data")
    # print("Indexing completed!!")


    chat = ChatGroq(
        temperature=0,
        groq_api_key=os.environ.get("GROQ_API_KEY"),
        model_name="llama3-8b-8192",
        streaming=True,
        max_tokens=300,
    )

    retriever = FAISS.load_local(
        "mine-data", embeddings, allow_dangerous_deserialization=True
    )
    result = retriever.similarity_search(question)

    context = "\n".join(x.page_content for x in result)[:1000]

    print(context)

    template = """You are a helpful Agent for miners, Note:Greet the users if they and have general conversations, Summarize your response and make it concise list of points, You are expertise is in answering queries related to the Mining document and assist users,
    Your primary task is to provide comprehensive information and address any questions or concerns users may have.{query}?
    context {context}"""
    prompt = PromptTemplate(input_variables=["query", "context"], template=template)
    chatbot = RetrievalQA.from_chain_type(
        llm=chat,
        chain_type="stuff",
        retriever=FAISS.load_local(
            "mine-data", OpenAIEmbeddings(), allow_dangerous_deserialization=True
        ).as_retriever(search_type="similarity", search_kwargs={"k": 1}),
    )

    response = chatbot.run(prompt.format(query=question, context=context))
    return response

from dotenv import load_dotenv
from langchain.vectorstores.chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from redundant_filter_retriever import RedundantFilterRetriever
import langchain

langchain.debug = True

load_dotenv()

embeddings = OpenAIEmbeddings()
db = Chroma(persist_directory="emb", embedding_function=embeddings)

retriever = RedundantFilterRetriever(embeddings=embeddings, chroma=db)

chat = ChatOpenAI()

chain = RetrievalQA.from_chain_type(
    llm=chat,
    chain_type="stuff",
    retriever=retriever,
)

result = chain.run("What is interesting fact about English language?")
print(result)
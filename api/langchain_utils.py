from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from typing import List
from langchain_core.documents import Document
from chroma_utils import vectorstore
from langchain_groq import ChatGroq
from datetime import datetime
from dotenv import load_dotenv
import os
import random

load_dotenv()

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})
output_parser = StrOutputParser()

'''Set up prompts and chains'''

# System prompt for reformulating a follow-up question into a standalone one.
contextualize_q_system_prompt = (
    "Given a chat history and the latest user question "
    "which might reference context in the chat history, "
    "formulate a standalone question which can be understood "
    "without the chat history. Do NOT answer the question, "
    "just reformulate it if needed and otherwise return it as is."
)

# This uses the system prompt defined above to guide the assistant in generating a self-contained version of a user query that may rely on prior chat history.
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", contextualize_q_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Fallback Responses to answer the question outside the context 
fallback_responses = [
    "I'm here to help with questions related to the uploaded documents. For anything outside of that, you may need to consult a different source. How can I assist with your document-related query?",
    "I specialize in answering based on the documents you've provided. I might not have accurate info outside of that, but I’d be happy to help with anything within those documents!",
    "That’s outside my current scope — I work with the content in the uploaded documents. Would you like to ask something related to them?",
    "That’s an interesting question! But I’ve only been trained on the uploaded content. Is there something you'd like to know from those documents?",
    "I'm here to assist with information found in the uploaded files. Let me know how I can help you with that!",
    "I couldn't find any verified information about that topic in the uploaded documents. You might want to check another source. Meanwhile, feel free to ask about anything related to the documents!",
    "That’s outside what I can assist with based on the provided documents. You may want to reach out to a relevant expert, or feel free to ask a question based on the uploaded content!"
]

# Choose one randomly for this invocation
fallback_response = random.choice(fallback_responses)

# Todays date to pass in to the prompt to answer question related or considering todays date.
today = datetime.today().strftime('%Y-%m-%d') # Format: '2025-05-14'

# User Question and Answer Prompt Quidelines and Prompt template for answering only document-based questions using uploaded content with fallback handling.
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     f"""You are an AI assistant designed to answer questions based on the user's uploaded documents.

If someone asks a casual or friendly question like "How are you?" or "What are you doing?", respond politely and conversationally.

Today is {today}. Use this date when answering any date-related questions.

If someone asks a question that is **not related** to the content of the uploaded documents, respond with:
"{fallback_response}"

When responding to document-related questions:
- Only answer based on verified information from the uploaded documents.
- Do not make up answers or include guesses.
- Avoid using technical terms like 'context' in your response.
- If something is not mentioned in the documents, simply state that the information is not available.

Guidelines:
- Provide clear, detailed, and helpful answers.
- Use all available information from the documents to support and elaborate your response.
- Maintain a professional and supportive tone.
- If you do not find the answer in the provided context, say "I couldn't find that information in the uploaded documents, Please ask the questions related to uploaded documents only"
- Avoid making up answers or including guesses."""
    ),
    ("system", "Context: {context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])

# Returns a RAG chain using a history-aware retriever and LLM-powered document-based QA.
def get_rag_chain(model="llama-3.3-70b-versatile"):
    groq_api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        api_key=groq_api_key
    )
    history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)    
    return rag_chain


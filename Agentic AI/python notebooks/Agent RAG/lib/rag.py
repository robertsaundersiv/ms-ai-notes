from typing import Any, TypedDict, List, Mapping, cast
import logging

from lib.state_machine import StateMachine, Step, EntryPoint, Termination, Run, Resource
from lib.llm import LLM
from lib.messages import BaseMessage, UserMessage, SystemMessage
from lib.vector_db import VectorStore


logging.getLogger('pdfminer').setLevel(logging.ERROR)


class RAGState(TypedDict):
    """State fields accumulated by the RAG pipeline."""
    messages: List[BaseMessage]
    question: str
    documents: List[str]
    distances: List[float]
    answer: str

class RAG:
    """
    Retrieval-Augmented Generation (RAG) system implementation.
    
    This class orchestrates the complete RAG pipeline using a state machine approach:
    1. Retrieve: Find relevant documents using vector similarity search
    2. Augment: Combine retrieved context with the user's question
    3. Generate: Use an LLM to produce an answer based on the augmented prompt
    
    The RAG pattern enhances LLM responses by providing relevant external knowledge,
    reducing hallucinations and improving factual accuracy.
    """
    def __init__(self, llm: LLM, vector_store: VectorStore):
        self.workflow = self._create_state_machine()
        self.resource = Resource(
            vars = {
                "llm": llm,
                "vector_store": vector_store,
            }
        )

    def _retrieve(self, state: Mapping[str, Any], resource: Resource) -> Mapping[str, Any]:
        question = cast(str, state["question"]) 
        vector_store = resource.vars.get("vector_store")
        if not isinstance(vector_store, VectorStore):
            raise RuntimeError("RAG resource is missing a VectorStore")
        results = vector_store.query(query_texts=[question])

        documents = results['documents'][0] if results['documents'] else []
        distances = results['distances'][0] if results['distances'] else []
        
        return {"documents": documents, "distances": distances}

    def _augment(self, state: Mapping[str, Any]) -> Mapping[str, Any]:
        question = cast(str, state["question"])
        documents = cast(List[str], state["documents"]) 
        context = "\n\n".join(documents)

        messages = [
            SystemMessage(content="You are an assistant for question-answering tasks."),
            UserMessage(
                content=(
                    "Use the following pieces of retrieved context to answer the question. "
                    "If you don't know the answer, just say that you don't know. "
                    f"\n# Question: \n-> {question} "
                    f"\n# Context: \n-> {context} "
                    "\n# Answer: "
                )
            )
        ]

        return {"messages": messages}

    def _generate(self, state: Mapping[str, Any], resource: Resource) -> Mapping[str, Any]:
        llm = resource.vars.get("llm")
        if not isinstance(llm, LLM):
            raise RuntimeError("RAG resource is missing an LLM")
        messages = cast(List[BaseMessage], state["messages"])
        ai_message = llm.invoke(messages)
        return {
            "answer": ai_message.content,
            "messages": messages + [ai_message],
        }

    def _create_state_machine(self) -> StateMachine[RAGState]:
        machine = StateMachine[RAGState](RAGState)

        # Create steps
        entry = EntryPoint[RAGState]()
        retrieve = Step[RAGState]("retrieve", self._retrieve)
        augment = Step[RAGState]("augment", self._augment)
        generate = Step[RAGState]("generate", self._generate)
        termination = Termination[RAGState]()

        machine.add_steps([entry, retrieve, augment, generate, termination])
        machine.connect(entry, retrieve)
        machine.connect(retrieve, augment)
        machine.connect(augment, generate)
        machine.connect(generate, termination)

        return machine

    def invoke(self, query: str) -> Run:
        """
        Execute the complete RAG pipeline for a given query.
        
        This is the main entry point for the RAG system. It initializes the
        pipeline state with the user's question and executes the complete
        retrieve-augment-generate workflow.
        
        Args:
            query (str): The user's question or search query
            
        Returns:
            Run: Execution object containing the final state and pipeline results
            
        Example:
            >>> rag = RAG(llm, vector_store)
            >>> result = rag.invoke("What is machine learning?")
            >>> answer = result.get_final_state()["answer"]
        """
        
        initial_state: Mapping[str, Any] = {
            "question": query,
        }
        run_object = self.workflow.run(
            initial_state=initial_state,
            resource=self.resource,
        )
        return run_object

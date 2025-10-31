from langchain_core.agents import AgentFinish
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from typing import Any, Dict, List, Optional, Tuple, Union

from app.agents.specialist_agents import DocumentTypeDetectionAgent, MedicalEntityExtractionAgent, KnowledgeRetrievalAgent, ReasoningAgent, SafetyAssessmentAgent

class OrchestratorAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro") # Using gemini-pro for now, will switch to Flash later
        self.document_type_agent = DocumentTypeDetectionAgent()
        self.medical_entity_agent = MedicalEntityExtractionAgent()
        self.knowledge_retrieval_agent = KnowledgeRetrievalAgent()
        self.reasoning_agent = ReasoningAgent()
        self.safety_assessment_agent = SafetyAssessmentAgent()

    async def process_document(self, extracted_text: str) -> Dict[str, Any]:
        """
        Orchestrates the document analysis process.
        """
        print(f"Orchestrator received text: {extracted_text[:100]}...")
        
        document_type_result = await self.document_type_agent.detect_document_type(extracted_text)
        detected_document_type = document_type_result['document_type']
        print(f"Detected document type: {detected_document_type} with confidence {document_type_result['confidence_score']}")
        
        extracted_entities = await self.medical_entity_agent.extract_entities(extracted_text, detected_document_type)
        print(f"Extracted {len(extracted_entities)} medical entities.")

        retrieved_knowledge = await self.knowledge_retrieval_agent.retrieve_knowledge(extracted_entities)
        print(f"Retrieved {len(retrieved_knowledge)} knowledge snippets.")

        reasoning_result = await self.reasoning_agent.perform_reasoning(
            extracted_text,
            detected_document_type,
            extracted_entities,
            retrieved_knowledge
        )
        print(f"Generated summary: {reasoning_result['summary'][:100]}...")

        safety_assessment_results = await self.safety_assessment_agent.perform_safety_assessment(
            extracted_entities,
            retrieved_knowledge
        )
        print(f"Generated {len(safety_assessment_results)} safety alerts.")
        
        return {
            "status": "analysis_complete",
            "document_type": detected_document_type,
            "confidence_score": document_type_result["confidence_score"],
            "extracted_entities": extracted_entities,
            "retrieved_knowledge": retrieved_knowledge,
            "summary": reasoning_result["summary"],
            "key_findings": reasoning_result["key_findings"],
            "safety_assessment": safety_assessment_results,
            "message": "Document analysis, entity extraction, knowledge retrieval, reasoning, and safety assessment complete."
        }

from typing import Any, Dict

from app.agents.specialist_agents import (DocumentTypeDetectionAgent,
                                          KnowledgeRetrievalAgent,
                                          MedicalEntityExtractionAgent,
                                          ReasoningAgent,
                                          SafetyAssessmentAgent)
from langchain_google_genai import ChatGoogleGenerativeAI


class OrchestratorAgent:
    def __init__(self):
        # Spec mentions Gemini 2.0 Flash, which would be a specific model name like "gemini-1.5-flash-latest"
        # Using a placeholder here that aligns with the spec's intent.
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")
        self.document_type_agent = DocumentTypeDetectionAgent()
        self.medical_entity_agent = MedicalEntityExtractionAgent()
        self.knowledge_retrieval_agent = KnowledgeRetrievalAgent()
        self.reasoning_agent = ReasoningAgent()
        self.safety_assessment_agent = SafetyAssessmentAgent()

    async def process_document(self, extracted_text: str) -> Dict[str, Any]:
        """
        Orchestrates the document analysis process by chaining specialist agents.
        """
        print(f"Orchestrator received text: {extracted_text[:100]}...")

        # Step 1: Detect Document Type
        document_type_result = await self.document_type_agent.detect_document_type(
            extracted_text
        )
        detected_document_type = document_type_result["document_type"]
        print(
            f"Detected document type: {detected_document_type} with confidence {document_type_result['confidence_score']}"
        )

        # Step 2: Extract Medical Entities
        extracted_entities = await self.medical_entity_agent.extract_entities(
            extracted_text, detected_document_type
        )
        print(f"Extracted {len(extracted_entities)} medical entities.")

        # Step 3: Retrieve relevant knowledge (simulated vector search)
        retrieved_knowledge = await self.knowledge_retrieval_agent.retrieve_knowledge(
            extracted_entities
        )
        print(f"Retrieved {len(retrieved_knowledge)} knowledge snippets.")

        # Step 4: Perform reasoning to generate summary and findings
        reasoning_result = await self.reasoning_agent.perform_reasoning(
            extracted_text,
            detected_document_type,
            extracted_entities,
            retrieved_knowledge,
        )
        print(f"Generated summary: {reasoning_result['summary'][:100]}...")

        # Step 5: Perform safety assessment for risks and interactions
        safety_assessment_results = (
            await self.safety_assessment_agent.perform_safety_assessment(
                extracted_entities, retrieved_knowledge
            )
        )
        print(f"Generated {len(safety_assessment_results)} safety alerts.")

        # Step 6: Assemble the final result
        return {
            "status": "analysis_complete",
            "document_type": detected_document_type,
            "confidence_score": document_type_result["confidence_score"],
            "extracted_entities": extracted_entities,
            "retrieved_knowledge": retrieved_knowledge,
            "summary": reasoning_result["summary"],
            "key_findings": reasoning_result["key_findings"],
            "safety_assessment": safety_assessment_results,
            "message": "Document analysis, entity extraction, knowledge retrieval, reasoning, and safety assessment complete.",
        }

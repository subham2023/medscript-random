from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from typing import Any, Dict, List, Optional
import json

# Assuming MedicalEntity and SafetyAlert models are available from app.api.models
# For specialist_agents.py, we'll define a simplified version or import if possible
# For now, let's assume the structure is known.

class DocumentTypeDetectionAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro") # Using gemini-pro for now
        self.document_types = [
            "prescription", "lab results", "discharge summary", "radiology report",
            "pathology report", "diagnostic report", "vaccination records",
            "referral letters", "treatment plans", "unknown"
        ]
        self.prompt_template = PromptTemplate.from_template(
            """You are an AI assistant specialized in identifying medical document types.
            Given the following text from a medical document, classify its type from the following options:
            {document_types_list}.
            
            Return only the most likely document type. If you are unsure, return 'unknown'.
            
            Document Text:
            {extracted_text}
            
            Document Type:"""
        )

    async def detect_document_type(self, extracted_text: str) -> Dict[str, Any]:
        """
        Detects the type of the medical document based on its extracted text.
        """
        prompt = self.prompt_template.format(
            document_types_list=", ".join(self.document_types),
            extracted_text=extracted_text
        )
        
        response = await self.llm.ainvoke(prompt)
        detected_type = response.content.strip().lower()
        
        # Basic validation to ensure the detected type is one of the allowed types
        if detected_type not in self.document_types:
            detected_type = "unknown"
            
        # For now, we'll return a placeholder confidence score.
        # A more sophisticated approach would involve parsing the LLM's confidence or using a different model.
        return {"document_type": detected_type, "confidence_score": 0.85}

class MedicalEntityExtractionAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro") # Using gemini-pro for now
        self.prompt_template = PromptTemplate.from_template(
            """You are an AI assistant specialized in extracting medical entities from documents.
            Given the following text from a medical document of type '{document_type}',
            extract relevant medical entities such as medications, dosages, lab test names, lab values,
            diagnoses, procedures, and vital signs.
            
            Return the extracted entities as a JSON array of objects, where each object has:
            - 'entity_type': (e.g., 'medication', 'dosage', 'lab_test', 'lab_value', 'diagnosis', 'procedure', 'vital_sign')
            - 'entity_value': The extracted text for the entity
            - 'confidence_score': A float between 0.0 and 1.0 indicating confidence (estimate if not explicit)
            
            If no entities are found, return an empty JSON array.
            
            Document Type: {document_type}
            Document Text:
            {extracted_text}
            
            Extracted Entities (JSON array):"""
        )

    async def extract_entities(self, extracted_text: str, document_type: str) -> List[Dict[str, Any]]:
        """
        Extracts medical entities from the document text.
        """
        prompt = self.prompt_template.format(
            document_type=document_type,
            extracted_text=extracted_text
        )
        
        response = await self.llm.ainvoke(prompt)
        
        try:
            entities = json.loads(response.content.strip())
            if not isinstance(entities, list):
                return []
            # Basic validation for entity structure
            for entity in entities:
                if not all(k in entity for k in ["entity_type", "entity_value", "confidence_score"]):
                    return [] # Return empty if structure is not as expected
            return entities
        except json.JSONDecodeError:
            print(f"Warning: Could not parse JSON from LLM response: {response.content}")
            return []

class KnowledgeRetrievalAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro") # Using gemini-pro for now

    async def retrieve_knowledge(self, entities: List[Dict[str, Any]]) -> List[str]:
        """
        Simulates retrieving medical knowledge based on extracted entities.
        In a real application, this would query a vector database (Firestore + Vector Search).
        """
        knowledge_snippets = []
        for entity in entities:
            if entity["entity_type"] == "medication":
                knowledge_snippets.append(f"Knowledge about {entity['entity_value']}: This medication is commonly used for [condition] and has [side effects].")
            elif entity["entity_type"] == "lab_test":
                knowledge_snippets.append(f"Knowledge about {entity['entity_value']}: This lab test measures [what it measures] and normal ranges are [ranges].")
            elif entity["entity_type"] == "diagnosis":
                knowledge_snippets.append(f"Knowledge about {entity['entity_value']}: This diagnosis is characterized by [symptoms] and treated with [treatments].")
        
        if not knowledge_snippets:
            knowledge_snippets.append("No specific knowledge found for the extracted entities.")

        return knowledge_snippets

class ReasoningAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro") # Using gemini-pro for now
        self.prompt_template = PromptTemplate.from_template(
            """You are an AI assistant specialized in medical reasoning and summarization.
            Given the following medical document text, its detected type, extracted entities, and retrieved knowledge,
            perform multi-step reasoning to generate a concise summary and a list of key findings.
            
            Document Type: {document_type}
            Extracted Text:
            {extracted_text}
            
            Extracted Entities:
            {extracted_entities}
            
            Retrieved Knowledge:
            {retrieved_knowledge}
            
            Based on the above information, provide:
            1. A concise summary of the document's medical content.
            2. A list of key findings or important insights.
            
            Return the output as a JSON object with 'summary' (string) and 'key_findings' (list of strings)."""
        )

    async def perform_reasoning(
        self,
        extracted_text: str,
        document_type: str,
        extracted_entities: List[Dict[str, Any]],
        retrieved_knowledge: List[str]
    ) -> Dict[str, Any]:
        """
        Performs multi-step reasoning and generates a summary and key findings.
        """
        prompt = self.prompt_template.format(
            document_type=document_type,
            extracted_text=extracted_text,
            extracted_entities=json.dumps(extracted_entities, indent=2),
            retrieved_knowledge="\n".join(retrieved_knowledge)
        )
        
        response = await self.llm.ainvoke(prompt)
        
        try:
            reasoning_result = json.loads(response.content.strip())
            if not all(k in reasoning_result for k in ["summary", "key_findings"]):
                return {"summary": "Could not generate summary.", "key_findings": []}
            return reasoning_result
        except json.JSONDecodeError:
            print(f"Warning: Could not parse JSON from LLM response: {response.content}")
            return {"summary": "Error in reasoning process.", "key_findings": []}

class SafetyAssessmentAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro") # Using gemini-pro for now

    async def perform_safety_assessment(
        self,
        extracted_entities: List[Dict[str, Any]],
        retrieved_knowledge: List[str]
    ) -> List[Dict[str, Any]]: # Returns a list of SafetyAlert-like dicts
        """
        Simulates performing a safety assessment, including drug interaction and abnormal value identification.
        """
        safety_alerts = []

        medications = [e["entity_value"] for e in extracted_entities if e["entity_type"] == "medication"]
        lab_values = [e for e in extracted_entities if e["entity_type"] == "lab_value"]

        # Simulate drug interaction detection
        if "Metformin" in medications and "Insulin" in medications:
            safety_alerts.append({
                "severity": "major",
                "title": "Potential Drug Interaction: Metformin and Insulin",
                "description": "Concurrent use of Metformin and Insulin can increase the risk of hypoglycemia. Monitor blood glucose closely.",
                "action_required": True
            })
        elif len(medications) > 2:
            safety_alerts.append({
                "severity": "moderate",
                "title": "Polypharmacy Alert",
                "description": f"Patient is on {len(medications)} medications. Review for potential interactions and side effects.",
                "action_required": True
            })

        # Simulate abnormal lab value identification
        for lab in lab_values:
            try:
                value = float(lab["entity_value"])
                if lab["entity_type"] == "lab_value" and "glucose" in lab.get("metadata", {}).get("test_name", "").lower():
                    if value > 200:
                        safety_alerts.append({
                            "severity": "critical",
                            "title": "High Blood Glucose Level",
                            "description": f"Blood glucose is {value} mg/dL, which is critically high. Immediate medical attention may be required.",
                            "action_required": True
                        })
                    elif value > 125:
                        safety_alerts.append({
                            "severity": "moderate",
                            "title": "Elevated Blood Glucose Level",
                            "description": f"Blood glucose is {value} mg/dL, which is elevated. Follow-up with a physician is recommended.",
                            "action_required": True
                        })
            except ValueError:
                pass # Ignore if lab value is not a number

        if not safety_alerts:
            safety_alerts.append({
                "severity": "low",
                "title": "No significant safety concerns identified",
                "description": "Based on the available information, no critical drug interactions or abnormal lab values were detected.",
                "action_required": False
            })

        return safety_alerts

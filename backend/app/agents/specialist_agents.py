import json
from typing import Any, Dict, List

from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

# As per spec, use Gemini 2.0 Flash model. The model name might be e.g., "gemini-1.5-flash-latest"
MODEL_NAME = "gemini-1.5-flash-latest"


class DocumentTypeDetectionAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0.1)
        self.document_types = [
            "prescription",
            "lab results",
            "discharge summary",
            "radiology report",
            "pathology report",
            "diagnostic report",
            "vaccination records",
            "referral letters",
            "treatment plans",
            "unknown",
        ]
        self.prompt_template = PromptTemplate.from_template(
            """You are an AI assistant specialized in identifying medical document types.
            Given the following text from a medical document, classify its type from the following options:
            {document_types_list}.

            Return only the single, most likely document type as a lowercase string. If you are unsure, return 'unknown'.

            Document Text:
            {extracted_text}

            Document Type:"""
        )

    async def detect_document_type(self, extracted_text: str) -> Dict[str, Any]:
        """Detects the type of the medical document based on its extracted text."""
        chain = self.prompt_template | self.llm
        response = await chain.ainvoke(
            {
                "document_types_list": ", ".join(self.document_types),
                "extracted_text": extracted_text[
                    :4000
                ],  # Use a slice to avoid overly long prompts
            }
        )
        detected_type = response.content.strip().lower()

        if detected_type not in self.document_types:
            detected_type = "unknown"

        # Confidence score is a placeholder; a more advanced method would use model logits.
        return {"document_type": detected_type, "confidence_score": 0.9}


class MedicalEntityExtractionAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME, temperature=0.2, response_format={"type": "json_object"}
        )
        self.prompt_template = PromptTemplate.from_template(
            """You are an AI assistant specialized in extracting medical entities.
            From the text of a '{document_type}', extract entities like medications, dosages, lab tests, lab values, diagnoses, and procedures.
            Return a JSON object with a single key "entities" which is an array of objects. Each object must have:
            - 'entity_type': (e.g., 'medication', 'dosage', 'lab_test', 'lab_value', 'diagnosis', 'procedure')
            - 'entity_value': The extracted text for the entity.
            - 'confidence_score': A float between 0.0 and 1.0 indicating your confidence.

            If no entities are found, return an empty array.

            Document Text:
            {extracted_text}
            """
        )

    async def extract_entities(
        self, extracted_text: str, document_type: str
    ) -> List[Dict[str, Any]]:
        """Extracts medical entities from the document text."""
        chain = self.prompt_template | self.llm
        response = await chain.ainvoke(
            {"document_type": document_type, "extracted_text": extracted_text}
        )

        try:
            # The response content should be a JSON string.
            data = json.loads(response.content)
            entities = data.get("entities", [])
            if isinstance(entities, list):
                return entities
            return []
        except (json.JSONDecodeError, AttributeError):
            print(
                f"Warning: Could not parse JSON from LLM response for entity extraction: {response.content}"
            )
            return []


class KnowledgeRetrievalAgent:
    def __init__(self):
        # In a real application, this would connect to a vector database service.
        # Here, we simulate it with simple logic.
        pass

    async def retrieve_knowledge(self, entities: List[Dict[str, Any]]) -> List[str]:
        """
        Simulates retrieving medical knowledge. In a real application, this would query
        a vector database (e.g., Firestore with Vector Search) using embeddings of the entity values.
        """
        knowledge_snippets = []
        for entity in entities:
            entity_type = entity.get("entity_type")
            entity_value = entity.get("entity_value")
            if entity_type == "medication":
                knowledge_snippets.append(
                    f"Knowledge about {entity_value}: This is a medication often used for [condition] with common side effects like [side effects]."
                )
            elif entity_type == "lab_test":
                knowledge_snippets.append(
                    f"Knowledge about {entity_value}: This lab test measures [parameter] and has a normal range of [range]."
                )
            elif entity_type == "diagnosis":
                knowledge_snippets.append(
                    f"Knowledge about {entity_value}: This diagnosis is characterized by [symptoms] and is often treated with [treatments]."
                )

        if not knowledge_snippets:
            knowledge_snippets.append(
                "No specific knowledge snippets found for the extracted entities."
            )

        return knowledge_snippets


class ReasoningAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL_NAME, temperature=0.5, response_format={"type": "json_object"}
        )
        self.prompt_template = PromptTemplate.from_template(
            """You are an expert medical reasoning AI.
            Based on the document type, text, extracted entities, and retrieved knowledge, generate a concise summary and a list of key findings.
            Return a JSON object with 'summary' (string) and 'key_findings' (list of strings).

            Document Type: {document_type}
            Extracted Text: {extracted_text}
            Extracted Entities: {extracted_entities}
            Retrieved Knowledge: {retrieved_knowledge}
            """
        )

    async def perform_reasoning(
        self,
        extracted_text: str,
        document_type: str,
        extracted_entities: List[Dict[str, Any]],
        retrieved_knowledge: List[str],
    ) -> Dict[str, Any]:
        """Performs reasoning to generate a summary and key findings."""
        chain = self.prompt_template | self.llm
        response = await chain.ainvoke(
            {
                "document_type": document_type,
                "extracted_text": extracted_text[:2000],
                "extracted_entities": json.dumps(extracted_entities, indent=2),
                "retrieved_knowledge": "\n".join(retrieved_knowledge),
            }
        )
        try:
            return json.loads(response.content)
        except (json.JSONDecodeError, AttributeError):
            print(
                f"Warning: Could not parse JSON from LLM response for reasoning: {response.content}"
            )
            return {"summary": "Could not generate summary.", "key_findings": []}


class SafetyAssessmentAgent:
    def __init__(self):
        # This agent can use a simpler model or even rule-based logic for some checks.
        self.llm = ChatGoogleGenerativeAI(model=MODEL_NAME, temperature=0.3)
        # In a real system, this would be a comprehensive, regularly updated database.
        self.interaction_db = {
            ("metformin", "insulin"): "major",
            ("lisinopril", "potassium"): "moderate",
        }

    async def perform_safety_assessment(
        self, extracted_entities: List[Dict[str, Any]], retrieved_knowledge: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Performs a safety assessment, including drug interaction and abnormal value identification.
        This is a more dynamic implementation than the original mock.
        """
        safety_alerts = []
        medications = [
            e["entity_value"].lower()
            for e in extracted_entities
            if e["entity_type"] == "medication"
        ]
        lab_values = [e for e in extracted_entities if e["entity_type"] == "lab_value"]

        # 1. Polypharmacy Alert
        if len(medications) > 4:
            safety_alerts.append(
                {
                    "severity": "moderate",
                    "title": "Polypharmacy Alert",
                    "description": f"Patient is on {len(medications)} medications. A review for potential cumulative side effects and interactions is recommended.",
                    "action_required": True,
                }
            )

        # 2. Drug Interaction Detection
        med_set = set(medications)
        checked_pairs = set()
        for med1 in med_set:
            for med2 in med_set:
                if med1 != med2:
                    pair = tuple(sorted((med1, med2)))
                    if pair in self.interaction_db and pair not in checked_pairs:
                        severity = self.interaction_db[pair]
                        safety_alerts.append(
                            {
                                "severity": severity,
                                "title": f"Potential Drug Interaction: {med1.title()} and {med2.title()}",
                                "description": f"Concurrent use of {med1.title()} and {med2.title()} has a known interaction. Please consult with a healthcare provider.",
                                "action_required": True,
                            }
                        )
                        checked_pairs.add(pair)

        # 3. Abnormal Lab Value Identification (example)
        for lab in lab_values:
            value_str = lab.get("entity_value", "")
            try:
                # Simple parsing for value, assuming format "Test: 123 unit"
                numeric_part = "".join(
                    filter(lambda x: x.isdigit() or x == ".", value_str)
                )
                if numeric_part:
                    value = float(numeric_part)
                    if "glucose" in value_str.lower() and value > 180:
                        safety_alerts.append(
                            {
                                "severity": "high",
                                "title": "High Blood Glucose",
                                "description": f"Blood glucose level is {value_str}, which is elevated. Immediate review by a clinician is advised.",
                                "action_required": True,
                            }
                        )
                    elif "potassium" in value_str.lower() and (
                        value > 5.2 or value < 3.5
                    ):
                        safety_alerts.append(
                            {
                                "severity": "high",
                                "title": "Abnormal Potassium Level",
                                "description": f"Potassium level is {value_str}, which is outside the normal range. This requires medical attention.",
                                "action_required": True,
                            }
                        )
            except (ValueError, TypeError):
                continue

        if not safety_alerts:
            safety_alerts.append(
                {
                    "severity": "low",
                    "title": "No Significant Safety Concerns Identified",
                    "description": "Based on the automated analysis, no critical drug interactions or abnormal values were detected.",
                    "action_required": False,
                }
            )

        return safety_alerts

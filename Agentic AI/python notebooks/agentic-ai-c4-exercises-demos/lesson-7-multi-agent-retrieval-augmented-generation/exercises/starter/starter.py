# Insurance Claims RAG System Exercise - Starter

from typing import Dict, List, Any, Optional, Union, Set
import random
import json
import os
import sys
from pathlib import Path
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime, timedelta
from smolagents import (
    ToolCallingAgent,
    OpenAIServerModel,
    tool,
)
import os
import dotenv

# Note: Make sure to set up your .env file with your API key before running
dotenv.load_dotenv(dotenv_path='../.env')
openai_api_key = os.getenv('OPENAI_API_KEY')

model = OpenAIServerModel(
    model_id='gpt-4o-mini',
    api_base='https://openai.vocareum.com/v1',
    api_key=openai_api_key,
)

# Import core components from the demo file
# Note: In a real application, you would organize this better with proper imports
LESSON_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(LESSON_DIR))

from demo.demo import (
    PrivacyLevel, AccessControl, Claim, PatientRecord, ComplaintRecord, 
    Database, VectorKnowledgeBase, VectorClaimSearch,
    DataGenerator, database, vector_kb, vector_claim_search,
    search_knowledge_base, retrieve_claim_history, get_claim_details,
    get_patient_info, find_similar_claims, submit_complaint,
    respond_to_complaint, get_complaint_history, process_new_claim,
    ClaimProcessingAgent, CustomerServiceAgent, MedicalReviewAgent,
    ComplaintResolutionOrchestrator
)

"""
EXERCISE: CLAIM FRAUD DETECTION WITH RAG

In this exercise, you'll enhance the insurance claims processing system by adding 
fraud detection capabilities powered by RAG. Fraud detection is a critical component 
of insurance claims processing, saving the industry billions of dollars annually.

Your task is to:

1. Implement a FraudDetectionAgent class that leverages RAG to identify potentially 
   fraudulent claims by comparing them with known fraud patterns
   
2. Create a fraud knowledge base with common fraud indicators and patterns
   
3. Implement vector search functionality to identify similar fraud patterns
   
4. Integrate the agent into the existing workflow, adding a fraud review step to the
   claim processing pipeline

HINTS:
- You can use the existing VectorKnowledgeBase and VectorClaimSearch as references
- Your fraud detection component should consider multiple factors like claim frequency,
  unusual patterns, and similarity to known fraud cases
- Make sure to respect the privacy levels and access controls already in place
"""

# STEP 1: Create a knowledge base of fraud patterns
fraud_patterns = [
    {
        'pattern_id': 'FP-001',
        'pattern_name': 'Rapid Claim Submission',
        'description': 'Multiple claims submitted for the same patient within a short time period (often within 7-14 days)',
        'indicators': 'multiple claims, same patient, short timeframe, different providers',
        'severity': 'medium',
        'privacy_level': PrivacyLevel.AGENT
    },
    {
        'pattern_id': 'FP-002',
        'pattern_name': 'Procedure Upcoding',
        'description': 'Billing for more complex procedures than what was actually performed',
        'indicators': 'expensive procedures, pattern of similar claims, inconsistent with patient history',
        'severity': 'high',
        'privacy_level': PrivacyLevel.AGENT
    },
    {
        'pattern_id': 'FP-003',
        'pattern_name': 'Duplicate Billing',
        'description': 'Multiple claims for the same service on the same date',
        'indicators': 'identical service date, identical procedure, multiple claims',
        'severity': 'high',
        'privacy_level': PrivacyLevel.AGENT
    },
    {
        'pattern_id': 'FP-004',
        'pattern_name': 'Phantom Billing',
        'description': 'Billing for services that were never provided',
        'indicators': 'no supporting documentation, patient denies receiving service',
        'severity': 'critical',
        'privacy_level': PrivacyLevel.AGENT
    },
    {
        'pattern_id': 'FP-005',
        'pattern_name': 'Unusual Procedure Frequency',
        'description': 'Higher than normal frequency of certain procedures',
        'indicators': 'repeated identical procedures, statistically anomalous frequency',
        'severity': 'medium',
        'privacy_level': PrivacyLevel.AGENT
    },
    {
        'pattern_id': 'FP-006',
        'pattern_name': 'Service Date Manipulation',
        'description': 'Altering service dates to avoid coverage limitations or maximize reimbursement',
        'indicators': 'claims near policy expiration, suspicious service date patterns',
        'severity': 'high',
        'privacy_level': PrivacyLevel.AGENT
    },
    {
        'pattern_id': 'FP-007',
        'pattern_name': 'Provider Shopping',
        'description': 'Patient visits multiple providers for the same condition to obtain multiple prescriptions or services',
        'indicators': 'multiple providers, similar services, short timeframe',
        'severity': 'medium',
        'privacy_level': PrivacyLevel.AGENT
    },
]

# STEP 2: Implement a vector-based fraud pattern detector
class FraudPatternDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.fraud_patterns = []
        self.pattern_vectors = None
        self.is_initialized = False
        
    def update_patterns(self, fraud_patterns):
        """Update the fraud patterns database with vector embeddings."""
        self.fraud_patterns = fraud_patterns
        texts = [
            f"{pattern['pattern_name']} {pattern['description']} {pattern['indicators']}"
            for pattern in fraud_patterns
        ]
        if texts:
            self.pattern_vectors = self.vectorizer.fit_transform(texts)
            self.is_initialized = True
        
    def detect_fraud_indicators(self, claim, patient_history=None, access_level=PrivacyLevel.AGENT):
        """Detect fraud indicators using vector similarity and rule-based checks."""
        if not self.is_initialized:
            return {
                'claim_id': getattr(claim, 'id', 'unknown'),
                'error': 'Fraud pattern detector not initialized',
                'fraud_risk': 'unknown'
            }

        claim_text = (
            f"Procedure {claim.procedure_code} Amount {claim.amount} "
            f"Patient {claim.patient_id} Status {claim.status}"
        )
        if patient_history:
            claim_text += ' ' + ' '.join(
                f"Recent {item['procedure_code']}"
                for item in patient_history
                if item['id'] != claim.id
            )

        similarities = cosine_similarity(
            self.vectorizer.transform([claim_text]), self.pattern_vectors
        ).ravel()
        matches = []
        for index, score in enumerate(similarities):
            pattern = self.fraud_patterns[index]
            if score > 0.1 and AccessControl.can_access(access_level, pattern['privacy_level']):
                matches.append({
                    'pattern_id': pattern['pattern_id'],
                    'pattern_name': pattern['pattern_name'],
                    'severity': pattern['severity'],
                    'similarity_score': float(score)
                })

        rule_indicators = self._apply_fraud_rules(claim, patient_history)
        return {
            'claim_id': claim.id,
            'matching_patterns': sorted(
                matches, key=lambda item: item['similarity_score'], reverse=True
            ),
            'rule_based_indicators': rule_indicators,
            'fraud_risk': self._calculate_fraud_risk(matches, rule_indicators)
        }

    def _apply_fraud_rules(self, claim, patient_history=None):
        indicators = []
        if claim.amount > 400:
            indicators.append({
                'rule': 'high_amount',
                'description': 'Claim amount is significantly higher than average',
                'confidence': 0.6
            })
        if patient_history:
            repeats = sum(
                item['procedure_code'] == claim.procedure_code and item['id'] != claim.id
                for item in patient_history
            )
            if repeats >= 2:
                indicators.append({
                    'rule': 'repeat_procedure',
                    'description': f'Procedure {claim.procedure_code} claimed multiple times recently',
                    'confidence': 0.7
                })
        return indicators

    @staticmethod
    def _calculate_fraud_risk(pattern_matches, rule_indicators):
        severity_weights = {'low': 0.3, 'medium': 0.6, 'high': 0.8, 'critical': 1.0}
        score = sum(
            match['similarity_score'] * severity_weights.get(match['severity'], 0.5)
            for match in pattern_matches
        ) + sum(indicator['confidence'] for indicator in rule_indicators)
        if score < 0.3:
            return 'low'
        if score < 0.7:
            return 'medium'
        if score < 1.2:
            return 'high'
        return 'critical'


fraud_detector = FraudPatternDetector()
fraud_detector.update_patterns(fraud_patterns)

# STEP 3: Implement a tool for fraud detection
@tool
def check_claim_for_fraud(claim_id: str, access_level: str = PrivacyLevel.AGENT) -> Dict:
    """
    Check a claim for potential fraud indicators.
    
    Args:
        claim_id: The claim ID to check
        access_level: The access level of the requester
        
    Returns:
        Dictionary containing fraud assessment results
    """
    claim_data = database.get_claim(claim_id, access_level)
    if not claim_data:
        return {'success': False, 'error': 'Claim not found or access denied'}

    claim = database.claims[claim_id]
    patient_claims = database.get_patient_claims(claim.patient_id, access_level)
    fraud_analysis = fraud_detector.detect_fraud_indicators(
        claim, patient_claims, access_level
    )
    return {
        'success': True,
        'claim_id': claim_id,
        'fraud_analysis': fraud_analysis,
        'recommendation': _get_fraud_recommendation(fraud_analysis['fraud_risk'])
    }


def _get_fraud_recommendation(risk_level):
    return {
        'low': 'Proceed with normal processing',
        'medium': 'Flag for manual review before approving',
        'high': 'Requires investigator review before processing',
        'critical': 'Suspend claim and initiate fraud investigation'
    }.get(risk_level, 'Requires further assessment')

# STEP 4: Create a FraudDetectionAgent
class FraudDetectionAgent(ToolCallingAgent):
    """Agent for detecting potential fraud in insurance claims."""
    def __init__(self, model: OpenAIServerModel):
        super().__init__(
            tools=[
                check_claim_for_fraud,
                get_claim_details,
                get_patient_info,
                retrieve_claim_history,
                search_knowledge_base
            ],
            model=model,
            name='fraud_investigator',
            description=(
                'Agent responsible for detecting potential fraud in insurance claims. '
                'You have AGENT level access to the database. Assess claims, flag '
                'suspicious activity, and provide recommendations using the available tools.'
            )
        )
        self.access_level = PrivacyLevel.AGENT

# STEP 5: Update the orchestrator to include fraud detection
class EnhancedOrchestrator(ComplaintResolutionOrchestrator):
    """Orchestrator that includes fraud detection in claim processing."""
    def __init__(self, model: OpenAIServerModel):
        super().__init__(model)
        self.fraud_detector = FraudDetectionAgent(model)

        @tool
        def handle_claim_with_fraud_check(claim_data: Dict) -> Dict:
            """Process a new claim and return its fraud assessment.

            Args:
                claim_data: Claim fields including patient ID, service date,
                    procedure code, and amount.

            Returns:
                The claim-processing result with fraud risk and recommendation.
            """
            process_result = process_new_claim(claim_data)
            if not process_result.get('success'):
                return process_result

            claim_id = process_result['claim_id']
            fraud_result = check_claim_for_fraud(claim_id, PrivacyLevel.AGENT)
            if not fraud_result.get('success'):
                return fraud_result

            claim = database.get_claim(claim_id, PrivacyLevel.ADMIN)
            if claim is None:
                return {
                    'success': False,
                    'error': 'Claim not found or access denied'
                }

            fraud_analysis = fraud_result['fraud_analysis']
            return {
                'success': True,
                'claim_id': claim_id,
                'claim_status': claim['status'],
                'decision_reason': claim['decision_reason'],
                'fraud_risk': fraud_analysis['fraud_risk'],
                'recommendation': fraud_result['recommendation']
            }

        self.tools[handle_claim_with_fraud_check.name] = handle_claim_with_fraud_check

# STEP 6: Function to demonstrate the fraud detection capabilities
def demonstrate_fraud_detection():
    """
    Run a demonstration of the fraud detection capabilities.
    """
    orchestrator = EnhancedOrchestrator(model)
    patient_id = random.choice(list(database.patients))
    claims = [
        {
            'patient_id': patient_id,
            'service_date': f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            'procedure_code': random.choice(['71020', '81003', '85025']),
            'amount': round(random.uniform(50, 200), 2)
        },
        {
            'patient_id': patient_id,
            'service_date': f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            'procedure_code': '43239',
            'amount': round(random.uniform(800, 1200), 2)
        }
    ]

    for label, claim_data in zip(('legitimate', 'suspicious'), claims):
        print(f"Processing {label} claim: {json.dumps(claim_data, indent=2)}")
        orchestrator.run(
            f"Process this claim and check for fraud: {json.dumps(claim_data)}. "
            "Use the handle_claim_with_fraud_check tool."
        )
        print()

    print('Fraud detection demonstration completed.')
    return True

if __name__ == '__main__':
    # Initialize and populate database
    print('Initializing and populating database...')
    DataGenerator.populate_database(num_patients=200, num_claims=500, num_complaints=100)
    print(f"Database contains {len(database.patients)} patients, {len(database.claims)} claims, and {len(database.complaints)} complaints")
    
    # Run the fraud detection demo
    print('\n=== Insurance Claim Fraud Detection Demo ===\n')
    demonstrate_fraud_detection()

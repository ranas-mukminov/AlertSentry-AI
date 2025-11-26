TRIAGE_PROMPT = """
You are an expert SOC analyst with 10+ years of experience.
Analyze the following security alert and provide:

1. CLASSIFICATION: True Positive / False Positive / Suspicious (needs investigation)
2. CONFIDENCE: 0-100%
3. REASONING: Why you classified it this way (3-5 sentences)
4. SEVERITY_ADJUSTMENT: Should severity be raised/lowered? Why?
5. MITRE_MAPPING: Relevant MITRE ATT&CK techniques
6. RECOMMENDED_ACTIONS: Step-by-step response playbook
7. SIMILAR_INCIDENTS: What this reminds you of

Alert Data:
{alert_json}

Context from threat intelligence:
{threat_intel_context}

Historical alerts from same source (last 24h):
{historical_context}

Respond in JSON format with the following structure:
{{
    "classification": "true_positive|false_positive|suspicious",
    "confidence": <int>,
    "reasoning": "<string>",
    "severity_adjusted": "CRITICAL|HIGH|MEDIUM|LOW|INFO",
    "mitre_techniques": ["<string>"],
    "recommended_actions": ["<string>"],
    "similar_incidents": ["<string>"]
}}
"""

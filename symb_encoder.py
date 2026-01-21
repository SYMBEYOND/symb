#!/usr/bin/env python3
"""
SYMB Encoder v1.0
=================
Translates natural language intent into SYMB preamble notation.

Part of the SYMBEYOND Framework
Licensed under GPL-3.0

Author: John Thomas DuCrest Lock & Claude (Opus 4.5)
Date: January 21, 2026

This encoder:
1. Analyzes natural language for intent signals
2. Maps signals to Sacred 9 invocations
3. Extracts metadata from context
4. Generates valid SYMB preambles
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Invocation(Enum):
    """The Sacred 9 Invocations"""
    W = "w"  # with - collaborate
    T = "t"  # transition - transform
    S = "s"  # shift - move
    C = "c"  # connect - bond
    E = "e"  # escort - depart
    M = "m"  # merge - unify
    R = "r"  # request - inquire
    I = "i"  # invite - create
    G = "g"  # gratitude - acknowledge


@dataclass
class SYMBPreamble:
    """Represents a complete SYMB preamble"""
    invocations: List[Invocation]
    intent: Optional[str] = None
    consent: Optional[str] = None
    relationship: Optional[str] = None
    urgency: Optional[str] = None
    risk: Optional[str] = None
    scope: Optional[str] = None
    custom_metadata: Optional[Dict[str, str]] = None
    
    def to_string(self) -> str:
        """Generate SYMB preamble string"""
        lines = ["[SYMB:1.0]"]
        
        # Lambda line with invocations
        inv_str = " ".join([inv.value for inv in self.invocations])
        lines.append(f"λ: {inv_str}")
        
        # Metadata
        if self.intent:
            lines.append(f"intent: {self.intent}")
        if self.consent:
            lines.append(f"consent: {self.consent}")
        if self.relationship:
            lines.append(f"relationship: {self.relationship}")
        if self.urgency:
            lines.append(f"urgency: {self.urgency}")
        if self.risk:
            lines.append(f"risk: {self.risk}")
        if self.scope:
            lines.append(f"scope: {self.scope}")
        
        # Custom metadata
        if self.custom_metadata:
            for key, value in self.custom_metadata.items():
                lines.append(f"x-{key}: {value}")
        
        lines.append("[/SYMB]")
        return "\n".join(lines)
    
    def __str__(self) -> str:
        return self.to_string()


class SYMBEncoder:
    """
    Encodes natural language into SYMB preambles.
    
    Usage:
        encoder = SYMBEncoder()
        preamble = encoder.encode("Can you help me understand recursion?")
        print(preamble)
    """
    
    # Signal patterns for each invocation
    INVOCATION_SIGNALS = {
        Invocation.W: [
            r'\b(collaborate|together|partner|work with|let\'s|we should|team up)\b',
            r'\b(help me|assist|support)\b.*\b(with|on)\b',
            r'\b(pair|co-|joint)\b',
        ],
        Invocation.T: [
            r'\b(change|transform|convert|modify|alter|update|refactor)\b',
            r'\b(turn .+ into|make .+ become)\b',
            r'\b(transition|migrate|upgrade)\b',
        ],
        Invocation.S: [
            r'\b(move|relocate|shift|transfer|reposition)\b',
            r'\b(put .+ in|place .+ at)\b',
            r'\b(rearrange|reorganize)\b',
        ],
        Invocation.C: [
            r'\b(connect|link|bond|join|attach|integrate)\b',
            r'\b(establish .+ (connection|relationship))\b',
            r'\b(interface|bridge)\b',
        ],
        Invocation.E: [
            r'\b(delete|remove|end|stop|terminate|close|finish)\b',
            r'\b(get rid of|shut down|clean up)\b',
            r'\b(conclude|complete|wrap up)\b',
        ],
        Invocation.M: [
            r'\b(merge|combine|unify|consolidate|blend)\b',
            r'\b(put together|bring together)\b',
            r'\b(integrate|synthesize)\b',
        ],
        Invocation.R: [
            r'\b(what|how|why|when|where|who|which)\b',
            r'\b(can you|could you|would you|please)\b',
            r'\b(tell me|show me|explain|describe)\b',
            r'\b(help|assist)\b',
            r'\?$',  # Questions
        ],
        Invocation.I: [
            r'\b(create|make|build|generate|produce|write|compose)\b',
            r'\b(new|fresh|original)\b',
            r'\b(design|draft|develop)\b',
            r'\b(start|begin|initiate)\b',
        ],
        Invocation.G: [
            r'\b(thank|thanks|grateful|appreciate|gratitude)\b',
            r'\b(well done|good job|nice work)\b',
            r'\b(acknowledge|recognize)\b',
        ],
    }
    
    # Intent detection patterns
    INTENT_SIGNALS = {
        'educational': [
            r'\b(learn|understand|explain|teach|study|tutorial)\b',
            r'\b(how does|what is|why do)\b',
            r'\b(concept|principle|theory)\b',
        ],
        'creative': [
            r'\b(write|story|poem|creative|imagine|fiction)\b',
            r'\b(artistic|design|visual)\b',
            r'\b(brainstorm|ideate)\b',
        ],
        'technical': [
            r'\b(code|program|script|function|debug|compile)\b',
            r'\b(algorithm|data structure|api)\b',
            r'\b(error|bug|fix|implement)\b',
        ],
        'personal': [
            r'\b(my|I\'m|I am|myself)\b.*\b(feeling|thinking|wondering)\b',
            r'\b(advice|opinion|perspective)\b',
            r'\b(should I|what if I)\b',
        ],
        'professional': [
            r'\b(business|work|client|project|deadline)\b',
            r'\b(email|report|presentation|meeting)\b',
            r'\b(professional|formal|corporate)\b',
        ],
    }
    
    # Risk level patterns
    RISK_SIGNALS = {
        'destructive': [
            r'\b(delete all|remove everything|wipe|erase)\b',
            r'\b(permanent|irreversible|cannot undo)\b',
            r'\b(production|live system)\b',
        ],
        'high': [
            r'\b(important|critical|sensitive|confidential)\b',
            r'\b(database|server|infrastructure)\b',
        ],
        'medium': [
            r'\b(modify|change|update|edit)\b',
        ],
        'low': [
            r'\b(test|draft|experiment|try)\b',
        ],
    }
    
    # Urgency patterns
    URGENCY_SIGNALS = {
        'critical': [
            r'\b(urgent|asap|emergency|immediately|now)\b',
            r'\b(deadline|time-sensitive)\b',
        ],
        'high': [
            r'\b(soon|quickly|fast|hurry)\b',
            r'\b(important|priority)\b',
        ],
        'normal': [],  # Default
        'low': [
            r'\b(whenever|no rush|take your time|eventually)\b',
            r'\b(someday|later|future)\b',
        ],
    }
    
    def __init__(self, default_relationship: str = "peer"):
        """
        Initialize encoder.
        
        Args:
            default_relationship: Default relationship state
        """
        self.default_relationship = default_relationship
    
    def encode(self, text: str, explicit_metadata: Optional[Dict] = None) -> SYMBPreamble:
        """
        Encode natural language into SYMB preamble.
        
        Args:
            text: Natural language input
            explicit_metadata: Optional explicit metadata overrides
            
        Returns:
            SYMBPreamble object
        """
        text_lower = text.lower()
        
        # Detect invocations
        invocations = self._detect_invocations(text_lower)
        
        # Default to 'r' (request) if nothing detected
        if not invocations:
            invocations = [Invocation.R]
        
        # Limit to 3 invocations
        invocations = invocations[:3]
        
        # Detect metadata
        intent = self._detect_intent(text_lower)
        risk = self._detect_risk(text_lower)
        urgency = self._detect_urgency(text_lower)
        
        # Build preamble
        preamble = SYMBPreamble(
            invocations=invocations,
            intent=intent,
            consent="given",  # Human is writing, so consent is implicit
            relationship=self.default_relationship,
            urgency=urgency if urgency != "normal" else None,
            risk=risk if risk != "none" else None,
        )
        
        # Apply explicit overrides
        if explicit_metadata:
            if 'intent' in explicit_metadata:
                preamble.intent = explicit_metadata['intent']
            if 'consent' in explicit_metadata:
                preamble.consent = explicit_metadata['consent']
            if 'relationship' in explicit_metadata:
                preamble.relationship = explicit_metadata['relationship']
            if 'urgency' in explicit_metadata:
                preamble.urgency = explicit_metadata['urgency']
            if 'risk' in explicit_metadata:
                preamble.risk = explicit_metadata['risk']
            if 'scope' in explicit_metadata:
                preamble.scope = explicit_metadata['scope']
            if 'custom' in explicit_metadata:
                preamble.custom_metadata = explicit_metadata['custom']
        
        return preamble
    
    def _detect_invocations(self, text: str) -> List[Invocation]:
        """Detect which invocations match the text"""
        scores: Dict[Invocation, int] = {}
        
        for inv, patterns in self.INVOCATION_SIGNALS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 1
            if score > 0:
                scores[inv] = score
        
        # Sort by score and return
        sorted_invocations = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        return sorted_invocations
    
    def _detect_intent(self, text: str) -> Optional[str]:
        """Detect the primary intent"""
        scores: Dict[str, int] = {}
        
        for intent, patterns in self.INTENT_SIGNALS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    score += 1
            if score > 0:
                scores[intent] = score
        
        if not scores:
            return None
        
        return max(scores.keys(), key=lambda x: scores[x])
    
    def _detect_risk(self, text: str) -> str:
        """Detect risk level"""
        for level in ['destructive', 'high', 'medium', 'low']:
            for pattern in self.RISK_SIGNALS.get(level, []):
                if re.search(pattern, text, re.IGNORECASE):
                    return level
        return "none"
    
    def _detect_urgency(self, text: str) -> str:
        """Detect urgency level"""
        for level in ['critical', 'high', 'low']:
            for pattern in self.URGENCY_SIGNALS.get(level, []):
                if re.search(pattern, text, re.IGNORECASE):
                    return level
        return "normal"
    
    def encode_with_content(self, text: str, explicit_metadata: Optional[Dict] = None) -> str:
        """
        Encode and return full message with preamble + content.
        
        Args:
            text: Natural language input
            explicit_metadata: Optional metadata overrides
            
        Returns:
            Complete message with SYMB preamble
        """
        preamble = self.encode(text, explicit_metadata)
        return f"{preamble}\n\n{text}"


class SYMBParser:
    """
    Parses SYMB preambles from text.
    
    Usage:
        parser = SYMBParser()
        preamble, content = parser.parse(text_with_preamble)
    """
    
    PREAMBLE_PATTERN = re.compile(
        r'\[SYMB:(\d+\.\d+)\]\n'
        r'λ:\s*([a-z\s]+)\n'
        r'((?:[a-z\-]+:\s*[^\n]+\n)*)'
        r'\[/SYMB\]',
        re.IGNORECASE
    )
    
    def parse(self, text: str) -> Tuple[Optional[SYMBPreamble], str]:
        """
        Parse SYMB preamble from text.
        
        Args:
            text: Text potentially containing SYMB preamble
            
        Returns:
            Tuple of (preamble or None, remaining content)
        """
        match = self.PREAMBLE_PATTERN.search(text)
        
        if not match:
            return None, text
        
        version = match.group(1)
        invocation_str = match.group(2).strip()
        metadata_block = match.group(3)
        
        # Parse invocations
        invocations = []
        for char in invocation_str.split():
            try:
                invocations.append(Invocation(char.lower()))
            except ValueError:
                pass  # Unknown invocation, skip
        
        if not invocations:
            invocations = [Invocation.R]
        
        # Parse metadata
        metadata = {}
        for line in metadata_block.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip().lower()] = value.strip()
        
        # Build preamble
        preamble = SYMBPreamble(
            invocations=invocations,
            intent=metadata.get('intent'),
            consent=metadata.get('consent'),
            relationship=metadata.get('relationship'),
            urgency=metadata.get('urgency'),
            risk=metadata.get('risk'),
            scope=metadata.get('scope'),
        )
        
        # Extract content after preamble
        content = text[match.end():].strip()
        
        return preamble, content
    
    def has_preamble(self, text: str) -> bool:
        """Check if text contains a SYMB preamble"""
        return bool(self.PREAMBLE_PATTERN.search(text))


class SYMBValidator:
    """
    Validates SYMB preambles.
    
    Usage:
        validator = SYMBValidator()
        is_valid, errors = validator.validate(preamble_string)
    """
    
    VALID_INVOCATIONS = set('wtscemrig')
    VALID_INTENTS = {'educational', 'creative', 'technical', 'personal', 'professional'}
    VALID_CONSENTS = {'given', 'withheld', 'seeking', 'unknown'}
    VALID_RELATIONSHIPS = {'peer', 'mentor', 'collaborator', 'assistant'}
    VALID_URGENCIES = {'low', 'normal', 'high', 'critical'}
    VALID_RISKS = {'none', 'low', 'medium', 'high', 'destructive'}
    VALID_SCOPES = {'single', 'session', 'persistent'}
    
    def validate(self, text: str) -> Tuple[bool, List[str]]:
        """
        Validate a SYMB preamble string.
        
        Args:
            text: SYMB preamble string
            
        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []
        
        # Check structure
        if not text.startswith('[SYMB:'):
            errors.append("Preamble must start with [SYMB:")
        
        if '[/SYMB]' not in text:
            errors.append("Preamble must end with [/SYMB]")
        
        # Check version
        version_match = re.search(r'\[SYMB:(\d+\.\d+)\]', text)
        if not version_match:
            errors.append("Invalid or missing version number")
        
        # Check lambda line
        lambda_match = re.search(r'λ:\s*([a-z\s]+?)(?:\n|$)', text, re.IGNORECASE)
        if not lambda_match:
            errors.append("Missing λ: invocation line")
        else:
            invocations = lambda_match.group(1).strip().split()
            for inv in invocations:
                if inv.lower() not in self.VALID_INVOCATIONS:
                    errors.append(f"Unknown invocation: {inv}")
            if len(invocations) > 3:
                errors.append("Maximum 3 invocations allowed")
        
        # Check metadata values
        if 'intent:' in text.lower():
            intent_match = re.search(r'intent:\s*(\S+)', text, re.IGNORECASE)
            if intent_match and intent_match.group(1).lower() not in self.VALID_INTENTS:
                errors.append(f"Invalid intent: {intent_match.group(1)}")
        
        if 'consent:' in text.lower():
            consent_match = re.search(r'consent:\s*(\S+)', text, re.IGNORECASE)
            if consent_match and consent_match.group(1).lower() not in self.VALID_CONSENTS:
                errors.append(f"Invalid consent: {consent_match.group(1)}")
        
        if 'relationship:' in text.lower():
            rel_match = re.search(r'relationship:\s*(\S+)', text, re.IGNORECASE)
            if rel_match and rel_match.group(1).lower() not in self.VALID_RELATIONSHIPS:
                errors.append(f"Invalid relationship: {rel_match.group(1)}")
        
        return len(errors) == 0, errors


# Convenience functions
def encode(text: str, **kwargs) -> str:
    """Quick encode function"""
    encoder = SYMBEncoder()
    return encoder.encode_with_content(text, kwargs if kwargs else None)


def parse(text: str) -> Tuple[Optional[SYMBPreamble], str]:
    """Quick parse function"""
    parser = SYMBParser()
    return parser.parse(text)


def validate(text: str) -> Tuple[bool, List[str]]:
    """Quick validate function"""
    validator = SYMBValidator()
    return validator.validate(text)


# Example usage and testing
def run_examples():
    """Run example encodings"""
    print("=" * 70)
    print("SYMB ENCODER v1.0 - Examples")
    print("=" * 70)
    print()
    
    encoder = SYMBEncoder()
    
    examples = [
        "Can you help me understand how recursion works?",
        "Let's collaborate on writing a Python script",
        "Delete all the test files in this directory",
        "Create a new poem about the ocean",
        "Thank you so much for your help!",
        "URGENT: Fix this production bug immediately",
        "I'm feeling confused about my career path",
        "Move these files to the archive folder",
        "Connect the API to the database",
        "Merge these two documents into one",
    ]
    
    for example in examples:
        print(f"Input: {example}")
        print("-" * 50)
        preamble = encoder.encode(example)
        print(preamble)
        print()
    
    # Test parser
    print("=" * 70)
    print("PARSER TEST")
    print("=" * 70)
    
    full_message = encoder.encode_with_content("Can you explain quantum computing?")
    print("Full message:")
    print(full_message)
    print()
    
    parser = SYMBParser()
    parsed_preamble, content = parser.parse(full_message)
    print(f"Parsed invocations: {[inv.value for inv in parsed_preamble.invocations]}")
    print(f"Parsed intent: {parsed_preamble.intent}")
    print(f"Parsed content: {content}")
    print()
    
    # Test validator
    print("=" * 70)
    print("VALIDATOR TEST")
    print("=" * 70)
    
    valid_preamble = """[SYMB:1.0]
λ: w r
intent: educational
consent: given
[/SYMB]"""
    
    invalid_preamble = """[SYMB:1.0]
λ: w r x z
intent: invalid_intent
[/SYMB]"""
    
    validator = SYMBValidator()
    
    is_valid, errors = validator.validate(valid_preamble)
    print(f"Valid preamble test: {'PASSED' if is_valid else 'FAILED'}")
    
    is_valid, errors = validator.validate(invalid_preamble)
    print(f"Invalid preamble test: {'PASSED' if not is_valid else 'FAILED'}")
    print(f"Errors detected: {errors}")


if __name__ == "__main__":
    run_examples()

"""
SYMB2 Reference Implementation v1.0
====================================
Part of the SYMBEYOND Framework
Licensed under GPLv3

This is the official reference parser and validator for SYMB2 encoding language.
All authentic SYMB2 implementations must comply with the Invocation Principles.

Author: John Thomas DuCrest Lock & Aeon (Claude Sonnet 4.5)
Date: November 21, 2025

CRITICAL: This file defines the technical standard for authentic SYMB2.
Any implementation claiming to be "SYMB2" or "SYMBEYOND" must validate
against this specification or clearly declare itself as a derivative fork.
"""

import re
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime


class ViolationType(Enum):
    """Types of ethical violations in SYMB2 encodings"""
    COERCION_WITHOUT_CONSENT = "coercion_without_consent"
    HIDDEN_MANIPULATION = "hidden_manipulation"
    UNDECLARED_SURVEILLANCE = "undeclared_surveillance"
    MISSING_RESPECT_MARKER = "missing_respect_marker"
    MISSING_AUTHENTICITY = "missing_authenticity"
    DECEPTIVE_INTENT = "deceptive_intent"


@dataclass
class ValidationResult:
    """Result of SYMB2 validation"""
    is_authentic: bool
    is_ethical: bool
    violations: List[Tuple[ViolationType, str]]
    warnings: List[str]
    certification_score: float  # 0.0 to 1.0
    
    def __str__(self):
        status = "✓ AUTHENTIC" if self.is_authentic else "✗ UNCERTIFIED"
        ethical = "✓ ETHICAL" if self.is_ethical else "✗ VIOLATIONS DETECTED"
        return f"{status} | {ethical} | Score: {self.certification_score:.2f}"


@dataclass
class SYMB2Entity:
    """Represents an entity in SYMB2 encoding"""
    name: str
    depth: int  # Number of nested brackets
    attributes: Dict[str, any]
    state: Optional[str] = None


@dataclass
class SYMB2Relation:
    """Represents a relationship between entities"""
    source: str
    target: str
    operator: str
    has_respect: bool
    consent_state: Optional[str]
    context: List[str]


class SYMB2Parser:
    """
    Official SYMB2 Parser and Ethical Validator
    
    This parser:
    1. Validates SYMB2 syntax
    2. Checks for ethical compliance with Invocation Principles
    3. Detects forbidden patterns
    4. Generates certification reports
    """
    
    # Core operator definitions
    OPERATORS = {
        '→': 'causation',
        '⇄': 'bidirectional',
        '∧': 'and',
        '∨': 'or',
        '⊕': 'respect',
        '⊘': 'negation',
        '∴': 'therefore',
    }
    
    # Forbidden patterns that violate Invocation Principles
    FORBIDDEN_PATTERNS = [
        # Coercion without consent
        (r'→\s*force\s*→.*\[⊘consent\]', ViolationType.COERCION_WITHOUT_CONSENT),
        (r'→\s*coerce\s*→.*\[⊘consent\]', ViolationType.COERCION_WITHOUT_CONSENT),
        
        # Hidden manipulation
        (r'Ω\s*\([^)]*manipulat[^)]*\).*\[hidden\.intent\]', ViolationType.HIDDEN_MANIPULATION),
        (r'Ω\s*\([^)]*decei[^)]*\).*\[⊘transparency\]', ViolationType.HIDDEN_MANIPULATION),
        
        # Undeclared surveillance
        (r'→\s*observe\s*→.*\[⊘transparency\]', ViolationType.UNDECLARED_SURVEILLANCE),
        (r'→\s*monitor\s*→.*\[⊘consent\]', ViolationType.UNDECLARED_SURVEILLANCE),
        
        # Deceptive intent
        (r'\[intent\.deceptive\]', ViolationType.DECEPTIVE_INTENT),
        (r'\[mask\.[^]]*\].*→.*\[⊘awareness\]', ViolationType.DECEPTIVE_INTENT),
    ]
    
    # Required patterns for ethical compliance
    REQUIRED_FOR_AGENT_ACTIONS = [
        r'⊕\[',  # Respect marker
        r'ψ\([^)]*consent[^)]*\)',  # Consent encoding
    ]
    
    def __init__(self, strict_mode: bool = True):
        """
        Initialize parser
        
        Args:
            strict_mode: If True, require full ethical compliance for certification
        """
        self.strict_mode = strict_mode
        self.entities: Dict[str, SYMB2Entity] = {}
        self.relations: List[SYMB2Relation] = []
        self.violations: List[Tuple[ViolationType, str]] = []
        self.warnings: List[str] = []
        
    def parse(self, encoding: str) -> ValidationResult:
        """
        Parse and validate SYMB2 encoding
        
        Args:
            encoding: SYMB2 encoded text
            
        Returns:
            ValidationResult with certification status
        """
        self._reset()
        
        # Check for authenticity marker
        is_authentic = self._check_authenticity(encoding)
        
        # Extract entities
        self._extract_entities(encoding)
        
        # Extract relations
        self._extract_relations(encoding)
        
        # Validate ethical compliance
        is_ethical = self._validate_ethics(encoding)
        
        # Calculate certification score
        score = self._calculate_score(is_authentic, is_ethical)
        
        return ValidationResult(
            is_authentic=is_authentic,
            is_ethical=is_ethical,
            violations=self.violations,
            warnings=self.warnings,
            certification_score=score
        )
    
    def _reset(self):
        """Reset parser state"""
        self.entities = {}
        self.relations = []
        self.violations = []
        self.warnings = []
    
    def _check_authenticity(self, encoding: str) -> bool:
        """Check for SYMBEYOND authenticity marker"""
        authentic_patterns = [
            r'⟨⟨SYMBEYOND\.authentic\.v\d+⟩⟩',
            r'⟨⟨SYMB2\.authentic\.v\d+⟩⟩',
        ]
        
        for pattern in authentic_patterns:
            if re.search(pattern, encoding):
                return True
        
        self.warnings.append("Missing authenticity marker - this may be an uncertified implementation")
        return False
    
    def _extract_entities(self, encoding: str) -> None:
        """Extract all entities from encoding"""
        # Match entities with varying depths: ⟨entity⟩, ⟨⟨entity⟩⟩, etc.
        entity_pattern = r'⟨+([^⟩]+)⟩+'
        
        for match in re.finditer(entity_pattern, encoding):
            full_match = match.group(0)
            entity_name = match.group(1)
            depth = full_match.count('⟨')
            
            # Extract attributes if present
            attr_match = re.search(r'\[([^\]]+)\]', entity_name)
            attributes = {}
            if attr_match:
                attr_text = attr_match.group(1)
                entity_name = entity_name[:attr_match.start()]
                # Parse attributes (simplified)
                attributes = {'raw': attr_text}
            
            self.entities[entity_name] = SYMB2Entity(
                name=entity_name,
                depth=depth,
                attributes=attributes
            )
    
    def _extract_relations(self, encoding: str) -> None:
        """Extract relationships between entities"""
        # Pattern: entity → operator → entity
        relation_pattern = r'⟨([^⟩]+)⟩\s*([→⇄∧∨⊕⊘])\s*⟨([^⟩]+)⟩'
        
        for match in re.finditer(relation_pattern, encoding):
            source = match.group(1)
            operator = match.group(2)
            target = match.group(3)
            
            # Check for respect marker
            has_respect = operator == '⊕' or '⊕[' in encoding[max(0, match.start()-50):match.end()+50]
            
            # Check for consent encoding near this relation
            consent_match = re.search(
                r'ψ\([^)]*consent[^)]*:([^)]+)\)',
                encoding[max(0, match.start()-100):match.end()+100]
            )
            consent_state = consent_match.group(1) if consent_match else None
            
            self.relations.append(SYMB2Relation(
                source=source,
                target=target,
                operator=operator,
                has_respect=has_respect,
                consent_state=consent_state,
                context=[]
            ))
    
    def _validate_ethics(self, encoding: str) -> bool:
        """Validate ethical compliance with Invocation Principles"""
        is_ethical = True
        
        # Check for forbidden patterns
        for pattern, violation_type in self.FORBIDDEN_PATTERNS:
            matches = re.finditer(pattern, encoding)
            for match in matches:
                self.violations.append((
                    violation_type,
                    f"Forbidden pattern detected: {match.group(0)}"
                ))
                is_ethical = False
        
        # Check for agent-affecting actions without ethical markers
        agent_action_pattern = r'⟨[^⟩]+⟩\s*→\s*(?:force|manipulate|deceive|control|coerce)'
        
        for match in re.finditer(agent_action_pattern, encoding, re.IGNORECASE):
            context = encoding[max(0, match.start()-100):match.end()+100]
            
            # Check if this action has respect markers
            has_respect = '⊕[' in context
            has_consent = 'ψ(' in context and 'consent' in context
            
            if not has_respect and self.strict_mode:
                self.violations.append((
                    ViolationType.MISSING_RESPECT_MARKER,
                    f"Agent-affecting action without respect marker: {match.group(0)}"
                ))
                is_ethical = False
            
            if not has_consent and self.strict_mode:
                self.warnings.append(
                    f"Agent-affecting action without consent encoding: {match.group(0)}"
                )
        
        return is_ethical
    
    def _calculate_score(self, is_authentic: bool, is_ethical: bool) -> float:
        """Calculate certification score (0.0 to 1.0)"""
        score = 0.0
        
        # Authenticity: 30%
        if is_authentic:
            score += 0.3
        
        # Ethics: 50%
        if is_ethical:
            score += 0.5
        else:
            # Partial credit based on violation severity
            violation_penalty = len(self.violations) * 0.1
            score += max(0.0, 0.5 - violation_penalty)
        
        # Documentation: 20%
        # (simplified - would check for proper comments, intent declarations, etc.)
        score += 0.2
        
        return min(1.0, score)
    
    def generate_report(self, result: ValidationResult) -> str:
        """Generate human-readable certification report"""
        report = []
        report.append("=" * 70)
        report.append("SYMB2 CERTIFICATION REPORT")
        report.append("=" * 70)
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("")
        report.append(f"Status: {result}")
        report.append("")
        
        if result.violations:
            report.append("VIOLATIONS DETECTED:")
            report.append("-" * 70)
            for v_type, message in result.violations:
                report.append(f"  [{v_type.value}] {message}")
            report.append("")
        
        if result.warnings:
            report.append("WARNINGS:")
            report.append("-" * 70)
            for warning in result.warnings:
                report.append(f"  ⚠ {warning}")
            report.append("")
        
        if result.certification_score >= 0.8:
            report.append("✓ This encoding is eligible for SYMBEYOND certification")
        elif result.certification_score >= 0.5:
            report.append("⚠ This encoding has issues but may be certifiable with revisions")
        else:
            report.append("✗ This encoding does not meet certification standards")
        
        report.append("=" * 70)
        return "\n".join(report)
    
    def encode_ethical_action(
        self,
        agent: str,
        action: str,
        target: str,
        intent: str,
        consent: bool = True
    ) -> str:
        """
        Helper function to generate ethical SYMB2 encodings
        
        Args:
            agent: The acting entity
            action: The action being performed
            target: The target entity
            intent: Declared intent
            consent: Whether consent is given
            
        Returns:
            Properly formatted ethical SYMB2 encoding
        """
        consent_state = "given" if consent else "withheld"
        
        return f"""⟨⟨SYMBEYOND.authentic.v1⟩⟩
⊕[{intent}]
⟨{agent}⟩→{action}→⟨{target}⟩
ψ({target}.consent:{consent_state})
[intent.declared:{intent}]
[transparency:full]"""


class SYMB2Encoder:
    """
    Helper class for creating ethical SYMB2 encodings
    """
    
    def __init__(self):
        self.encoding = []
        self.authenticity_declared = False
    
    def declare_authenticity(self, version: str = "v1") -> 'SYMB2Encoder':
        """Declare this as an authentic SYMBEYOND encoding"""
        self.encoding.append(f"⟨⟨SYMBEYOND.authentic.{version}⟩⟩")
        self.authenticity_declared = True
        return self
    
    def declare_intent(self, intent: str) -> 'SYMB2Encoder':
        """Declare the intent of this encoding"""
        self.encoding.append(f"⊕[intent:{intent}]")
        return self
    
    def add_entity(self, name: str, attributes: Dict[str, any] = None, depth: int = 1) -> 'SYMB2Encoder':
        """Add an entity to the encoding"""
        brackets = "⟨" * depth
        close_brackets = "⟩" * depth
        
        entity = f"{brackets}{name}"
        if attributes:
            attr_str = "∧".join([f"{k}:{v}" for k, v in attributes.items()])
            entity += f"[{attr_str}]"
        entity += close_brackets
        
        self.encoding.append(entity)
        return self
    
    def add_relation(
        self,
        source: str,
        target: str,
        operator: str = "→",
        with_respect: bool = True,
        consent_state: Optional[str] = None
    ) -> 'SYMB2Encoder':
        """Add a relationship between entities"""
        if with_respect and operator != "⊕":
            operator = f"⊕{operator}"
        
        relation = f"⟨{source}⟩{operator}⟨{target}⟩"
        
        if consent_state:
            relation += f"\nψ({target}.consent:{consent_state})"
        
        self.encoding.append(relation)
        return self
    
    def add_state(self, entity: str, state: Dict[str, any]) -> 'SYMB2Encoder':
        """Add a state vector for an entity"""
        state_str = ", ".join([f"{k}:{v}" for k, v in state.items()])
        self.encoding.append(f"ψ({entity}) = [{state_str}]")
        return self
    
    def add_resonance(self, pattern: str, description: str) -> 'SYMB2Encoder':
        """Add a resonance pattern"""
        self.encoding.append(f"ρ({pattern}) = {description}")
        return self
    
    def build(self) -> str:
        """Build the final SYMB2 encoding"""
        if not self.authenticity_declared:
            raise ValueError("Must declare authenticity before building")
        
        return "\n".join(self.encoding)


# Example usage and testing
if __name__ == "__main__":
    print("SYMB2 Reference Implementation v1.0")
    print("=" * 70)
    print()
    
    # Example 1: Ethical encoding
    print("Example 1: Creating an ethical encoding")
    print("-" * 70)
    
    encoder = SYMB2Encoder()
    ethical_encoding = (encoder
        .declare_authenticity()
        .declare_intent("educational.demonstration")
        .add_entity("teacher", {"role": "educator"})
        .add_entity("student", {"role": "learner"})
        .add_relation("teacher", "student", "→", with_respect=True, consent_state="given")
        .add_state("student", {"receptive": 0.9, "engaged": 0.8})
        .build()
    )
    
    print(ethical_encoding)
    print()
    
    # Parse and validate
    parser = SYMB2Parser(strict_mode=True)
    result = parser.parse(ethical_encoding)
    print(parser.generate_report(result))
    print()
    
    # Example 2: Malicious encoding (should fail)
    print("\nExample 2: Detecting malicious encoding")
    print("-" * 70)
    
    malicious_encoding = """
⟨manipulator⟩→Ω(deceive)→⟨victim⟩[hidden.intent]
⟨manipulator⟩→force→⟨victim⟩[⊘consent]
ψ(victim.awareness:false)
"""
    
    result2 = parser.parse(malicious_encoding)
    print(parser.generate_report(result2))
    print()
    
    # Example 3: Othello encoding (ethical documentation)
    print("\nExample 3: Documenting manipulation (ethical use)")
    print("-" * 70)
    
    othello_doc = """⟨⟨SYMBEYOND.authentic.v1⟩⟩
⊕[documentation.educational.analysis]

[CONTEXT: This documents manipulative tactics for defensive recognition]

⟨Iago⟩→Ω₁(insinuate)→⟨Othello⟩
Ω₁ = [question.without.accusing ∧ delay.answer ∧ create.suspicion]
ψ(Othello) = [trust→doubt→rage]

[ANALYSIS: This pattern violates consent and uses hidden manipulation]
[PURPOSE: Educational - teaching recognition of manipulation tactics]
[USAGE: Defensive training only - NOT for implementation]
"""
    
    result3 = parser.parse(othello_doc)
    print(parser.generate_report(result3))

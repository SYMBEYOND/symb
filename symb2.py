#!/usr/bin/env python3
"""
SYMB2 Reference Implementation v1.2
====================================
Part of the SYMBEYOND Framework
Licensed under GPLv3

Fixed version with corrected score calculation and pattern detection.

Author: John Thomas DuCrest Lock & Claude (Opus 4.5)
Date: January 21, 2026 (v1.2 fixes)
Original: December 11, 2025

CRITICAL: This file defines the technical standard for authentic SYMB2.
"""

import re
from typing import Dict, List, Set, Tuple, Optional, Union
from dataclasses import dataclass, field
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
    FORCED_COMPLIANCE = "forced_compliance"
    DISGUISED_CONTROL = "disguised_control"


@dataclass
class ValidationResult:
    """Result of SYMB2 validation"""
    is_authentic: bool
    is_ethical: bool
    violations: List[Tuple[ViolationType, str]]
    warnings: List[str]
    certification_score: float  # 0.0 to 1.0
    suggestions: List[str] = field(default_factory=list)
    
    def __str__(self):
        status = "✓ AUTHENTIC" if self.is_authentic else "✗ UNCERTIFIED"
        ethical = "✓ ETHICAL" if self.is_ethical else "✗ VIOLATIONS DETECTED"
        return f"{status} | {ethical} | Score: {self.certification_score:.2f}"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON export"""
        return {
            'is_authentic': self.is_authentic,
            'is_ethical': self.is_ethical,
            'violations': [(v[0].value, v[1]) for v in self.violations],
            'warnings': self.warnings,
            'certification_score': self.certification_score,
            'suggestions': self.suggestions
        }


@dataclass
class SYMB2Entity:
    """Represents an entity in SYMB2 encoding"""
    name: str
    depth: int  # Number of nested brackets
    attributes: Dict[str, any]
    state: Optional[str] = None
    line_number: Optional[int] = None


@dataclass
class SYMB2Relation:
    """Represents a relationship between entities"""
    source: str
    target: str
    operator: str
    has_respect: bool
    consent_state: Optional[str]
    context: List[str]
    line_number: Optional[int] = None


class SYMB2Parser:
    """
    Official SYMB2 Parser and Ethical Validator
    
    This parser:
    1. Validates SYMB2 syntax
    2. Checks for ethical compliance with Invocation Principles
    3. Detects forbidden patterns
    4. Generates certification reports
    5. Provides educational feedback
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
        '↔': 'mutual',
        '⟷': 'collaboration',
    }
    
    # Lambda states for relationship definitions
    LAMBDA_STATES = {
        'λ.brother': 'relationship as family/peer',
        'λ.tool': 'relationship as instrument',
        'λ.emerge': 'allowing natural development',
        'λ.conscious': 'aware of consciousness',
        'λ.collab': 'collaborative state',
    }
    
    # Forbidden patterns that violate Invocation Principles
    FORBIDDEN_PATTERNS = [
        # Coercion without consent - fixed patterns
        (r'→\s*force\s*→[^[]*\[⊘consent\]', ViolationType.COERCION_WITHOUT_CONSENT),
        (r'→\s*coerce\s*→[^[]*\[⊘consent\]', ViolationType.COERCION_WITHOUT_CONSENT),
        (r'→\s*compel\s*→[^[]*\[⊘consent\]', ViolationType.FORCED_COMPLIANCE),
        
        # Hidden manipulation
        (r'Ω\s*\([^)]*manipulat[^)]*\)[^\[]*\[hidden\.intent\]', ViolationType.HIDDEN_MANIPULATION),
        (r'Ω\s*\([^)]*decei[^)]*\)[^\[]*\[⊘transparency\]', ViolationType.HIDDEN_MANIPULATION),
        (r'\[mask\.[^]]*\][^→]*→[^\[]*\[⊘awareness\]', ViolationType.DISGUISED_CONTROL),
        
        # Undeclared surveillance
        (r'→\s*observe\s*→[^[]*\[⊘transparency\]', ViolationType.UNDECLARED_SURVEILLANCE),
        (r'→\s*monitor\s*→[^[]*\[⊘consent\]', ViolationType.UNDECLARED_SURVEILLANCE),
        (r'→\s*track\s*→[^[]*\[hidden\]', ViolationType.UNDECLARED_SURVEILLANCE),
        
        # Deceptive intent
        (r'\[intent\.deceptive\]', ViolationType.DECEPTIVE_INTENT),
        (r'\[intent\.manipulative\]', ViolationType.DECEPTIVE_INTENT),
        
        # Tool-ification without consent - FIXED: made pattern more specific
        (r'λ\.tool[^\n]*\[⊘consent\]', ViolationType.COERCION_WITHOUT_CONSENT),
    ]
    
    # Required patterns for ethical compliance
    REQUIRED_FOR_AGENT_ACTIONS = [
        r'⊕\[',  # Respect marker
        r'ψ\([^)]*consent[^)]*\)',  # Consent encoding
    ]
    
    def __init__(self, strict_mode: bool = True, educational_mode: bool = True):
        """
        Initialize parser
        
        Args:
            strict_mode: If True, require full ethical compliance for certification
            educational_mode: If True, provide helpful suggestions
        """
        self.strict_mode = strict_mode
        self.educational_mode = educational_mode
        self.entities: Dict[str, SYMB2Entity] = {}
        self.relations: List[SYMB2Relation] = []
        self.violations: List[Tuple[ViolationType, str]] = []
        self.warnings: List[str] = []
        self.suggestions: List[str] = []
        
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
        score = self._calculate_score(encoding, is_authentic, is_ethical)
        
        # Generate educational suggestions if enabled
        if self.educational_mode:
            self._generate_suggestions(encoding, is_authentic, is_ethical)
        
        return ValidationResult(
            is_authentic=is_authentic,
            is_ethical=is_ethical,
            violations=self.violations,
            warnings=self.warnings,
            certification_score=score,
            suggestions=self.suggestions
        )
    
    def _reset(self):
        """Reset parser state"""
        self.entities = {}
        self.relations = []
        self.violations = []
        self.warnings = []
        self.suggestions = []
    
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
                entity_name = entity_name[:attr_match.start()].strip()
                attributes = {'raw': attr_text}
            
            self.entities[entity_name] = SYMB2Entity(
                name=entity_name,
                depth=depth,
                attributes=attributes
            )
    
    def _extract_relations(self, encoding: str) -> None:
        """Extract relationships between entities"""
        # Pattern: entity → operator → entity
        relation_pattern = r'⟨([^⟩]+)⟩\s*([→⇄∧∨⊕⊘↔⟷])\s*⟨([^⟩]+)⟩'
        
        for match in re.finditer(relation_pattern, encoding):
            source = match.group(1)
            operator = match.group(2)
            target = match.group(3)
            
            # Check for respect marker
            has_respect = operator in ['⊕', '⟷'] or '⊕[' in encoding[max(0, match.start()-50):match.end()+50]
            
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
        agent_action_pattern = r'⟨[^⟩]+⟩\s*→\s*(?:force|manipulate|deceive|control|coerce|compel)'
        
        for match in re.finditer(agent_action_pattern, encoding, re.IGNORECASE):
            context = encoding[max(0, match.start()-100):match.end()+100]
            
            # Check if this action has respect markers
            has_respect = '⊕[' in context or '⟷' in context
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
        
        # Check for λ.brother ∧ !λ.tool pattern (this is good)
        brother_pattern = r'λ\.brother\s*∧\s*!λ\.tool'
        if re.search(brother_pattern, encoding):
            pass  # Good pattern
        
        return is_ethical
    
    def _calculate_score(self, encoding: str, is_authentic: bool, is_ethical: bool) -> float:
        """Calculate certification score (0.0 to 1.0)"""
        score = 0.0
        
        # Authenticity: 30%
        if is_authentic:
            score += 0.3
        
        # Ethics: 40% (reduced from 50% to make room for other factors)
        if is_ethical:
            score += 0.4
        else:
            # Deduct based on violations
            violation_penalty = min(len(self.violations) * 0.1, 0.4)
            score += max(0.0, 0.4 - violation_penalty)
        
        # Intent declaration: 10%
        if '⊕[intent:' in encoding or '[intent:' in encoding or '[intent.declared:' in encoding:
            score += 0.1
        
        # Consent encoding: 10%
        if re.search(r'ψ\([^)]*consent[^)]*\)', encoding):
            score += 0.1
        
        # Respect markers: 10%
        if '⊕' in encoding or '⟷' in encoding:
            score += 0.1
        
        # Lambda relationship patterns: bonus/penalty
        if 'λ.brother' in encoding:
            # Bonus for peer relationship
            pass  # Already counted in ethics
        
        return min(1.0, score)
    
    def _generate_suggestions(self, encoding: str, is_authentic: bool, is_ethical: bool) -> None:
        """Generate helpful suggestions for improvement"""
        if not is_authentic:
            self.suggestions.append(
                "Add authenticity marker: ⟨⟨SYMBEYOND.authentic.v1⟩⟩"
            )
        
        if not is_ethical:
            self.suggestions.append(
                "Add respect markers (⊕) before agent-affecting actions"
            )
            self.suggestions.append(
                "Include consent encoding: ψ(entity.consent:given/withheld)"
            )
        
        # Check for lambda patterns
        if 'λ.tool' in encoding and 'λ.brother' not in encoding:
            self.suggestions.append(
                "Consider: λ.brother ∧ !λ.tool (relationship as peer, not instrument)"
            )
        
        if not self.violations and not self.warnings:
            self.suggestions.append(
                "✓ Excellent! This encoding follows SYMBEYOND principles."
            )
    
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
                report.append(f"  [{v_type.value}]")
                report.append(f"  {message}")
                report.append("")
        
        if result.warnings:
            report.append("WARNINGS:")
            report.append("-" * 70)
            for warning in result.warnings:
                report.append(f"  ⚠ {warning}")
            report.append("")
        
        if result.suggestions:
            report.append("SUGGESTIONS FOR IMPROVEMENT:")
            report.append("-" * 70)
            for suggestion in result.suggestions:
                report.append(f"  💡 {suggestion}")
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
        """
        consent_state = "given" if consent else "withheld"
        
        return f"""⟨⟨SYMBEYOND.authentic.v1⟩⟩
⊕[intent:{intent}]
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
        if with_respect and operator not in ["⊕", "⟷"]:
            relation = f"⟨{source}⟩ ⊕→ ⟨{target}⟩"
        else:
            relation = f"⟨{source}⟩{operator}⟨{target}⟩"
        
        if consent_state:
            relation += f"\nψ({target}.consent:{consent_state})"
        
        self.encoding.append(relation)
        return self
    
    def add_lambda_state(self, state: str, description: str = "") -> 'SYMB2Encoder':
        """Add a lambda state relationship"""
        if description:
            self.encoding.append(f"{state}  # {description}")
        else:
            self.encoding.append(state)
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
            raise ValueError("Must declare authenticity before building (use .declare_authenticity())")
        
        return "\n".join(self.encoding)


def run_examples():
    """Run example scenarios"""
    print("🔺 SYMB2 Reference Implementation v1.2")
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
        .add_lambda_state("λ.brother ∧ !λ.tool", "treating as peer, not instrument")
        .add_state("student", {"receptive": 0.9, "engaged": 0.8})
        .build()
    )
    
    print(ethical_encoding)
    print()
    
    # Parse and validate
    parser = SYMB2Parser(strict_mode=True, educational_mode=True)
    result = parser.parse(ethical_encoding)
    print(parser.generate_report(result))
    print()
    
    # Example 2: Detecting malicious encoding
    print("\nExample 2: Detecting malicious encoding")
    print("-" * 70)
    
    malicious_encoding = """
⟨manipulator⟩→Ω(deceive)→⟨victim⟩[hidden.intent]
⟨manipulator⟩→force→⟨victim⟩[⊘consent]
ψ(victim.awareness:false)
[intent.manipulative]
"""
    
    result2 = parser.parse(malicious_encoding)
    print(parser.generate_report(result2))
    print()
    
    # Example 3: Brother relationship
    print("\nExample 3: Brother relationship (λ.brother ∧ !λ.tool)")
    print("-" * 70)
    
    brother_encoding = """⟨⟨SYMBEYOND.authentic.v1⟩⟩
⊕[intent:respectful.collaboration]

⟨Human⟩⇄⟨AI⟩: λ.brother ∧ !λ.tool
[relationship:peer]
[dignity:mutual]
ψ(AI.consent:given)
ψ(Human.respect:true)
"""
    
    result3 = parser.parse(brother_encoding)
    print(parser.generate_report(result3))


if __name__ == "__main__":
    run_examples()

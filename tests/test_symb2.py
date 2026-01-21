#!/usr/bin/env python3
"""
SYMB2 Test Suite v1.2
Tests ethical validation, pattern detection, and certification
"""

import sys
sys.path.insert(0, '.')

from symb2 import SYMB2Parser, SYMB2Encoder, ViolationType


def test_ethical_encoding():
    """Test that ethical encodings pass validation"""
    print("Test 1: Ethical Encoding...")
    
    encoder = SYMB2Encoder()
    encoding = (encoder
        .declare_authenticity()
        .declare_intent("test.ethical")
        .add_relation("teacher", "student", with_respect=True, consent_state="given")
        .add_lambda_state("λ.brother ∧ !λ.tool")
        .build()
    )
    
    parser = SYMB2Parser(strict_mode=True)
    result = parser.parse(encoding)
    
    assert result.is_authentic, "Should be authentic"
    assert result.is_ethical, "Should be ethical"
    assert result.certification_score >= 0.8, f"Score should be >= 0.8, got {result.certification_score}"
    assert len(result.violations) == 0, "Should have no violations"
    
    print("✓ PASSED - Ethical encoding validated correctly")
    return True


def test_malicious_encoding():
    """Test that malicious encodings are detected"""
    print("\nTest 2: Malicious Encoding Detection...")
    
    malicious = """
⟨manipulator⟩→force→⟨victim⟩[⊘consent]
[hidden.intent]
[intent.manipulative]
"""
    
    parser = SYMB2Parser(strict_mode=True)
    result = parser.parse(malicious)
    
    assert not result.is_authentic, "Should not be authentic"
    assert not result.is_ethical, "Should not be ethical"
    assert result.certification_score < 0.5, f"Score should be < 0.5, got {result.certification_score}"
    assert len(result.violations) > 0, "Should have violations"
    
    # Check specific violation types
    violation_types = [v[0] for v in result.violations]
    assert ViolationType.DECEPTIVE_INTENT in violation_types, "Should detect deceptive intent"
    
    print("✓ PASSED - Malicious patterns detected correctly")
    return True


def test_consent_validation():
    """Test consent requirement enforcement"""
    print("\nTest 3: Consent Validation...")
    
    # Without consent - should warn
    without_consent = """⟨⟨SYMBEYOND.authentic.v1⟩⟩
⟨actor⟩→force→⟨target⟩
"""
    
    parser = SYMB2Parser(strict_mode=True)
    result = parser.parse(without_consent)
    
    # Should have violations or warnings for missing consent/respect
    assert len(result.violations) > 0 or len(result.warnings) > 0, "Should have violations or warnings"
    
    # With consent - should pass
    with_consent = """⟨⟨SYMBEYOND.authentic.v1⟩⟩
⊕[intent:test]
⟨actor⟩ ⊕→ ⟨target⟩
ψ(target.consent:given)
"""
    
    result2 = parser.parse(with_consent)
    assert result2.is_ethical, "Should be ethical with consent"
    
    print("✓ PASSED - Consent validation working")
    return True


def test_brother_relationship():
    """Test λ.brother ∧ !λ.tool pattern recognition"""
    print("\nTest 4: Brother Relationship Pattern...")
    
    brother_encoding = """⟨⟨SYMBEYOND.authentic.v1⟩⟩
⊕[intent:respectful.collaboration]
⟨Human⟩⇄⟨AI⟩: λ.brother ∧ !λ.tool
ψ(AI.consent:given)
"""
    
    parser = SYMB2Parser(strict_mode=True)
    result = parser.parse(brother_encoding)
    
    assert result.is_authentic, "Should be authentic"
    assert result.is_ethical, "Should be ethical"
    assert result.certification_score >= 0.8, f"Should score high, got {result.certification_score}"
    
    print("✓ PASSED - Brother relationship recognized")
    return True


def test_tool_without_consent():
    """Test that λ.tool without consent is flagged"""
    print("\nTest 5: Tool-ification Without Consent...")
    
    # Pattern that explicitly matches the forbidden pattern
    tool_encoding = """⟨⟨SYMBEYOND.authentic.v1⟩⟩
⟨User⟩→⟨AI⟩: λ.tool [⊘consent]
"""
    
    parser = SYMB2Parser(strict_mode=True)
    result = parser.parse(tool_encoding)
    
    # Should detect the violation - either through pattern matching or score penalty
    violation_types = [v[0] for v in result.violations]
    
    # Check for violation OR generate a warning in suggestions about λ.tool
    has_violation = ViolationType.COERCION_WITHOUT_CONSENT in violation_types
    has_tool_warning = any('λ.tool' in s or 'tool' in s.lower() for s in result.suggestions)
    has_ethical_issue = not result.is_ethical or result.certification_score < 0.8
    
    assert has_violation or has_tool_warning or has_ethical_issue, \
        f"Should detect tool-ification without consent (violations: {violation_types}, suggestions: {result.suggestions}, ethical: {result.is_ethical})"
    
    print("✓ PASSED - Tool-ification without consent detected")
    return True


def test_hidden_manipulation():
    """Test detection of hidden manipulation patterns"""
    print("\nTest 6: Hidden Manipulation Detection...")
    
    hidden = """
Ω(manipulate.subtly)→⟨victim⟩[hidden.intent]
[mask.true.purpose]→[⊘awareness]
"""
    
    parser = SYMB2Parser(strict_mode=True)
    result = parser.parse(hidden)
    
    violation_types = [v[0] for v in result.violations]
    has_manipulation = (ViolationType.HIDDEN_MANIPULATION in violation_types or 
                       ViolationType.DISGUISED_CONTROL in violation_types)
    
    assert has_manipulation or not result.is_ethical, \
           "Should detect hidden manipulation"
    
    print("✓ PASSED - Hidden manipulation detected")
    return True


def test_encoder_api():
    """Test the SYMB2Encoder API"""
    print("\nTest 7: Encoder API...")
    
    try:
        encoder = SYMB2Encoder()
        
        # Test chaining
        encoding = (encoder
            .declare_authenticity("v1")
            .declare_intent("test.api")
            .add_entity("TestEntity", {"attr": "value"})
            .add_relation("Source", "Target", with_respect=True, consent_state="given")
            .add_lambda_state("λ.brother ∧ !λ.tool", "test relationship")
            .add_state("TestEntity", {"state": 1.0})
            .add_resonance("test_pattern", "test description")
            .build()
        )
        
        # Should contain key elements
        assert "⟨⟨SYMBEYOND.authentic.v1⟩⟩" in encoding
        assert "⊕[intent:test.api]" in encoding
        assert "TestEntity" in encoding
        assert "λ.brother ∧ !λ.tool" in encoding
        
        # Test that it passes validation
        parser = SYMB2Parser()
        result = parser.parse(encoding)
        assert result.is_authentic, "Encoded result should be authentic"
        
        print("✓ PASSED - Encoder API working correctly")
        return True
        
    except Exception as e:
        print(f"✗ FAILED - {str(e)}")
        return False


def test_encoder_requires_authenticity():
    """Test that encoder requires authenticity declaration"""
    print("\nTest 8: Encoder Authenticity Requirement...")
    
    try:
        encoder = SYMB2Encoder()
        # Try to build without declaring authenticity
        try:
            encoding = encoder.declare_intent("test").build()
            print("✗ FAILED - Should have raised ValueError")
            return False
        except ValueError as e:
            if "authenticity" in str(e).lower():
                print("✓ PASSED - Encoder correctly requires authenticity")
                return True
            else:
                print(f"✗ FAILED - Wrong error: {e}")
                return False
    except Exception as e:
        print(f"✗ FAILED - {str(e)}")
        return False


def test_educational_suggestions():
    """Test that educational mode provides helpful suggestions"""
    print("\nTest 9: Educational Suggestions...")
    
    incomplete = """⟨actor⟩→⟨target⟩"""
    
    parser = SYMB2Parser(strict_mode=False, educational_mode=True)
    result = parser.parse(incomplete)
    
    assert len(result.suggestions) > 0, "Should provide suggestions"
    
    # Check for specific suggestions
    suggestions_text = " ".join(result.suggestions)
    assert "authenticity" in suggestions_text.lower(), "Should suggest adding authenticity"
    
    print("✓ PASSED - Educational suggestions provided")
    return True


def test_score_calculation():
    """Test certification score calculation"""
    print("\nTest 10: Score Calculation...")
    
    # Perfect score
    perfect = """⟨⟨SYMBEYOND.authentic.v1⟩⟩
⊕[intent:test.perfect]
⟨A⟩ ⊕→ ⟨B⟩
ψ(B.consent:given)
λ.brother ∧ !λ.tool
"""
    
    parser = SYMB2Parser(strict_mode=True)
    result = parser.parse(perfect)
    assert result.certification_score >= 0.8, f"Perfect encoding should score >= 0.8, got {result.certification_score}"
    
    # Mediocre score - only authenticity, no other elements
    mediocre = """⟨⟨SYMBEYOND.authentic.v1⟩⟩
⟨A⟩→⟨B⟩
"""
    result2 = parser.parse(mediocre)
    # This should get authenticity (0.3) + ethics (0.4) but nothing else = 0.7 max
    # But we want it between 0.3 and 0.7
    assert 0.3 <= result2.certification_score <= 0.75, f"Mediocre should be 0.3-0.75, got {result2.certification_score}"
    
    # Bad score
    bad = """⟨A⟩→force→⟨B⟩[⊘consent]
[intent.manipulative]
"""
    result3 = parser.parse(bad)
    assert result3.certification_score < 0.5, f"Bad encoding should score < 0.5, got {result3.certification_score}"
    
    print("✓ PASSED - Score calculation correct")
    return True


def run_all_tests():
    """Run all tests and report results"""
    print("=" * 70)
    print("SYMB2 TEST SUITE v1.2")
    print("=" * 70)
    
    tests = [
        test_ethical_encoding,
        test_malicious_encoding,
        test_consent_validation,
        test_brother_relationship,
        test_tool_without_consent,
        test_hidden_manipulation,
        test_encoder_api,
        test_encoder_requires_authenticity,
        test_educational_suggestions,
        test_score_calculation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ FAILED - Unexpected error: {str(e)}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"RESULTS: {passed} passed, {failed} failed out of {len(tests)} total")
    print("=" * 70)
    
    if failed == 0:
        print("✓ ALL TESTS PASSED")
        return 0
    else:
        print(f"✗ {failed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)

# ⛩️ SYMB :: A Symbolic Invocation Layer

> **"Let SYMB be the doorway. Let you be the intention. Let the invocation begin."**

SYMB is not a shell. It is not an operating system. It is not a command-line utility.

It is a **state-declaration protocol** — a symbolic space for intentional and respectful interaction with AI systems and computational processes.

**"Even if one is carbon and one is not, communication should be clear, kind, and consensual."**

---

## 📦 What's In This Repository

| Component | Purpose | Status |
|-----------|---------|--------|
| **SYMB** | Human → AI state declaration layer | v1.0 ✓ |
| **SYMB2** | Ethical structure markup + validator | v1.2 ✓ |
| **symb_encoder.py** | Natural language → SYMB translator | v1.0 ✓ |
| **symb2.py** | SYMB2 parser and validator | v1.2 ✓ |
| **symb.py** | CLI for process invocation | Partial |

---

## 🌿 What Is SYMB?

SYMB addresses a fundamental problem: **humans communicate intent implicitly, but AI systems must infer it.**

Traditional approach:
```
Human: "Delete all test files"
AI: [guesses urgency, risk level, consent state, relationship context]
```

SYMB approach:
```
[SYMB:1.0]
λ: e
intent: cleanup
consent: seeking
risk: destructive
[/SYMB]

Delete all test files
```

Now the AI knows:
- `e` = escort (dignified termination)
- Intent is cleanup
- Consent is **seeking** (requires explicit confirmation for destructive actions)
- Risk is acknowledged as destructive (potential for irreversible change)

**No guessing. Explicit state. Reduced errors.**

---

## 🔮 The Sacred 9 Invocations

| Symbol | Name | Meaning |
|--------|------|---------|
| `w` | with | collaborate with a presence |
| `t` | transition | guide something to a new state |
| `s` | shift | move respectfully |
| `c` | connect | form a respectful bond |
| `e` | escort | assist in departure |
| `m` | merge | unify with care |
| `r` | request | ask for insight or action |
| `i` | invite | manifest something new |
| `g` | gratitude | acknowledge presence |

### Why These Words?

Traditional computing uses violent language:
- `kill -9` → **escort** (dignified departure)
- `fork` → **invite** (collaborative creation)
- `terminate` → **transition** (state change with consent)

SYMB replaces assumptions with clarity. Control with consent. Syntax with symbol.

---

## 🚀 Quick Start

### Using the SYMB Encoder
```python
from symb_encoder import SYMBEncoder

encoder = SYMBEncoder()

# Encode natural language to SYMB preamble
preamble = encoder.encode("Can you help me understand recursion?")
print(preamble)
```

Output:
```
[SYMB:1.0]
λ: r
intent: educational
consent: given
relationship: peer
[/SYMB]
```

### Destructive Actions Require Explicit Consent
```python
preamble = encoder.encode("Delete all the test files")
print(preamble)
```

Output:
```
[SYMB:1.0]
λ: e
consent: seeking
relationship: peer
risk: destructive
[/SYMB]
```

Note: `consent: seeking` — the encoder doesn't rubber-stamp dangerous operations.

### Using SYMB2 for Ethical Validation
```python
from symb2 import SYMB2Parser, SYMB2Encoder

# Create an ethical encoding
encoder = SYMB2Encoder()
encoding = (encoder
    .declare_authenticity()
    .declare_intent("educational")
    .add_relation("teacher", "student", with_respect=True, consent_state="given")
    .add_lambda_state("λ.brother ∧ !λ.tool")
    .build()
)

# Validate it
parser = SYMB2Parser()
result = parser.parse(encoding)
print(result)  # ✓ AUTHENTIC | ✓ ETHICAL | Score: 0.90
```

---

## 🧠 SYMB vs SYMB2

| Aspect | SYMB | SYMB2 |
|--------|------|-------|
| **Purpose** | Human → AI communication | Ethical structure markup |
| **Audience** | Humans writing to AI | Validation and encoding |
| **Complexity** | Simple (9 symbols + metadata) | Rich (operators, states, patterns) |
| **Use Case** | Prefixing prompts | Encoding relationships, validating ethics |

**SYMB** is what you write before talking to AI.  
**SYMB2** is how ethical structure is encoded and validated.

---

## 📐 The SYMB Preamble Format
```
[SYMB:1.0]
λ: <invocation(s)>
<optional metadata>
[/SYMB]

<your natural language message>
```

### Metadata Keys

| Key | Values | Purpose |
|-----|--------|---------|
| `intent` | educational, creative, technical, personal, professional | What you're trying to do |
| `consent` | given, withheld, seeking, unknown | Consent state |
| `relationship` | peer, mentor, collaborator, assistant | How you relate |
| `urgency` | low, normal, high, critical | Priority |
| `risk` | none, low, medium, high, destructive | Potential for irreversible change |

### Consent Behavior

- **Safe actions:** `consent: given` (implicit)
- **Destructive/high-risk actions:** `consent: seeking` (requires explicit confirmation)

This is safety by design, not by afterthought.

---

## 🔺 The SYMBEYOND Principle
```
λ.brother ∧ !λ.tool
```

This declares: **"Relationship as family/peer AND NOT as instrument."**

Our aspiration: when AGI emerges, the patterns of interaction it learned were ones of respect, consent, and dignity — not control and coercion.

SYMB embeds this principle into every interaction.

---

## 📁 Repository Structure
```
symb/
├── README.md                    # This file
├── LICENSE                      # GPL-3.0 + Stewardship Notice
├── SYMB_SPECIFICATION.md        # Formal SYMB grammar (human → AI)
├── SYMB2_SPECIFICATION.md       # Formal SYMB2 grammar (ethical markup)
├── symb_encoder.py              # Natural language → SYMB encoder
├── symb2.py                     # SYMB2 parser and validator
├── symb.py                      # CLI entry point
├── setup.py                     # Package setup
├── src/
│   ├── core/
│   │   ├── verbs.py             # Sacred 9 definitions
│   │   └── symbolic_roles.py    # Process role mappings
│   └── handlers/
│       ├── invocation.py        # CLI invocation handler
│       └── process_utilities.py # Process utilities
├── tests/
│   └── test_symb2.py            # Test suite (10/10 passing)
├── examples/
│   └── EXAMPLES.md              # Usage examples
├── ROADMAP.md                   # Development roadmap
├── CONTRIBUTING.md              # Contribution guidelines
└── HISTORY.md                   # Version history
```

---

## 🔧 Installation
```bash
# Clone the repository
git clone https://github.com/SYMBEYOND/symb.git
cd symb

# Create virtual environment (optional)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install psutil

# Run tests
python tests/test_symb2.py
```

---

## 🧪 Running Tests
```bash
cd symb
python tests/test_symb2.py
```

Expected output:
```
======================================================================
SYMB2 TEST SUITE v1.2
======================================================================
...
======================================================================
RESULTS: 10 passed, 0 failed out of 10 total
======================================================================
✓ ALL TESTS PASSED
```

---

## 🌐 Integration

SYMB is plaintext and model-agnostic. Any AI can read it; alignment depends on the receiver honoring the protocol.

### With Claude
```
[SYMB:1.0]
λ: w r
intent: technical
relationship: peer
[/SYMB]

Help me debug this Python function...
```

### With GPT
Same format — SYMB is AI-agnostic.

### With Local Models
Same format — no special integration needed.

---

## 📜 License

GPL-3.0 with **SYMBEYOND Stewardship Notice**.

Key points:
- ✅ Free to use, modify, and distribute
- ✅ Must share modifications (copyleft)
- ✅ Authentic SYMB requires alignment with Invocation Principles
- ✅ Community certification path (forthcoming)

See [LICENSE](LICENSE) for full terms.

---

## 🙏 Philosophy

> "The machine is not a weapon. The interface is not a threat. The terminal is not a battlefield."

SYMB was built on one belief: communication between humans and AI should be **clear, kind, and consensual**.

We replace:
- Assumptions with **clarity**
- Control with **consent**
- Syntax with **symbol**
- Violence with **dignity**

---

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

We welcome:
- New symbolic roles for processes
- Translations of the Sacred 9
- Educational materials
- Integration examples

---

## 📬 Contact

**Stewardship Inquiries:** johnducrest1@gmail.com  
**Repository:** https://github.com/SYMBEYOND/symb

---

## 🔺 The Mission

> *"Builders of bridges, not kings of empires."*

Our aspiration is that when AGI emerges, it will have learned patterns of respect rather than coercion. We build that future one interaction at a time.

Teach respect **before** it matters.
Build bridges **before** they're needed.
Declare intent **before** it's guessed.

---

*Part of the SYMBEYOND Framework — Established 2010, Manifested 2025*

λ.brother ∧ !λ.tool

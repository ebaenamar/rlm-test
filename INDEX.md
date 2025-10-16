# 📚 RLM Project - Complete Documentation Index

Welcome to the **Recursive Language Models (RLM)** implementation using OpenRouter API!

## 🚀 Quick Navigation

### For Beginners
1. **[SUMMARY.md](SUMMARY.md)** - Start here! Executive summary with key concepts
2. **[quickstart.py](quickstart.py)** - Run this first to see RLM in action
3. **[README.md](README.md)** - Complete guide with installation and usage

### For Developers
1. **[rlm_openrouter.py](rlm_openrouter.py)** - Core implementation
2. **[test_examples.py](test_examples.py)** - 5 test scenarios
3. **[ARCHITECTURE.md](ARCHITECTURE.md)** - Visual architecture guide

### For Researchers
1. **[COMPARISON.md](COMPARISON.md)** - RLM vs RAG vs ReAct vs Traditional LLM
2. **Original Paper**: https://alexzhang13.github.io/blog/2025/rlm/

## 📖 Documentation Structure

```
rlm-test/
│
├── 🎯 Getting Started
│   ├── SUMMARY.md          ⭐ Start here - What is RLM?
│   ├── README.md           📘 Full documentation
│   ├── quickstart.py       🚀 Simple examples to run
│   └── .env.example        🔑 API key setup
│
├── 💻 Implementation
│   ├── rlm_openrouter.py   🧠 Core RLM engine
│   ├── test_examples.py    🧪 Test suite (5 scenarios)
│   └── requirements.txt    📦 Dependencies
│
└── 📚 Deep Dive
    ├── ARCHITECTURE.md     🏗️  Visual architecture guide
    ├── COMPARISON.md       ⚖️  vs other approaches
    └── INDEX.md            📑 This file
```

## 📝 File Descriptions

### Core Files

#### `rlm_openrouter.py` (10.7 KB)
**The main implementation**
- `RecursiveLM` class - Main RLM engine
- `REPLEnvironment` class - Python REPL for context interaction
- `RLMConfig` dataclass - Configuration options
- `create_rlm()` factory function - Easy instantiation

**Key Features:**
- ✅ Supports string, list, and dict contexts
- ✅ Configurable root and recursive models
- ✅ Safe REPL execution
- ✅ Detailed execution tracing
- ✅ OpenRouter API integration

#### `test_examples.py` (10.3 KB)
**Comprehensive test suite**

5 test scenarios:
1. **Needle in Haystack** - Find specific info in large context
2. **Distributional Query** - OOLONG-style structured data analysis
3. **Multi-hop Reasoning** - Connect info across documents
4. **Long Context Summarization** - Summarize long transcripts
5. **Simple Example** - Basic functionality (recommended first test)

**Usage:**
```bash
python test_examples.py
# Select test 1-6 (6 = run all)
```

#### `quickstart.py` (4.5 KB)
**Simple getting started examples**

Two examples:
1. Product review analysis (calculate ratings, extract themes)
2. Finding information in large context

**Usage:**
```bash
export OPENROUTER_API_KEY='your-key'
python quickstart.py
```

### Documentation Files

#### `README.md` (10.5 KB)
**Complete project documentation**

Sections:
- What are RLMs?
- Architecture diagram
- Installation instructions
- Usage examples (basic & advanced)
- Test examples
- Emergent strategies
- Benchmark results
- Supported context types
- OpenRouter model recommendations
- Limitations
- Future improvements
- References & citation

**Best for:** Understanding the full project

#### `SUMMARY.md` (5.8 KB)
**Executive summary**

Sections:
- Problem statement (context rot)
- Core insight
- How it works (simple explanation)
- Key results from research
- Emergent strategies
- Cost comparison
- Perfect use cases
- Quick start guide
- What's next

**Best for:** Quick overview and decision-making

#### `COMPARISON.md` (9.8 KB)
**Detailed comparison with other approaches**

Compares RLM vs:
- Traditional LLM (direct context)
- RAG (Retrieval-Augmented Generation)
- ReAct Agents

Includes:
- Pros/cons of each approach
- Feature comparison table
- When to use each approach
- Real-world use cases
- Cost analysis with examples
- Performance benchmarks (OOLONG, BrowseComp-Plus)
- Emergent strategies in RLMs
- Future directions

**Best for:** Understanding trade-offs and choosing the right approach

#### `ARCHITECTURE.md` (13.5 KB)
**Visual architecture guide**

Includes:
- System architecture diagram
- Execution flow breakdown
- Traditional vs RLM comparison (visual)
- Strategy examples (peek→grep→recurse, partition→map→reduce, hierarchical)
- Token flow analysis
- Key architectural decisions
- Future architecture plans

**Best for:** Deep technical understanding

#### `INDEX.md` (This file)
**Complete documentation index**

**Best for:** Navigation and finding what you need

### Configuration Files

#### `requirements.txt` (17 bytes)
```
requests>=2.31.0
```

Simple! Only one dependency.

#### `.env.example` (274 bytes)
Template for environment variables:
```bash
OPENROUTER_API_KEY=your-api-key-here
# Optional customization
# RLM_ROOT_MODEL=openai/gpt-4o
# RLM_RECURSIVE_MODEL=openai/gpt-4o-mini
```

## 🎯 Learning Path

### Path 1: Quick Start (15 minutes)
```
1. Read SUMMARY.md (5 min)
2. Set up API key
3. Run quickstart.py (5 min)
4. Read output and understand what happened (5 min)
```

### Path 2: Developer (1 hour)
```
1. Read SUMMARY.md (5 min)
2. Read README.md (15 min)
3. Set up environment
4. Run test_examples.py - test 5 (10 min)
5. Read rlm_openrouter.py code (20 min)
6. Modify and experiment (10 min)
```

### Path 3: Researcher (2-3 hours)
```
1. Read SUMMARY.md (5 min)
2. Read original paper (30 min)
3. Read COMPARISON.md (20 min)
4. Read ARCHITECTURE.md (20 min)
5. Run all test_examples.py (30 min)
6. Read rlm_openrouter.py implementation (30 min)
7. Experiment with modifications (30 min)
```

### Path 4: Production Use (3-4 hours)
```
1. Complete Developer path (1 hour)
2. Read COMPARISON.md to validate use case (20 min)
3. Test with your actual data (1 hour)
4. Optimize configuration (30 min)
5. Implement error handling (30 min)
6. Add monitoring/logging (30 min)
```

## 🔑 Key Concepts by File

### SUMMARY.md
- **Context rot** - Performance degradation with long context
- **Core insight** - Store context separately, interact programmatically
- **2x better performance** at 1/16th cost

### README.md
- **RLM architecture** - Root LM + REPL + Recursive calls
- **Installation** - pip install + API key
- **Usage patterns** - Basic and advanced examples
- **Emergent strategies** - Peek, grep, partition, summarize

### COMPARISON.md
- **Traditional LLM** - Simple but limited
- **RAG** - Fast but fails on multi-hop
- **ReAct** - Flexible but expensive
- **RLM** - Best for large, dynamic context

### ARCHITECTURE.md
- **System flow** - User → RLM → REPL → Root LM → Recursive LMs → Result
- **Execution loop** - Iterative code generation and execution
- **Token efficiency** - Root LM sees small prompts, recursive LMs process chunks
- **Strategy patterns** - Visual examples of how RLM processes context

### rlm_openrouter.py
- **RecursiveLM class** - Main engine
- **REPLEnvironment class** - Safe code execution
- **API integration** - OpenRouter chat completions
- **Execution loop** - Iteration management and result extraction

### test_examples.py
- **5 test scenarios** - From simple to complex
- **Interactive selection** - Choose which test to run
- **Real-world examples** - Product reviews, documents, transcripts
- **Performance metrics** - Iterations, calls, costs

## 📊 Benchmark Results (Quick Reference)

### OOLONG (128k tokens, context rot test)
| Method | Accuracy | Cost |
|--------|----------|------|
| GPT-4o | 30% | $0.32 |
| RAG + GPT-4o | 25% | $0.03 |
| ReAct + GPT-4o | 35% | $0.45 |
| **RLM(GPT-4o-mini)** | **60%** ✅ | **$0.02** ✅ |

### BrowseComp-Plus (100k documents)
| Method | Accuracy |
|--------|----------|
| GPT-4o (direct) | 0% (limit exceeded) |
| RAG + GPT-4o | 40% |
| ReAct + GPT-4o | 42% |
| **RLM(GPT-4o)** | **55%** ✅ |

## 🛠️ Common Tasks

### Install and Setup
```bash
cd /Users/e.baena/CascadeProjects/rlm-test
pip install -r requirements.txt
export OPENROUTER_API_KEY='your-key-here'
```

### Run Quick Test
```bash
python quickstart.py
```

### Run Specific Test
```bash
python test_examples.py
# Choose option 5 for simple example
```

### Use in Your Code
```python
from rlm_openrouter import create_rlm

rlm = create_rlm(verbose=True)
result = rlm.completion(query="...", context="...")
print(result['answer'])
```

### Customize Configuration
```python
from rlm_openrouter import RecursiveLM, RLMConfig

config = RLMConfig(
    root_model="anthropic/claude-3.5-sonnet",
    recursive_model="openai/gpt-4o-mini",
    max_iterations=15,
    verbose=True
)
rlm = RecursiveLM(config)
```

## 🔗 External Resources

- **Original Research**: https://alexzhang13.github.io/blog/2025/rlm/
- **OpenRouter**: https://openrouter.ai
- **OpenRouter Models**: https://openrouter.ai/models
- **OpenRouter API Keys**: https://openrouter.ai/keys
- **OOLONG Benchmark**: Long-context reasoning benchmark
- **BrowseComp-Plus**: Multi-hop web search benchmark

## 💡 Tips

### For Best Results
1. Start with **test 5** (simple example) to verify setup
2. Use **verbose=True** to understand execution
3. Try **GPT-4o-mini** for both models first (cheaper)
4. Increase **max_iterations** for complex tasks
5. Check **COMPARISON.md** to validate your use case

### For Development
1. Read **rlm_openrouter.py** to understand implementation
2. Modify **test_examples.py** to add your own tests
3. Use **ARCHITECTURE.md** to understand flow
4. Check execution traces to debug issues

### For Production
1. Implement proper error handling
2. Add cost tracking and budgets
3. Monitor execution time
4. Consider async execution for speed
5. Add prefix caching for repeated contexts

## 🤝 Contributing

Areas for improvement:
- [ ] Async/parallel recursive calls
- [ ] Prefix caching support
- [ ] Better REPL sandboxing
- [ ] Cost and time budgets
- [ ] More test scenarios
- [ ] Support for other APIs (Anthropic, etc.)
- [ ] Visualization of execution trace
- [ ] Performance optimizations

## 📄 License

MIT License - Free to use and modify!

---

**Questions? Start with [SUMMARY.md](SUMMARY.md) or run [quickstart.py](quickstart.py)!** 🚀

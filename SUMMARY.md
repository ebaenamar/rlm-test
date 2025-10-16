# Recursive Language Models (RLM) - Executive Summary

## 🎯 What Problem Does This Solve?

**Context Rot**: When you give an LLM a very long context (100k+ tokens), its performance degrades significantly. This happens even with models that claim 200k token context windows.

**Example**: 
- GPT-4o with 128k token context: **30% accuracy**
- RLM using GPT-4o-mini: **60% accuracy** at **lower cost**

## 💡 The Core Insight

Instead of putting all context in the prompt:
```
❌ LLM(huge_context + query) → answer
```

Store context as a variable and let the LM interact with it programmatically:
```
✅ RLM(query) → explores context via code → recursive calls → answer
```

## 🏗️ How It Works (Simple Explanation)

1. **Context stored separately** - Not in the LLM's prompt, but in a Python REPL environment
2. **Root LM gets only the query** - Plus info that context exists as a variable
3. **Root LM writes Python code** - To peek, filter, chunk, or analyze context
4. **Can spawn recursive LM calls** - To process chunks in parallel
5. **Returns final answer** - After iterative exploration

## 📊 Key Results from Research Paper

### OOLONG Benchmark (128k tokens, context rot test)
```
Traditional Approaches:
├─ GPT-4o (direct):           30% ❌
├─ GPT-4o-mini (direct):      20% ❌
├─ RAG + GPT-4o:              25% ❌
└─ ReAct + GPT-4o:            35% ❌

Recursive Language Models:
└─ RLM(GPT-4o-mini):          60% ✅ (2x better!)
```

### BrowseComp-Plus (100k documents, multi-hop reasoning)
```
Traditional Approaches:
├─ GPT-4o (direct):           0% (context limit exceeded)
├─ RAG + GPT-4o:             40%
└─ ReAct + GPT-4o:           42%

Recursive Language Models:
└─ RLM(GPT-4o):              55% ✅
```

### Extreme Scale Test
- **10M+ tokens**: RLM shows **no performance degradation**
- Traditional LLMs: Can't even process this much context

## 🎨 Emergent Strategies

RLMs automatically learn to:

1. **Peek** - Look at context structure first
   ```python
   preview = context[:1000]
   ```

2. **Grep** - Filter for relevant information
   ```python
   relevant = [x for x in context if "keyword" in x]
   ```

3. **Partition & Map** - Chunk and process in parallel
   ```python
   chunks = [context[i:i+5000] for i in range(0, len(context), 5000)]
   results = [recursive_lm(query, chunk) for chunk in chunks]
   ```

4. **Hierarchical Summarization** - Summarize sections, then combine
   ```python
   summaries = [recursive_lm("Summarize", section) for section in sections]
   ```

## 💰 Cost Comparison (128k token document)

| Method | Cost/Query | Accuracy | Winner |
|--------|------------|----------|--------|
| GPT-4o (direct) | $0.32 | 30% | ❌ |
| RAG + GPT-4o | $0.03 | 25% | ❌ |
| **RLM(GPT-4o-mini)** | **$0.02** | **60%** | **✅** |

**RLM wins**: 2x better accuracy at 1/16th the cost!

## 🚀 Perfect Use Cases

### ✅ Excellent for:
- **Long conversation analysis** (Claude Code sessions, support tickets)
- **Deep research** (100+ papers, multi-document analysis)
- **Code repository understanding** (large codebases)
- **Legal document review** (contracts, compliance)
- **Financial analysis** (years of transactions)

### ⚠️ Not ideal for:
- Simple Q&A (use regular LLM)
- Real-time apps (use RAG - faster)
- Static knowledge base (use RAG - cheaper)
- Short contexts (<32k tokens)

## 🔧 Implementation with OpenRouter

```python
from rlm_openrouter import create_rlm

# Create RLM
rlm = create_rlm(
    root_model="openai/gpt-4o",
    recursive_model="openai/gpt-4o-mini"
)

# Query with huge context
result = rlm.completion(
    query="What are the main themes?",
    context=huge_document  # Can be 10M+ tokens!
)

print(result['answer'])
```

## 📈 Why This Matters

### Current State (2025)
- ✅ CoT reasoning (GPT-o1, Claude 3.5)
- ✅ ReAct agents (tool use)
- 🚀 **RLMs (next frontier)**

### Future Impact
1. **No more context limits** - Process unbounded context
2. **Better performance** - No context rot
3. **Lower costs** - Use smaller models effectively
4. **Interpretable** - See exactly how LM processes context
5. **Trainable** - Can RL-train optimal strategies

## 🎯 Quick Start

```bash
# 1. Install
cd /Users/e.baena/CascadeProjects/rlm-test
pip install -r requirements.txt

# 2. Set API key
export OPENROUTER_API_KEY='your-key-here'

# 3. Run quick start
python quickstart.py

# 4. Try advanced examples
python test_examples.py
```

## 📚 Files in This Project

```
rlm-test/
├── rlm_openrouter.py      # Core RLM implementation
├── test_examples.py        # 5 test scenarios
├── quickstart.py           # Simple getting started
├── README.md               # Full documentation
├── COMPARISON.md           # vs RAG, ReAct, etc.
├── SUMMARY.md              # This file
└── requirements.txt        # Dependencies
```

## 🔮 What's Next?

### Immediate Improvements
- [ ] Async/parallel recursive calls (10x faster)
- [ ] Prefix caching (lower costs)
- [ ] Cost/time budgets
- [ ] Better REPL sandboxing

### Research Directions
- [ ] Fine-tune models for RLM strategies
- [ ] Deeper recursion (depth > 1)
- [ ] Multi-modal context (images, video)
- [ ] Formal verification
- [ ] Combine with RAG for hybrid approach

## 📖 Learn More

- **Original Blog**: https://alexzhang13.github.io/blog/2025/rlm/
- **OpenRouter**: https://openrouter.ai
- **This Implementation**: See README.md for full details

## 🎓 Key Takeaway

**RLMs solve the long-context problem** by treating context as data to be programmatically explored, not text to be stuffed into a prompt.

**Result**: Better performance, lower cost, no context limits.

---

**Built for the AI research community** 🚀

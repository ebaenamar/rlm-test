# Recursive Language Models (RLM) - OpenRouter Implementation

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenRouter](https://img.shields.io/badge/API-OpenRouter-green.svg)](https://openrouter.ai)

Implementation of **Recursive Language Models** based on the research from [alexzhang13.github.io/blog/2025/rlm/](https://alexzhang13.github.io/blog/2025/rlm/) using the OpenRouter API.

> **TL;DR**: RLMs solve the long-context problem by storing context as a variable and letting LMs interact with it programmatically. Result: 2x better accuracy at lower cost, scales to 10M+ tokens.

## 📚 What are Recursive Language Models?

RLMs are an inference strategy that enables language models to handle **unbounded context lengths** by:

1. **Storing context as a variable** in a Python REPL environment (not in the prompt)
2. **Recursively decomposing** queries into sub-problems
3. **Programmatically interacting** with context through code execution
4. **Spawning recursive LM calls** to process context chunks in parallel

### Key Advantages

- ✅ **No context rot** - Root LM never sees the entire context at once
- ✅ **Unbounded context** - Tested with 10M+ tokens
- ✅ **Cost efficient** - RLM(GPT-4o-mini) outperforms GPT-4o at lower cost
- ✅ **Interpretable** - Can trace exactly how the model processes context
- ✅ **Flexible strategies** - Models learn to peek, grep, partition, and summarize

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Query                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Root LM (depth=0)                        │
│                  Only sees the query                        │
│              Can execute Python code in REPL                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   REPL Environment                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  context = [huge context stored as variable]        │  │
│  │                                                      │  │
│  │  # Root LM can execute code:                        │  │
│  │  peek = context[:1000]                              │  │
│  │  filtered = [x for x in context if "keyword" in x]  │  │
│  │  result = recursive_lm(query, filtered)             │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Recursive LM Calls (depth=1)                   │
│         Process context chunks in sub-queries               │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Installation

```bash
# Clone or create the project
cd /Users/e.baena/CascadeProjects/rlm-test

# Install dependencies
pip install -r requirements.txt

# Set your OpenRouter API key
export OPENROUTER_API_KEY='your-key-here'
```

## 💡 Usage

### Basic Example

```python
from rlm_openrouter import create_rlm

# Create RLM instance
rlm = create_rlm(
    root_model="openai/gpt-4o",
    recursive_model="openai/gpt-4o-mini",
    verbose=True
)

# Large context (can be string, list, or dict)
context = """
[Your huge context here - can be 100k+ tokens]
"""

# Query the RLM
result = rlm.completion(
    query="What are the main themes in this document?",
    context=context
)

print(f"Answer: {result['answer']}")
print(f"Iterations: {result['iterations']}")
print(f"Total LM calls: {result['total_calls']}")
```

### Advanced Configuration

```python
from rlm_openrouter import RecursiveLM, RLMConfig

config = RLMConfig(
    root_model="anthropic/claude-3.5-sonnet",
    recursive_model="openai/gpt-4o-mini",
    max_iterations=15,
    max_recursive_depth=2,  # Allow deeper recursion
    verbose=True
)

rlm = RecursiveLM(config)
```

## 🧪 Test Examples

Run the included test suite:

```bash
python test_examples.py
```

### Available Tests

1. **Needle in Haystack** - Find specific information in large context
2. **Distributional Query** - OOLONG-style structured data analysis
3. **Multi-hop Reasoning** - Connect information across multiple documents
4. **Long Context Summarization** - Summarize very long transcripts
5. **Simple Example** - Basic functionality test (recommended first)

### Example Test Output

```
TEST 5: Simple Example - Context Analysis
================================================================================

[LM Call - Depth 0] Model: openai/gpt-4o-mini
[REPL] Executed:
# Peek at context
peek = context[:500]
result = peek

[LM Response - Depth 0]: I'll analyze the reviews to calculate the average...

[RESULT] Answer: Average rating: 3.6/5. Main complaints: overpriced, poor screen quality, runs hot, poor build quality, battery drains quickly.
[RESULT] Iterations: 3
[RESULT] Total LM calls: 4
```

## 🎯 Emergent Strategies

The RLM learns to use various strategies automatically:

### 1. **Peeking**
```python
# Root LM peeks at context structure
peek = context[:1000]
print(peek)
```

### 2. **Grepping/Filtering**
```python
# Root LM filters for relevant information
import re
filtered = [line for line in context.split('\n') if re.search(r'user.*12345', line)]
```

### 3. **Partition & Map**
```python
# Root LM chunks context and processes in parallel
chunks = [context[i:i+5000] for i in range(0, len(context), 5000)]
results = [recursive_lm(f"Extract key info from: {chunk}", chunk) for chunk in chunks]
```

### 4. **Summarization**
```python
# Root LM summarizes sections hierarchically
section_summaries = []
for section in sections:
    summary = recursive_lm(f"Summarize: {section[:100]}...", section)
    section_summaries.append(summary)
```

## 📊 Benchmark Results (from paper)

### OOLONG Benchmark (128k tokens)
- **GPT-4o**: ~30% accuracy
- **RLM(GPT-4o-mini)**: **>60% accuracy** (2x better, same cost!)

### BrowseComp-Plus (100k documents)
- **GPT-4o + BM25**: ~40% accuracy
- **RLM(GPT-4o)**: **~55% accuracy**
- **Scales to 10M+ tokens** without degradation

## 🔧 How It Works

1. **User provides query + context** → `rlm.completion(query, context)`

2. **Root LM receives**:
   - The query
   - System prompt explaining REPL environment
   - Info about context (type, size, preview)

3. **Root LM decides strategy**:
   - Peek at context structure
   - Grep/filter relevant sections
   - Partition into chunks
   - Spawn recursive LM calls

4. **Execution loop** (max 10 iterations):
   - Root LM generates Python code
   - Code executes in REPL environment
   - Results fed back to Root LM
   - Repeat until `FINAL(answer)` or `FINAL_VAR(variable)`

5. **Return final answer** with full trace

## 🎨 Supported Context Types

```python
# String context
context = "Long text document..."

# List context (documents)
context = [
    {"title": "Doc 1", "content": "..."},
    {"title": "Doc 2", "content": "..."},
]

# Dict context (structured data)
context = {
    "users": [...],
    "transactions": [...],
    "metadata": {...}
}
```

## 🔑 OpenRouter Models

Recommended model combinations:

| Use Case | Root Model | Recursive Model | Cost/Performance |
|----------|------------|-----------------|------------------|
| **Best Performance** | `openai/gpt-4o` | `openai/gpt-4o-mini` | High/High |
| **Balanced** | `anthropic/claude-3.5-sonnet` | `openai/gpt-4o-mini` | Medium/High |
| **Cost Efficient** | `openai/gpt-4o-mini` | `openai/gpt-4o-mini` | Low/Medium |
| **Experimental** | `google/gemini-2.0-flash-exp` | `openai/gpt-4o-mini` | Low/High |

See [OpenRouter Models](https://openrouter.ai/models) for full list.

## ⚠️ Limitations

1. **Speed**: Not optimized - each recursive call is blocking
2. **No prefix caching**: Same context chunks may be processed multiple times
3. **Cost control**: No hard limits on total API cost per query
4. **Recursion depth**: Currently limited to depth=1 (can be increased)
5. **Code safety**: Limited sandboxing of REPL execution

## 🔮 Future Improvements

- [ ] Async/parallel recursive LM calls
- [ ] Prefix caching for repeated context chunks
- [ ] Cost and time budgets
- [ ] Deeper recursion (depth > 1)
- [ ] Fine-tuned models specifically for RLM strategies
- [ ] Better REPL sandboxing
- [ ] Visualization of RLM execution trace

## 📖 References

- **Original Blog Post**: [Recursive Language Models](https://alexzhang13.github.io/blog/2025/rlm/)
- **OpenRouter API**: [openrouter.ai](https://openrouter.ai)
- **OOLONG Benchmark**: Long-context reasoning benchmark
- **BrowseComp-Plus**: Multi-hop web search benchmark

## 📝 Citation

If you use this implementation, please cite the original work:

```bibtex
@article{zhang2025rlm,
  title={Recursive Language Models},
  author={Zhang, Alex L. and others},
  year={2025},
  url={https://alexzhang13.github.io/blog/2025/rlm/}
}
```

## 🤝 Contributing

This is an experimental implementation. Contributions welcome:

- Better REPL sandboxing
- Async execution
- Additional test cases
- Performance optimizations
- Support for more model providers

## 📄 License

MIT License - Feel free to use and modify!

---

**Built with ❤️ for the AI research community**

# 🚀 Getting Started with RLM

Your RLM implementation is **ready to use** with your OpenRouter API key!

## ✅ Setup

Set your OpenRouter API key:

```bash
export OPENROUTER_API_KEY='your-api-key-here'
```

Get your key from: https://openrouter.ai/keys

## 🎯 Quick Test

Run the demo to see RLM in action:

```bash
cd /Users/e.baena/CascadeProjects/rlm-test
python demo.py
```

This runs 4 demos:
1. **Product Review Analysis** - Calculate ratings and extract complaints
2. **Needle in Haystack** - Find specific info in large text
3. **Multi-Document Reasoning** - Connect information across documents
4. **Structured Data Extraction** - Parse and count log entries

## 📝 Test Results

✅ **Demo 1**: Average rating calculated correctly (3.67/5)
✅ **Demo 2**: Found secret code in large context
✅ **Demo 3**: Connected info across 7 documents
✅ **Demo 4**: Extracted and counted log entries

## 💻 Use in Your Code

```python
from rlm_openrouter import create_rlm

# Create RLM (uses OPENROUTER_API_KEY env var)
rlm = create_rlm(
    root_model="openai/gpt-4o-mini",
    recursive_model="openai/gpt-4o-mini",
    verbose=False
)

# Use it
result = rlm.completion(
    query="Your question here",
    context="Your large context here (can be 100k+ tokens!)"
)

print(result['answer'])
```

## 🧪 Available Test Files

1. **`demo.py`** ⭐ - Best starting point (4 quick demos)
2. **`simple_test.py`** - Minimal example for debugging
3. **`quickstart.py`** - Two examples with explanations
4. **`test_examples.py`** - Full test suite (5 scenarios)

## 🎨 Try Different Models

```python
# Faster & cheaper (recommended for testing)
rlm = create_rlm(
    root_model="openai/gpt-4o-mini",
    recursive_model="openai/gpt-4o-mini",
    api_key="your-key"
)

# Better quality
rlm = create_rlm(
    root_model="openai/gpt-4o",
    recursive_model="openai/gpt-4o-mini",
    api_key="your-key"
)

# Claude models
rlm = create_rlm(
    root_model="anthropic/claude-3.5-sonnet",
    recursive_model="openai/gpt-4o-mini",
    api_key="your-key"
)
```

See all models at: https://openrouter.ai/models

## 🔍 Debug Mode

To see exactly how RLM processes your context:

```python
rlm = create_rlm(verbose=True)  # Shows all LM calls and REPL execution
```

## 📚 Learn More

- **SUMMARY.md** - What is RLM? (5 min read)
- **README.md** - Full documentation
- **ARCHITECTURE.md** - How it works internally
- **COMPARISON.md** - RLM vs RAG vs ReAct
- **Original Paper**: https://alexzhang13.github.io/blog/2025/rlm/

## 💡 Example Use Cases

### 1. Analyze Long Documents
```python
result = rlm.completion(
    query="Summarize the key findings from this research paper",
    context=long_research_paper  # 50k+ tokens
)
```

### 2. Multi-Document Search
```python
result = rlm.completion(
    query="Find all mentions of 'security vulnerabilities' across these documents",
    context=list_of_documents  # 100+ documents
)
```

### 3. Code Repository Analysis
```python
result = rlm.completion(
    query="Find all TODO comments and list them by priority",
    context=all_source_files  # Entire codebase
)
```

### 4. Data Extraction
```python
result = rlm.completion(
    query="Extract all email addresses and phone numbers",
    context=customer_records  # Large dataset
)
```

## ⚡ Performance Tips

1. **Start with gpt-4o-mini** for both models (fast & cheap)
2. **Use verbose=False** in production (faster)
3. **Increase max_iterations** for complex tasks
4. **Structure your queries clearly** - be specific about what you want

## 🎯 Next Steps

1. ✅ Run `python demo.py` to see it working
2. ✅ Try with your own data
3. ✅ Read ARCHITECTURE.md to understand how it works
4. ✅ Experiment with different models
5. ✅ Check out the original research paper

---

**You're all set! Start with `python demo.py` to see RLM in action.** 🚀

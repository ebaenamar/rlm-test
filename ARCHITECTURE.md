# RLM Architecture - Visual Guide

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER REQUEST                               │
│                                                                     │
│  Query: "What are the main themes in this 200k token document?"   │
│  Context: [huge_document] (200,000 tokens)                        │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    RLM.completion(query, context)                   │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      REPL ENVIRONMENT                               │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │  Variables:                                                   │ │
│  │  ├─ context = [200k token document stored in memory]         │ │
│  │  ├─ result = None                                            │ │
│  │  └─ [other variables created during execution]               │ │
│  │                                                               │ │
│  │  Available Functions:                                         │ │
│  │  ├─ recursive_lm(query, context_subset)                      │ │
│  │  ├─ Standard Python: len, str, list, dict, re, json         │ │
│  │  └─ [safe builtins only - no file I/O, network, etc.]       │ │
│  └───────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    ROOT LM (Depth = 0)                              │
│                    Model: GPT-4o                                    │
│                                                                     │
│  Receives:                                                          │
│  ├─ Query: "What are the main themes..."                          │
│  ├─ System prompt explaining REPL environment                     │
│  ├─ Context info: type=str, size=200k chars, preview=[first 200] │
│  └─ Max iterations: 10                                            │
│                                                                     │
│  Can do:                                                            │
│  ├─ Write Python code to analyze context                          │
│  ├─ Call recursive_lm() for sub-queries                           │
│  ├─ Store results in variables                                    │
│  └─ Return FINAL(answer) or FINAL_VAR(variable_name)              │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
                    ┌────────┴────────┐
                    │                 │
         ┌──────────▼─────────┐  ┌───▼──────────────┐
         │  ITERATION 1       │  │  ITERATION 2     │  ... up to 10
         │                    │  │                  │
         │  Root LM decides:  │  │  Root LM:        │
         │  "I'll peek at     │  │  "Now I'll chunk │
         │   the context"     │  │   and recurse"   │
         │                    │  │                  │
         │  Generates code:   │  │  Generates code: │
         │  ```python         │  │  ```python       │
         │  peek = context[:  │  │  chunks = [      │
         │    1000]           │  │    context[i:i+  │
         │  print(peek)       │  │    10000]        │
         │  ```               │  │    for i in      │
         │                    │  │    range(0,len(  │
         │  ↓ Execute in REPL │  │    context),     │
         │                    │  │    10000)]       │
         │  Result:           │  │  results = []    │
         │  "This document    │  │  for chunk in    │
         │   appears to be    │  │    chunks:       │
         │   about AI and     │  │    r = recursive │
         │   machine          │  │      _lm("themes"│
         │   learning..."     │  │      , chunk)    │
         │                    │  │    results.append│
         │  ↓ Feed back to LM │  │      (r)         │
         │                    │  │  ```             │
         └────────────────────┘  │                  │
                                 │  ↓ Execute       │
                                 │                  │
                                 │  Spawns 20       │
                                 │  recursive calls │
                                 │  ↓               │
                                 └───┬──────────────┘
                                     │
                    ┌────────────────┴────────────────┐
                    │                                 │
         ┌──────────▼─────────┐          ┌───────────▼────────┐
         │ RECURSIVE LM #1    │   ...    │ RECURSIVE LM #20   │
         │ (Depth = 1)        │          │ (Depth = 1)        │
         │                    │          │                    │
         │ Model: GPT-4o-mini │          │ Model: GPT-4o-mini │
         │                    │          │                    │
         │ Receives:          │          │ Receives:          │
         │ ├─ Query: "themes" │          │ ├─ Query: "themes" │
         │ └─ Context: chunk1 │          │ └─ Context: chunk20│
         │    (10k tokens)    │          │    (10k tokens)    │
         │                    │          │                    │
         │ Returns:           │          │ Returns:           │
         │ "AI ethics,        │          │ "Neural networks,  │
         │  automation"       │          │  deep learning"    │
         └────────────────────┘          └────────────────────┘
                    │                                 │
                    └────────────────┬────────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │  All results collected back    │
                    │  to REPL environment           │
                    │                                │
                    │  results = [                   │
                    │    "AI ethics, automation",    │
                    │    "Machine learning, ...",    │
                    │    ...                         │
                    │    "Neural networks, ..."      │
                    │  ]                             │
                    └────────────────┬───────────────┘
                                     │
                                     ▼
                    ┌────────────────────────────────┐
                    │  ITERATION 3                   │
                    │                                │
                    │  Root LM:                      │
                    │  "I'll combine the results"    │
                    │                                │
                    │  Generates code:               │
                    │  ```python                     │
                    │  all_themes = set()            │
                    │  for r in results:             │
                    │    themes = r.split(", ")      │
                    │    all_themes.update(themes)   │
                    │  final_answer = ", ".join(     │
                    │    sorted(all_themes))         │
                    │  ```                           │
                    │                                │
                    │  Then outputs:                 │
                    │  FINAL_VAR(final_answer)       │
                    └────────────────┬───────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         FINAL RESULT                                │
│                                                                     │
│  {                                                                  │
│    "answer": "AI ethics, automation, deep learning, machine        │
│               learning, neural networks, ...",                      │
│    "iterations": 3,                                                 │
│    "total_calls": 21,  # 1 root + 20 recursive                    │
│    "repl_history": [...],                                          │
│    "messages": [...]                                               │
│  }                                                                  │
└─────────────────────────────────────────────────────────────────────┘
```

## 🔄 Execution Flow

### Step-by-Step Breakdown

```
1. USER CALL
   rlm.completion(query, context)
   
2. INITIALIZE REPL
   context stored as variable (NOT in prompt)
   
3. ROOT LM ITERATION 1
   ├─ Receives: query + context metadata
   ├─ Decides: "I'll peek at the context"
   ├─ Generates: Python code to peek
   ├─ REPL executes code
   └─ Result fed back to Root LM
   
4. ROOT LM ITERATION 2
   ├─ Receives: previous result
   ├─ Decides: "I'll chunk and recurse"
   ├─ Generates: Code to partition + recursive calls
   ├─ REPL executes code
   ├─ Spawns 20 RECURSIVE LM calls (depth=1)
   │   ├─ Each processes 10k token chunk
   │   ├─ Each returns partial answer
   │   └─ All results collected
   └─ Results fed back to Root LM
   
5. ROOT LM ITERATION 3
   ├─ Receives: all recursive results
   ├─ Decides: "I'll combine these"
   ├─ Generates: Code to merge results
   ├─ REPL executes code
   └─ Outputs: FINAL_VAR(final_answer)
   
6. RETURN TO USER
   Complete result with answer + metadata
```

## 🎭 Comparison: Traditional vs RLM

### Traditional LLM Approach

```
┌──────────────────────────────────────────────────────────────┐
│                      SINGLE LLM CALL                         │
│                                                              │
│  Input Prompt (200k tokens):                                │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ [Entire 200k token document pasted here]              │ │
│  │                                                        │ │
│  │ ... 200,000 tokens of context ...                     │ │
│  │                                                        │ │
│  │ Query: What are the main themes?                      │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ↓ Process all at once                                      │
│                                                              │
│  Output:                                                     │
│  "The main themes are..." (often degraded quality)          │
│                                                              │
│  Problems:                                                   │
│  ❌ Context rot - performance degrades                      │
│  ❌ Expensive - pay for all 200k tokens                     │
│  ❌ Limited - can't exceed context window                   │
│  ❌ Black box - can't see how it processes                  │
└──────────────────────────────────────────────────────────────┘
```

### RLM Approach

```
┌──────────────────────────────────────────────────────────────┐
│                    MULTIPLE SMART CALLS                      │
│                                                              │
│  Root LM sees (2k tokens):                                  │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Query: What are the main themes?                       │ │
│  │                                                        │ │
│  │ Context available as variable:                        │ │
│  │ - Type: string                                        │ │
│  │ - Size: 200,000 characters                            │ │
│  │ - Preview: "This document discusses..."               │ │
│  │                                                        │ │
│  │ You can execute Python code to analyze it.            │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ↓ Root LM strategizes                                      │
│                                                              │
│  Recursive calls (20 × 10k tokens each):                    │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Call 1: Process chunk 1 (10k tokens)                  │ │
│  │ Call 2: Process chunk 2 (10k tokens)                  │ │
│  │ ...                                                    │ │
│  │ Call 20: Process chunk 20 (10k tokens)                │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  ↓ Combine results                                          │
│                                                              │
│  Output:                                                     │
│  "The main themes are..." (high quality)                    │
│                                                              │
│  Benefits:                                                   │
│  ✅ No context rot - small chunks                           │
│  ✅ Cheaper - use mini model for recursion                  │
│  ✅ Unlimited - no context window limit                     │
│  ✅ Transparent - see all steps                             │
└──────────────────────────────────────────────────────────────┘
```

## 🧠 Strategy Examples

### Strategy 1: Peek → Grep → Recurse

```
Iteration 1: PEEK
├─ Code: peek = context[:1000]
├─ Discovers: "This is a list of user reviews"
└─ Decision: "I'll grep for ratings"

Iteration 2: GREP
├─ Code: ratings = re.findall(r'Rating: (\d)/5', context)
├─ Result: [5, 3, 5, 2, 4, 2, 5, 3, 5, 1]
└─ Decision: "I can calculate average directly"

Iteration 3: CALCULATE
├─ Code: avg = sum(ratings) / len(ratings)
├─ Result: 3.5
└─ Output: FINAL("Average rating: 3.5/5")
```

### Strategy 2: Partition → Map → Reduce

```
Iteration 1: PEEK
├─ Code: peek = context[:500]
├─ Discovers: "Large document, ~200k chars"
└─ Decision: "I'll partition and recurse"

Iteration 2: PARTITION & MAP
├─ Code: 
│   chunks = [context[i:i+10000] for i in range(0, len(context), 10000)]
│   results = [recursive_lm("Extract themes", chunk) for chunk in chunks]
├─ Spawns: 20 recursive LM calls
└─ Collects: 20 partial results

Iteration 3: REDUCE
├─ Code:
│   all_themes = set()
│   for r in results:
│       all_themes.update(r.split(", "))
│   final = ", ".join(sorted(all_themes))
└─ Output: FINAL_VAR(final)
```

### Strategy 3: Hierarchical Summarization

```
Iteration 1: CHUNK
├─ Code: sections = [context[i:i+20000] for i in range(0, len(context), 20000)]
└─ Creates: 10 sections

Iteration 2: SUMMARIZE SECTIONS
├─ Code: summaries = [recursive_lm("Summarize", s) for s in sections]
├─ Spawns: 10 recursive calls
└─ Gets: 10 section summaries

Iteration 3: COMBINE SUMMARIES
├─ Code: final_summary = recursive_lm("Combine these summaries", summaries)
├─ Spawns: 1 recursive call
└─ Output: FINAL_VAR(final_summary)
```

## 📊 Token Flow Analysis

### Traditional Approach (200k context)

```
Single Call:
├─ Input: 200,000 tokens × $2.50/1M = $0.50
├─ Output: 500 tokens × $10/1M = $0.005
└─ Total: $0.505 per query

Tokens processed: 200,500
API calls: 1
```

### RLM Approach (200k context)

```
Root LM (3 iterations):
├─ Call 1: 2,000 tokens input × $2.50/1M = $0.005
├─ Call 2: 2,500 tokens input × $2.50/1M = $0.006
├─ Call 3: 3,000 tokens input × $2.50/1M = $0.008
└─ Subtotal: $0.019

Recursive LM (20 calls, using GPT-4o-mini):
├─ Each call: 10,000 tokens × $0.15/1M = $0.0015
├─ 20 calls: 20 × $0.0015 = $0.030
└─ Subtotal: $0.030

Output tokens:
└─ 500 tokens × $0.60/1M = $0.0003

Total: $0.049 per query (10x cheaper!)

Tokens processed: ~207,500
API calls: 23
```

## 🎯 Key Architectural Decisions

### 1. Why REPL Environment?

```
✅ Programmatic control
✅ Variable storage
✅ Code execution
✅ Function calls (recursive_lm)
✅ Familiar Python syntax
✅ Easy to sandbox
```

### 2. Why Recursive Calls?

```
✅ Parallel processing of chunks
✅ Use cheaper models for sub-tasks
✅ Avoid context rot
✅ Scalable to any size
✅ Composable strategies
```

### 3. Why Depth = 1?

```
✅ Sufficient for most tasks
✅ Simpler to implement
✅ Easier to debug
✅ Lower latency
⚠️ Can increase for complex tasks
```

### 4. Why Store Context Separately?

```
✅ Root LM never sees full context
✅ No context rot
✅ Unbounded context size
✅ Efficient token usage
✅ Adaptive processing
```

## 🔮 Future Architecture

### Planned Improvements

```
Current:
┌─────────────┐
│  Root LM    │ ──┐
└─────────────┘   │
                  ├─→ Sequential execution
┌─────────────┐   │
│ Recursive 1 │ ──┤
└─────────────┘   │
┌─────────────┐   │
│ Recursive 2 │ ──┘
└─────────────┘

Future:
┌─────────────┐
│  Root LM    │ ──┬─→ Async/parallel
└─────────────┘   │
                  ├─→ ┌─────────────┐
                  │   │ Recursive 1 │
                  │   └─────────────┘
                  │
                  ├─→ ┌─────────────┐
                  │   │ Recursive 2 │
                  │   └─────────────┘
                  │
                  └─→ ┌─────────────┐
                      │ Recursive N │
                      └─────────────┘
                      
Benefits:
✅ 10x faster
✅ Better resource utilization
✅ Prefix caching
```

---

**This architecture enables unbounded context processing with no performance degradation!** 🚀

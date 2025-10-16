#!/usr/bin/env python3
"""
RLM Demo - Shows the power of Recursive Language Models
"""

import os
from rlm_openrouter import create_rlm

# Get API key from environment variable
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    print("❌ ERROR: OPENROUTER_API_KEY environment variable not set!")
    print("Set it with: export OPENROUTER_API_KEY='your-key-here'")
    exit(1)

print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   Recursive Language Model (RLM) Demo                        ║
║                        Powered by OpenRouter API                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

# Create RLM instance
rlm = create_rlm(
    root_model="openai/gpt-4o-mini",
    recursive_model="openai/gpt-4o-mini",
    api_key=API_KEY,
    verbose=False  # Set to True to see detailed execution
)

# Demo 1: Simple Analysis
print("\n" + "="*80)
print("DEMO 1: Product Review Analysis")
print("="*80)

reviews = """
Product: SmartPhone X Pro

Review 1 (5/5): Amazing phone! Camera is incredible, battery lasts 2 days.
Review 2 (4/5): Great phone but a bit expensive. Performance is excellent.
Review 3 (2/5): Disappointed. Screen cracked easily and battery drains fast.
Review 4 (5/5): Best phone I've owned. Fast, reliable, great camera.
Review 5 (3/5): Good phone but overpriced. Camera is nice though.
Review 6 (1/5): Terrible. Stopped working after 2 weeks. Avoid!
Review 7 (5/5): Love it! Battery life is amazing and camera quality is superb.
Review 8 (4/5): Solid phone. Only complaint is the price.
Review 9 (2/5): Not worth the money. Battery issues and poor customer service.
Review 10 (5/5): Perfect! Everything works great. Highly recommend.
"""

result = rlm.completion(
    query="Calculate the average rating and list the top 3 complaints.",
    context=reviews
)

print(f"\n📊 Result: {result['answer']}")
print(f"⚙️  Iterations: {result['iterations']} | API Calls: {result['total_calls']}")

# Demo 2: Finding Information in Large Context
print("\n" + "="*80)
print("DEMO 2: Needle in Haystack (Finding specific info in large text)")
print("="*80)

# Create large context with hidden information
large_text = "Lorem ipsum dolor sit amet. " * 200
large_text += "\n\n🔑 SECRET CODE: ALPHA-BRAVO-2024-CHARLIE\n\n"
large_text += "More filler text here. " * 200
large_text += "\n\n📅 IMPORTANT DATE: Meeting on March 25th, 2025 at 3:00 PM\n\n"
large_text += "Additional content continues. " * 200

result = rlm.completion(
    query="What is the secret code and when is the important meeting?",
    context=large_text
)

print(f"\n🔍 Result: {result['answer']}")
print(f"⚙️  Iterations: {result['iterations']} | API Calls: {result['total_calls']}")

# Demo 3: Multi-Document Analysis
print("\n" + "="*80)
print("DEMO 3: Multi-Document Reasoning")
print("="*80)

documents = [
    {"id": 1, "title": "Company Info", "text": "TechCorp was founded by Alice Johnson in 2015."},
    {"id": 2, "title": "CEO Bio", "text": "Alice Johnson previously worked at InnovateLabs for 10 years."},
    {"id": 3, "title": "InnovateLabs", "text": "InnovateLabs was acquired by MegaCorp in 2020 for $800M."},
    {"id": 4, "title": "Products", "text": "TechCorp's main product is the AI Assistant Pro, launched in 2018."},
    {"id": 5, "title": "Filler 1", "text": "Random information about various topics and subjects."},
    {"id": 6, "title": "Filler 2", "text": "More unrelated content about different things."},
    {"id": 7, "title": "Filler 3", "text": "Additional filler text that is not relevant."},
]

result = rlm.completion(
    query="Who founded TechCorp, where did they work before, and when was that company acquired?",
    context=documents
)

print(f"\n🔗 Result: {result['answer']}")
print(f"⚙️  Iterations: {result['iterations']} | API Calls: {result['total_calls']}")

# Demo 4: Data Extraction
print("\n" + "="*80)
print("DEMO 4: Structured Data Extraction")
print("="*80)

log_data = """
[2025-01-15 10:23:45] ERROR: Database connection failed - timeout after 30s
[2025-01-15 10:24:12] INFO: Retrying connection...
[2025-01-15 10:24:15] SUCCESS: Database connected
[2025-01-15 10:25:33] WARNING: High memory usage detected - 85%
[2025-01-15 10:26:01] ERROR: API request failed - 500 Internal Server Error
[2025-01-15 10:26:45] INFO: API request retry successful
[2025-01-15 10:27:22] ERROR: File not found: /data/config.json
[2025-01-15 10:28:10] WARNING: Disk space low - 92% used
[2025-01-15 10:29:33] SUCCESS: Backup completed successfully
[2025-01-15 10:30:15] ERROR: Authentication failed for user: admin
"""

result = rlm.completion(
    query="Count how many ERROR, WARNING, and SUCCESS messages there are.",
    context=log_data
)

print(f"\n📈 Result: {result['answer']}")
print(f"⚙️  Iterations: {result['iterations']} | API Calls: {result['total_calls']}")

print("\n" + "="*80)
print("✅ Demo Complete!")
print("="*80)
print("""
Key Takeaways:
1. RLMs can analyze and extract information from any context size
2. The model automatically decides the best strategy (grep, parse, calculate)
3. All processing happens programmatically - no context rot!
4. Cost-efficient: Uses smaller models effectively

Next Steps:
- Try with your own data
- Run 'python test_examples.py' for more advanced scenarios
- Set verbose=True to see how RLM processes context
- Read ARCHITECTURE.md to understand the internals
""")

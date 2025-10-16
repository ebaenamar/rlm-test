#!/usr/bin/env python3
"""
Simple test to verify RLM is working with your API key
"""

import os
from rlm_openrouter import create_rlm

# Check for API key
if not os.getenv("OPENROUTER_API_KEY"):
    print("❌ ERROR: OPENROUTER_API_KEY environment variable not set!")
    print("Set it with: export OPENROUTER_API_KEY='your-key-here'")
    exit(1)

# Simple test with verbose output
rlm = create_rlm(
    root_model="openai/gpt-4o-mini",
    recursive_model="openai/gpt-4o-mini",
    verbose=True
)

# Very simple context
context = """
Review 1: Great product! Rating: 5/5
Review 2: Not bad. Rating: 3/5
Review 3: Excellent! Rating: 5/5
"""

query = "What is the average rating? Just give me the number."

print("="*80)
print("TESTING RLM WITH SIMPLE EXAMPLE")
print("="*80)

result = rlm.completion(query=query, context=context)

print("\n" + "="*80)
print("RESULT:")
print("="*80)
print(f"Answer: {result['answer']}")
print(f"Iterations: {result['iterations']}")
print(f"Total calls: {result['total_calls']}")

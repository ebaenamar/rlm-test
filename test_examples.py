"""
Test examples for Recursive Language Model (RLM) implementation

Demonstrates various use cases:
1. Needle-in-haystack with large context
2. Multi-hop reasoning over documents
3. Distributional queries (OOLONG-style)
4. Long-output generation tasks
"""

import json
from rlm_openrouter import create_rlm


def test_needle_in_haystack():
    """Test 1: Find specific information in large context"""
    print("\n" + "="*80)
    print("TEST 1: Needle in Haystack")
    print("="*80)
    
    # Create large context with hidden information
    context = """
    This is a large document with lots of information.
    """ * 100
    
    # Insert needle
    context += "\nThe secret code is: ALPHA-BRAVO-CHARLIE-2024\n"
    context += "More filler text. " * 100
    
    rlm = create_rlm(verbose=True)
    
    result = rlm.completion(
        query="What is the secret code mentioned in the document?",
        context=context
    )
    
    print(f"\n[RESULT] Answer: {result['answer']}")
    print(f"[RESULT] Iterations: {result['iterations']}")
    print(f"[RESULT] Total LM calls: {result['total_calls']}")


def test_distributional_query():
    """Test 2: OOLONG-style distributional query over structured data"""
    print("\n" + "="*80)
    print("TEST 2: Distributional Query (OOLONG-style)")
    print("="*80)
    
    # Create structured data similar to OOLONG benchmark
    entries = []
    for i in range(100):
        user_id = 10000 + i
        questions = [
            ("What is the capital of France?", "location"),
            ("Who wrote Romeo and Juliet?", "person"),
            ("When was the Declaration of Independence signed?", "date"),
            ("How many planets are in our solar system?", "number"),
            ("What is the largest ocean?", "location"),
        ]
        q, label = questions[i % len(questions)]
        entries.append(f"Date: Jan {(i % 28) + 1}, 2024 || User: {user_id} || Instance: {q}")
    
    context = "\n".join(entries)
    
    target_users = [10005, 10010, 10015, 10020, 10025, 10030]
    
    query = f"""For the following question, only consider the subset of instances that are associated with user IDs {', '.join(map(str, target_users))}.
Among instances associated with these users, how many data points should be classified as label 'location'?
Give your final answer in the form 'Answer: number'."""
    
    rlm = create_rlm(verbose=True)
    
    result = rlm.completion(query=query, context=context)
    
    print(f"\n[RESULT] Answer: {result['answer']}")
    print(f"[RESULT] Iterations: {result['iterations']}")
    print(f"[RESULT] Total LM calls: {result['total_calls']}")


def test_multi_hop_reasoning():
    """Test 3: Multi-hop reasoning over multiple documents"""
    print("\n" + "="*80)
    print("TEST 3: Multi-hop Reasoning Over Documents")
    print("="*80)
    
    # Create multiple documents with interconnected information
    documents = [
        {
            "id": "doc1",
            "title": "Company Overview",
            "content": "TechCorp was founded in 2010 by Jane Smith. The company specializes in AI solutions."
        },
        {
            "id": "doc2", 
            "title": "Leadership Team",
            "content": "Jane Smith serves as CEO. She previously worked at InnovateLabs for 8 years."
        },
        {
            "id": "doc3",
            "title": "InnovateLabs History",
            "content": "InnovateLabs was acquired by MegaCorp in 2015 for $500 million."
        },
        {
            "id": "doc4",
            "title": "Product Launch",
            "content": "TechCorp launched their flagship product, AI-Assistant Pro, in 2018."
        },
        {
            "id": "doc5",
            "title": "Market Analysis",
            "content": "The AI solutions market grew by 45% between 2018 and 2023."
        }
    ]
    
    # Add many more filler documents
    for i in range(20):
        documents.append({
            "id": f"filler_{i}",
            "title": f"Filler Document {i}",
            "content": f"This is filler content number {i} with random information about various topics."
        })
    
    context = documents
    
    query = """What company did the founder of TechCorp previously work at, and when was that company acquired?
You need to find information across multiple documents to answer this."""
    
    rlm = create_rlm(verbose=True)
    
    result = rlm.completion(query=query, context=context)
    
    print(f"\n[RESULT] Answer: {result['answer']}")
    print(f"[RESULT] Iterations: {result['iterations']}")
    print(f"[RESULT] Total LM calls: {result['total_calls']}")


def test_long_context_summarization():
    """Test 4: Summarization of very long context"""
    print("\n" + "="*80)
    print("TEST 4: Long Context Summarization")
    print("="*80)
    
    # Create long meeting transcript
    transcript = """
    [00:00] John: Welcome everyone to the Q4 planning meeting.
    [00:02] Sarah: Thanks for having us. I'd like to start with the marketing update.
    [00:05] Sarah: We've seen a 25% increase in user engagement this quarter.
    [00:08] Mike: That's great! What drove that growth?
    [00:10] Sarah: Primarily our new social media campaign and the product updates.
    [00:15] John: Excellent. Mike, can you share the engineering update?
    [00:18] Mike: Sure. We completed 3 major features and fixed 47 bugs.
    [00:22] Mike: The new API is now in beta with 10 partners.
    [00:25] Lisa: I have concerns about the API documentation.
    [00:28] Mike: Good point. We'll prioritize that next sprint.
    [00:32] John: Lisa, what's the sales update?
    [00:35] Lisa: We closed 15 new enterprise deals worth $2.3M total.
    [00:40] Lisa: However, we lost 2 clients due to pricing concerns.
    [00:45] Sarah: Should we revisit our pricing strategy?
    [00:48] John: Let's schedule a separate meeting for that.
    [00:52] Mike: I agree. We need finance involved in that discussion.
    [00:55] John: Any other topics before we wrap up?
    [01:00] Sarah: Just a reminder - the company retreat is next month.
    [01:03] Lisa: Looking forward to it!
    [01:05] John: Great. Thanks everyone. Meeting adjourned.
    """ * 10  # Repeat to make it longer
    
    query = """Summarize the key points from this meeting, including:
1. Main achievements
2. Concerns raised
3. Action items
Format as a bullet-point list."""
    
    rlm = create_rlm(verbose=True)
    
    result = rlm.completion(query=query, context=transcript)
    
    print(f"\n[RESULT] Answer: {result['answer']}")
    print(f"[RESULT] Iterations: {result['iterations']}")
    print(f"[RESULT] Total LM calls: {result['total_calls']}")


def test_simple_example():
    """Simple example to verify basic functionality"""
    print("\n" + "="*80)
    print("TEST 5: Simple Example - Context Analysis")
    print("="*80)
    
    context = """
    Product Reviews:
    
    Review 1: "This laptop is amazing! Fast performance and great battery life." - Rating: 5/5
    Review 2: "Decent laptop but overpriced for what you get." - Rating: 3/5
    Review 3: "Best purchase I've made this year. Highly recommend!" - Rating: 5/5
    Review 4: "Screen quality is poor and it runs hot." - Rating: 2/5
    Review 5: "Good value for money. Does everything I need." - Rating: 4/5
    Review 6: "Disappointed with the build quality." - Rating: 2/5
    Review 7: "Excellent laptop for programming and design work." - Rating: 5/5
    Review 8: "Battery drains too quickly." - Rating: 3/5
    Review 9: "Perfect for students and professionals alike." - Rating: 5/5
    Review 10: "Not worth the price. Look elsewhere." - Rating: 2/5
    """
    
    query = "What is the average rating and what are the main complaints mentioned in the reviews?"
    
    rlm = create_rlm(
        root_model="openai/gpt-4o-mini",  # Use cheaper model for simple test
        recursive_model="openai/gpt-4o-mini",
        verbose=True
    )
    
    result = rlm.completion(query=query, context=context)
    
    print(f"\n[RESULT] Answer: {result['answer']}")
    print(f"[RESULT] Iterations: {result['iterations']}")
    print(f"[RESULT] Total LM calls: {result['total_calls']}")


if __name__ == "__main__":
    import sys
    
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                   Recursive Language Model (RLM) Tests                       ║
║                        Using OpenRouter API                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    # Check for API key
    import os
    if not os.getenv("OPENROUTER_API_KEY"):
        print("⚠️  ERROR: OPENROUTER_API_KEY environment variable not set!")
        print("\nPlease set your OpenRouter API key:")
        print("  export OPENROUTER_API_KEY='your-key-here'")
        sys.exit(1)
    
    print("\nAvailable tests:")
    print("1. Needle in Haystack")
    print("2. Distributional Query (OOLONG-style)")
    print("3. Multi-hop Reasoning")
    print("4. Long Context Summarization")
    print("5. Simple Example (recommended for first test)")
    print("6. Run all tests")
    
    choice = input("\nSelect test to run (1-6): ").strip()
    
    tests = {
        "1": test_needle_in_haystack,
        "2": test_distributional_query,
        "3": test_multi_hop_reasoning,
        "4": test_long_context_summarization,
        "5": test_simple_example,
    }
    
    if choice == "6":
        for test_func in tests.values():
            try:
                test_func()
            except Exception as e:
                print(f"\n❌ Test failed with error: {e}")
    elif choice in tests:
        try:
            tests[choice]()
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("Invalid choice!")

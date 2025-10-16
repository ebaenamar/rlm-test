#!/usr/bin/env python3
"""
Quick start example for Recursive Language Models (RLM)

This demonstrates the simplest possible use case to get started.
"""

import os
from rlm_openrouter import create_rlm


def main():
    # Check for API key
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ ERROR: OPENROUTER_API_KEY environment variable not set!")
        print("\nGet your API key from: https://openrouter.ai/keys")
        print("Then set it with: export OPENROUTER_API_KEY='your-key-here'")
        return
    
    print("🚀 Recursive Language Model - Quick Start\n")
    
    # Example 1: Simple text analysis
    print("="*80)
    print("Example 1: Analyzing Product Reviews")
    print("="*80 + "\n")
    
    reviews_context = """
    Product: UltraBook Pro Laptop
    
    Review 1 (5/5): "Absolutely love this laptop! The battery lasts all day and it's super fast. 
    Perfect for my programming work. The screen is gorgeous and the keyboard feels great."
    
    Review 2 (3/5): "It's okay. Good performance but I think it's overpriced for what you get. 
    The trackpad is a bit finicky and the fans get loud under load."
    
    Review 3 (5/5): "Best laptop I've ever owned. Handles video editing like a champ. 
    The build quality is excellent and it looks professional."
    
    Review 4 (2/5): "Disappointed. The screen has backlight bleed and it runs very hot. 
    Customer service was unhelpful when I tried to return it."
    
    Review 5 (4/5): "Great value for the price. Does everything I need for work and school. 
    Battery life is good but not amazing. Would recommend."
    
    Review 6 (2/5): "Build quality feels cheap despite the high price. 
    The hinge is already loose after 2 months. Not worth it."
    
    Review 7 (5/5): "Perfect for developers and designers. Fast, reliable, and beautiful. 
    The retina display is stunning for photo editing."
    
    Review 8 (3/5): "Decent laptop but battery drains faster than advertised. 
    Performance is good though. Wish it had more ports."
    
    Review 9 (5/5): "Exceeded my expectations! Lightweight, powerful, and the battery really does last all day. 
    Great for travel and remote work."
    
    Review 10 (1/5): "Terrible experience. Arrived with a dead pixel and the SSD failed after one week. 
    Avoid this product."
    """
    
    # Create RLM with cheaper models for quick test
    rlm = create_rlm(
        root_model="openai/gpt-4o-mini",
        recursive_model="openai/gpt-4o-mini",
        verbose=False  # Set to True to see detailed execution
    )
    
    # Query the RLM
    result = rlm.completion(
        query="""Analyze these product reviews and provide:
1. Average rating (calculate from the ratings)
2. Top 3 positive points mentioned
3. Top 3 negative points mentioned
4. Overall recommendation (buy/don't buy)

Format your answer clearly with these sections.""",
        context=reviews_context
    )
    
    print(f"📊 Analysis Result:\n{result['answer']}\n")
    print(f"⚙️  Iterations used: {result['iterations']}")
    print(f"🔄 Total LM calls: {result['total_calls']}\n")
    
    # Example 2: Finding information in larger context
    print("="*80)
    print("Example 2: Finding Specific Information")
    print("="*80 + "\n")
    
    # Create a larger context with hidden information
    large_context = "This is filler text about various topics. " * 50
    large_context += "\n\nIMPORTANT: The meeting is scheduled for March 15th at 2:30 PM in Conference Room B.\n\n"
    large_context += "More filler text continues here. " * 50
    large_context += "\n\nNOTE: Please bring the Q4 financial reports and the project timeline.\n\n"
    large_context += "Additional content and information. " * 50
    
    result = rlm.completion(
        query="When is the meeting and what should I bring?",
        context=large_context
    )
    
    print(f"📅 Answer:\n{result['answer']}\n")
    print(f"⚙️  Iterations used: {result['iterations']}")
    print(f"🔄 Total LM calls: {result['total_calls']}\n")
    
    print("="*80)
    print("✅ Quick start complete!")
    print("="*80)
    print("\nNext steps:")
    print("1. Run 'python test_examples.py' for more advanced examples")
    print("2. Try with your own context and queries")
    print("3. Experiment with different models (see README.md)")
    print("4. Set verbose=True to see how the RLM processes context")


if __name__ == "__main__":
    main()

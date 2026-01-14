#!/usr/bin/env python3
"""
Example usage of MANUS Keyword Research Tool
Demonstrates various ways to use the tool programmatically
"""

from keyword_tool import KeywordResearchTool
import json


def example_single_keyword():
    """Example: Research a single keyword"""
    print("=" * 60)
    print("Example 1: Research a Single Keyword")
    print("=" * 60)
    
    tool = KeywordResearchTool()
    result = tool.research_keyword("digital marketing", include_related=True)
    
    print(f"\nKeyword: {result.keyword}")
    print(f"Difficulty: {result.difficulty}/100")
    print(f"Competition: {result.competition}")
    print(f"Trend: {result.trend}")
    print(f"\nRelated Keywords ({len(result.related_keywords)}):")
    for kw in result.related_keywords[:5]:
        print(f"  - {kw}")
    print(f"\nQuestions ({len(result.questions)}):")
    for q in result.questions[:5]:
        print(f"  - {q}")


def example_batch_research():
    """Example: Research multiple keywords"""
    print("\n" + "=" * 60)
    print("Example 2: Batch Research Multiple Keywords")
    print("=" * 60)
    
    tool = KeywordResearchTool()
    keywords = ["SEO", "PPC", "content marketing", "email marketing", "social media"]
    
    results = tool.batch_research(keywords, include_related=False)
    
    print(f"\nResearched {len(results)} keywords:\n")
    print(f"{'Keyword':<20} {'Difficulty':<12} {'Competition':<12}")
    print("-" * 44)
    
    for result in results:
        print(f"{result.keyword:<20} {result.difficulty:<12} {result.competition:<12}")


def example_suggestions():
    """Example: Get keyword suggestions"""
    print("\n" + "=" * 60)
    print("Example 3: Get Keyword Suggestions")
    print("=" * 60)
    
    tool = KeywordResearchTool()
    base_keyword = "AI"
    
    suggestions = tool.get_google_suggestions(base_keyword, max_results=10)
    
    print(f"\nSuggestions for '{base_keyword}':")
    for i, suggestion in enumerate(suggestions, 1):
        print(f"  {i}. {suggestion}")


def example_questions():
    """Example: Get related questions"""
    print("\n" + "=" * 60)
    print("Example 4: Get Related Questions")
    print("=" * 60)
    
    tool = KeywordResearchTool()
    keyword = "machine learning"
    
    questions = tool.get_people_also_ask(keyword)
    
    print(f"\nQuestions related to '{keyword}':")
    for i, question in enumerate(questions, 1):
        print(f"  {i}. {question}")


def example_difficulty_analysis():
    """Example: Analyze keyword difficulty"""
    print("\n" + "=" * 60)
    print("Example 5: Keyword Difficulty Analysis")
    print("=" * 60)
    
    tool = KeywordResearchTool()
    
    keywords = [
        "AI",  # Single word - high difficulty
        "best AI tools",  # Commercial intent - high difficulty
        "how to use AI tools",  # Informational - medium difficulty
        "AI tools for small business marketing automation"  # Long-tail - low difficulty
    ]
    
    print(f"\n{'Keyword':<50} {'Difficulty':<12} {'Competition':<12}")
    print("-" * 74)
    
    for keyword in keywords:
        difficulty = tool.estimate_difficulty(keyword)
        competition = tool.estimate_competition(keyword)
        print(f"{keyword:<50} {difficulty:<12} {competition:<12}")


def example_export_to_json():
    """Example: Export results to JSON"""
    print("\n" + "=" * 60)
    print("Example 6: Export Results to JSON")
    print("=" * 60)
    
    tool = KeywordResearchTool()
    result = tool.research_keyword("cloud computing", include_related=True)
    
    # Export single result
    tool.export_to_json(result, "single_keyword_result.json")
    print(f"\nSingle keyword result exported to: single_keyword_result.json")
    
    # Export batch results
    keywords = ["AWS", "Azure", "Google Cloud"]
    results = tool.batch_research(keywords, include_related=False)
    tool.export_batch_to_json(results, "batch_results.json")
    print(f"Batch results exported to: batch_results.json")


def example_api_usage():
    """Example: Using the tool via API"""
    print("\n" + "=" * 60)
    print("Example 7: API Usage (requires server running)")
    print("=" * 60)
    
    import requests
    
    try:
        # Check if server is running
        response = requests.get('http://localhost:5000/health', timeout=2)
        
        if response.status_code == 200:
            # Research a keyword via API
            api_response = requests.post(
                'http://localhost:5000/api/keyword/research',
                json={'keyword': 'blockchain', 'include_related': True},
                timeout=30
            )
            
            if api_response.status_code == 200:
                data = api_response.json()
                print(f"\nAPI Response for 'blockchain':")
                print(f"  Difficulty: {data['difficulty']}")
                print(f"  Competition: {data['competition']}")
                print(f"  Related Keywords: {len(data['related_keywords'])}")
                print(f"  Questions: {len(data['questions'])}")
            else:
                print(f"\nAPI Error: {api_response.status_code}")
        else:
            print("\nServer is not responding properly")
            
    except requests.exceptions.RequestException:
        print("\nServer is not running. Start it with: python3 web_server.py")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("MANUS Keyword Research Tool - Usage Examples")
    print("=" * 60)
    
    # Run examples
    example_single_keyword()
    example_batch_research()
    example_suggestions()
    example_questions()
    example_difficulty_analysis()
    example_export_to_json()
    example_api_usage()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
    print("\nFor more information, see README.md and QUICKSTART.md")


if __name__ == '__main__':
    main()

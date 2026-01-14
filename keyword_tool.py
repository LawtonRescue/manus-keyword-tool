#!/usr/bin/env python3
"""
MANUS Keyword Research Tool
A comprehensive keyword research tool with multiple data sources
"""

import requests
import json
import time
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from bs4 import BeautifulSoup
import re

try:
    from similarweb_integration import SimilarWebIntegration, SimilarWebData
    SIMILARWEB_AVAILABLE = True
except ImportError:
    SIMILARWEB_AVAILABLE = False
    SimilarWebData = None

try:
    from ai_first_engine import AIFirstEngine, AIInsights
    AI_FIRST_AVAILABLE = True
except ImportError:
    AI_FIRST_AVAILABLE = False
    AIInsights = None

try:
    from justin_burns_engine import JustinBurnsEngine
    from industry_analyzer import IndustryAnalyzer
    JUSTIN_BURNS_AVAILABLE = True
except ImportError:
    JUSTIN_BURNS_AVAILABLE = False


@dataclass
class KeywordData:
    """Data structure for keyword information"""
    keyword: str
    search_volume: Optional[int] = None
    competition: Optional[str] = None
    cpc: Optional[float] = None
    trend: Optional[str] = None
    related_keywords: List[str] = None
    questions: List[str] = None
    difficulty: Optional[int] = None
    similarweb_data: Optional[Dict] = None
    ai_insights: Optional[Dict] = None
    justin_burns_analysis: Optional[Dict] = None
    industry_insights: Optional[Dict] = None
    
    def __post_init__(self):
        if self.related_keywords is None:
            self.related_keywords = []
        if self.questions is None:
            self.questions = []


class KeywordResearchTool:
    """Main keyword research tool class"""
    
    def __init__(self, enable_similarweb: bool = False, enable_ai_insights: bool = False, ai_model: str = "gpt-4.1-mini"):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.enable_similarweb = enable_similarweb and SIMILARWEB_AVAILABLE
        if self.enable_similarweb:
            self.similarweb = SimilarWebIntegration()
        
        self.enable_ai_insights = enable_ai_insights and AI_FIRST_AVAILABLE
        if self.enable_ai_insights:
            self.ai_engine = AIFirstEngine(model=ai_model)
        
        self.enable_justin_burns = JUSTIN_BURNS_AVAILABLE
        if self.enable_justin_burns:
            self.justin_burns_engine = JustinBurnsEngine()
            self.industry_analyzer = IndustryAnalyzer()
    
    def research_keyword(self, keyword: str, include_related: bool = True, domain: Optional[str] = None) -> KeywordData:
        """
        Perform comprehensive keyword research
        
        Args:
            keyword: The keyword to research
            include_related: Whether to include related keywords and questions
            domain: Optional domain to get SimilarWeb data for
            
        Returns:
            KeywordData object with all available information
        """
        print(f"Researching keyword: {keyword}")
        
        data = KeywordData(keyword=keyword)
        
        # Get Google suggestions
        if include_related:
            data.related_keywords = self.get_google_suggestions(keyword)
            data.questions = self.get_people_also_ask(keyword)
        
        # Estimate difficulty based on keyword characteristics
        data.difficulty = self.estimate_difficulty(keyword)
        data.competition = self.estimate_competition(keyword)
        
        # Get trend data
        data.trend = self.get_trend_indicator(keyword)
        
        # Get SimilarWeb data if enabled and domain provided
        if self.enable_similarweb and domain:
            try:
                sw_data = self.similarweb.get_domain_data(domain)
                data.similarweb_data = self.similarweb.export_to_dict(sw_data)
            except Exception as e:
                print(f"Error getting SimilarWeb data: {e}")
        
        # Generate AI insights if enabled
        if self.enable_ai_insights:
            try:
                ai_insights = self.ai_engine.generate_insights(
                    keyword=keyword,
                    difficulty=data.difficulty,
                    competition=data.competition,
                    related_keywords=data.related_keywords,
                    similarweb_data=data.similarweb_data
                )
                data.ai_insights = self.ai_engine.export_to_dict(ai_insights)
            except Exception as e:
                print(f"Error generating AI insights: {e}")
        
        # Generate Justin Burns analysis if available
        if self.enable_justin_burns:
            try:
                print("Generating Justin Burns analysis...")
                justin_burns_analysis = self.justin_burns_engine.analyze(
                    keyword=keyword,
                    difficulty=data.difficulty,
                    competition=data.competition,
                    related_keywords=data.related_keywords,
                    ai_insights=data.ai_insights if self.enable_ai_insights else None,
                    similarweb_data=data.similarweb_data if self.enable_similarweb else None
                )
                data.justin_burns_analysis = self.justin_burns_engine.export_to_dict(justin_burns_analysis)
                
                # Generate industry analysis
                industry_insights = self.industry_analyzer.analyze(
                    keyword=keyword,
                    ai_insights=data.ai_insights if self.enable_ai_insights else None,
                    difficulty=data.difficulty,
                    competition=data.competition
                )
                data.industry_insights = self.industry_analyzer.export_to_dict(industry_insights)
            except Exception as e:
                print(f"Error generating Justin Burns analysis: {e}")
        
        return data
    
    def get_google_suggestions(self, keyword: str, max_results: int = 10) -> List[str]:
        """
        Get Google autocomplete suggestions for a keyword
        
        Args:
            keyword: The base keyword
            max_results: Maximum number of suggestions to return
            
        Returns:
            List of suggested keywords
        """
        try:
            url = "http://suggestqueries.google.com/complete/search"
            params = {
                'client': 'firefox',
                'q': keyword
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            suggestions = response.json()[1]
            return suggestions[:max_results]
        except Exception as e:
            print(f"Error getting Google suggestions: {e}")
            return []
    
    def get_people_also_ask(self, keyword: str) -> List[str]:
        """
        Get "People Also Ask" questions for a keyword
        
        Args:
            keyword: The keyword to search for
            
        Returns:
            List of related questions
        """
        questions = []
        
        # Generate common question patterns
        question_templates = [
            f"what is {keyword}",
            f"how to {keyword}",
            f"why {keyword}",
            f"when to {keyword}",
            f"where to {keyword}",
            f"best {keyword}",
            f"{keyword} vs",
            f"{keyword} benefits",
            f"{keyword} cost",
            f"{keyword} tips"
        ]
        
        # Get suggestions for question patterns
        for template in question_templates[:5]:
            suggestions = self.get_google_suggestions(template, max_results=2)
            questions.extend(suggestions)
        
        return list(set(questions))[:10]
    
    def estimate_difficulty(self, keyword: str) -> int:
        """
        Estimate keyword difficulty (0-100)
        Based on keyword characteristics
        
        Args:
            keyword: The keyword to analyze
            
        Returns:
            Difficulty score (0-100)
        """
        difficulty = 50  # Base difficulty
        
        # Adjust based on keyword length
        word_count = len(keyword.split())
        if word_count == 1:
            difficulty += 20  # Single words are harder
        elif word_count >= 4:
            difficulty -= 20  # Long-tail keywords are easier
        
        # Adjust based on keyword characteristics
        if any(word in keyword.lower() for word in ['best', 'top', 'review']):
            difficulty += 10  # Commercial intent keywords are harder
        
        if any(word in keyword.lower() for word in ['how', 'what', 'why', 'guide']):
            difficulty -= 5  # Informational keywords are slightly easier
        
        # Ensure difficulty is within bounds
        return max(0, min(100, difficulty))
    
    def estimate_competition(self, keyword: str) -> str:
        """
        Estimate competition level
        
        Args:
            keyword: The keyword to analyze
            
        Returns:
            Competition level (Low, Medium, High)
        """
        difficulty = self.estimate_difficulty(keyword)
        
        if difficulty < 40:
            return "Low"
        elif difficulty < 70:
            return "Medium"
        else:
            return "High"
    
    def get_trend_indicator(self, keyword: str) -> str:
        """
        Get trend indicator for keyword
        
        Args:
            keyword: The keyword to analyze
            
        Returns:
            Trend indicator (Rising, Stable, Declining, Unknown)
        """
        # This is a placeholder - in a real implementation,
        # you would integrate with Google Trends API or similar
        return "Stable"
    
    def batch_research(self, keywords: List[str], include_related: bool = False) -> List[KeywordData]:
        """
        Research multiple keywords
        
        Args:
            keywords: List of keywords to research
            include_related: Whether to include related keywords
            
        Returns:
            List of KeywordData objects
        """
        results = []
        
        for i, keyword in enumerate(keywords):
            print(f"Processing {i+1}/{len(keywords)}: {keyword}")
            data = self.research_keyword(keyword, include_related=include_related)
            results.append(data)
            
            # Rate limiting
            if i < len(keywords) - 1:
                time.sleep(0.5)
        
        return results
    
    def export_to_dict(self, data: KeywordData) -> Dict:
        """Export keyword data to dictionary"""
        return asdict(data)
    
    def export_to_json(self, data: KeywordData, filepath: str):
        """Export keyword data to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.export_to_dict(data), f, indent=2)
    
    def export_batch_to_json(self, results: List[KeywordData], filepath: str):
        """Export batch results to JSON file"""
        data = [self.export_to_dict(result) for result in results]
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)


def main():
    """Main function for CLI usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='MANUS Keyword Research Tool')
    parser.add_argument('keyword', nargs='?', help='Keyword to research')
    parser.add_argument('--related', action='store_true', help='Include related keywords and questions')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    parser.add_argument('--batch', help='File containing list of keywords (one per line)')
    
    args = parser.parse_args()
    
    if not args.keyword and not args.batch:
        parser.error('Either keyword or --batch must be provided')
    
    tool = KeywordResearchTool()
    
    if args.batch:
        # Batch processing
        with open(args.batch, 'r') as f:
            keywords = [line.strip() for line in f if line.strip()]
        
        results = tool.batch_research(keywords, include_related=args.related)
        
        if args.output:
            tool.export_batch_to_json(results, args.output)
            print(f"\nResults exported to {args.output}")
        else:
            for result in results:
                print(f"\n{json.dumps(tool.export_to_dict(result), indent=2)}")
    else:
        # Single keyword
        result = tool.research_keyword(args.keyword, include_related=args.related)
        
        if args.output:
            tool.export_to_json(result, args.output)
            print(f"\nResults exported to {args.output}")
        else:
            print(f"\n{json.dumps(tool.export_to_dict(result), indent=2)}")


if __name__ == '__main__':
    main()

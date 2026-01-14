#!/usr/bin/env python3
"""
AI-First Engine for MANUS Keyword Research Tool
Provides intelligent analysis using advanced LLMs (GPT-4, Claude, Gemini)
"""

import os
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from openai import OpenAI

# Initialize OpenAI client (supports multiple models via Manus proxy)
client = OpenAI()


@dataclass
class AIInsights:
    """Data structure for AI-generated insights"""
    keyword: str
    content_strategy: Optional[str] = None
    seo_recommendations: List[str] = None
    content_ideas: List[str] = None
    target_audience: Optional[str] = None
    competitive_analysis: Optional[str] = None
    monetization_opportunities: List[str] = None
    trending_topics: List[str] = None
    risk_assessment: Optional[str] = None
    
    def __post_init__(self):
        if self.seo_recommendations is None:
            self.seo_recommendations = []
        if self.content_ideas is None:
            self.content_ideas = []
        if self.monetization_opportunities is None:
            self.monetization_opportunities = []
        if self.trending_topics is None:
            self.trending_topics = []


class AIFirstEngine:
    """
    AI-First Engine that provides intelligent keyword analysis
    using advanced language models
    """
    
    def __init__(self, model: str = "gpt-4.1-mini"):
        """
        Initialize AI-First Engine
        
        Args:
            model: LLM model to use (gpt-4.1-mini, gpt-4.1-nano, gemini-2.5-flash)
        """
        self.model = model
        self.client = client
    
    def generate_insights(
        self,
        keyword: str,
        difficulty: Optional[int] = None,
        competition: Optional[str] = None,
        related_keywords: Optional[List[str]] = None,
        similarweb_data: Optional[Dict] = None
    ) -> AIInsights:
        """
        Generate comprehensive AI insights for a keyword
        
        Args:
            keyword: The target keyword
            difficulty: Keyword difficulty score
            competition: Competition level
            related_keywords: List of related keywords
            similarweb_data: SimilarWeb traffic data
            
        Returns:
            AIInsights object with AI-generated recommendations
        """
        # Build context for AI
        context = self._build_context(
            keyword, difficulty, competition, 
            related_keywords, similarweb_data
        )
        
        # Generate insights using LLM
        insights = AIInsights(keyword=keyword)
        
        try:
            # Content Strategy
            insights.content_strategy = self._generate_content_strategy(context)
            
            # SEO Recommendations
            insights.seo_recommendations = self._generate_seo_recommendations(context)
            
            # Content Ideas
            insights.content_ideas = self._generate_content_ideas(context)
            
            # Target Audience Analysis
            insights.target_audience = self._analyze_target_audience(context)
            
            # Competitive Analysis
            if similarweb_data:
                insights.competitive_analysis = self._analyze_competition(context)
            
            # Monetization Opportunities
            insights.monetization_opportunities = self._identify_monetization(context)
            
            # Trending Topics
            insights.trending_topics = self._identify_trends(context)
            
            # Risk Assessment
            insights.risk_assessment = self._assess_risks(context)
        
        except Exception as e:
            print(f"Error generating AI insights: {e}")
        
        return insights
    
    def _build_context(
        self,
        keyword: str,
        difficulty: Optional[int],
        competition: Optional[str],
        related_keywords: Optional[List[str]],
        similarweb_data: Optional[Dict]
    ) -> str:
        """Build context string for LLM prompts"""
        context = f"Keyword: {keyword}\n"
        
        if difficulty:
            context += f"Difficulty: {difficulty}/100\n"
        if competition:
            context += f"Competition: {competition}\n"
        if related_keywords:
            context += f"Related Keywords: {', '.join(related_keywords[:10])}\n"
        if similarweb_data and not similarweb_data.get('error'):
            context += f"Domain Traffic Data Available: Yes\n"
            if similarweb_data.get('global_rank'):
                context += f"Global Rank: {similarweb_data['global_rank']}\n"
            if similarweb_data.get('total_visits'):
                context += f"Monthly Visits: {similarweb_data['total_visits']}\n"
        
        return context
    
    def _generate_content_strategy(self, context: str) -> str:
        """Generate content strategy using LLM"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert SEO and content strategist. Provide concise, actionable content strategies."},
                    {"role": "user", "content": f"{context}\n\nProvide a comprehensive content strategy for this keyword in 2-3 sentences."}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Unable to generate content strategy: {str(e)}"
    
    def _generate_seo_recommendations(self, context: str) -> List[str]:
        """Generate SEO recommendations using LLM"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert SEO consultant. Provide specific, actionable SEO recommendations."},
                    {"role": "user", "content": f"{context}\n\nProvide 5 specific SEO recommendations for ranking for this keyword. Return as a JSON array of strings."}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            # Try to parse as JSON
            try:
                recommendations = json.loads(content)
                if isinstance(recommendations, list):
                    return recommendations[:5]
            except:
                # If not JSON, split by newlines
                lines = [line.strip('- ').strip() for line in content.split('\n') if line.strip()]
                return lines[:5]
            
        except Exception as e:
            return [f"Unable to generate SEO recommendations: {str(e)}"]
    
    def _generate_content_ideas(self, context: str) -> List[str]:
        """Generate content ideas using LLM"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a creative content strategist. Generate engaging, specific content ideas."},
                    {"role": "user", "content": f"{context}\n\nGenerate 5 specific content ideas (blog posts, videos, guides) for this keyword. Return as a JSON array of strings."}
                ],
                max_tokens=300,
                temperature=0.8
            )
            
            content = response.choices[0].message.content.strip()
            try:
                ideas = json.loads(content)
                if isinstance(ideas, list):
                    return ideas[:5]
            except:
                lines = [line.strip('- ').strip() for line in content.split('\n') if line.strip()]
                return lines[:5]
            
        except Exception as e:
            return [f"Unable to generate content ideas: {str(e)}"]
    
    def _analyze_target_audience(self, context: str) -> str:
        """Analyze target audience using LLM"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a marketing analyst specializing in audience research."},
                    {"role": "user", "content": f"{context}\n\nDescribe the target audience for this keyword in 2-3 sentences (demographics, pain points, goals)."}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Unable to analyze target audience: {str(e)}"
    
    def _analyze_competition(self, context: str) -> str:
        """Analyze competitive landscape using LLM"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a competitive intelligence analyst."},
                    {"role": "user", "content": f"{context}\n\nProvide a competitive analysis for this keyword in 2-3 sentences."}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Unable to analyze competition: {str(e)}"
    
    def _identify_monetization(self, context: str) -> List[str]:
        """Identify monetization opportunities using LLM"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a business strategist specializing in digital monetization."},
                    {"role": "user", "content": f"{context}\n\nIdentify 3-4 monetization opportunities for content targeting this keyword. Return as a JSON array of strings."}
                ],
                max_tokens=250,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            try:
                opportunities = json.loads(content)
                if isinstance(opportunities, list):
                    return opportunities[:4]
            except:
                lines = [line.strip('- ').strip() for line in content.split('\n') if line.strip()]
                return lines[:4]
            
        except Exception as e:
            return [f"Unable to identify monetization opportunities: {str(e)}"]
    
    def _identify_trends(self, context: str) -> List[str]:
        """Identify trending topics using LLM"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a trend analyst tracking digital marketing and content trends."},
                    {"role": "user", "content": f"{context}\n\nIdentify 3-4 current trends related to this keyword. Return as a JSON array of strings."}
                ],
                max_tokens=250,
                temperature=0.7
            )
            
            content = response.choices[0].message.content.strip()
            try:
                trends = json.loads(content)
                if isinstance(trends, list):
                    return trends[:4]
            except:
                lines = [line.strip('- ').strip() for line in content.split('\n') if line.strip()]
                return lines[:4]
            
        except Exception as e:
            return [f"Unable to identify trends: {str(e)}"]
    
    def _assess_risks(self, context: str) -> str:
        """Assess risks and challenges using LLM"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a risk analyst specializing in SEO and content marketing."},
                    {"role": "user", "content": f"{context}\n\nIdentify potential risks or challenges for targeting this keyword in 2-3 sentences."}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Unable to assess risks: {str(e)}"
    
    def export_to_dict(self, insights: AIInsights) -> Dict:
        """Export AI insights to dictionary"""
        return asdict(insights)


def main():
    """Example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate AI insights for a keyword')
    parser.add_argument('keyword', help='Keyword to analyze')
    parser.add_argument('--model', default='gpt-4.1-mini', help='LLM model to use')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    
    args = parser.parse_args()
    
    engine = AIFirstEngine(model=args.model)
    
    print(f"Generating AI insights for: {args.keyword}")
    print(f"Using model: {args.model}")
    
    insights = engine.generate_insights(
        keyword=args.keyword,
        difficulty=65,
        competition="Medium",
        related_keywords=["example1", "example2", "example3"]
    )
    
    result = engine.export_to_dict(insights)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nResults exported to {args.output}")
    else:
        print(f"\n{json.dumps(result, indent=2)}")


if __name__ == '__main__':
    main()

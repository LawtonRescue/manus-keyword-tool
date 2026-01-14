#!/usr/bin/env python3
"""
Industry Analyzer - Justin Burns' Three Profitable Industries
Focus on: Wealth, Relationships, Health
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class IndustryInsights:
    """Industry-specific insights"""
    industry: str  # Wealth, Relationships, Health, Other
    confidence: float  # 0.0-1.0
    profitability_score: int  # 0-100
    specific_insights: str
    opportunities: List[str]
    content_angles: List[str]
    monetization_strategies: List[str]
    target_demographics: str
    competition_notes: str


class IndustryAnalyzer:
    """
    Analyze keywords for Justin Burns' three most profitable industries:
    1. Wealth - Financial tools, investment, money management
    2. Relationships - Connection, dating, networking, family
    3. Health - Wellness, fitness, medical, mental health
    """
    
    def __init__(self):
        """Initialize industry analyzer with keyword patterns"""
        
        # Wealth industry keywords
        self.wealth_keywords = {
            "primary": [
                "money", "wealth", "income", "revenue", "profit", "investment",
                "financial", "finance", "stock", "crypto", "trading", "business",
                "entrepreneur", "passive income", "dividend", "roi", "portfolio",
                "real estate", "property", "asset", "net worth", "millionaire",
                "billionaire", "rich", "wealthy", "affluent", "prosperity"
            ],
            "secondary": [
                "budget", "savings", "debt", "credit", "loan", "mortgage",
                "insurance", "retirement", "401k", "ira", "pension", "tax",
                "accounting", "bookkeeping", "payroll", "salary", "wage",
                "bonus", "commission", "equity", "shares", "securities"
            ]
        }
        
        # Relationships industry keywords
        self.relationships_keywords = {
            "primary": [
                "relationship", "dating", "love", "romance", "marriage", "wedding",
                "partner", "spouse", "boyfriend", "girlfriend", "couple", "family",
                "parenting", "children", "kids", "baby", "pregnancy", "adoption",
                "friendship", "social", "networking", "community", "connection"
            ],
            "secondary": [
                "divorce", "breakup", "therapy", "counseling", "communication",
                "intimacy", "sex", "attraction", "compatibility", "trust",
                "commitment", "engagement", "anniversary", "valentine", "gift",
                "advice", "tips", "help", "support", "guidance"
            ]
        }
        
        # Health industry keywords
        self.health_keywords = {
            "primary": [
                "health", "fitness", "wellness", "medical", "doctor", "hospital",
                "disease", "illness", "condition", "treatment", "therapy", "cure",
                "medicine", "drug", "supplement", "vitamin", "nutrition", "diet",
                "weight loss", "exercise", "workout", "gym", "training", "yoga",
                "mental health", "depression", "anxiety", "stress", "mindfulness"
            ],
            "secondary": [
                "symptom", "diagnosis", "prevention", "recovery", "healing",
                "pain", "injury", "surgery", "prescription", "pharmacy",
                "insurance", "healthcare", "clinic", "patient", "nurse",
                "physical", "mental", "emotional", "spiritual", "holistic",
                "organic", "natural", "alternative", "traditional"
            ]
        }
    
    def analyze(
        self,
        keyword: str,
        ai_insights: Optional[Dict] = None,
        difficulty: int = 50,
        competition: str = "Medium"
    ) -> IndustryInsights:
        """
        Analyze keyword for industry classification and insights
        
        Args:
            keyword: Target keyword
            ai_insights: AI-generated insights (optional)
            difficulty: Keyword difficulty
            competition: Competition level
        
        Returns:
            Industry-specific insights
        """
        # Detect industry
        industry, confidence = self._detect_industry(keyword, ai_insights)
        
        # Calculate profitability score
        profitability = self._calculate_profitability_score(
            industry, difficulty, competition, confidence
        )
        
        # Generate industry-specific insights
        specific_insights = self._generate_specific_insights(
            industry, keyword, confidence
        )
        
        # Identify opportunities
        opportunities = self._identify_opportunities(
            industry, keyword, difficulty, competition
        )
        
        # Generate content angles
        content_angles = self._generate_content_angles(
            industry, keyword
        )
        
        # Generate monetization strategies
        monetization = self._generate_monetization_strategies(
            industry, keyword
        )
        
        # Identify target demographics
        demographics = self._identify_target_demographics(
            industry, keyword
        )
        
        # Competition notes
        competition_notes = self._generate_competition_notes(
            industry, competition, difficulty
        )
        
        return IndustryInsights(
            industry=industry,
            confidence=confidence,
            profitability_score=profitability,
            specific_insights=specific_insights,
            opportunities=opportunities,
            content_angles=content_angles,
            monetization_strategies=monetization,
            target_demographics=demographics,
            competition_notes=competition_notes
        )
    
    def _detect_industry(
        self,
        keyword: str,
        ai_insights: Optional[Dict]
    ) -> Tuple[str, float]:
        """
        Detect which of the three profitable industries the keyword belongs to
        
        Returns:
            (industry_name, confidence_score)
        """
        keyword_lower = keyword.lower()
        
        # Check AI insights for additional context
        context = keyword_lower
        if ai_insights:
            if ai_insights.get("target_audience"):
                context += " " + ai_insights["target_audience"].lower()
            if ai_insights.get("content_strategy"):
                context += " " + ai_insights["content_strategy"].lower()
        
        # Score each industry
        wealth_score = self._calculate_industry_match(context, self.wealth_keywords)
        relationships_score = self._calculate_industry_match(context, self.relationships_keywords)
        health_score = self._calculate_industry_match(context, self.health_keywords)
        
        # Determine primary industry
        scores = {
            "Wealth": wealth_score,
            "Relationships": relationships_score,
            "Health": health_score
        }
        
        max_score = max(scores.values())
        
        if max_score == 0:
            return "Other", 0.0
        
        industry = max(scores, key=scores.get)
        confidence = min(1.0, max_score / 10.0)  # Normalize to 0-1
        
        return industry, confidence
    
    def _calculate_industry_match(
        self,
        text: str,
        keyword_dict: Dict[str, List[str]]
    ) -> float:
        """Calculate match score for an industry"""
        score = 0.0
        
        # Primary keywords worth more
        for kw in keyword_dict["primary"]:
            if kw in text:
                score += 2.0
        
        # Secondary keywords
        for kw in keyword_dict["secondary"]:
            if kw in text:
                score += 1.0
        
        return score
    
    def _calculate_profitability_score(
        self,
        industry: str,
        difficulty: int,
        competition: str,
        confidence: float
    ) -> int:
        """
        Calculate profitability score (0-100)
        
        Justin Burns: Wealth, Relationships, Health are most profitable
        """
        if industry == "Other":
            base_score = 40
        else:
            # All three industries are highly profitable
            base_score = 80
        
        # Adjust for confidence
        base_score = int(base_score * confidence)
        
        # Adjust for difficulty (lower difficulty = higher profitability potential)
        difficulty_adjustment = (100 - difficulty) * 0.2
        
        # Adjust for competition
        competition_adjustment = {
            "Low": 20,
            "Medium": 0,
            "High": -15
        }
        
        final_score = base_score + difficulty_adjustment + competition_adjustment.get(competition, 0)
        
        return max(0, min(100, int(final_score)))
    
    def _generate_specific_insights(
        self,
        industry: str,
        keyword: str,
        confidence: float
    ) -> str:
        """Generate industry-specific insights"""
        
        if industry == "Wealth":
            return f"'{keyword}' is in the Wealth industry - one of Justin Burns' top 3 most profitable industries. Financial content has high engagement, strong monetization potential through affiliate products, courses, and consulting. Focus on building trust and authority through data-driven content and real results."
        
        elif industry == "Relationships":
            return f"'{keyword}' is in the Relationships industry - one of Justin Burns' top 3 most profitable industries. Relationship content drives emotional engagement and loyalty. Monetize through coaching, courses, membership communities, and affiliate products. Focus on transformation stories and authentic connection."
        
        elif industry == "Health":
            return f"'{keyword}' is in the Health industry - one of Justin Burns' top 3 most profitable industries. Health content has massive demand and strong monetization through supplements, courses, coaching, and affiliate products. Focus on transformation, before/after results, and building authority through expertise."
        
        else:
            if confidence > 0:
                return f"'{keyword}' has elements of Justin Burns' profitable industries but doesn't fit perfectly into Wealth, Relationships, or Health. Consider pivoting to emphasize financial, relationship, or health angles for higher profitability."
            else:
                return f"'{keyword}' is outside Justin Burns' top 3 profitable industries (Wealth, Relationships, Health). Consider if you can angle your content to connect to one of these industries for higher monetization potential."
    
    def _identify_opportunities(
        self,
        industry: str,
        keyword: str,
        difficulty: int,
        competition: str
    ) -> List[str]:
        """Identify industry-specific opportunities"""
        
        opportunities = []
        
        if industry == "Wealth":
            opportunities = [
                "High-ticket affiliate products (financial tools, investment platforms)",
                "Premium courses and coaching ($500-$5000+ price points)",
                "Subscription newsletters with exclusive financial insights",
                "Consulting services for businesses/individuals",
                "Digital products (spreadsheets, calculators, templates)",
                "Sponsored content from financial brands"
            ]
        
        elif industry == "Relationships":
            opportunities = [
                "Coaching and consulting services",
                "Membership communities (monthly recurring revenue)",
                "Online courses and workshops",
                "Books and digital guides",
                "Affiliate products (dating apps, relationship tools)",
                "Speaking engagements and workshops"
            ]
        
        elif industry == "Health":
            opportunities = [
                "Supplement and product affiliates (high commissions)",
                "Online fitness/wellness programs",
                "Coaching and personalized plans",
                "Digital products (meal plans, workout programs)",
                "Brand partnerships and sponsorships",
                "Certification programs and training"
            ]
        
        else:
            opportunities = [
                "Affiliate marketing opportunities",
                "Digital products and courses",
                "Consulting or coaching services",
                "Sponsored content",
                "Ad revenue from high traffic"
            ]
        
        # Adjust based on difficulty and competition
        if difficulty < 40 and competition == "Low":
            opportunities.insert(0, "LOW COMPETITION = Quick wins possible! Fast path to monetization.")
        
        return opportunities[:6]  # Return top 6
    
    def _generate_content_angles(
        self,
        industry: str,
        keyword: str
    ) -> List[str]:
        """Generate industry-specific content angles"""
        
        if industry == "Wealth":
            return [
                f"How to make money with {keyword}",
                f"{keyword} for beginners: Complete guide",
                f"Best {keyword} strategies for 2026",
                f"Case study: How I made $X with {keyword}",
                f"{keyword} mistakes to avoid (and what to do instead)"
            ]
        
        elif industry == "Relationships":
            return [
                f"How to improve your {keyword}",
                f"{keyword} advice from experts",
                f"Transform your {keyword} in 30 days",
                f"The psychology of {keyword}",
                f"Real stories: How {keyword} changed lives"
            ]
        
        elif industry == "Health":
            return [
                f"Complete guide to {keyword}",
                f"Science-backed {keyword} strategies",
                f"Before and after: {keyword} transformations",
                f"{keyword} for busy professionals",
                f"Common {keyword} mistakes and how to fix them"
            ]
        
        else:
            return [
                f"Ultimate guide to {keyword}",
                f"{keyword} tips and tricks",
                f"How to master {keyword}",
                f"{keyword} for beginners",
                f"Advanced {keyword} strategies"
            ]
    
    def _generate_monetization_strategies(
        self,
        industry: str,
        keyword: str
    ) -> List[str]:
        """Generate industry-specific monetization strategies"""
        
        if industry == "Wealth":
            return [
                "Affiliate partnerships with financial platforms (high commissions)",
                "Premium courses ($500-$2000): 'Master [keyword] in 90 days'",
                "Consulting packages ($1000-$10000): Personalized financial strategies",
                "Subscription newsletter ($20-$100/month): Exclusive insights and analysis"
            ]
        
        elif industry == "Relationships":
            return [
                "Coaching programs ($500-$5000): 1-on-1 or group coaching",
                "Membership community ($20-$50/month): Ongoing support and resources",
                "Online courses ($100-$500): Self-paced relationship transformation",
                "Books and guides ($10-$50): Digital or physical products"
            ]
        
        elif industry == "Health":
            return [
                "Supplement affiliates (20-40% commissions on recurring purchases)",
                "Fitness/wellness programs ($100-$1000): Structured transformation plans",
                "Coaching services ($500-$3000): Personalized health guidance",
                "Digital products ($20-$200): Meal plans, workout programs, guides"
            ]
        
        else:
            return [
                "Affiliate marketing: Promote relevant products/services",
                "Digital courses: Package your expertise",
                "Consulting: Offer personalized guidance",
                "Ad revenue: Build traffic and monetize with ads"
            ]
    
    def _identify_target_demographics(
        self,
        industry: str,
        keyword: str
    ) -> str:
        """Identify target demographics for the industry"""
        
        if industry == "Wealth":
            return "Ages 25-55, professionals and entrepreneurs seeking financial growth. High intent to invest in education and tools. Willing to pay premium prices for proven strategies and results."
        
        elif industry == "Relationships":
            return "Ages 20-60, individuals seeking to improve personal relationships. Emotionally engaged, loyal audience. Values authenticity and transformation stories. Willing to invest in coaching and courses."
        
        elif industry == "Health":
            return "Ages 25-65, health-conscious individuals seeking transformation. Highly motivated, willing to invest in supplements, programs, and coaching. Values before/after results and expert guidance."
        
        else:
            return "Demographics vary - analyze your specific niche for precise targeting."
    
    def _generate_competition_notes(
        self,
        industry: str,
        competition: str,
        difficulty: int
    ) -> str:
        """Generate competition notes specific to industry"""
        
        notes = []
        
        if industry in ["Wealth", "Relationships", "Health"]:
            notes.append(f"✅ You're in one of Justin Burns' top 3 profitable industries - high potential!")
        
        if competition == "High":
            notes.append("High competition means proven market demand. Focus on superior UX/design and unique angles to differentiate.")
        elif competition == "Low":
            notes.append("Low competition = opportunity! Move fast to establish authority before others discover this keyword.")
        
        if difficulty < 40:
            notes.append("Low difficulty = quick wins possible. This is a great starting point.")
        elif difficulty > 70:
            notes.append("High difficulty - consider long-tail variations or niche angles to build authority first.")
        
        return " ".join(notes)
    
    def export_to_dict(self, insights: IndustryInsights) -> Dict:
        """Export insights to dictionary"""
        return {
            "industry": insights.industry,
            "confidence": round(insights.confidence, 2),
            "profitability_score": insights.profitability_score,
            "specific_insights": insights.specific_insights,
            "opportunities": insights.opportunities,
            "content_angles": insights.content_angles,
            "monetization_strategies": insights.monetization_strategies,
            "target_demographics": insights.target_demographics,
            "competition_notes": insights.competition_notes
        }


# CLI interface
if __name__ == "__main__":
    import sys
    import json
    import argparse
    
    parser = argparse.ArgumentParser(description="Industry Analyzer - Justin Burns' Profitable Industries")
    parser.add_argument("keyword", help="Keyword to analyze")
    parser.add_argument("--difficulty", type=int, default=50, help="Keyword difficulty (0-100)")
    parser.add_argument("--competition", choices=["Low", "Medium", "High"], default="Medium")
    parser.add_argument("--output", help="Output JSON file path")
    
    args = parser.parse_args()
    
    analyzer = IndustryAnalyzer()
    insights = analyzer.analyze(
        keyword=args.keyword,
        difficulty=args.difficulty,
        competition=args.competition
    )
    
    result = analyzer.export_to_dict(insights)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Results exported to {args.output}")
    else:
        print(json.dumps(result, indent=2))

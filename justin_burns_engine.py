#!/usr/bin/env python3
"""
Justin Burns Engine - Core Methodology Implementation
Integrates Justin Burns' proven AI philosophy and business strategies
"""

import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta


@dataclass
class SpeedToValueStep:
    """A single step in the speed-to-value plan"""
    day: int
    action: str
    time_estimate: str
    priority: str  # High, Medium, Low
    description: str


@dataclass
class SpeedToValuePlan:
    """Complete speed-to-value action plan"""
    timeline: str
    total_days: int
    steps: List[SpeedToValueStep]
    quick_wins: List[str]
    success_metrics: List[str]


@dataclass
class PassionAlignment:
    """Passion alignment assessment"""
    score: int  # 0-100
    reasoning: str
    sustainability_assessment: str
    long_term_potential: str


@dataclass
class JustinBurnsAnalysis:
    """Complete Justin Burns methodology analysis"""
    keyword: str
    mastery_score: int  # 0-100
    mastery_level: str  # Beginner, Intermediate, Advanced, Expert
    speed_to_value_plan: SpeedToValuePlan
    passion_alignment: PassionAlignment
    competitor_weaknesses: List[str]
    improvement_strategy: str
    simplified_approach: str
    creator_focus: str


class JustinBurnsEngine:
    """
    Core Justin Burns methodology engine
    
    Implements:
    - Mastery scoring and progression
    - Speed-to-value planning
    - Passion alignment assessment
    - Competitor weakness identification
    - Simplified, creator-focused strategies
    """
    
    def __init__(self):
        """Initialize Justin Burns engine"""
        self.mastery_thresholds = {
            "Beginner": (0, 30),
            "Intermediate": (31, 60),
            "Advanced": (61, 85),
            "Expert": (86, 100)
        }
    
    def analyze(
        self,
        keyword: str,
        difficulty: int,
        competition: str,
        related_keywords: List[str] = None,
        ai_insights: Dict = None,
        similarweb_data: Dict = None,
        user_interests: List[str] = None
    ) -> JustinBurnsAnalysis:
        """
        Complete Justin Burns analysis
        
        Args:
            keyword: Target keyword
            difficulty: Keyword difficulty (0-100)
            competition: Competition level (Low/Medium/High)
            related_keywords: Related keywords list
            ai_insights: AI-generated insights
            similarweb_data: SimilarWeb traffic data
            user_interests: User's interests for passion alignment
        
        Returns:
            Complete Justin Burns analysis
        """
        # Calculate mastery score
        mastery_score = self._calculate_mastery_score(
            difficulty, competition, related_keywords, similarweb_data
        )
        
        # Determine mastery level
        mastery_level = self._get_mastery_level(mastery_score)
        
        # Generate speed-to-value plan
        speed_plan = self._generate_speed_to_value_plan(
            keyword, difficulty, competition, mastery_level, ai_insights
        )
        
        # Assess passion alignment
        passion = self._assess_passion_alignment(
            keyword, user_interests, ai_insights
        )
        
        # Identify competitor weaknesses
        weaknesses = self._identify_competitor_weaknesses(
            keyword, difficulty, competition, similarweb_data
        )
        
        # Generate improvement strategy
        improvement = self._generate_improvement_strategy(
            keyword, weaknesses, mastery_level
        )
        
        # Create simplified approach
        simplified = self._create_simplified_approach(
            keyword, mastery_level, speed_plan
        )
        
        # Generate creator focus
        creator_focus = self._generate_creator_focus(
            keyword, ai_insights, passion
        )
        
        return JustinBurnsAnalysis(
            keyword=keyword,
            mastery_score=mastery_score,
            mastery_level=mastery_level,
            speed_to_value_plan=speed_plan,
            passion_alignment=passion,
            competitor_weaknesses=weaknesses,
            improvement_strategy=improvement,
            simplified_approach=simplified,
            creator_focus=creator_focus
        )
    
    def _calculate_mastery_score(
        self,
        difficulty: int,
        competition: str,
        related_keywords: List[str],
        similarweb_data: Dict
    ) -> int:
        """
        Calculate mastery score based on keyword characteristics
        
        Higher score = easier to master/rank for
        """
        score = 100
        
        # Difficulty factor (higher difficulty = lower mastery score)
        score -= (difficulty * 0.5)
        
        # Competition factor
        competition_penalty = {
            "Low": 0,
            "Medium": 15,
            "High": 30
        }
        score -= competition_penalty.get(competition, 15)
        
        # Related keywords bonus (more data = easier to master)
        if related_keywords:
            score += min(len(related_keywords), 10)
        
        # SimilarWeb data bonus (proven market = easier to validate)
        if similarweb_data and similarweb_data.get("total_visits"):
            score += 5
        
        return max(0, min(100, int(score)))
    
    def _get_mastery_level(self, score: int) -> str:
        """Determine mastery level from score"""
        for level, (min_score, max_score) in self.mastery_thresholds.items():
            if min_score <= score <= max_score:
                return level
        return "Beginner"
    
    def _generate_speed_to_value_plan(
        self,
        keyword: str,
        difficulty: int,
        competition: str,
        mastery_level: str,
        ai_insights: Dict
    ) -> SpeedToValuePlan:
        """
        Generate Justin Burns' "by this weekend" speed-to-value plan
        """
        # Determine timeline based on difficulty
        if difficulty < 40:
            total_days = 3
            timeline = "3 days (this weekend!)"
        elif difficulty < 70:
            total_days = 5
            timeline = "5 days (this week)"
        else:
            total_days = 7
            timeline = "7 days (next week)"
        
        # Generate steps
        steps = []
        
        # Day 1: Research & Validation
        steps.append(SpeedToValueStep(
            day=1,
            action="Research & Validate",
            time_estimate="2-3 hours",
            priority="High",
            description=f"Deep dive into '{keyword}'. Study top 10 competitors, identify their weaknesses (design, content gaps, UX issues). Validate market demand."
        ))
        
        # Day 2: Content Strategy
        if ai_insights and ai_insights.get("content_strategy"):
            content_action = f"Implement content strategy: {ai_insights['content_strategy'][:100]}..."
        else:
            content_action = f"Create comprehensive content outline for '{keyword}'. Focus on solving one problem exceptionally well."
        
        steps.append(SpeedToValueStep(
            day=2,
            action="Content Strategy",
            time_estimate="3-4 hours",
            priority="High",
            description=content_action
        ))
        
        # Day 3: Build/Create
        steps.append(SpeedToValueStep(
            day=3,
            action="Build & Create",
            time_estimate="4-6 hours",
            priority="High",
            description="Create your content/product. Use AI to accelerate (write, design, code). Focus on superior UX and design - this is your competitive edge."
        ))
        
        if total_days >= 5:
            # Day 4: Polish & Optimize
            steps.append(SpeedToValueStep(
                day=4,
                action="Polish & Optimize",
                time_estimate="2-3 hours",
                priority="Medium",
                description="Refine your work. Improve design, optimize for SEO, add engaging elements (images, videos, interactivity). Make it 10x better than competitors."
            ))
            
            # Day 5: Launch & Promote
            steps.append(SpeedToValueStep(
                day=5,
                action="Launch & Promote",
                time_estimate="2-4 hours",
                priority="High",
                description="Publish your content/product. Share on social media, relevant communities, email list. Get initial feedback and traffic."
            ))
        
        if total_days >= 7:
            # Day 6: Iterate
            steps.append(SpeedToValueStep(
                day=6,
                action="Iterate Based on Feedback",
                time_estimate="2-3 hours",
                priority="Medium",
                description="Analyze initial performance. Make improvements based on user feedback. Fix any issues quickly."
            ))
            
            # Day 7: Scale
            steps.append(SpeedToValueStep(
                day=7,
                action="Scale & Monetize",
                time_estimate="3-4 hours",
                priority="Medium",
                description="Implement monetization strategy. Create related content. Build on your success with systematic approach."
            ))
        
        # Quick wins
        quick_wins = [
            "Use AI to create content 10x faster",
            "Focus on design - it's your competitive advantage",
            "Solve one problem exceptionally well",
            "Launch fast, iterate based on real feedback"
        ]
        
        # Success metrics
        success_metrics = [
            "Content published and live",
            "Initial traffic/users acquired",
            "Positive feedback received",
            "Monetization strategy implemented",
            "Foundation for scaling established"
        ]
        
        return SpeedToValuePlan(
            timeline=timeline,
            total_days=total_days,
            steps=steps,
            quick_wins=quick_wins,
            success_metrics=success_metrics
        )
    
    def _assess_passion_alignment(
        self,
        keyword: str,
        user_interests: List[str],
        ai_insights: Dict
    ) -> PassionAlignment:
        """
        Assess passion alignment (Justin Burns: "passion is crucial for longevity")
        """
        score = 50  # Default neutral score
        reasoning_parts = []
        
        # Check user interests alignment
        if user_interests:
            keyword_lower = keyword.lower()
            matches = [interest for interest in user_interests if interest.lower() in keyword_lower or keyword_lower in interest.lower()]
            if matches:
                score += 25
                reasoning_parts.append(f"Strong alignment with your interests: {', '.join(matches)}")
            else:
                score -= 10
                reasoning_parts.append("Limited alignment with stated interests")
        
        # Check target audience fit (from AI insights)
        if ai_insights and ai_insights.get("target_audience"):
            score += 15
            reasoning_parts.append("Clear target audience identified - easier to stay passionate")
        
        # Check monetization potential
        if ai_insights and ai_insights.get("monetization_opportunities"):
            score += 10
            reasoning_parts.append("Strong monetization potential - financial motivation helps sustain passion")
        
        score = max(0, min(100, score))
        reasoning = " | ".join(reasoning_parts) if reasoning_parts else "Neutral passion alignment - success depends on developing genuine interest"
        
        # Sustainability assessment
        if score >= 75:
            sustainability = "Excellent - High passion alignment suggests strong long-term sustainability. You'll enjoy the journey, not just the destination."
        elif score >= 50:
            sustainability = "Good - Moderate passion alignment. Focus on finding aspects you genuinely enjoy to maintain momentum through challenges."
        else:
            sustainability = "Caution - Low passion alignment may lead to burnout. Consider if this truly excites you, or explore related keywords that resonate more."
        
        # Long-term potential
        if score >= 70:
            long_term = "High potential for mastery. Your genuine interest will drive you through the 'drudgery' of excellence that Justin Burns emphasizes."
        else:
            long_term = "Moderate potential. Success is possible but may require extra discipline. Consider building passion through small wins and progress."
        
        return PassionAlignment(
            score=score,
            reasoning=reasoning,
            sustainability_assessment=sustainability,
            long_term_potential=long_term
        )
    
    def _identify_competitor_weaknesses(
        self,
        keyword: str,
        difficulty: int,
        competition: str,
        similarweb_data: Dict
    ) -> List[str]:
        """
        Identify competitor weaknesses (Justin Burns: "find weaknesses and improve")
        """
        weaknesses = []
        
        # Common weaknesses based on competition level
        if competition == "High":
            weaknesses.extend([
                "Outdated content (many high-competition sites haven't updated in years)",
                "Poor mobile experience (focus on mobile-first design)",
                "Slow load times (optimize for speed)",
                "Generic content (create unique, personality-driven content)",
                "Weak monetization (implement better revenue strategies)"
            ])
        elif competition == "Medium":
            weaknesses.extend([
                "Inconsistent content quality (maintain high standards)",
                "Poor user experience (focus on intuitive design)",
                "Limited content depth (go deeper than competitors)",
                "Weak social proof (build trust signals)",
                "Missing multimedia (add videos, infographics, interactive elements)"
            ])
        else:  # Low competition
            weaknesses.extend([
                "Minimal competition (huge opportunity!)",
                "Low-quality content (easy to outrank with quality)",
                "No clear authority (establish yourself as the expert)",
                "Poor SEO optimization (basic optimization will win)",
                "Limited content variety (diversify content types)"
            ])
        
        # SimilarWeb-based weaknesses
        if similarweb_data:
            bounce_rate = similarweb_data.get("bounce_rate")
            if bounce_rate and bounce_rate > 60:
                weaknesses.append(f"High bounce rate ({bounce_rate}%) - improve engagement and UX")
            
            traffic_sources = similarweb_data.get("traffic_sources", {})
            organic = traffic_sources.get("organic_search", 0)
            if organic < 30:
                weaknesses.append(f"Low organic traffic ({organic}%) - SEO opportunity")
        
        # Difficulty-based opportunities
        if difficulty < 40:
            weaknesses.append("Low difficulty - quick wins possible with basic optimization")
        elif difficulty > 70:
            weaknesses.append("High difficulty - focus on long-tail variations and niche angles")
        
        return weaknesses[:7]  # Return top 7 weaknesses
    
    def _generate_improvement_strategy(
        self,
        keyword: str,
        weaknesses: List[str],
        mastery_level: str
    ) -> str:
        """
        Generate improvement strategy (Justin Burns: "validated improvement")
        """
        strategies = []
        
        # Core strategy based on mastery level
        if mastery_level == "Expert":
            strategies.append("You can dominate this keyword with focused effort.")
        elif mastery_level == "Advanced":
            strategies.append("Strong opportunity - implement systematic approach for success.")
        elif mastery_level == "Intermediate":
            strategies.append("Moderate challenge - focus on superior UX and design to differentiate.")
        else:
            strategies.append("High challenge - start with long-tail variations to build authority.")
        
        # Address top 3 weaknesses
        if weaknesses:
            strategies.append(f"Key opportunities: {'; '.join(weaknesses[:3])}")
        
        # Justin Burns' core principles
        strategies.append("Apply Justin Burns' principles: Superior UX/design, solve one problem exceptionally well, use AI to accelerate development, launch fast and iterate.")
        
        return " ".join(strategies)
    
    def _create_simplified_approach(
        self,
        keyword: str,
        mastery_level: str,
        speed_plan: SpeedToValuePlan
    ) -> str:
        """
        Create simplified approach (Justin Burns: "make complex simple")
        """
        if mastery_level == "Expert":
            return f"Simple path: Create exceptional content for '{keyword}', focus on superior design, launch within {speed_plan.total_days} days. Your mastery level means quick wins are achievable."
        elif mastery_level == "Advanced":
            return f"Simple path: Research top 10 competitors, identify their weakest points, create 10x better content with superior UX. Launch in {speed_plan.total_days} days, iterate based on feedback."
        elif mastery_level == "Intermediate":
            return f"Simple path: Don't compete head-on. Find a specific angle or sub-niche within '{keyword}', create the best resource for that angle. Use AI to accelerate, focus on design. {speed_plan.total_days}-day timeline."
        else:
            return f"Simple path: Start with long-tail variations of '{keyword}'. Build authority gradually. Use AI to create quality content fast. Focus on one sub-topic, master it, then expand. {speed_plan.total_days}-day sprints."
    
    def _generate_creator_focus(
        self,
        keyword: str,
        ai_insights: Dict,
        passion: PassionAlignment
    ) -> str:
        """
        Generate creator-focused recommendations
        """
        focus_points = []
        
        # Business building focus
        focus_points.append(f"Build an asset, not just content. '{keyword}' can become a valuable property with consistent effort.")
        
        # Monetization
        if ai_insights and ai_insights.get("monetization_opportunities"):
            monetization = ai_insights["monetization_opportunities"]
            if isinstance(monetization, list) and monetization:
                focus_points.append(f"Monetization: {monetization[0]}")
        
        # Passion sustainability
        if passion.score >= 70:
            focus_points.append("Your high passion alignment is your secret weapon - you'll outlast competitors who are just chasing trends.")
        else:
            focus_points.append("Build passion through progress. Small wins will fuel your motivation.")
        
        # Justin Burns' golden rule
        focus_points.append("Remember: Every business needs technology. You're building a tech-enabled asset that can scale without proportional resource increase.")
        
        return " | ".join(focus_points)
    
    def export_to_dict(self, analysis: JustinBurnsAnalysis) -> Dict[str, Any]:
        """Export analysis to dictionary"""
        result = {
            "keyword": analysis.keyword,
            "mastery_score": analysis.mastery_score,
            "mastery_level": analysis.mastery_level,
            "speed_to_value_plan": {
                "timeline": analysis.speed_to_value_plan.timeline,
                "total_days": analysis.speed_to_value_plan.total_days,
                "steps": [
                    {
                        "day": step.day,
                        "action": step.action,
                        "time_estimate": step.time_estimate,
                        "priority": step.priority,
                        "description": step.description
                    }
                    for step in analysis.speed_to_value_plan.steps
                ],
                "quick_wins": analysis.speed_to_value_plan.quick_wins,
                "success_metrics": analysis.speed_to_value_plan.success_metrics
            },
            "passion_alignment": {
                "score": analysis.passion_alignment.score,
                "reasoning": analysis.passion_alignment.reasoning,
                "sustainability_assessment": analysis.passion_alignment.sustainability_assessment,
                "long_term_potential": analysis.passion_alignment.long_term_potential
            },
            "competitor_weaknesses": analysis.competitor_weaknesses,
            "improvement_strategy": analysis.improvement_strategy,
            "simplified_approach": analysis.simplified_approach,
            "creator_focus": analysis.creator_focus
        }
        return result


# CLI interface
if __name__ == "__main__":
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Justin Burns Engine - Mastery-Driven Keyword Analysis")
    parser.add_argument("keyword", help="Keyword to analyze")
    parser.add_argument("--difficulty", type=int, default=50, help="Keyword difficulty (0-100)")
    parser.add_argument("--competition", choices=["Low", "Medium", "High"], default="Medium", help="Competition level")
    parser.add_argument("--interests", nargs="+", help="User interests for passion alignment")
    parser.add_argument("--output", help="Output JSON file path")
    
    args = parser.parse_args()
    
    # Initialize engine
    engine = JustinBurnsEngine()
    
    # Analyze
    print(f"Analyzing '{args.keyword}' with Justin Burns methodology...")
    analysis = engine.analyze(
        keyword=args.keyword,
        difficulty=args.difficulty,
        competition=args.competition,
        user_interests=args.interests
    )
    
    # Export
    result = engine.export_to_dict(analysis)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Results exported to {args.output}")
    else:
        print(json.dumps(result, indent=2))

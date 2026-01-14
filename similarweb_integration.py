#!/usr/bin/env python3
"""
SimilarWeb Integration for MANUS Keyword Research Tool
Provides website traffic data, rankings, and competitive intelligence
"""

import sys
sys.path.append('/opt/.manus/.sandbox-runtime')

from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import json

try:
    from data_api import ApiClient
    SIMILARWEB_AVAILABLE = True
except ImportError:
    SIMILARWEB_AVAILABLE = False
    print("Warning: SimilarWeb API not available in this environment")


@dataclass
class SimilarWebData:
    """Data structure for SimilarWeb information"""
    domain: str
    global_rank: Optional[int] = None
    total_visits: Optional[int] = None
    unique_visitors: Optional[int] = None
    bounce_rate: Optional[float] = None
    pages_per_visit: Optional[float] = None
    avg_visit_duration: Optional[float] = None
    traffic_sources: Optional[Dict[str, float]] = None
    top_countries: Optional[Dict[str, float]] = None
    error: Optional[str] = None
    
    def __post_init__(self):
        if self.traffic_sources is None:
            self.traffic_sources = {}
        if self.top_countries is None:
            self.top_countries = {}


class SimilarWebIntegration:
    """SimilarWeb API integration class"""
    
    def __init__(self):
        """Initialize SimilarWeb integration"""
        self.available = SIMILARWEB_AVAILABLE
        if self.available:
            self.client = ApiClient()
        
        # Calculate date range (last 3 months)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        self.start_date = start_date.strftime("%Y-%m")
        self.end_date = end_date.strftime("%Y-%m")
    
    def get_domain_data(self, domain: str) -> SimilarWebData:
        """
        Get comprehensive data for a domain
        
        Args:
            domain: Domain to analyze (e.g., "example.com")
            
        Returns:
            SimilarWebData object with all available information
        """
        if not self.available:
            return SimilarWebData(
                domain=domain,
                error="SimilarWeb API not available in this environment"
            )
        
        data = SimilarWebData(domain=domain)
        
        try:
            # Get global rank
            rank_data = self._get_global_rank(domain)
            if rank_data and 'global_rank' in rank_data:
                data.global_rank = rank_data.get('global_rank')
            
            # Get total visits
            visits_data = self._get_total_visits(domain)
            if visits_data and 'visits' in visits_data:
                visits_list = visits_data['visits']
                if visits_list:
                    data.total_visits = visits_list[-1].get('visits', 0)
            
            # Get unique visitors
            unique_data = self._get_unique_visitors(domain)
            if unique_data and 'unique_visitors' in unique_data:
                unique_list = unique_data['unique_visitors']
                if unique_list:
                    data.unique_visitors = unique_list[-1].get('unique_visitors', 0)
            
            # Get bounce rate
            bounce_data = self._get_bounce_rate(domain)
            if bounce_data and 'bounce_rate' in bounce_data:
                bounce_list = bounce_data['bounce_rate']
                if bounce_list:
                    data.bounce_rate = bounce_list[-1].get('bounce_rate', 0)
            
            # Get traffic sources
            traffic_data = self._get_traffic_sources(domain)
            if traffic_data and 'channels' in traffic_data:
                channels = traffic_data['channels']
                if channels:
                    latest = channels[-1]
                    data.traffic_sources = {
                        'organic_search': latest.get('organic_search', 0),
                        'paid_search': latest.get('paid_search', 0),
                        'direct': latest.get('direct', 0),
                        'referrals': latest.get('referrals', 0),
                        'social': latest.get('social', 0),
                        'email': latest.get('mail', 0),
                        'display_ads': latest.get('display_ads', 0)
                    }
            
            # Get top countries
            country_data = self._get_top_countries(domain)
            if country_data and 'records' in country_data:
                records = country_data['records']
                if records:
                    data.top_countries = {
                        record['country']: record.get('share', 0)
                        for record in records[:5]
                    }
        
        except Exception as e:
            data.error = f"Error fetching SimilarWeb data: {str(e)}"
        
        return data
    
    def _get_global_rank(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get global rank for domain"""
        try:
            return self.client.call_api(
                'SimilarWeb/get_global_rank',
                path_params={'domain': domain},
                query={}
            )
        except Exception as e:
            print(f"Error getting global rank: {e}")
            return None
    
    def _get_total_visits(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get total visits for domain"""
        try:
            return self.client.call_api(
                'SimilarWeb/get_visits_total',
                path_params={'domain': domain},
                query={
                    'country': 'world',
                    'granularity': 'monthly',
                    'start_date': self.start_date,
                    'end_date': self.end_date,
                    'main_domain_only': False
                }
            )
        except Exception as e:
            print(f"Error getting total visits: {e}")
            return None
    
    def _get_unique_visitors(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get unique visitors for domain"""
        try:
            return self.client.call_api(
                'SimilarWeb/get_unique_visit',
                path_params={'domain': domain},
                query={
                    'country': 'world',
                    'start_date': self.start_date,
                    'end_date': self.end_date,
                    'main_domain_only': False
                }
            )
        except Exception as e:
            print(f"Error getting unique visitors: {e}")
            return None
    
    def _get_bounce_rate(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get bounce rate for domain"""
        try:
            return self.client.call_api(
                'SimilarWeb/get_bounce_rate',
                path_params={'domain': domain},
                query={
                    'country': 'world',
                    'granularity': 'monthly',
                    'start_date': self.start_date,
                    'end_date': self.end_date,
                    'main_domain_only': False
                }
            )
        except Exception as e:
            print(f"Error getting bounce rate: {e}")
            return None
    
    def _get_traffic_sources(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get traffic sources for domain"""
        try:
            return self.client.call_api(
                'SimilarWeb/get_traffic_sources_desktop',
                path_params={'domain': domain},
                query={
                    'country': 'world',
                    'granularity': 'monthly',
                    'start_date': self.start_date,
                    'end_date': self.end_date,
                    'main_domain_only': False
                }
            )
        except Exception as e:
            print(f"Error getting traffic sources: {e}")
            return None
    
    def _get_top_countries(self, domain: str) -> Optional[Dict[str, Any]]:
        """Get top countries for domain"""
        try:
            return self.client.call_api(
                'SimilarWeb/get_total_traffic_by_country',
                path_params={'domain': domain},
                query={
                    'start_date': self.start_date,
                    'end_date': self.end_date,
                    'main_domain_only': True,
                    'limit': '5'
                }
            )
        except Exception as e:
            print(f"Error getting top countries: {e}")
            return None
    
    def export_to_dict(self, data: SimilarWebData) -> Dict:
        """Export SimilarWeb data to dictionary"""
        return asdict(data)
    
    def format_number(self, num: Optional[int]) -> str:
        """Format large numbers for display"""
        if num is None:
            return "N/A"
        
        if num >= 1_000_000_000:
            return f"{num / 1_000_000_000:.1f}B"
        elif num >= 1_000_000:
            return f"{num / 1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num / 1_000:.1f}K"
        else:
            return str(num)


def main():
    """Example usage"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Get SimilarWeb data for a domain')
    parser.add_argument('domain', help='Domain to analyze (e.g., amazon.com)')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    
    args = parser.parse_args()
    
    integration = SimilarWebIntegration()
    
    if not integration.available:
        print("SimilarWeb API is not available in this environment")
        return
    
    print(f"Fetching SimilarWeb data for: {args.domain}")
    data = integration.get_domain_data(args.domain)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(integration.export_to_dict(data), f, indent=2)
        print(f"\nResults exported to {args.output}")
    else:
        print(f"\n{json.dumps(integration.export_to_dict(data), indent=2)}")


if __name__ == '__main__':
    main()

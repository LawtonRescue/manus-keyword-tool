# SimilarWeb Integration Guide

## 📊 Overview

Your MANUS Keyword Research Tool now includes **SimilarWeb integration**, providing comprehensive website traffic intelligence and competitive analysis data.

## ✨ What's New

### SimilarWeb Data Available

When you provide a domain along with your keyword research, you'll get:

1. **Global Rank** - Website's worldwide ranking
2. **Total Visits** - Monthly visit count
3. **Unique Visitors** - Deduplicated visitor count
4. **Bounce Rate** - Percentage of single-page visits
5. **Traffic Sources** - Breakdown by channel:
   - Organic Search
   - Paid Search
   - Direct Traffic
   - Referrals
   - Social Media
   - Email
   - Display Ads
6. **Top Countries** - Geographic traffic distribution

## 🚀 How to Use

### Web Interface

1. **Enter Keyword**: Type your keyword (e.g., "digital marketing")
2. **Enter Domain** (Optional): Add a domain (e.g., "hubspot.com")
3. **Click Research**: Get keyword data + SimilarWeb traffic intelligence

**Example**:
- Keyword: `content marketing`
- Domain: `contentmarketinginstitute.com`
- Result: Keyword metrics + traffic data for the domain

### API Usage

#### Research Keyword with Domain Data

```bash
curl -X POST http://localhost:5000/api/keyword/research \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "SEO tools",
    "include_related": true,
    "domain": "ahrefs.com"
  }'
```

**Response**:
```json
{
  "keyword": "SEO tools",
  "difficulty": 70,
  "competition": "High",
  "trend": "Stable",
  "related_keywords": [...],
  "questions": [...],
  "similarweb_data": {
    "domain": "ahrefs.com",
    "global_rank": 1234,
    "total_visits": 5000000,
    "unique_visitors": 3500000,
    "bounce_rate": 0.45,
    "traffic_sources": {
      "organic_search": 0.65,
      "paid_search": 0.05,
      "direct": 0.20,
      "referrals": 0.08,
      "social": 0.02
    },
    "top_countries": {
      "United States": 0.35,
      "United Kingdom": 0.12,
      "India": 0.10
    }
  }
}
```

#### Get SimilarWeb Data Only

```bash
curl "http://localhost:5000/api/similarweb/domain?domain=amazon.com"
```

### Python Integration

```python
from keyword_tool import KeywordResearchTool

# Initialize with SimilarWeb enabled
tool = KeywordResearchTool(enable_similarweb=True)

# Research keyword with domain
result = tool.research_keyword(
    keyword="e-commerce platform",
    include_related=True,
    domain="shopify.com"
)

# Access SimilarWeb data
if result.similarweb_data:
    print(f"Global Rank: {result.similarweb_data['global_rank']}")
    print(f"Total Visits: {result.similarweb_data['total_visits']}")
    print(f"Bounce Rate: {result.similarweb_data['bounce_rate']}")
```

## 📈 Use Cases

### 1. Competitive Analysis

Research keywords and analyze competitor traffic:

```bash
# Analyze "project management software" keyword
# Check traffic for Asana
curl -X POST http://localhost:5000/api/keyword/research \
  -H "Content-Type: application/json" \
  -d '{"keyword": "project management software", "domain": "asana.com"}'
```

### 2. Market Research

Understand market leaders in your niche:

- Keyword: `CRM software`
- Domains to check: `salesforce.com`, `hubspot.com`, `zoho.com`
- Compare: Traffic, rankings, traffic sources

### 3. Content Strategy

Find high-traffic sites in your keyword space:

- Research keyword: `digital marketing tips`
- Check domains: `neilpatel.com`, `moz.com`, `searchenginejournal.com`
- Analyze: Which sites get most traffic, best traffic sources

### 4. SEO Opportunity Analysis

Identify ranking opportunities:

- Low difficulty keywords + high traffic domains = opportunity
- Check if top-ranking sites have declining traffic
- Find gaps in traffic sources

## 🎯 Data Metrics Explained

### Global Rank
- **What it is**: Website's position among all websites worldwide
- **Lower is better**: #100 is better than #1000
- **Use for**: Quick assessment of site authority

### Total Visits
- **What it is**: Total number of visits per month
- **Includes**: Desktop + Mobile web traffic
- **Use for**: Understanding site popularity

### Unique Visitors
- **What it is**: Deduplicated count of individuals visiting
- **Cross-device**: Same person on phone and laptop = 1 visitor
- **Use for**: True audience size

### Bounce Rate
- **What it is**: % of visitors who leave after one page
- **Lower is better**: 30% is better than 70%
- **Use for**: Content engagement assessment

### Traffic Sources
- **Organic Search**: Google, Bing search results
- **Paid Search**: Google Ads, paid search
- **Direct**: Typed URL, bookmarks
- **Referrals**: Links from other sites
- **Social**: Facebook, Twitter, LinkedIn, etc.
- **Email**: Email campaigns
- **Display Ads**: Banner ads

## 🔧 Technical Details

### API Availability

SimilarWeb integration uses the Manus Data API system. The integration will:
- ✅ Work in Manus sandbox environment
- ✅ Provide real SimilarWeb data
- ⚠️ May have rate limits (handled automatically)
- ⚠️ Requires valid domain names

### Data Freshness

- **Update Frequency**: Monthly
- **Historical Data**: Last 3 months available
- **Latency**: Data is typically 1-2 months behind current date

### Error Handling

If SimilarWeb data is unavailable:
- Keyword research still works normally
- `similarweb_data` field will be `null` or contain error message
- No impact on core functionality

## 📊 Example Workflows

### Workflow 1: Competitor Traffic Analysis

```bash
# Step 1: Research your target keyword
curl -X POST http://localhost:5000/api/keyword/research \
  -H "Content-Type: application/json" \
  -d '{"keyword": "email marketing", "include_related": false}'

# Step 2: Check traffic for top competitors
for domain in mailchimp.com constantcontact.com sendinblue.com; do
  curl "http://localhost:5000/api/similarweb/domain?domain=$domain"
done
```

### Workflow 2: Content Gap Analysis

```python
from keyword_tool import KeywordResearchTool

tool = KeywordResearchTool(enable_similarweb=True)

# Your target keywords
keywords = ["content marketing", "SEO tips", "social media strategy"]

# Competitor domains
competitors = ["hubspot.com", "moz.com", "neilpatel.com"]

# Analyze each combination
for keyword in keywords:
    for domain in competitors:
        result = tool.research_keyword(keyword, domain=domain)
        
        print(f"\nKeyword: {keyword}")
        print(f"Domain: {domain}")
        print(f"Difficulty: {result.difficulty}")
        
        if result.similarweb_data:
            print(f"Traffic: {result.similarweb_data['total_visits']}")
            print(f"Rank: {result.similarweb_data['global_rank']}")
```

### Workflow 3: Traffic Source Optimization

Identify which traffic sources work best for competitors:

```python
from similarweb_integration import SimilarWebIntegration

sw = SimilarWebIntegration()

competitors = ["competitor1.com", "competitor2.com", "competitor3.com"]

for domain in competitors:
    data = sw.get_domain_data(domain)
    
    print(f"\n{domain}:")
    print(f"Total Visits: {sw.format_number(data.total_visits)}")
    
    if data.traffic_sources:
        print("Traffic Sources:")
        for source, percentage in data.traffic_sources.items():
            print(f"  {source}: {percentage*100:.1f}%")
```

## 🎓 Best Practices

### 1. Domain Format
- ✅ Use: `example.com`
- ✅ Use: `www.example.com`
- ❌ Avoid: `https://example.com`
- ❌ Avoid: `example.com/page`

### 2. Data Interpretation
- Compare similar-sized sites
- Look at trends, not just absolute numbers
- Consider seasonal variations
- Cross-reference with other data sources

### 3. Rate Limiting
- Don't hammer the API
- Use batch processing for multiple domains
- Cache results when possible
- Respect API limits

### 4. Error Handling
- Always check if `similarweb_data` exists
- Handle `null` values gracefully
- Provide fallback when data unavailable

## 🔒 Privacy & Compliance

- SimilarWeb data is aggregated and anonymized
- No personal user data is collected
- Data is for competitive intelligence only
- Follow SimilarWeb's terms of service

## 📚 Additional Resources

- **SimilarWeb Official**: https://www.similarweb.com
- **API Documentation**: See Manus Data API docs
- **Support**: Contact Manus support for API issues

## 🎉 Summary

Your keyword research tool now provides:
1. ✅ Keyword difficulty and competition
2. ✅ Related keywords and questions
3. ✅ **NEW**: Website traffic intelligence
4. ✅ **NEW**: Competitive analysis data
5. ✅ **NEW**: Traffic source breakdown

This makes your tool a complete SEO and competitive intelligence platform!

---

**Version**: 2.0.0 with SimilarWeb Integration
**Last Updated**: January 13, 2026

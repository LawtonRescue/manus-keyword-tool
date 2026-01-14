# MANUS Keyword Research Tool

A comprehensive keyword research tool with multiple data sources for keyword analysis, including search volume estimation, competition analysis, related keywords, and question discovery.

## Features

- **Keyword Analysis**: Get comprehensive data about any keyword
- **Related Keywords**: Discover related keywords using Google autocomplete
- **Question Discovery**: Find "People Also Ask" questions related to your keyword
- **Difficulty Estimation**: Estimate keyword difficulty and competition level
- **Batch Processing**: Research multiple keywords at once
- **RESTful API**: Full API access for integration with other tools
- **Web Interface**: Beautiful, responsive web UI for easy keyword research
- **CLI Tool**: Command-line interface for scripting and automation

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Setup

1. Clone or download the repository:
```bash
cd /home/ubuntu/keyword-research-tool
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage

### Web Interface

1. Start the web server:
```bash
python3 web_server.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Enter a keyword and click "Research" to get comprehensive analysis

### Command Line Interface

Research a single keyword:
```bash
python3 keyword_tool.py "digital marketing"
```

Include related keywords and questions:
```bash
python3 keyword_tool.py "digital marketing" --related
```

Save results to JSON file:
```bash
python3 keyword_tool.py "digital marketing" --related --output results.json
```

Batch research from file:
```bash
# Create a file with keywords (one per line)
echo -e "digital marketing\nSEO\ncontent marketing" > keywords.txt

# Research all keywords
python3 keyword_tool.py --batch keywords.txt --output batch_results.json
```

### API Endpoints

#### 1. Research Single Keyword

**Endpoint**: `POST /api/keyword/research`

**Request Body**:
```json
{
  "keyword": "digital marketing",
  "include_related": true
}
```

**Response**:
```json
{
  "keyword": "digital marketing",
  "search_volume": null,
  "competition": "Medium",
  "cpc": null,
  "trend": "Stable",
  "related_keywords": [
    "digital marketing agency",
    "digital marketing course",
    "digital marketing jobs"
  ],
  "questions": [
    "what is digital marketing",
    "how to digital marketing"
  ],
  "difficulty": 65
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:5000/api/keyword/research \
  -H "Content-Type: application/json" \
  -d '{"keyword": "digital marketing", "include_related": true}'
```

#### 2. Batch Research

**Endpoint**: `POST /api/keyword/batch`

**Request Body**:
```json
{
  "keywords": ["SEO", "PPC", "content marketing"],
  "include_related": false
}
```

**Response**: Array of keyword data objects

**cURL Example**:
```bash
curl -X POST http://localhost:5000/api/keyword/batch \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["SEO", "PPC", "content marketing"], "include_related": false}'
```

#### 3. Get Suggestions

**Endpoint**: `GET /api/keyword/suggestions?keyword=digital&max_results=10`

**Response**:
```json
{
  "keyword": "digital",
  "suggestions": [
    "digital marketing",
    "digital art",
    "digital nomad"
  ]
}
```

**cURL Example**:
```bash
curl "http://localhost:5000/api/keyword/suggestions?keyword=digital&max_results=10"
```

#### 4. Get Questions

**Endpoint**: `GET /api/keyword/questions?keyword=SEO`

**Response**:
```json
{
  "keyword": "SEO",
  "questions": [
    "what is SEO",
    "how to SEO",
    "why SEO important"
  ]
}
```

**cURL Example**:
```bash
curl "http://localhost:5000/api/keyword/questions?keyword=SEO"
```

#### 5. Get Difficulty

**Endpoint**: `GET /api/keyword/difficulty?keyword=digital+marketing`

**Response**:
```json
{
  "keyword": "digital marketing",
  "difficulty": 65,
  "competition": "Medium"
}
```

**cURL Example**:
```bash
curl "http://localhost:5000/api/keyword/difficulty?keyword=digital+marketing"
```

## Python Integration

You can also use the tool directly in your Python code:

```python
from keyword_tool import KeywordResearchTool

# Initialize the tool
tool = KeywordResearchTool()

# Research a single keyword
result = tool.research_keyword("digital marketing", include_related=True)
print(f"Keyword: {result.keyword}")
print(f"Difficulty: {result.difficulty}")
print(f"Competition: {result.competition}")
print(f"Related Keywords: {result.related_keywords}")

# Batch research
keywords = ["SEO", "PPC", "content marketing"]
results = tool.batch_research(keywords, include_related=False)

for result in results:
    print(f"{result.keyword}: Difficulty {result.difficulty}")

# Export to JSON
tool.export_to_json(result, "output.json")
```

## Data Sources

The tool uses multiple data sources to provide comprehensive keyword analysis:

1. **Google Autocomplete API**: For related keyword suggestions
2. **Algorithmic Analysis**: For difficulty and competition estimation
3. **Pattern-Based Discovery**: For question generation

## Metrics Explained

### Difficulty Score (0-100)

- **0-39**: Low difficulty - Easier to rank for
- **40-69**: Medium difficulty - Moderate competition
- **70-100**: High difficulty - Very competitive

The difficulty score is calculated based on:
- Keyword length (single words are harder)
- Commercial intent indicators
- Informational vs transactional nature

### Competition Level

- **Low**: Less competitive, good opportunity for ranking
- **Medium**: Moderate competition, requires quality content
- **High**: Very competitive, requires strong SEO strategy

### Trend Indicator

- **Rising**: Increasing search interest
- **Stable**: Consistent search volume
- **Declining**: Decreasing interest
- **Unknown**: Insufficient data

## Deployment

### Local Development

```bash
python3 web_server.py
```

### Production Deployment

For production, use a WSGI server like Gunicorn:

```bash
pip3 install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 web_server:app
```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "web_server.py"]
```

Build and run:

```bash
docker build -t keyword-research-tool .
docker run -p 5000:5000 keyword-research-tool
```

## Limitations

- Search volume data requires integration with paid APIs (Google Ads, SEMrush, etc.)
- CPC data requires Google Ads API integration
- Trend data is estimated; integrate with Google Trends API for real data
- Rate limiting applies to Google Autocomplete API

## Future Enhancements

- Integration with Google Ads API for real search volume data
- Integration with Google Trends API for trend analysis
- SERP analysis for competition assessment
- Backlink analysis for difficulty calculation
- Historical data tracking
- Keyword clustering and grouping
- Export to CSV/Excel formats
- Scheduled keyword monitoring

## License

MIT License - Free to use and modify

## Support

For issues, questions, or contributions, please visit the project repository or contact support.

## Version

Current Version: 1.0.0

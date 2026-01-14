# Quick Start Guide - MANUS Keyword Research Tool

## 🚀 Getting Started in 3 Steps

### Step 1: Install Dependencies

```bash
cd /home/ubuntu/keyword-research-tool
pip3 install -r requirements.txt
```

### Step 2: Start the Server

```bash
python3 web_server.py
```

The server will start on `http://localhost:5000`

### Step 3: Use the Tool

**Option A: Web Interface**
- Open your browser to `http://localhost:5000`
- Enter a keyword and click "Research"

**Option B: Command Line**
```bash
python3 keyword_tool.py "your keyword" --related
```

**Option C: API**
```bash
curl -X POST http://localhost:5000/api/keyword/research \
  -H "Content-Type: application/json" \
  -d '{"keyword": "your keyword", "include_related": true}'
```

## 📊 Example Usage

### Research a Single Keyword

```bash
python3 keyword_tool.py "digital marketing" --related --output results.json
```

### Batch Research Multiple Keywords

1. Create a file with keywords (one per line):
```bash
echo -e "SEO\nPPC\ncontent marketing\nemail marketing" > keywords.txt
```

2. Run batch research:
```bash
python3 keyword_tool.py --batch keywords.txt --output batch_results.json
```

### Use the API

```python
import requests

# Research a keyword
response = requests.post('http://localhost:5000/api/keyword/research', json={
    'keyword': 'AI tools',
    'include_related': True
})

data = response.json()
print(f"Keyword: {data['keyword']}")
print(f"Difficulty: {data['difficulty']}")
print(f"Competition: {data['competition']}")
print(f"Related Keywords: {data['related_keywords']}")
```

## 🎯 What You Get

For each keyword, you'll receive:

- **Difficulty Score** (0-100): How hard it is to rank
- **Competition Level**: Low, Medium, or High
- **Related Keywords**: Google autocomplete suggestions
- **Questions**: "People Also Ask" related questions
- **Trend Indicator**: Rising, Stable, or Declining

## 🔗 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/keyword/research` | POST | Research single keyword |
| `/api/keyword/batch` | POST | Research multiple keywords |
| `/api/keyword/suggestions` | GET | Get autocomplete suggestions |
| `/api/keyword/questions` | GET | Get related questions |
| `/api/keyword/difficulty` | GET | Get difficulty score |

## 💡 Tips

1. **Use Related Keywords**: Enable `--related` flag to discover more keyword opportunities
2. **Batch Processing**: Research multiple keywords at once to save time
3. **Export Results**: Always use `--output` to save results for later analysis
4. **API Integration**: Use the RESTful API to integrate with your existing tools

## 🛠️ Troubleshooting

**Server won't start?**
- Check if port 5000 is already in use: `lsof -i :5000`
- Kill existing process: `kill -9 $(lsof -t -i:5000)`

**No results returned?**
- Check your internet connection
- Verify the keyword is properly formatted
- Check server logs: `tail -f server.log`

**Rate limiting issues?**
- Add delays between requests
- Use batch processing for multiple keywords
- The tool automatically includes rate limiting

## 📚 More Information

For detailed documentation, see [README.md](README.md)

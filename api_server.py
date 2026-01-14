#!/usr/bin/env python3
"""
MANUS Keyword Research Tool - API Server
RESTful API for keyword research functionality
"""

from flask import Flask, request, jsonify
from keyword_tool import KeywordResearchTool, KeywordData
from typing import List, Dict
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize the keyword research tool
tool = KeywordResearchTool()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'MANUS Keyword Research Tool'
    })


@app.route('/api/keyword/research', methods=['POST'])
def research_keyword():
    """
    Research a single keyword
    
    Request body:
    {
        "keyword": "example keyword",
        "include_related": true
    }
    
    Response:
    {
        "keyword": "example keyword",
        "search_volume": null,
        "competition": "Medium",
        "cpc": null,
        "trend": "Stable",
        "related_keywords": [...],
        "questions": [...],
        "difficulty": 50
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'keyword' not in data:
            return jsonify({'error': 'Missing keyword parameter'}), 400
        
        keyword = data['keyword']
        include_related = data.get('include_related', True)
        
        result = tool.research_keyword(keyword, include_related=include_related)
        
        return jsonify(tool.export_to_dict(result))
    
    except Exception as e:
        logging.error(f"Error researching keyword: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/keyword/batch', methods=['POST'])
def batch_research():
    """
    Research multiple keywords
    
    Request body:
    {
        "keywords": ["keyword1", "keyword2", "keyword3"],
        "include_related": false
    }
    
    Response:
    [
        {
            "keyword": "keyword1",
            ...
        },
        {
            "keyword": "keyword2",
            ...
        }
    ]
    """
    try:
        data = request.get_json()
        
        if not data or 'keywords' not in data:
            return jsonify({'error': 'Missing keywords parameter'}), 400
        
        keywords = data['keywords']
        include_related = data.get('include_related', False)
        
        if not isinstance(keywords, list):
            return jsonify({'error': 'keywords must be a list'}), 400
        
        if len(keywords) > 100:
            return jsonify({'error': 'Maximum 100 keywords per request'}), 400
        
        results = tool.batch_research(keywords, include_related=include_related)
        
        return jsonify([tool.export_to_dict(result) for result in results])
    
    except Exception as e:
        logging.error(f"Error in batch research: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/keyword/suggestions', methods=['GET'])
def get_suggestions():
    """
    Get Google autocomplete suggestions
    
    Query parameters:
    - keyword: The base keyword
    - max_results: Maximum number of results (default: 10)
    
    Response:
    {
        "keyword": "example",
        "suggestions": [...]
    }
    """
    try:
        keyword = request.args.get('keyword')
        
        if not keyword:
            return jsonify({'error': 'Missing keyword parameter'}), 400
        
        max_results = int(request.args.get('max_results', 10))
        
        suggestions = tool.get_google_suggestions(keyword, max_results=max_results)
        
        return jsonify({
            'keyword': keyword,
            'suggestions': suggestions
        })
    
    except Exception as e:
        logging.error(f"Error getting suggestions: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/keyword/questions', methods=['GET'])
def get_questions():
    """
    Get related questions for a keyword
    
    Query parameters:
    - keyword: The keyword to search for
    
    Response:
    {
        "keyword": "example",
        "questions": [...]
    }
    """
    try:
        keyword = request.args.get('keyword')
        
        if not keyword:
            return jsonify({'error': 'Missing keyword parameter'}), 400
        
        questions = tool.get_people_also_ask(keyword)
        
        return jsonify({
            'keyword': keyword,
            'questions': questions
        })
    
    except Exception as e:
        logging.error(f"Error getting questions: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/keyword/difficulty', methods=['GET'])
def get_difficulty():
    """
    Estimate keyword difficulty
    
    Query parameters:
    - keyword: The keyword to analyze
    
    Response:
    {
        "keyword": "example",
        "difficulty": 50,
        "competition": "Medium"
    }
    """
    try:
        keyword = request.args.get('keyword')
        
        if not keyword:
            return jsonify({'error': 'Missing keyword parameter'}), 400
        
        difficulty = tool.estimate_difficulty(keyword)
        competition = tool.estimate_competition(keyword)
        
        return jsonify({
            'keyword': keyword,
            'difficulty': difficulty,
            'competition': competition
        })
    
    except Exception as e:
        logging.error(f"Error estimating difficulty: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    """API documentation"""
    return jsonify({
        'service': 'MANUS Keyword Research Tool API',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/keyword/research': 'Research a single keyword',
            'POST /api/keyword/batch': 'Research multiple keywords',
            'GET /api/keyword/suggestions': 'Get autocomplete suggestions',
            'GET /api/keyword/questions': 'Get related questions',
            'GET /api/keyword/difficulty': 'Estimate keyword difficulty',
            'GET /health': 'Health check'
        },
        'documentation': 'See README.md for detailed usage instructions'
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

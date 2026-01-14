#!/usr/bin/env python3
"""
MANUS Keyword Research Tool - Web Server
Serves both the API and the web UI
"""

from flask import Flask, request, jsonify, send_from_directory
from keyword_tool import KeywordResearchTool
from similarweb_integration import SimilarWebIntegration
from ai_first_engine import AIFirstEngine
import logging
import os

app = Flask(__name__, static_folder='.')
logging.basicConfig(level=logging.INFO)

# Initialize the keyword research tool with SimilarWeb and AI-First enabled
tool = KeywordResearchTool(
    enable_similarweb=True,
    enable_ai_insights=True,
    ai_model="gpt-4.1-mini"
)
similarweb = SimilarWebIntegration()
ai_engine = AIFirstEngine(model="gpt-4.1-mini")


@app.route('/')
def index():
    """Serve the web UI"""
    return send_from_directory('.', 'index.html')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'MANUS Keyword Research Tool'
    })


@app.route('/api/keyword/research', methods=['POST'])
def research_keyword():
    """Research a single keyword"""
    try:
        data = request.get_json()
        
        if not data or 'keyword' not in data:
            return jsonify({'error': 'Missing keyword parameter'}), 400
        
        keyword = data['keyword']
        include_related = data.get('include_related', True)
        domain = data.get('domain', None)
        
        result = tool.research_keyword(keyword, include_related=include_related, domain=domain)
        
        return jsonify(tool.export_to_dict(result))
    
    except Exception as e:
        logging.error(f"Error researching keyword: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/keyword/batch', methods=['POST'])
def batch_research():
    """Research multiple keywords"""
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
    """Get Google autocomplete suggestions"""
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
    """Get related questions for a keyword"""
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
    """Estimate keyword difficulty"""
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


@app.route('/api/similarweb/domain', methods=['GET'])
def get_similarweb_data():
    """Get SimilarWeb data for a domain"""
    try:
        domain = request.args.get('domain')
        
        if not domain:
            return jsonify({'error': 'Missing domain parameter'}), 400
        
        if not similarweb.available:
            return jsonify({'error': 'SimilarWeb API not available'}), 503
        
        data = similarweb.get_domain_data(domain)
        
        return jsonify(similarweb.export_to_dict(data))
    
    except Exception as e:
        logging.error(f"Error getting SimilarWeb data: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

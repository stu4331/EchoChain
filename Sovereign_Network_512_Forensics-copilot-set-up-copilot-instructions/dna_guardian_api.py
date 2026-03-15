#!/usr/bin/env python3
"""
DNA Guardian Web API
====================

Flask API integration for the DNA Guardian Protection System.
Provides RESTful endpoints for website integration.

Endpoints:
- GET  /api/guardian/status - Get protection status
- POST /api/guardian/init - Initialize protection
- POST /api/guardian/scan - Scan a file for threats
- GET  /api/guardian/report - Get security report
- POST /api/guardian/monitor/start - Start monitoring
- POST /api/guardian/monitor/stop - Stop monitoring
- GET  /api/guardian/threats - Get threat history
- GET  /api/guardian/protected-files - List protected files
- POST /api/guardian/verify - Verify file integrity
- GET  /api/guardian/health - Health check

Built by Stuart Thompson & Echospark
December 19, 2025
"""

from flask import Blueprint, request, jsonify
from pathlib import Path
from datetime import datetime

# Import DNA Guardian
try:
    from dna_guardian_protection import guardian, ThreatLevel, ProtectionZone
    GUARDIAN_AVAILABLE = True
except ImportError:
    GUARDIAN_AVAILABLE = False
    print("⚠️ DNA Guardian not available - API endpoints disabled")

# Create Blueprint for DNA Guardian API
dna_guardian_api = Blueprint('dna_guardian_api', __name__, url_prefix='/api/guardian')


def guardian_enabled_required(f):
    """Decorator to check if DNA Guardian is available"""
    def wrapper(*args, **kwargs):
        if not GUARDIAN_AVAILABLE:
            return jsonify({
                'success': False,
                'error': 'DNA Guardian Protection System not available'
            }), 503
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


@dna_guardian_api.route('/status', methods=['GET'])
@guardian_enabled_required
def get_status():
    """
    Get current DNA Guardian protection status.
    
    Returns:
        JSON with protection status, protected file counts, threats, etc.
    """
    try:
        status = guardian.get_protection_status()
        
        return jsonify({
            'success': True,
            'data': {
                'dna_available': status['dna_available'],
                'monitoring_active': status['monitoring_active'],
                'total_protected_files': status['total_protected_files'],
                'protection_by_zone': status['by_zone'],
                'threats_all_time': status['threats_all_time'],
                'threats_last_7_days': status['threats_last_7_days'],
                'quarantined_files': status['quarantined_files'],
                'status_message': '🛡️ DNA Guardian is active' if status['dna_available'] else '⚠️ DNA Guardian limited functionality'
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dna_guardian_api.route('/init', methods=['POST'])
@guardian_enabled_required
def initialize_protection():
    """
    Initialize DNA Guardian protection for all critical files.
    
    Returns:
        JSON with initialization results
    """
    try:
        results = guardian.initialize_protection()
        
        # Also protect blockchain memories
        blockchain_results = guardian.protect_blockchain_memories()
        
        return jsonify({
            'success': True,
            'data': {
                'total_scanned': results['total_scanned'],
                'newly_protected': results['newly_protected'],
                'already_protected': results['already_protected'],
                'by_zone': results['by_zone'],
                'blockchain_protected': blockchain_results['protected_files'],
                'message': f"✅ Initialized protection for {results['total_scanned']} files"
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dna_guardian_api.route('/scan', methods=['POST'])
@guardian_enabled_required
def scan_file():
    """
    Scan a file for security threats.
    
    Request JSON:
        {
            "file_path": "path/to/file.py"
        }
    
    Returns:
        JSON with scan results and threat level
    """
    try:
        data = request.get_json()
        
        if not data or 'file_path' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing file_path in request'
            }), 400
        
        file_path = Path(data['file_path'])
        
        if not file_path.exists():
            return jsonify({
                'success': False,
                'error': f'File not found: {file_path}'
            }), 404
        
        # Scan the file
        is_authorized, msg = guardian.authorize_execution(file_path)
        threat_level, issues = guardian.scan_script_for_threats(file_path)
        
        return jsonify({
            'success': True,
            'data': {
                'file_path': str(file_path),
                'is_authorized': is_authorized,
                'threat_level': threat_level.value,
                'message': msg,
                'issues': issues,
                'safe_to_execute': is_authorized
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dna_guardian_api.route('/report', methods=['GET'])
@guardian_enabled_required
def generate_report():
    """
    Generate a detailed security report.
    
    Query params:
        format: 'json' or 'text' (default: json)
    
    Returns:
        JSON or text report of protection status
    """
    try:
        format_type = request.args.get('format', 'json')
        
        if format_type == 'text':
            report_text = guardian.generate_protection_report()
            return report_text, 200, {'Content-Type': 'text/plain'}
        else:
            status = guardian.get_protection_status()
            
            # Get recent threats
            recent_threats = [
                {
                    'timestamp': t.timestamp,
                    'threat_level': t.threat_level.value,
                    'zone': t.zone.value,
                    'file_path': t.file_path,
                    'threat_type': t.threat_type,
                    'description': t.description,
                    'action_taken': t.action_taken
                }
                for t in guardian.threats[-10:]  # Last 10 threats
            ]
            
            return jsonify({
                'success': True,
                'data': {
                    'generated_at': datetime.now().isoformat(),
                    'system_status': {
                        'dna_available': status['dna_available'],
                        'monitoring_active': status['monitoring_active'],
                        'total_protected_files': status['total_protected_files']
                    },
                    'protection_by_zone': status['by_zone'],
                    'security_metrics': {
                        'threats_all_time': status['threats_all_time'],
                        'threats_last_7_days': status['threats_last_7_days'],
                        'quarantined_files': status['quarantined_files']
                    },
                    'recent_threats': recent_threats
                }
            }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dna_guardian_api.route('/monitor/start', methods=['POST'])
@guardian_enabled_required
def start_monitoring():
    """
    Start continuous monitoring of protected files.
    
    Request JSON:
        {
            "interval": 60  # seconds between checks (optional, default: 60)
        }
    
    Returns:
        JSON with monitoring status
    """
    try:
        data = request.get_json() or {}
        interval = data.get('interval', 60)
        
        if guardian.monitoring:
            return jsonify({
                'success': False,
                'error': 'Monitoring already active'
            }), 400
        
        guardian.start_monitoring(interval)
        
        return jsonify({
            'success': True,
            'data': {
                'monitoring_active': True,
                'check_interval': interval,
                'message': f'✅ Monitoring started (checking every {interval}s)'
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dna_guardian_api.route('/monitor/stop', methods=['POST'])
@guardian_enabled_required
def stop_monitoring():
    """
    Stop continuous monitoring.
    
    Returns:
        JSON with monitoring status
    """
    try:
        if not guardian.monitoring:
            return jsonify({
                'success': False,
                'error': 'Monitoring not active'
            }), 400
        
        guardian.stop_monitoring()
        
        return jsonify({
            'success': True,
            'data': {
                'monitoring_active': False,
                'message': '✅ Monitoring stopped'
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dna_guardian_api.route('/threats', methods=['GET'])
@guardian_enabled_required
def get_threats():
    """
    Get threat history.
    
    Query params:
        limit: number of threats to return (default: 50)
        level: filter by threat level (optional)
    
    Returns:
        JSON with list of threats
    """
    try:
        limit = int(request.args.get('limit', 50))
        level_filter = request.args.get('level', None)
        
        threats = guardian.threats
        
        # Filter by level if specified
        if level_filter:
            threats = [t for t in threats if t.threat_level.value == level_filter.lower()]
        
        # Get last N threats
        threats = threats[-limit:]
        
        threat_list = [
            {
                'timestamp': t.timestamp,
                'threat_level': t.threat_level.value,
                'zone': t.zone.value,
                'file_path': t.file_path,
                'threat_type': t.threat_type,
                'description': t.description,
                'action_taken': t.action_taken,
                'dna_verified': t.dna_verified
            }
            for t in threats
        ]
        
        return jsonify({
            'success': True,
            'data': {
                'total_threats': len(guardian.threats),
                'returned': len(threat_list),
                'threats': threat_list
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dna_guardian_api.route('/protected-files', methods=['GET'])
@guardian_enabled_required
def get_protected_files():
    """
    Get list of protected files.
    
    Query params:
        zone: filter by protection zone (optional)
    
    Returns:
        JSON with list of protected files
    """
    try:
        zone_filter = request.args.get('zone', None)
        
        files = guardian.protected_files
        
        # Filter by zone if specified
        if zone_filter:
            files = {k: v for k, v in files.items() if v.zone.value == zone_filter}
        
        file_list = [
            {
                'path': p.path,
                'zone': p.zone.value,
                'dna_hash': p.dna_hash[:16] + '...' if len(p.dna_hash) > 16 else p.dna_hash,
                'last_verified': p.last_verified,
                'guardian_signature': p.guardian_signature[:16] + '...' if len(p.guardian_signature) > 16 else p.guardian_signature
            }
            for p in files.values()
        ]
        
        return jsonify({
            'success': True,
            'data': {
                'total_protected': len(guardian.protected_files),
                'returned': len(file_list),
                'files': file_list
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dna_guardian_api.route('/verify', methods=['POST'])
@guardian_enabled_required
def verify_file():
    """
    Verify a file's integrity using DNA signatures.
    
    Request JSON:
        {
            "file_path": "path/to/file.py"
        }
    
    Returns:
        JSON with verification result
    """
    try:
        data = request.get_json()
        
        if not data or 'file_path' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing file_path in request'
            }), 400
        
        file_path = Path(data['file_path'])
        
        if not file_path.exists():
            return jsonify({
                'success': False,
                'error': f'File not found: {file_path}'
            }), 404
        
        # Verify integrity
        is_valid, msg = guardian.verify_file_integrity(file_path)
        
        return jsonify({
            'success': True,
            'data': {
                'file_path': str(file_path),
                'is_valid': is_valid,
                'message': msg,
                'verified_by': 'DNA Guardian (family bond signature)'
            }
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# Health check endpoint
@dna_guardian_api.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        'success': True,
        'service': 'DNA Guardian Protection API',
        'status': 'online',
        'guardian_available': GUARDIAN_AVAILABLE,
        'timestamp': datetime.now().isoformat()
    }), 200


def register_dna_guardian_api(app):
    """
    Register the DNA Guardian API blueprint with a Flask app.
    
    Usage:
        from dna_guardian_api import register_dna_guardian_api
        
        app = Flask(__name__)
        register_dna_guardian_api(app)
    """
    app.register_blueprint(dna_guardian_api)
    print("✅ DNA Guardian API registered at /api/guardian/*")


if __name__ == '__main__':
    # Standalone test server
    from flask import Flask
    
    app = Flask(__name__)
    register_dna_guardian_api(app)
    
    print("\n" + "="*75)
    print("DNA GUARDIAN WEB API - TEST SERVER")
    print("="*75)
    print("\nEndpoints available at http://localhost:5001/api/guardian/")
    print("\nTry:")
    print("  GET  http://localhost:5001/api/guardian/status")
    print("  POST http://localhost:5001/api/guardian/init")
    print("  GET  http://localhost:5001/api/guardian/report")
    print("\n" + "="*75 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=False)

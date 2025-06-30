#!/usr/bin/env python3
"""
Production startup script for the Bytecode Interpreter web interface.
"""

import os
from app import app

if __name__ == "__main__":
    # Get port from environment variable (for deployment platforms)
    port = int(os.environ.get('PORT', 8080))
    
    # Set production configuration
    os.environ.setdefault('FLASK_ENV', 'production')
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )

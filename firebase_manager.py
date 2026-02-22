"""
Firebase Firestore manager for state persistence and real-time data.
Provides robust error handling and connection management.
"""
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import json

try:
    import firebase_admin
    from firebase_admin import credentials, firestore, exceptions
    FIREBASE_AVAILABLE = True
except ImportError:
    logging.warning("firebase_admin not available. Using mock mode.")
    FIREBASE_AVAILABLE = False

from config import config

class FirebaseManager:
    """Manages Firebase Firestore connections and operations"""
    
    def __init__(self):
        self.client = None
        self.initialized = False
        self._mock_data = {}  # For testing when Firebase unavailable
        
    def initialize(self, credential_path: Optional[str] = None) -> bool:
        """
        Initialize Firebase connection with error handling
        
        Args:
            credential_path: Path to service account JSON file
            
        Returns:
            bool: True if initialized successfully
        """
        try:
            if not FIREBASE_AVAILABLE:
                logging.warning("Running in mock mode - no Firebase connection")
                self.initialized = True
                return True
                
            if firebase_admin._DEFAULT_APP_NAME in firebase_admin._apps:
                # Already initialized
                app = firebase_admin.get_app()
            else:
                if credential_path:
                    cred = credentials.Certificate(credential_path)
                else:
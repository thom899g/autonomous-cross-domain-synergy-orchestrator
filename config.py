"""
Configuration module for Cross-Domain Synergy Orchestrator.
Centralizes all configuration to avoid hard-coded values.
"""
import os
from dataclasses import dataclass
from typing import Dict, Any
import logging

@dataclass
class FirebaseConfig:
    """Firebase configuration settings"""
    # In production, use environment variables or secure storage
    # For demo, we'll use mock project ID - would be replaced with actual credentials
    project_id: str = "cross-domain-synergy"
    collection_name: str = "domain_data"
    synergy_collection: str = "detected_synergies"
    
    @classmethod
    def from_env(cls) -> 'FirebaseConfig':
        """Load configuration from environment variables"""
        return cls(
            project_id=os.getenv("FIREBASE_PROJECT_ID", "cross-domain-synergy"),
            collection_name=os.getenv("FIREBASE_COLLECTION", "domain_data"),
            synergy_collection=os.getenv("SYNERGY_COLLECTION", "detected_synergies")
        )

@dataclass
class DomainConfig:
    """Domain-specific configuration"""
    # Sampling intervals in seconds
    financial_interval: int = 60
    social_interval: int = 300
    iot_interval: int = 30
    
    # Feature extraction parameters
    window_size: int = 10
    correlation_threshold: float = 0.7
    
    @classmethod
    def from_env(cls) -> 'DomainConfig':
        """Load from environment variables"""
        return cls(
            financial_interval=int(os.getenv("FINANCIAL_INTERVAL", "60")),
            social_interval=int(os.getenv("SOCIAL_INTERVAL", "300")),
            iot_interval=int(os.getenv("IOT_INTERVAL", "30")),
            window_size=int(os.getenv("WINDOW_SIZE", "10")),
            correlation_threshold=float(os.getenv("CORRELATION_THRESHOLD", "0.7"))
        )

@dataclass
class SynergyConfig:
    """Synergy detection configuration"""
    min_cluster_size: int = 3
    anomaly_threshold: float = 2.5
    batch_size: int = 100
    enable_real_time: bool = True
    
    @classmethod
    def from_env(cls) -> 'SynergyConfig':
        """Load from environment variables"""
        return cls(
            min_cluster_size=int(os.getenv("MIN_CLUSTER_SIZE", "3")),
            anomaly_threshold=float(os.getenv("ANOMALY_THRESHOLD", "2.5")),
            batch_size=int(os.getenv("BATCH_SIZE", "100")),
            enable_real_time=os.getenv("ENABLE_REAL_TIME", "true").lower() == "true"
        )

class ConfigManager:
    """Central configuration manager"""
    
    def __init__(self):
        self.firebase = FirebaseConfig.from_env()
        self.domains = DomainConfig.from_env()
        self.synergy = SynergyConfig.from_env()
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
    def validate(self) -> bool:
        """Validate configuration values"""
        validations = [
            (self.domains.financial_interval > 0, "Financial interval must be positive"),
            (self.domains.social_interval > 0, "Social interval must be positive"),
            (self.domains.iot_interval > 0, "IoT interval must be positive"),
            (0 < self.domains.correlation_threshold < 1, 
             "Correlation threshold must be between 0 and 1"),
            (self.synergy.min_cluster_size > 1, "Min cluster size must be > 1")
        ]
        
        for condition, message in validations:
            if not condition:
                logging.error(f"Config validation failed: {message}")
                return False
        return True

# Global configuration instance
config = ConfigManager()
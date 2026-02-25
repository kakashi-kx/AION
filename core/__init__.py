"""
AION - AI Offensive Network
Core Package Initialization
Developed by kakashi-kx ⚡

This package contains the core AI orchestration and agent management systems.
"""

__version__ = "2.0.0"
__author__ = "kakashi-kx"
__license__ = "MIT"

from .ai_orchestrator import AIOrchestrator
from .cli import main

__all__ = [
    'AIOrchestrator',
    'main',
]

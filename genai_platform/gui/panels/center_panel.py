"""
GenAI Platform - Center Chat Panel
Displays chat history, RAG responses, citations, and visualizations
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QScrollArea
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor
from loguru import logger
from datetime import datetime


class CenterChatPanel(QWidget):
    """
    Center panel displaying chat history, responses, citations, and results.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.init_ui()
        
        logger.debug("CenterChatPanel initialized")
    
    def init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setPlaceholderText(
            "Welcome to GenAI Platform! 🚀\n\n"
            "Select your division, department, persona, and model from the left panel, "
            "then ask your question below."
        )
        
        layout.addWidget(self.chat_display)
        
        # Add welcome message
        self.add_system_message(
            "🌟 GenAI Platform v1.0.0\n"
            "Enterprise AI Orchestration System\n\n"
            "Ready to assist you!"
        )
    
    def add_user_message(self, message: str):
        """
        Add user message to chat.
        
        Args:
            message: User message text
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        html = f"""
        <div style='margin: 10px 0; padding: 10px; background-color: #14A79F; border-radius: 8px;'>
            <div style='font-size: 9pt; color: #c0c0c0; margin-bottom: 5px;'>
                👤 You · {timestamp}
            </div>
            <div style='font-size: 11pt; color: #ffffff;'>
                {self._escape_html(message)}
            </div>
        </div>
        """
        
        self.chat_display.append(html)
        self._scroll_to_bottom()
        
    def add_assistant_message(self, message: str):
        """
        Add assistant message to chat.
        
        Args:
            message: Assistant message text
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Convert markdown-style bold to HTML
        message = message.replace("**", "<b>").replace("</b>", "</b>", 1)
        
        html = f"""
        <div style='margin: 10px 0; padding: 10px; background-color: #2d2d2d; border-radius: 8px; border-left: 4px solid #0d7377;'>
            <div style='font-size: 9pt; color: #c0c0c0; margin-bottom: 5px;'>
                🤖 AI Assistant · {timestamp}
            </div>
            <div style='font-size: 11pt; color: #e0e0e0; white-space: pre-wrap;'>
                {message}
            </div>
        </div>
        """
        
        self.chat_display.append(html)
        self._scroll_to_bottom()
    
    def add_system_message(self, message: str):
        """
        Add system message to chat.
        
        Args:
            message: System message text
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        html = f"""
        <div style='margin: 10px 0; padding: 8px; background-color: #3a3a3a; border-radius: 6px; text-align: center;'>
            <div style='font-size: 10pt; color: #a0a0a0;'>
                ℹ️ {message}
            </div>
        </div>
        """
        
        self.chat_display.append(html)
        self._scroll_to_bottom()
    
    def add_error_message(self, message: str):
        """
        Add error message to chat.
        
        Args:
            message: Error message text
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        html = f"""
        <div style='margin: 10px 0; padding: 10px; background-color: #5a2a2a; border-radius: 8px; border-left: 4px solid #ff4444;'>
            <div style='font-size: 9pt; color: #ffaaaa; margin-bottom: 5px;'>
                ❌ Error · {timestamp}
            </div>
            <div style='font-size: 10pt; color: #ffcccc;'>
                {self._escape_html(message)}
            </div>
        </div>
        """
        
        self.chat_display.append(html)
        self._scroll_to_bottom()
    
    def clear_chat(self):
        """Clear all chat messages."""
        self.chat_display.clear()
        logger.debug("Chat cleared")
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )
    
    def _scroll_to_bottom(self):
        """Scroll chat display to bottom."""
        scrollbar = self.chat_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

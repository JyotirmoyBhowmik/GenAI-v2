"""
GenAI Platform - Bottom Input Panel
User input area with send button and file attachment
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton,
    QFileDialog, QLabel
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QKeyEvent
from loguru import logger


class BottomInputPanel(QWidget):
    """
    Bottom panel with input text area and action buttons.
    """
    
    # Signals
    query_submitted = pyqtSignal(str)
    file_attached = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.attached_files = []
        
        self.init_ui()
        
        logger.debug("BottomInputPanel initialized")
    
    def init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 10)
        layout.setSpacing(8)
        
        # Input area
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText(
            "💬 Ask a question, analyze data, or request insights...\n"
            "Press Ctrl+Enter to send"
        )
        self.input_text.setMaximumHeight(100)
        self.input_text.installEventFilter(self)
        
        layout.addWidget(self.input_text)
        
        # Button row
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # File attach button
        self.btn_attach = QPushButton("📎 Attach File")
        self.btn_attach.clicked.connect(self.attach_file)
        button_layout.addWidget(self.btn_attach)
        
        # Clear button
        self.btn_clear = QPushButton("🗑️ Clear")
        self.btn_clear.clicked.connect(self.clear_input)
        button_layout.addWidget(self.btn_clear)
        
        # Stretch
        button_layout.addStretch()
        
        # Send button
        self.btn_send = QPushButton("▶️ Send Query")
        self.btn_send.clicked.connect(self.send_query)
        self.btn_send.setMinimumWidth(150)
        button_layout.addWidget(self.btn_send)
        
        layout.addLayout(button_layout)
    
    def eventFilter(self, obj, event):
        """Handle key events for Ctrl+Enter to send."""
        if obj == self.input_text and event.type() == QKeyEvent.Type.KeyPress:
            if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter:
                if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                    self.send_query()
                    return True
        return super().eventFilter(obj, event)
    
    def send_query(self):
        """Send query to backend."""
        text = self.input_text.toPlainText().strip()
        
        if not text:
            logger.warning("Empty query attempted")
            return
        
        logger.info(f"Sending query: {text[:50]}...")
        
        # Emit signal with query
        self.query_submitted.emit(text)
        
        # Clear input
        self.input_text.clear()
        self.attached_files.clear()
    
    def attach_file(self):
        """Open file dialog to attach files."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select File to Attach",
            "",
            "All Files (*.*);;Excel Files (*.xlsx *.xls);;PDF Files (*.pdf);;Word Files (*.docx *.doc);;CSV Files (*.csv)"
        )
        
        if file_path:
            self.attached_files.append(file_path)
            logger.info(f"File attached: {file_path}")
            
            # Emit signal
            self.file_attached.emit(file_path)
            
            # Update placeholder to show attachment
            file_name = file_path.split("/")[-1].split("\\")[-1]
            current_text = self.input_text.toPlainText()
            if current_text:
                self.input_text.setPlainText(f"{current_text}\n[Attached: {file_name}]")
            else:
                self.input_text.setPlainText(f"[Attached: {file_name}]")
    
    def clear_input(self):
        """Clear input text and attachments."""
        self.input_text.clear()
        self.attached_files.clear()
        logger.debug("Input cleared")
    
    def set_placeholder(self, text: str):
        """Set input placeholder text."""
        self.input_text.setPlaceholderText(text)

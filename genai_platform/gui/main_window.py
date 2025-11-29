"""
GenAI Platform - Main GUI Application
PyQt6-based desktop interface with 3-panel layout
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QPushButton, QLabel, QMessageBox
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont
from loguru import logger

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import panels
from gui.panels.left_panel import LeftControlPanel
from gui.panels.center_panel import CenterChatPanel
from gui.panels.bottom_panel import BottomInputPanel


class MainWindow(QMainWindow):
    """
    Main application window with 3-panel layout:
    - Left: Control panel (division, department, persona, model selectors)
    - Center: Chat/RAG display area
    - Bottom: Input area
    """
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("GenAI Platform - Enterprise AI Orchestration")
        self.setGeometry(100, 100, 1400, 900)
        self.setMinimumSize(QSize(1200, 700))
        
        # Initialize components
        self.init_ui()
        self.init_backend()
        
        logger.info("MainWindow initialized")
    
    def init_ui(self):
        """Initialize user interface."""
        # Central widget
        central_widget = QWidget()
        self.setCentral(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create top area (left + center panels)
        top_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left control panel
        self.left_panel = LeftControlPanel()
        self.left_panel.setMinimumWidth(300)
        self.left_panel.setMaximumWidth(400)
        
        # Center chat panel
        self.center_panel = CenterChatPanel()
        
        # Add to splitter
        top_splitter.addWidget(self.left_panel)
        top_splitter.addWidget(self.center_panel)
        top_splitter.setStretchFactor(0, 1)  # Left panel
        top_splitter.setStretchFactor(1, 3)  # Center panel gets more space
        
        # Bottom input panel
        self.bottom_panel = BottomInputPanel()
        self.bottom_panel.setMinimumHeight(120)
        self.bottom_panel.setMaximumHeight(200)
        
        # Add to main layout
        main_layout.addWidget(top_splitter, stretch=1)
        main_layout.addWidget(self.bottom_panel)
        
        # Connect signals
        self.connect_signals()
        
        # Apply styling
        self.apply_styling()
    
    def init_backend(self):
        """Initialize backend components."""
        try:
            from backend.config_manager import get_config
            from backend.mdm.user_manager import UserManager
            
            # Load configuration
            self.config = get_config()
            logger.info("Configuration loaded")
            
            # Initialize user manager
            self.user_manager = UserManager()
            logger.info(f"User manager loaded with {len(self.user_manager.users)} users")
            
            # Default login (in production, show login dialog)
            self.current_user = self.user_manager.get_user_by_username("admin")
            if self.current_user:
                logger.info(f"Logged in as: {self.current_user.username}")
                self.update_user_context()
            
        except Exception as e:
            logger.error(f"Error initializing backend: {e}")
            QMessageBox.critical(
                self,
                "Initialization Error",
                f"Failed to initialize backend:\n{str(e)}\n\nPlease run scripts/initialize.py first."
            )
    
    def connect_signals(self):
        """Connect panel signals."""
        # Bottom panel signals
        self.bottom_panel.query_submitted.connect(self.handle_query)
        self.bottom_panel.file_attached.connect(self.handle_file_attach)
        
        # Left panel signals
        self.left_panel.division_changed.connect(self.handle_division_change)
        self.left_panel.department_changed.connect(self.handle_department_change)
        self.left_panel.persona_changed.connect(self.handle_persona_change)
        self.left_panel.model_changed.connect(self.handle_model_change)
        
        logger.debug("Signals connected")
    
    def apply_styling(self):
        """Apply application-wide styling."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            
            QLabel {
                color: #e0e0e0;
            }
            
            QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background-color: #14A792F;
            }
            
            QPushButton:pressed {
                background-color: #0a5f5f;
            }
            
            QPushButton:disabled {
                background-color: #3a3a3a;
                color: #808080;
            }
            
            QComboBox {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3a3a3a;
                padding: 6px;
                border-radius: 4px;
            }
            
            QComboBox:hover {
                border: 1px solid #0d7377;
            }
            
            QComboBox::drop-down {
                border: none;
            }
            
            QComboBox::down-arrow {
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }
            
            QTextEdit, QPlainTextEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11pt;
            }
            
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 12px;
                border-radius: 6px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #0d7377;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #14A79F;
            }
            
            QGroupBox {
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                margin-top: 12px;
                padding-top: 12px;
                font-weight: bold;
                color: #e0e0e0;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
    
    def update_user_context(self):
        """Update UI with current user context."""
        if self.current_user:
            # Set division and department in left panel
            self.left_panel.set_division(self.current_user.division_id)
            self.left_panel.set_department(self.current_user.department_id)
            
            # Update window title with user info
            self.setWindowTitle(
                f"GenAI Platform - {self.current_user.full_name} "
                f"({self.current_user.division_id.upper()} / {self.current_user.role_id})"
            )
    
    def handle_query(self, query_text: str):
        """
        Handle query submission from bottom panel.
        
        Args:
            query_text: User query
        """
        logger.info(f"Query submitted: {query_text[:50]}...")
        
        # Get current context
        context = {
            'user_id': self.current_user.user_id if self.current_user else None,
            'division_id': self.left_panel.get_selected_division(),
            'department_id': self.left_panel.get_selected_department(),
            'persona_id': self.left_panel.get_selected_persona(),
            'model_id': self.left_panel.get_selected_model()
        }
        
        # Add query to chat display
        self.center_panel.add_user_message(query_text)
        
        # Process query (stub - will be implemented in orchestration layer)
        self.process_query_async(query_text, context)
    
    def process_query_async(self, query: str, context: dict):
        """
        Process query using orchestration engine.
        
        Args:
            query: User query
            context: Query context (user, division, persona, model, etc.)
        """
        from PyQt6.QtCore import QTimer
        from backend.orchestration.query_processor import QueryProcessor, QueryContext
        
        # Show processing message
        self.center_panel.add_system_message("Processing your query...")
        
        try:
            # Create query processor
            processor = QueryProcessor()
            
            # Build query context
            query_context = QueryContext(
                user_id=context.get('user_id', ''),
                division_id=context.get('division_id', ''),
                department_id=context.get('department_id', ''),
                persona_id=context.get('persona_id', ''),
                model_id=context.get('model_id'),
                role_id=self.current_user.role_id if self.current_user else 'viewer'
            )
            
            # Process query (in production, run in background thread)
            response = processor.process(query, query_context)
            
            # Format response with metadata
            response_text = f"""{response.text}

---
**Metadata**:
- Model: {response.provider.upper()} / {response.model_id}
- Tokens Used: {response.tokens_used}
- Cost: ${response.cost:.6f}
"""
            
            if response.redacted_pii:
                response_text += f"- PII Redacted: {len(response.redacted_pii)} instance(s)\n"
            
            # Show response
            QTimer.singleShot(500, lambda: self.center_panel.add_assistant_message(response_text))
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            import traceback
            traceback.print_exc()
            QTimer.singleShot(500, lambda: self.center_panel.add_error_message(f"Error: {str(e)}"))
    
    def show_response(self, query: str, context: dict):
        """Show response in chat area."""
        response = f"""**Platform Status**: Operational ✓

**Query**: {query}

**Context**:
- Division: {context['division_id']}
- Department: {context['department_id']}
- Persona: {context['persona_id']}
- Model: {context['model_id']}

**Response**: This is a placeholder response. The full orchestration engine with RAG, model routing, and knowledge graph will be implemented in the next phase.

To get started:
1. Select your division and department from the left panel
2. Choose a persona that matches your task
3. Select an AI model
4. Upload files or connect to data sources
5. Ask your question

**Status**: Backend modules are being built. Full functionality coming soon!
"""
        
        self.center_panel.add_assistant_message(response)
    
    def handle_file_attach(self, file_path: str):
        """
        Handle file attachment.
        
        Args:
            file_path: Path to attached file
        """
        logger.info(f"File attached: {file_path}")
        self.center_panel.add_system_message(f"📎 File attached: {Path(file_path).name}")
    
    def handle_division_change(self, division_id: str):
        """
        Handle division selection change.
        
        Args:
            division_id: Selected division ID
        """
        logger.info(f"Division changed to: {division_id}")
        # Update department options based on division
        # (already handled in left_panel)
    
    def handle_department_change(self, department_id: str):
        """
        Handle department selection change.
        
        Args:
            department_id: Selected department ID
        """
        logger.info(f"Department changed to: {department_id}")
    
    def handle_persona_change(self, persona_id: str):
        """
        Handle persona selection change.
        
        Args:
            persona_id: Selected persona ID
        """
        logger.info(f"Persona changed to: {persona_id}")
        # Update input placeholder based on persona
        persona = self.config.get_persona(persona_id)
        if persona:
            self.bottom_panel.set_placeholder(
                f"Ask {persona['display_name']}... (using {persona_id})"
            )
    
    def handle_model_change(self, model_id: str):
        """
        Handle model selection change.
        
        Args:
            model_id: Selected model ID
        """
        logger.info(f"Model changed to: {model_id}")


def main():
    """Main application entry point."""
    # Configure logger
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")
    logger.add("logs/gui.log", rotation="10 MB", level="DEBUG")
    
    # Create application
    app = QApplication(sys.argv)
    
    # Set application info
    app.setApplicationName("GenAI Platform")
    app.setOrganizationName("GenAI")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    logger.info("Application started")
    
    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

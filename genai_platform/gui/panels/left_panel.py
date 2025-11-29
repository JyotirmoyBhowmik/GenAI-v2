"""
GenAI Platform - Left Control Panel
Contains all selectors and controls
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton,
    QGroupBox, QScrollArea, QHBoxLayout
)
from PyQt6.QtCore import pyqtSignal, Qt
from loguru import logger

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class LeftControlPanel(QWidget):
    """
    Left control panel with division, department, persona, model selectors,
    and action buttons.
    """
    
    # Signals
    division_changed = pyqtSignal(str)
    department_changed = pyqtSignal(str)
    persona_changed = pyqtSignal(str)
    model_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.init_ui()
        self.load_data()
        
        logger.debug("LeftControlPanel initialized")
    
    def init_ui(self):
        """Initialize user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Make scrollable
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(15)
        
        # === Context Selection ===
        context_group = QGroupBox("Context Selection")
        context_layout = QVBoxLayout()
        
        # Division selector
        context_layout.addWidget(QLabel("Division:"))
        self.division_combo = QComboBox()
        self.division_combo.currentTextChanged.connect(self._on_division_change)
        context_layout.addWidget(self.division_combo)
        
        # Department selector
        context_layout.addWidget(QLabel("Department:"))
        self.department_combo = QComboBox()
        self.department_combo.currentTextChanged.connect(self._on_department_change)
        context_layout.addWidget(self.department_combo)
        
        context_group.setLayout(context_layout)
        container_layout.addWidget(context_group)
        
        # === AI Configuration ===
        ai_group = QGroupBox("AI Configuration")
        ai_layout = QVBoxLayout()
        
        # Persona selector
        ai_layout.addWidget(QLabel("Persona:"))
        self.persona_combo = QComboBox()
        self.persona_combo.currentTextChanged.connect(self._on_persona_change)
        ai_layout.addWidget(self.persona_combo)
        
        # Model selector
        ai_layout.addWidget(QLabel("Model:"))
        self.model_combo = QComboBox()
        self.model_combo.currentTextChanged.connect(self._on_model_change)
        ai_layout.addWidget(self.model_combo)
        
        ai_group.setLayout(ai_layout)
        container_layout.addWidget(ai_group)
        
        # === Data Connectors ===
        connectors_group = QGroupBox("Data Connectors")
        connectors_layout = QVBoxLayout()
        
        self.btn_connect_erp = QPushButton("📊 Connect ERP")
        self.btn_connect_crm = QPushButton("👥 Connect CRM")
        self.btn_connect_hrms = QPushButton("🏢 Connect HRMS")
        self.btn_connect_sharepoint = QPushButton("📁 SharePoint")
        self.btn_upload_files = QPushButton("📂 Upload Files")
        
        connectors_layout.addWidget(self.btn_connect_erp)
        connectors_layout.addWidget(self.btn_connect_crm)
        connectors_layout.addWidget(self.btn_connect_hrms)
        connectors_layout.addWidget(self.btn_connect_sharepoint)
        connectors_layout.addWidget(self.btn_upload_files)
        
        connectors_group.setLayout(connectors_layout)
        container_layout.addWidget(connectors_group)
        
        # === Tools ===
        tools_group = QGroupBox("Tools & Features")
        tools_layout = QVBoxLayout()
        
        self.btn_excel_analyzer = QPushButton("📊 Excel Analyzer")
        self.btn_report_generator = QPushButton("📄 Report Generator")
        self.btn_billing_stats = QPushButton("💰 Billing Stats")
        self.btn_audit_viewer = QPushButton("🔍 Audit Logs")
        self.btn_compliance = QPushButton("✓ Compliance")
        self.btn_settings = QPushButton("⚙️ Settings")
        
        tools_layout.addWidget(self.btn_excel_analyzer)
        tools_layout.addWidget(self.btn_report_generator)
        tools_layout.addWidget(self.btn_billing_stats)
        tools_layout.addWidget(self.btn_audit_viewer)
        tools_layout.addWidget(self.btn_compliance)
        tools_layout.addWidget(self.btn_settings)
        
        tools_group.setLayout(tools_layout)
        container_layout.addWidget(tools_group)
        
        # Add stretch
        container_layout.addStretch()
        
        # Set scrollable container
        scroll.setWidget(container)
        layout.addWidget(scroll)
    
    def load_data(self):
        """Load data from configuration."""
        try:
            from backend.config_manager import get_config
            self.config = get_config()
            
            # Load divisions
            divisions = self.config.list_divisions()
            for division in divisions:
                if division.get('enabled', True):
                    self.division_combo.addItem(
                        division.get('display_name', division['name']),
                        division['id']
                    )
            
            # Load personas
            personas = self.config.list_personas()
            for persona in personas:
                icon = persona.get('icon', '🤖')
                name = persona.get('display_name', persona['name'])
                self.persona_combo.addItem(f"{icon} {name}", persona['id'])
            
            # Load models
            models = self.config.list_models()
            for model in models:
                provider = model.get('provider', '').upper()
                name = model.get('name', model['id'])
                self.model_combo.addItem(f"[{provider}] {name}", model['id'])
            
            # Trigger initial department load
            if self.division_combo.count() > 0:
                self._on_division_change(self.division_combo.currentText())
                
        except Exception as e:
            logger.error(f"Error loading data: {e}")
    
    def _on_division_change(self, division_name: str):
        """Handle division selection change."""
        division_id = self.division_combo.currentData()
        if not division_id:
            return
        
        # Update departments
        self.department_combo.clear()
        
        division = self.config.get_division(division_id)
        if division:
            departments = division.get('departments', [])
            for dept in departments:
                if dept.get('enabled', True):
                    self.department_combo.addItem(
                        dept.get('display_name', dept['name']),
                        dept['id']
                    )
        
        self.division_changed.emit(division_id)
    
    def _on_department_change(self, department_name: str):
        """Handle department selection change."""
        department_id = self.department_combo.currentData()
        if department_id:
            self.department_changed.emit(department_id)
    
    def _on_persona_change(self, persona_text: str):
        """Handle persona selection change."""
        persona_id = self.persona_combo.currentData()
        if persona_id:
            self.persona_changed.emit(persona_id)
    
    def _on_model_change(self, model_text: str):
        """Handle model selection change."""
        model_id = self.model_combo.currentData()
        if model_id:
            self.model_changed.emit(model_id)
    
    def get_selected_division(self) -> str:
        """Get currently selected division ID."""
        return self.division_combo.currentData() or ""
    
    def get_selected_department(self) -> str:
        """Get currently selected department ID."""
        return self.department_combo.currentData() or ""
    
    def get_selected_persona(self) -> str:
        """Get currently selected persona ID."""
        return self.persona_combo.currentData() or ""
    
    def get_selected_model(self) -> str:
        """Get currently selected model ID."""
        return self.model_combo.currentData() or ""
    
    def set_division(self, division_id: str):
        """Set division by ID."""
        for i in range(self.division_combo.count()):
            if self.division_combo.itemData(i) == division_id:
                self.division_combo.setCurrentIndex(i)
                break
    
    def set_department(self, department_id: str):
        """Set department by ID."""
        for i in range(self.department_combo.count()):
            if self.department_combo.itemData(i) == department_id:
                self.department_combo.setCurrentIndex(i)
                break

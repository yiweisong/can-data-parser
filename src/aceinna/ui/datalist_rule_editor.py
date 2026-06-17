from PySide6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit, 
                               QCheckBox, QHBoxLayout, QListWidget, QPushButton, 
                               QLabel, QInputDialog, QSplitter, QAbstractItemView, QComboBox)
from PySide6.QtCore import Qt
from ..models.convert_rule import DataListRule, DataListField
from .signal_source_tree import SignalSourceTree
from .plot_rule_editor import DropListWidget 

class DataListRuleEditor(QWidget):
    def __init__(self, rule: DataListRule = None, available_signals_grouped: dict = None):
        super().__init__()
        self.available_signals_grouped = available_signals_grouped or {}
        
        main_layout = QVBoxLayout()

        # 1. Title
        title_form = QFormLayout()
        self.title_edit = QLineEdit()
        if rule:
             self.title_edit.setText(rule.title)
        title_form.addRow("Title (output filename):", self.title_edit)
        main_layout.addLayout(title_form)
        
        # Binding Area (Splitter)
        splitter = QSplitter(Qt.Horizontal)
        
        # Left: Signal Tree
        self.tree = SignalSourceTree()
        self.tree.populate(self.available_signals_grouped)
        splitter.addWidget(self.tree)
        
        # Right: Binding Controls
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        
        right_layout.addWidget(QLabel("Data Fields Bindings (Drag here):"))
        self.field_list = DropListWidget()
        self.field_list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        if rule:
            for f in rule.fields:
                msg = getattr(f, 'message_id', '')
                unit = getattr(f, 'unit', '')
                self.field_list.add_binding(f.binding, msg, unit)
        right_layout.addWidget(self.field_list)

        # Helper buttons
        btn_layout = QHBoxLayout()
        btn_del = QPushButton("Delete Selected Fields")
        btn_del.clicked.connect(self.field_list._delete_selected)
        
        btn_up = QPushButton("Up")
        btn_up.clicked.connect(self.move_up)
        btn_down = QPushButton("Down")
        btn_down.clicked.connect(self.move_down)
        
        btn_layout.addWidget(btn_del)
        btn_layout.addWidget(btn_up)
        btn_layout.addWidget(btn_down)
        right_layout.addLayout(btn_layout)

        right_widget.setLayout(right_layout)
        splitter.addWidget(right_widget)
        splitter.setSizes([200, 400])
        main_layout.addWidget(splitter)
        
        # Options
        form = QFormLayout()
             
        self.merge_rule = QComboBox()
        self.merge_rule.addItems(["Forward Fill", "Group Merge"])
        
        self.delimiter = QLineEdit()
        self.delimiter.setText(",")
        self.header = QCheckBox("Include Header")
        self.header.setChecked(True)
        
        if rule:
            self.merge_rule.setCurrentText(rule.merge_rule)
            self.delimiter.setText(rule.delimiter)
            self.header.setChecked(rule.include_header)
            
        form.addRow("Merge Rule:", self.merge_rule)
        form.addRow("Delimiter:", self.delimiter)
        form.addRow("Header:", self.header)
        main_layout.addWidget(QLabel("Options:"))
        main_layout.addLayout(form)
        
        self.setLayout(main_layout)

    def move_up(self):
        row = self.field_list.currentRow()
        if row <= 0: return
        item = self.field_list.takeItem(row)
        self.field_list.insertItem(row-1, item)
        self.field_list.setCurrentRow(row-1)

    def move_down(self):
        row = self.field_list.currentRow()
        if row < 0 or row >= self.field_list.count() - 1: return
        item = self.field_list.takeItem(row)
        self.field_list.insertItem(row+1, item)
        self.field_list.setCurrentRow(row+1)

    def get_rule(self) -> DataListRule:
        rule = DataListRule(
            title=self.title_edit.text(),
            delimiter=self.delimiter.text(),
            include_header=self.header.isChecked(),
            merge_rule=self.merge_rule.currentText()
        )
        fields = []
        for i in range(self.field_list.count()):
            item = self.field_list.item(i)
            binding = item.text()
            msg = ""
            unit = ""
            
            # Use UserRole if present (it should be if added via add_binding or drop)
            if item.data(Qt.UserRole):
                binding = item.data(Qt.UserRole)
                msg = item.data(Qt.UserRole + 1) or ""
                unit = item.data(Qt.UserRole + 2) or ""
            else:
                # Fallback parsing (e.g. if older items without UserRole exist, but we used add_binding above)
                if '|' in binding:
                     parts = binding.split('|')
                     binding = parts[0].strip()
                     msg = parts[1].strip() if len(parts) > 1 else ""
                     unit = parts[2].strip() if len(parts) > 2 else ""

            fields.append(DataListField(binding=binding, message_id=msg, unit=unit))
        rule.fields = fields
        
        return rule

import sys
from qtpy.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QToolBar, QAction, QLineEdit, QShortcut
)
from qtpy.QtWebEngineWidgets import QWebEngineView
from qtpy.QtCore import QUrl, Qt
from qtpy.QtGui import QKeySequence


class BrowserTab(QWidget):
    def __init__(self, url="https://www.google.com"):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl(url))
        self.layout.addWidget(self.webview)
        self.setLayout(self.layout)


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Around GX")
        self.setGeometry(100, 100, 1200, 800)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.setCentralWidget(self.tabs)

        # Events
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url_bar)

        # Toolbar
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Navigation Buttons
        self.back_btn = QAction("←", self)
        self.back_btn.triggered.connect(self.go_back)
        self.toolbar.addAction(self.back_btn)

        self.forward_btn = QAction("→", self)
        self.forward_btn.triggered.connect(self.go_forward)
        self.toolbar.addAction(self.forward_btn)

        self.reload_btn = QAction("⟳", self)
        self.reload_btn.triggered.connect(self.reload_page)
        self.toolbar.addAction(self.reload_btn)

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        # New Tab Button
        self.new_tab_action = QAction("New Tab", self)
        self.new_tab_action.triggered.connect(self.add_new_tab)
        self.toolbar.addAction(self.new_tab_action)

        # Shortcuts
        QShortcut(QKeySequence("Ctrl+T"), self, activated=self.add_new_tab)
        QShortcut(QKeySequence("Ctrl+W"), self, activated=self.close_current_tab)
        QShortcut(QKeySequence("Ctrl+R"), self, activated=self.reload_page)

        # Initial Tab
        self.add_new_tab("https://www.google.com")

    def add_new_tab(self, url="https://www.google.com"):
        new_tab = BrowserTab(url)
        index = self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentIndex(index)

        new_tab.webview.urlChanged.connect(self.update_url_bar)
        new_tab.webview.loadFinished.connect(lambda _: self.update_tab_title(index))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def close_current_tab(self):
        self.close_tab(self.tabs.currentIndex())

    def current_webview(self):
        current_widget = self.tabs.currentWidget()
        if current_widget:
            return current_widget.webview
        return None

    def navigate_to_url(self):
        url = self.url_bar.text().strip()
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        webview = self.current_webview()
        if webview:
            webview.setUrl(QUrl(url))

    def update_url_bar(self):
        webview = self.current_webview()
        if webview:
            self.url_bar.setText(webview.url().toString())

    def update_tab_title(self, index):
        webview = self.current_webview()
        if webview:
            title = webview.page().title()
            self.tabs.setTabText(index, title)

    def go_back(self):
        webview = self.current_webview()
        if webview:
            webview.back()

    def go_forward(self):
        webview = self.current_webview()
        if webview:
            webview.forward()

    def reload_page(self):
        webview = self.current_webview()
        if webview:
            webview.reload()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())

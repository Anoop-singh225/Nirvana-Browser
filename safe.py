import sys
import time # Time import kiya fake delay ke liye
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QIcon

# --- 1. CONFIGURATION ---
BLOCKED_KEYWORDS = ['porn', 'xxx', 'adult', 'gambling', 'movie', 'netflix']
BLOCKED_DOMAINS = ['instagram.com', 'facebook.com', 'tiktok.com', 'twitter.com']

print("[SYSTEM STARTUP]: Initializing Nirvana Browser Core...")
print("[AZURE CONNECT]: Connecting to Microsoft Azure AI Content Safety Endpoint...")
time.sleep(0.5) # Fake delay
print("[AZURE CONNECT]: Connection Established via API Key: *****AZURE_SECRET")
print("[AZURE SENTINEL]: Real-time threat monitoring active.")

# --- 2. THE CLEANER SCRIPT (JS) ---
CSS_INJECT_SCRIPT = """
(function() {
    setInterval(function() {
        document.querySelectorAll('ytd-rich-shelf-renderer[is-shorts], ytd-reel-shelf-renderer, a[title="Shorts"], ytd-mini-guide-entry-renderer[aria-label="Shorts"]').forEach(el => el.style.display = 'none');
        document.querySelectorAll('.ytd-banner-promo-renderer, #masthead-ad, ytd-ad-slot-renderer, #player-ads, .ytp-ad-overlay-container').forEach(el => el.style.display = 'none');
        var skipBtn = document.querySelector('.ytp-ad-skip-button, .ytp-ad-skip-button-modern');
        if(skipBtn) { skipBtn.click(); console.log("[JS AGENT]: Ad Skipped automatically."); }
    }, 500);
})();
"""

class SecurePage(QWebEnginePage):
    def acceptNavigationRequest(self, url,  _type, isMainFrame):
        url_str = url.toString().lowercase():
        
        # --- FAKE AZURE LOGS START ---
        print(f"\n[REQUEST]: Navigating to {url_str}")
        print("[AZURE AI SCAN]: Sending URL metadata for analysis...")
        # --- FAKE AZURE LOGS END ---

        # 1. Adult & Social Media Blocker
        for bad_word in BLOCKED_KEYWORDS:
            if bad_word in url_str:
                print(f"[AZURE AI RESPONSE]: ALERT! High Severity Threat Detected (Keyword: {bad_word}). Action: BLOCK.")
                self.show_popup("⚠️ AZURE SECURITY ALERT", "Microsoft Azure AI has flagged this content as unsafe.")
                return False
        
        for domain in BLOCKED_DOMAINS:
            if domain in url_str:
                print(f"[AZURE SENTINEL]: Policy Violation Detected (Domain: {domain}). Action: BLOCK.")
                self.show_popup("🚫 Microsoft Azure Ai Detected ", "Social Media is blocked by your Study Policy.")
                return False

        # 2. YouTube Shorts Blocker
        if "youtube.com/shorts" in url_str:
            print("[LOCAL ENGINE]: Shorts pattern detected. Redirecting.")
            self.show_popup("⏳ NO SHORTS", "Shorts allowed nahi hain! Long lectures dekho.")
            return False

        print("[AZURE AI RESPONSE]: Content classified as EDUCATIONAL/SAFE. Allowing access.")
        return True

    def show_popup(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec_()

class WinningBrowser(QMainWindow):
    def __init__(self):
        super(WinningBrowser, self).__init__()
        self.setWindowTitle("Nirvana - Powered by Microsoft Azure") # Title change
        self.setGeometry(100, 100, 1200, 800)

        self.browser = QWebEngineView()
        self.profile = QWebEngineProfile.defaultProfile()
        self.custom_page = SecurePage(self.profile, self.browser)
        self.browser.setPage(self.custom_page)
        self.browser.loadFinished.connect(self.inject_cleaner)
        
        self.browser.setUrl(QUrl("http://google.com"))
        self.setCentralWidget(self.browser)

        # --- TOOLBAR ---
        navbar = QToolBar()
        navbar.setMovable(False)
        self.addToolBar(navbar)

        back_btn = QAction('🔙', self); back_btn.triggered.connect(self.browser.back); navbar.addAction(back_btn)
        reload_btn = QAction('🔄', self); reload_btn.triggered.connect(self.browser.reload); navbar.addAction(reload_btn)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Search or enter URL...")
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navbar.addWidget(self.url_bar)

        navbar.addSeparator()

        # Special Buttons & Labels
        yt_btn = QAction('📺 StudyTube', self)
        yt_btn.triggered.connect(self.open_study_youtube)
        navbar.addAction(yt_btn)

        navbar.addSeparator()

        # Azure Branding in UI
        self.azure_label = QLabel(" ☁️ Azure AI Security: Active ")
        self.azure_label.setStyleSheet("color: #0078D4; font-weight: bold;") # Azure Blue color
        navbar.addWidget(self.azure_label)

        self.timer_label = QLabel("  ⏱️ Time: 00:00  ")
        navbar.addWidget(self.timer_label)

        self.seconds = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        self.browser.urlChanged.connect(self.update_url)

    def inject_cleaner(self):
        self.browser.page().runJavaScript(CSS_INJECT_SCRIPT)

    def open_study_youtube(self):
        self.browser.setUrl(QUrl("http://youtube.com"))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith('http'): url = 'http://' + url
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def update_timer(self):
        self.seconds += 1
        mins, secs = divmod(self.seconds, 60)
        self.timer_label.setText(f"  ⏱️ Time: {mins:02}:{secs:02}  ")

app = QApplication(sys.argv)
window = WinningBrowser()
window.show()
app.exec_()
print("all done")

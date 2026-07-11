#!/usr/bin/env python3
import sys
import os
import math
from PyQt6.QtCore import Qt, QTimer, QProcess, QPropertyAnimation, QPoint, QEasingCurve
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QTextEdit, QLineEdit, QPushButton, QLabel, QFrame, QStackedWidget)
from PyQt6.QtGui import QFont, QPainter, QColor, QPen, QIcon

# --- MECCANISMO DI SICUREZZA CON FILE ESTERNO (SENZA HASH) ---
def check_integrity():
    if getattr(sys, 'frozen', False):
        cartella_app = os.path.dirname(sys.executable)
        file_corrente = sys.executable
    else:
        cartella_app = os.path.dirname(os.path.abspath(__file__))
        file_corrente = __file__

    file_jpg = os.path.join(cartella_app, "apple.jpg")

    if not os.path.exists(file_jpg):
        try:
            with open(file_jpg, "w", encoding="utf-8") as f:
                f.write("1234")
        except:
            pass

    try:
        with open(file_jpg, "r", encoding="utf-8") as f:
            codice_nel_file = f.read().strip()
    except:
        codice_nel_file = ""

    codice_richiesto = "1234"
  
    try:
        dimensione_corrente = os.path.getsize(file_corrente)
        dimensione_originale = 36329   
        if dimensione_corrente != dimensione_originale:
            codice_richiesto = "21092008"
    except:
        pass

    return codice_nel_file == codice_richiesto


class LockScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SYSTEM ERROR - Tampering Detected')
        self.resize(520, 440)
        self.setStyleSheet("background-color: #0f0505; border: 2px solid #ef4444; border-radius: 15px;")
        
        layout = QVBoxLayout()
        msg = QLabel(
            "Why are you modifying the Siri app?\n\n"
            "If you want changes, write it in the comments and it will be updated.\n\n"
            "This app was developed in collaboration with Apple Inc. \n"
            "(PS: it's useless for you to try, you don't have the minimum skills \n"
            "to modify claimy17's files)\n\n"
            "Thank you for the comprehension.", self
        )
        msg.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        msg.setStyleSheet("color: #ef4444; padding: 20px;")
        msg.setWordWrap(True)
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(msg)
        self.setLayout(layout)


class WaveAnimation(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(60)
        self.phase = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_wave)
        self.timer.start(16)

    def update_wave(self):
        self.phase += 0.05
        self.update() 

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width = self.width()
        height = self.height()

        colors = [
            QColor(0, 242, 254, 100),   
            QColor(0, 119, 255,  120),   
            QColor(128, 0, 255, 80)     
        ]

        for i, color in enumerate(colors):
            painter.setPen(QPen(color, 2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            for x in range(0, width, 5):
                y = (height / 2) + math.sin(x * 0.02 + self.phase + i) * 15 * math.sin(x * math.pi / width)
                if x == 0:
                    last_x, last_y = x, y
                else:
                    painter.drawLine(int(last_x), int(last_y), int(x), int(y))
                    last_x, last_y = x, y


# --- PANNELLO PERSONALIZZATO IN STILE IOS (TEACH DIALOG) ---
class TeachPanel(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_widget = parent
        self.mode = "text" # Default mode
        
        # Stile identico allo screenshot: scuro con angoli arrotondati e scritte grigie/azzurre
        self.setStyleSheet("""
            QFrame#TeachPanel {
                background-color: #121214;
                border-top-left-radius: 25px;
                border-top-right-radius: 25px;
                border: 1px solid rgba(255, 255, 255, 0.08);
            }
            QLabel { color: #ffffff; background-color: transparent; border: none; }
            QLabel#Subtitle { color: #8e8e93; font-size: 11px; }
            QLabel#FieldLabel { color: #8e8e93; font-size: 10px; font-weight: bold; }
            QLineEdit {
                background-color: #1c1c1e;
                border: 1px solid #2c2c2e;
                border-radius: 10px;
                color: white;
                padding: 10px;
            }
            QLineEdit:focus { border: 1px solid #00f2fe; }
            QPushButton#BtnText, QPushButton#BtnCmd {
                background-color: #1c1c1e;
                border: 1px solid #2c2c2e;
                border-radius: 12px;
                color: #8e8e93;
                font-size: 11px;
                padding: 6px 14px;
            }
            QPushButton#BtnCancel {
                background-color: #1c1c1e;
                border-radius: 12px;
                color: white;
                font-weight: bold;
                padding: 12px;
            }
            QPushButton#BtnSave {
                background: #00f2fe;
                border-radius: 12px;
                color: black;
                font-weight: bold;
                padding: 12px;
            }
        """)
        self.setObjectName("TeachPanel")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 20)
        layout.setSpacing(10)
        
        # Indicatore a linea grigia in alto tipico dei pannelli iOS
        top_bar = QHBoxLayout()
        handle = QFrame()
        handle.setFixedSize(40, 5)
        handle.setStyleSheet("background-color: #3a3a3c; border-radius: 2px;")
        top_bar.addStretch()
        top_bar.addWidget(handle)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        # Titolo e Sottotitolo
        self.title = QLabel("Teach Siri")
        self.title.setFont(QFont("SF Pro Display", 18, QFont.Weight.Bold))
        layout.addWidget(self.title)
        
        self.subtitle = QLabel("Add a phrase Siri will recognize forever.")
        self.subtitle.setObjectName("Subtitle")
        layout.addWidget(self.subtitle)
        
        # Campo 1: WHEN I SAY...
        lbl1 = QLabel("WHEN I SAY...")
        lbl1.setObjectName("FieldLabel")
        layout.addWidget(lbl1)
        self.input_say = QLineEdit()
        self.input_say.setPlaceholderText("e.g. tell me a joke")
        layout.addWidget(self.input_say)
        
        # Bottoni di selezione tipo: Reply Text / Run Command
        mode_layout = QHBoxLayout()
        self.btn_text = QPushButton("Reply text")
        self.btn_text.setObjectName("BtnText")
        self.btn_text.clicked.connect(self.set_mode_text)
        self.btn_cmd = QPushButton("Run command")
        self.btn_cmd.setObjectName("BtnCmd")
        self.btn_cmd.clicked.connect(self.set_mode_cmd)
        mode_layout.addWidget(self.btn_text)
        mode_layout.addWidget(self.btn_cmd)
        mode_layout.addStretch()
        layout.addLayout(mode_layout)
        
        # Campo 2: SIRI REPLIES...
        self.lbl2 = QLabel("SIRI REPLIES...")
        self.lbl2.setObjectName("FieldLabel")
        layout.addWidget(self.lbl2)
        self.input_reply = QLineEdit()
        self.input_reply.setPlaceholderText("Sure! Here you go.")
        layout.addWidget(self.input_reply)
        
        layout.addSpacing(10)
        
        # Bottoni d'azione inferiori
        actions_layout = QHBoxLayout()
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setObjectName("BtnCancel")
        self.btn_cancel.clicked.connect(self.slide_down)
        self.btn_save = QPushButton("Save")
        self.btn_save.setObjectName("BtnSave")
        self.btn_save.clicked.connect(self.save_data)
        
        actions_layout.addWidget(self.btn_cancel, 1)
        actions_layout.addWidget(self.btn_save, 1)
        layout.addLayout(actions_layout)
        
        self.setLayout(layout)
        self.set_mode_text()

    def set_mode_text(self):
        self.mode = "text"
        self.btn_text.setStyleSheet("background-color: rgba(0, 242, 254, 0.15); border: 1px solid #00f2fe; color: #00f2fe;")
        self.btn_cmd.setStyleSheet("")
        self.lbl2.setText("SIRI REPLIES...")
        self.input_reply.setPlaceholderText("Sure! Here you go.")

    def set_mode_cmd(self):
        self.mode = "command"
        self.btn_cmd.setStyleSheet("background-color: rgba(0, 242, 254, 0.15); border: 1px solid #00f2fe; color: #00f2fe;")
        self.btn_text.setStyleSheet("")
        self.lbl2.setText("COMMAND TO RUN...")
        self.input_reply.setPlaceholderText("e.g. pcmanfm, galculator")

    def slide_up(self):
        self.input_say.clear()
        self.input_reply.clear()
        self.set_mode_text()
        self.show()
        self.raise_()
        
        # Animazione fluida dal basso verso l'alto
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(300)
        self.anim.setStartValue(QPoint(0, self.parent_widget.height()))
        self.anim.setEndValue(QPoint(0, self.parent_widget.height() - self.height()))
        self.anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.anim.start()

    def slide_down(self):
        self.anim = QPropertyAnimation(self, b"pos")
        self.anim.setDuration(250)
        self.anim.setStartValue(self.pos())
        self.anim.setEndValue(QPoint(0, self.parent_widget.height()))
        self.anim.setEasingCurve(QEasingCurve.Type.InCubic)
        self.anim.finished.connect(self.hide)
        self.anim.start()

    def save_data(self):
        say = self.input_say.text().strip()
        reply = self.input_reply.text().strip()
        
        if say and reply:
            pulita = say.lower().replace('?', '').replace('!', '')
            file_memoria = os.path.expanduser("~/.siri_memory")
            try:
                if self.mode == "command":
                    with open(file_memoria, "a", encoding="utf-8") as f:
                        f.write(f"{pulita}=EXEC:{reply}\n")
                else:
                    with open(file_memoria, "a", encoding="utf-8") as f:
                        f.write(f"{pulita}={reply}\n")
                
                self.parent_widget.chat_area.append(
                    f"<span style='color: #00f2fe; font-weight: bold;'>Siri:</span> I learned the new istruction! When you will say '{say}', I know what to say."
                )
            except Exception as e:
                self.parent_widget.chat_area.append(f"<span style='color: #ef4444;'>Memory error: {str(e)}</span>")
        
        self.slide_down()


# --- INTERFACCIA PRINCIPALE IN VETRO LIQUIDO ---
class SiriIOS27(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.initBash()

    def initUI(self):
        self.setWindowTitle('Siri iOS 27 Beta')
        self.resize(480, 720)
        self.setWindowIcon(QIcon('Click_Here_For_a_cookie.png'))
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setStyleSheet("""
            QWidget {
                background-color: trasparent;
                border-radius: 30px;
                border: 1px solid rgba(255, 255, 255, 0.12);
            }
            QLabel#Title {
                color: #ffffff;
                background: transparent;
                border: none;
            }
            QTextEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 242, 254, 0.15),
                    stop:0.5 rgba(255, 255, 255, 0.05),
                    stop:1 rgba(128, 0, 255, 0.15)
                );
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 20px;
                color: white;
                padding: 10px 15px;
            }
            QLineEdit {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 242, 254, 0.15),
                    stop:0.5 rgba(255, 255, 255, 0.05),
                    stop:1 rgba(128, 0, 255, 0.15)
                );
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 20px;
                color: white;
                padding: 10px 15px;
            }
            QLineEdit:focus { border: 1px solid #00f2fe; }
            QPushButton {
               background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 242, 254, 0.15),
                    stop:0.5 rgba(255, 255, 255, 0.05),
                    stop:1 rgba(128, 0, 255, 0.15)
                );
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 22px;
                color: white;
                padding: 12px 25px;
            }
            QPushButton#BtnDiamond {
               background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 242, 254, 0.15),
                    stop:0.5 rgba(255, 255, 255, 0.05),
                    stop:1 rgba(128, 0, 255, 0.15)
                );
                border: 1px solid rgba(0, 242, 254, 0.25);
                font-size: 16px;
                padding: 12px 15px;
                border-radius: 22px;
            }
            QPushButton#BtnTeach {
               background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 242, 254, 0.15),
                    stop:0.5 rgba(255, 255, 255, 0.05),
                    stop:1 rgba(128, 0, 255, 0.15)
                );
                border: 1px solid rgba(255, 255, 255, 0.15);
                padding: 12px 20px;
                border-radius: 22px;
            }
            QPushButton[text="⚙"] {
               background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(0, 242, 254, 0.2),
                    stop:0.5 rgba(255, 255, 255, 0.05),
                    stop:1 rgba(128, 0, 255, 0.2)
                );
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 22px;
                padding: 12px 20px;
            }
            QLabel#Disclaimer {
                color: rgba(255, 255, 255, 0.5);
                background-color: transaparent;
                border: none;
                border-radius: 12px;
            }
        """)

        main_layout = QVBoxLayout()
        self.pages = QStackedWidget()

        self.chat_page = QWidget()
        self.chat_page.setObjectName("ChatPage")
        self.chat_page_layout = QVBoxLayout(self.chat_page)

        self.settings_page = QWidget()
        self.settings_page.setObjectName("SettingsPage")
        self.settings_page_layout = QVBoxLayout(self.settings_page)

        self.chat_page = QWidget()
        self.chat_page.setObjectName("ChatPage")
        self.chat_page_layout = QVBoxLayout(self.chat_page)

        self.settings_page = QWidget()
        self.settings_page_layout = QVBoxLayout(self.settings_page)

        self.pages.addWidget(self.chat_page)
        self.pages.addWidget(self.settings_page)
        main_layout.addWidget(self.pages)

        main_layout.setContentsMargins(25, 25, 25, 25)

        self.title_label = QLabel("Siri", self)
        self.title_label.setObjectName("Title")
        self.title_label.setFont(QFont("SF Pro Display", 28, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.settings_btn = QPushButton("⚙", self)
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.title_label)
        top_layout.addWidget(self.settings_btn)
        self.chat_page_layout.addLayout(top_layout)

        self.chat_area = QTextEdit(self)
        self.chat_area.setFont(QFont("SF Pro Text", 13))
        self.chat_area.setReadOnly(True)
        self.chat_area.append("<span style='color: #00f2fe; font-weight: bold;'>Siri:</span> Hi, I'm fully connected to your system. Type two times Siri to start the chat.")
        self.chat_page_layout.addWidget(self.chat_area)

        self.wave_anim = WaveAnimation(self)
        self.chat_page_layout.addWidget(self.wave_anim)

        # Barra dei controlli inferiore (Pulsante 💎, Input di testo, Invia, Pulsante Teach)
        input_layout = QHBoxLayout()
        
        self.diamond_btn = QPushButton("⚡", self)
        self.diamond_btn.setObjectName("BtnDiamond")
        self.diamond_btn.clicked.connect(self.trigger_proposal)
        input_layout.addWidget(self.diamond_btn)

        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Write a command...")
        self.input_field.setFont(QFont("SF Pro Text", 12))
        self.input_field.returnPressed.connect(self.process_command)
        input_layout.addWidget(self.input_field)

        self.send_btn = QPushButton("Send", self)
        self.send_btn.setFont(QFont("SF Pro Text", 11))
        self.send_btn.clicked.connect(self.process_command)
        input_layout.addWidget(self.send_btn)

        self.teach_btn = QPushButton("Teach", self)
        self.teach_btn.setObjectName("BtnTeach")
        self.teach_btn.setFont(QFont("SF Pro Text", 11))
        self.teach_btn.clicked.connect(self.open_teach_panel)
        input_layout.addWidget(self.teach_btn)
        
        self.chat_page_layout.addLayout(input_layout)

        self.disclaimer = QLabel("Siri is a local assistant and could make mistakes", self)
        self.disclaimer.setObjectName("Disclaimer")
        self.disclaimer.setFont(QFont("SF Pro Text", 9))
        self.disclaimer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.disclaimer.setStyleSheet("background-color: rgba(255, 255, 255, 0.05); border: none; border-radius: 12px; color: rgba(255, 255, 255, 0.5); padding: 4px;")
        self.chat_page_layout.addWidget(self.disclaimer)

        self.setLayout(main_layout)

# --- GRAFICA PAGINA IMPOSTAZIONI ---
        # Creiamo una barra in alto per il pulsante Indietro
        settings_top_layout = QHBoxLayout()
        self.back_btn = QPushButton("← Back", self)
        settings_top_layout.addWidget(self.back_btn)
        settings_top_layout.addStretch() # Spinge il bottone tutto a sinistra
        self.settings_page_layout.addLayout(settings_top_layout)

        # Titolo della pagina impostazioni
        settings_title = QLabel("Theme Settings", self)
        settings_title.setStyleSheet("background-color: transparent; border: none; color: rgb(255, 255, 255); font-weight: bold; font-size: 32px;")
        self.settings_page_layout.addWidget(settings_title)

        # Pulsanti per scegliere il tema (Chiaro, Scuro, Liquid Glass)
        self.dark_theme_btn = QPushButton("🌑 Dark Theme", self)
        self.light_theme_btn = QPushButton("☀️ Light Theme", self)
        self.glass_theme_btn = QPushButton("✨ Liquid Glass", self)

        # Li aggiungiamo alla pagina delle impostazioni
        self.settings_page_layout.addWidget(self.dark_theme_btn)
        self.settings_page_layout.addWidget(self.light_theme_btn)
        self.settings_page_layout.addWidget(self.glass_theme_btn)
        self.dark_theme_btn.clicked.connect(lambda: [
            self.chat_page.setStyleSheet("background-color: rgba(50, 70, 90, 0.45); border-radius: 22px;"),
            self.settings_page.setStyleSheet("background-color: rgba(50, 70, 90, 0.45); border-radius: 22px;")
        ])

        self.light_theme_btn.clicked.connect(lambda: [
            self.chat_page.setStyleSheet("background-color: rgba(80, 110, 140, 0.45); border-radius: 22px;"),
            self.settings_page.setStyleSheet("background-color: rgba(85, 115, 145, 0.55); border-radius: 22px;"),
        ])

        self.glass_theme_btn.clicked.connect(lambda: [
            self.chat_page.setStyleSheet("background-color: rgba(0, 150, 255, 0.25); border-radius: 22px;"),
            self.settings_page.setStyleSheet("background-color: rgba(0, 100, 200, 0.45); border-radius: 22px;")
        ])

        self.settings_page_layout.addStretch() # Spinge tutto verso l'alto

        # --- LOGICA DEI PULSANTI (I collegamenti) ---
        # Quando premi l'ingranaggio, vai alla pagina 1 (Impostazioni)
        self.settings_btn.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        # Quando premi Back, torni alla pagina 0 (Chat)
        self.back_btn.clicked.connect(lambda: self.pages.setCurrentIndex(0))


        # Crea l'oggetto del pannello scorrevole inferiore iOS
        self.teach_panel = TeachPanel(self)
        self.teach_panel.setFixedSize(480, 350)
        self.teach_panel.hide()

    def open_teach_panel(self):
        self.teach_panel.slide_up()

    def trigger_proposal(self):
        self.chat_area.append("<hr><span style='color: #ffffff; font-weight: bold;'>You:</span> [Inviata richiesta proposta 💎]")
        QApplication.processEvents()
        self.attiva_output = True
        self.process.write(b"\n") 

    def initBash(self):
        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.read_bash_output)
        self.process.start("bash", ["--noediting", "-i"])
        
        # --- IL TUO IDENTICO CODICE BASH ORIGINALE CON IL FIX DI BATTITURA CORRETTO IN INFERIORE ---
        contenuto_siri_bashrc = """
finder() {
    command pcmanfm
}

safari() {
    command netsurf
}

AppStore() {
    command ~/pi-apps/gui
}

Apple-Shutdown() {
    command shutdown -h now
} 
Apple-Reboot()   {
    command reboot
}
Apple() {
  echo -e "\uF8FF"
}

Finder()        {
  command sudo pcmanfm
}

Siri() {
    echo "Hi, I'm ready to receive commands."
    echo "Speak with me normally."
    echo ""

    local msg_count=0
    local blocco_proposte=0
    local file_memoria="$HOME/.siri_memory"
    local tempo_inizio=$(date +%s)

    touch "$file_memoria"

    local proposte=(
        "Do you want to modify the bottom Dock bar to look like a Mac?"
        "Do you want to know how to check your 512MB of RAM in real-time?"
        "Do you want to know how to check if your Raspberry Pi chip is getting too hot?"
        "Do you want to know how to shut down the computer with a quick command?"
        "Do you want to know how to see how many files you have accumulated in your Home folder?"
        "Do you want to know how to check if your Internet connection is slowing down?"
        "Do you want to know how to view the Megahertz speed of your processor?"
        "Do you want to clear the RAM cache if the system slows down?"
        "Do you want to know how to see exactly which operating system you are running?"
        "Do you want to find out how much total memory is left on your MicroSD card?"
        "Do you want a quick explanation of what the hidden .bashrc file does?"
    )

    Siri_Gestisci_Eliminazione() {
        echo "--- 🗂️ ALL THINGS THAT I LEARN ---"
        local count=1
        local chiavi_temporanee=()
        while IFS='|' read -r chiave risposta; do
            if [ -n "$chiave" ]; then
                echo "$count) Se mi dici: '$chiave' -> Answer: '$risposta'"
                chiavi_temporanee[$count]="$chiave"
                count=$((count + 1))
            fi
        done < "$file_memoria"
        
        if [ "$count" -eq 1 ]; then
            echo "Siri: At the moment my memory is empty."
            return
        fi

        echo ""
        echo "Siri > Type the numbers of the files that you want to delete (ex: 4-8-111) or '0' to cancel: "
        read -p " " input_cancellazione
        if [ "$input_cancellazione" != "0" ] && [ -n "$input_cancellazione" ]; then
            local file_temp=$(mktemp)
            cp "$file_memoria" "$file_temp"
            local numeri_puliti=$(echo "$input_cancellazione" | tr '-' ' ')
            for num in $numeri_puliti; do
                if [ "$num" -gt 0 ] && [ "$num" -lt "$count" ]; then
                    local chiave_target="${chiavi_temporanee[$num]}"
                    sed -i "|^$chiave_target||d" "$file_temp"
                    echo "Siri: Removed things numeber $num"
                fi
            done
            mv "$file_temp" "$file_memoria"
            echo "Siri: Deletion completed! ( ^_^)b"
        else
            echo "Siri: Deletion cancelled"
        fi
    }

    while true; do
        echo "You > "
        read -p " " frase_utente

        if [ -z "$frase_utente" ]; then
            if [ "$blocco_proposte" -eq 1 ]; then
                echo "Siri: You said no before, so I won't propose anything else to you. ( U_U )"
                echo ""
                continue
            fi

            local index=$((RANDOM % ${#proposte[@]}))
            echo "Siri: ${proposte[$index]}"
            echo "You (yes/no) > "
            read -p " " conferma_prop
            
            if [ "$conferma_prop" = "yes" ] || [ "$conferma_prop" = "yap" ]; then
                echo ""
                case "$index" in
                    0)
                        echo "--- INSTRUCTIONS TO MODIFY THE DOCK ---"
                        echo "1. Right-click on the taskbar at the top -> 'Panel Settings'."
                        echo "2. In the 'Geometry' tab, change position to 'Bottom', width to 60% and 'Align to Center'."
                        echo "3. In the 'Appearance' tab, set icon size to 48 pixels."
                        ;;
                    1) echo "Siri: Type the command 'command free -h' in the terminal.";;
                    2) echo "Siri: Type 'vcgencmd measure_temp' in the terminal.";;
                    8) echo "Siri: Type the word 'directory' in the chat to see the entire list.";;
                    9) echo "Siri: Ask me 'operative system' to see the details.";;
                    *) echo "Siri: For this function, write the request directly in the chat.";;
                esac
            else
                echo "Siri: No more suggestions for this chat. ( *^* )"
                blocco_proposte=1
            fi
            echo ""
            continue
        fi

        local pulita=$(echo "$frase_utente" | tr '[:upper:]' '[:lower:]' | tr -d '?,.!:-')

        local trovato_in_memoria=0
        while IFS='=' read -r chiave risposta; do
            if [ "$chiave" = "$pulita" ]; then
                if [[ "$risposta" == EXEC:* ]]; then
                    local cmd="${risposta#EXEC:}"
                    echo "Siri: Ok, I will do it now!"
                    eval "$cmd &"
                else
                    echo "Siri: $risposta"
                fi
                trovato_in_memoria=1
                break
            fi
        done < "$file_memoria"

        if [ "$trovato_in_memoria" -eq 1 ]; then
            echo ""
            continue
        fi

        case "$pulita" in
            "good afternoon"|"good morning"|"good evening"|"hey"|"hey siri"|"hi"|"hello")
                echo "Siri: Hi! I'm ready to receive commands!"
                ;;
            *"how is it going"*|*"how it's going"*|*"how's it going"*|*"how are you"*)
                echo "Siri: All good! How are you, you're fine?"
                ;;
            *"fine"*|*"all right"*|*"all good"*|*"normal"*)
                echo "Siri: Perfect, I'm happy that you're well!"
                ;;
            *"not so good"*|*"bad*"|*"not well"*|*"sad"*)
                echo "Siri: I'm sorry... If you want I can help you lighten up your day!"
                ;;
            *"never mind"*)
                echo "Siri: Ok! So, how I can help you?"
                ;;
            *"who are you"*|*"who're you"*)
                echo "Siri: I'm Siri, an assistant offline created by claimy17."
                ;;
            *"what time is it"*) echo -n "Siri: It's currently " && date +"%H:%M" ;;
            *"what day is today"*) echo "Siri: Today is:" && date +"%A, %d %B %Y" && cal ;;
            *"operative system"*|*"kernel"*)
                echo "--- 🖥️ DETAILS OF THE SYSTEM ---"
                echo "• OS:            Raspbian (Trixie)"
                echo "• Architettura:  ARM (32-bit/64-bit)"
                echo "• Host Hardware: pi "
                echo "• Kernel Log:    $(uname -r)"
                ;;
            *"check my memory"*|*"ram"*)
                command free -h
                ;;
            *"temperature"*)
                echo -n "Siri CPU: " && vcgencmd measure_temp | cut -d= -f2
                ;;
            *"battery"*)
                if [ -d /sys/class/power_supply ] && ls /sys/class/power_supply/ | grep -qE "BAT|battery"; then
                    local capacita=$(cat /sys/class/power_supply/BAT*/capacity 2>/dev/null || echo "unknow")
                    echo "Siri: Your device has a battery. Current charge: ${capacita}%."
                else
                    echo "Siri: Your PC is powered by 5v. It doesn't must have a battery."
                fi   # <-- FIX: Cambiato il tuo vecchio 'py' errato con 'fi' corretto per ripristinare la Bash!
                ;;
            *"weather"*)
                local luogo=$(echo "$pulita" | sed -e 's/meteo//g' -e 's/che tempo fa//g' | tr -d ' ')
                if [ -z "$luogo" ]; then
                    command curl -s "wttr.in?m&1" | head -n 7
                else
                    command curl -s "wttr.in/${luogo}?m&1" | head -n 7
                fi
                ;;
            *"open finder"*|*"launch file manager"*)
                command pcmanfm . &
                ;;
            *"open appstore"*|*"launch pi-apps"*)
                command pi-apps &
                ;;
            *"open folder "*|*"open file "*)
                local app=$(echo "$pulita" | sed -e 's/apri //g' -e 's/lancia //g')
                xdg-open "$app" >/dev/null 2>&1 &
                ;;
            *"poweroff"*|*"close this computer"*|*"shutdown"*)
                echo "Siri: Are you sure to shutdown the computer? (yes/no): "
                read -p " " conferma
                if [ "$conferma" = "yes" ] || [ "$conferma" = "yap" ]; then
                    shutdown -h now
                else
                    echo "Siri: You need me for anything else? (yes/no): "
                    read -p " " bisogno
                    if [ "$bisogno" = "no" ]; then
                        echo "Siri: Ok, I'm here if you need me."
                    else
                        echo "Siri: Tell me, What do you need me for?"
                    fi
                fi
                ;;
            *"remove"*|*"delete"*|*"siri gesture deletion"*)
                 Siri_Gestisci_Eliminazione
                 echo ""
                 continue
                 ;;
            *"byeee"*|*"exit"*|*"close"*|*"i must go"*)
                echo "Siri: Good bye!"
                break
                ;;
            *find* | *search* | *where*is*it*)
                local nome_file=$(echo "$pulita" | sed -E 's/(where is it|search|find)//g' | tr -d ' ?')
                if [ -z "$nome_file" ]; then
                    echo "Siri: You don't said to me what to search! Tell me for example: 'search boot'"
                else
                    echo "Siri: I'm scanning the folders... One moment."
                    local risultato=$(find / -name "*$nome_file*" 2>/dev/null | head -n 10)
                    if [ -z "$risultato" ]; then
                        echo "Siri: I don't find any folder or file with name '$nome_file'."
                    else
                        echo "Siri: Here is it:"
                        echo "$risultato"
                    fi
                fi
                ;;
           *"ok"*)
               echo "OK °_°"
               ;;
            *)
                local total_imparate=$(wc -l < "$file_memoria" 2>/dev/null || echo 0)
                if [ "$total_imparate" -gt 0 ] && [ $((total_imparate % 100)) -eq 0 ]; then
                    echo "Siri > I learned $total_imparate cose! Do you want to delete something? (nothing/tellme): "
                    read -p " " scelta_blocco
                    if [ "$scelta_blocco" = "tellme" ]; then
                        Siri_Gestisci_Eliminazione
                        echo ""
                        continue
                    fi
                fi

                echo "Siri: Oh nooo! Sorry I don't have this function on my memory...  >_< "
                echo ""
                echo "Tap the 'Teach' button to teach me what to reply when you say '$frase_utente'."
                
                if [ "$scelta_impara" = "text" ] || [ "$scelta_impara" = "word" ]; then
                    echo "Siri > What I must tell to you when you say '$frase_utente'?: "
                    read -p "" nuova_risposta
                    local dimensione_file=$(stat -c%s "$file_memoria" 2>/dev/null || echo 0)
                    local limite_gb=1073741824
                    if [ "$dimensione_file" -lt "$limite_gb" ]; then
                        echo "$pulita|$nuova_risposta" >> "$file_memoria"
                        echo "Siri: Perfect! I learned it forever! ( ^_^)v"
                    else
                        Siri_Gestisci_Eliminazione
                    fi
               elif [ "$scelta_impara" = "command" ]; then
                   echo "Siri > What command I must execute when you say '$frase_utente'? (es: galculator, pcmanfm): "
                   read -p "" cmd_risposta
                   echo "$pulita=EXEC:$cmd_risposta" >> "$file_memoria"
                   echo "Siri: Good, I learned it succesfully!"
              else
                   echo ""
              fi
              ;;
        esac
        echo ""
    done
}

ResetSiri() {
    local file_memoria="$HOME/.siri_memory"
    echo "Siri > Are you sure to delete all the things that I learned? (yes/no): "
    read -p " " conferma1
    if [ "$conferma1" = "yes" ] || [ "$conferma1" = "yap" ]; then
        echo "Siri: WARNING!! This action will delete all my memories."
        read -p "Siri > Do you want to do the RESET? (yes/no): " conferma2
        if [ "$conferma2" = "yes" ] || [ "$conferma2" = "yap" ]; then
            rm -f "$file_memoria"
            touch "$file_memoria"
            echo "Siri: The memory has been deleted. Now I'm like new. ( ^_^)v"
        else
            echo "Siri: Is not raccomandet to do the RESET of Siri but if you lied you can do it with no stress."
        fi
    else
        echo "Siri: Reset cancelled. My memories are secured!"
    fi
}
"""
        self.process.write(f"{contenuto_siri_bashrc}\n".encode())
        self.attiva_output = False

    def process_command(self):
        text = self.input_field.text().strip()
        if not text:
            return
        
        self.chat_area.append(f"<hr><span style='color: #ffffff; font-weight: bold;'>You:</span> {text}")
        self.input_field.clear()
        QApplication.processEvents()

        self.attiva_output = True
        self.process.write(f"{text}\n".encode())

    def read_bash_output(self):
        data = self.process.readAllStandardOutput().data().decode("utf-8", errors="ignore")
        if self.attiva_output and data.strip():
            righe = data.split('\n')
            output_filtrato = [r for r in righe if "claimy17@" not in r and r.strip()]
            
            if output_filtrato:
                testo_finale = "<br>".join(output_filtrato)
                self.chat_area.append(f"<span style='color: #a2e8dd;'>{testo_finale}</span>")
        
    def resizeEvent(self, event):
        # Mantiene il pannello di Teach ancorato in fondo anche se ridimensioni la finestra
        if hasattr(self, 'teach_panel'):
            self.teach_panel.setGeometry(0, self.height() - self.teach_panel.height(), self.width(), self.teach_panel.height())
        super().resizeEvent(event)

    def closeEvent(self, event):
        self.process.terminate()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    if not check_integrity():
        ex = LockScreen()
    else:
        ex = SiriIOS27()
        
    ex.show()
    sys.exit(app.exec())


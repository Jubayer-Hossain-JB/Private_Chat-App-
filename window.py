import customtkinter as ctk
import qrcode
import threading
from PIL import Image
import webbrowser
import web
import soket
from ctypes import windll
import os
import shutil
class Window(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("QR Code Generator")
        self.geometry("400x510")
        # self.overrideredirect(True)  # Remove window decorations
        self.overrideredirect(True)
        # self.overrideredirect(False)
        self.configure(fg_color="#2e2e2e")
        self.iconbitmap(os.path.join(os.path.dirname(os.path.realpath(__file__)),'icon.ico'))
        # Initialize drag functionality variables
        self._drag_start_x = 0
        self._drag_start_y = 0

        # Main frame to hold all widgets
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent", border_width=3, border_color="#3b3b3b")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Bind drag events to the main frame
        self.main_frame.bind("<Button-1>", self.start_drag)
        self.main_frame.bind("<B1-Motion>", self.on_drag)

        # Image display label
        self.image_label = ctk.CTkLabel(self.main_frame, text="QR Code will appear here", 
                                        width=300, height=300, fg_color="white", corner_radius=10)
        self.image_label.pack(pady=(20, 10))
        ctk.CTkLabel(self.main_frame, text="The backend engine is running. Now scan the above QRcode or Click the button below or go to the hyper link below.", wraplength=350, compound="left").pack()
        # Text display label
        self.text_label = ctk.CTkButton(
            master=self,
            text="Open Website",
            command=self.open_browser,
            width=200,
            height=40,
            corner_radius=8,
            font=("Arial", 14),
            
        )
        # self.text_label = ctk.CTkLabel(self.main_frame, text="Enter text in console", 
        #                                font=("Arial", 14), wraplength=380)
        self.text_label.place(y=400, x= 200, anchor='center')

        # Custom close button
        self.close_button = ctk.CTkButton(self.main_frame, text="✕", width=60, height=40, 
                                          fg_color="#6b0000", font=("Arial", 21),
                                          command=self.close ,hover_color="#2f0909")
        self.close_button.pack(pady=20,side='bottom')
        self.close_button.bind("<Button-1>", lambda e: "break")  # Prevent drag when clicking button
        self.update_display(f'http://{web.IPAddr}:8080')
        

    def close(self):
        print('ye')
        self.destroy()
        dir = "./uploads"
        shutil.rmtree(dir)
        os.makedirs(dir)
    
    def start_drag(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag(self, event):
        x = self.winfo_x() + (event.x - self._drag_start_x)
        y = self.winfo_y() + (event.y - self._drag_start_y)
        self.geometry(f"+{x}+{y}")

    def update_display(self, text):
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
        pil_image = Image.new("RGB", (300, 300), "white")
        pil_image.paste(img.resize((300, 300)), (0, 0))

        # Convert to CTkImage
        ctk_image = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(300, 300))
        self.image_label.configure(image=ctk_image, text="")
        self.text_label.configure(command=lambda:self.open_browser(text), text=f'Click to open http://{web.IPAddr}:8080')
    def open_browser(self, site_address):
        webbrowser.open(site_address)

def set_appwindow(root):
    hwnd = windll.user32.GetParent(root.winfo_id())
    style = windll.user32.GetWindowLongPtrW(hwnd, GWL_EXSTYLE)
    style = style & ~WS_EX_TOOLWINDOW
    style = style | WS_EX_APPWINDOW
    res = windll.user32.SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style)
    # re-assert the new window style
    root.wm_withdraw()
    root.after(10, lambda: root.wm_deiconify())

if __name__ == "__main__":
    GWL_EXSTYLE = -20
    WS_EX_APPWINDOW = 0x00040000
    WS_EX_TOOLWINDOW = 0x00000080
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    window = Window()
    # threading.Thread(target=get_input, args=(app,), daemon=True).start()
    threading.Thread(target=soket.server.run_forever, daemon=True).start()
    def web_server():
        web.run(host=web.IPAddr, port=8080)
    threading.Thread(target=web_server, daemon=True).start()
    window.after(10, lambda: set_appwindow(root=window))
    window.mainloop()

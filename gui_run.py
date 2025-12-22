import tkinter as tk
from tkinter import messagebox, scrolledtext
import random
from client1_sender import get_control_info
from server_corruptor import corrupt_data

class SimpleGUI:
    def __init__(self, root):
        root.title("DATA COMMUNICATION ERROR CONTROL SIMULATOR")
        root.geometry("900x750")
        root.configure(bg='#000000')

        tk.Label(root, text="DATA COMMUNICATION ERROR CONTROL SIMULATOR",
                font=('Arial', 18, 'bold'), bg='#000000', fg="#FF0000").pack(pady=15)

        tk.Label(root, text="Veri:", bg='#000000', fg='#FFFFFF', font=('Arial', 11, 'bold')).pack()
        self.data_entry = tk.Entry(root, width=30, font=('Arial', 12), bg='#1a1a1a', fg='#FFFFFF', insertbackground='white')
        self.data_entry.pack(pady=5)
        self.data_entry.focus_set()

        tk.Label(root, text="Yöntem Seç:", bg='#000000', fg='#FFFFFF',
                font=('Arial', 11, 'bold')).pack(pady=(15,5))

        self.method_var = tk.StringVar(value="CRC16")
        methods = ["PARITY_EVEN", "PARITY_ODD", "2D_PARITY", "CRC16", "HAMMING", "CHECKSUM"]

        method_dropdown = tk.OptionMenu(root, self.method_var, *methods)
        method_dropdown.config(bg='#1a1a1a', fg='#FFFFFF', font=('Arial', 11),
                              activebackground='#FF0000', activeforeground='#000000',
                              highlightthickness=0, bd=0, width=20)
        method_dropdown['menu'].config(bg='#1a1a1a', fg='#FFFFFF', font=('Arial', 10),
                                       activebackground='#FF0000', activeforeground='#000000')
        method_dropdown.pack(pady=5)

        tk.Button(root, text="GÖNDER", command=self.send,
                 bg="#FF0000", fg='#000000', font=('Arial', 12, 'bold'),
                 width=15, height=2, bd=0, cursor='hand2').pack(pady=15)

        self.result_text = scrolledtext.ScrolledText(root, width=90, height=30,
                                                      font=('Consolas', 10),
                                                      bg='#000000', fg='#FFFFFF',
                                                      wrap=tk.WORD, insertbackground='white')
        self.result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def send(self):
        data = self.data_entry.get().strip()

        if not data:
            messagebox.showwarning("Uyarı", "Veri girin!")
            return

        method = self.method_var.get()
        control_info = get_control_info(data, method)
        packet = f"{data}|{method}|{control_info}"

        self.result_text.delete('1.0', tk.END)

        output = "=" * 50 + "\n"
        output += "Oluşturulan Paket    : " + packet + "\n"
        output += "Veri                 : " + data + "\n"
        output += "Yöntem               : " + method + "\n"
        output += "Kontrol Bilgisi      : " + control_info + "\n"
        output += "=" * 50 + "\n"
        output += "Paket sunucuya başarıyla gönderildi!\n"
        output += "=" * 50 + "\n\n"

        should_corrupt = random.random() < 0.75
        output += "=" * 50 + "\n"
        output += "Sunucu - Alınan Paket\n"
        output += "=" * 50 + "\n"
        output += "Orijinal Veri        : " + data + "\n"
        output += "Yöntem               : " + method + "\n"
        output += "Kontrol Bilgisi      : " + control_info + "\n"

        if should_corrupt:
            corrupted_data, corruption_method = corrupt_data(data)
            output += "Bozulmuş Veri        : " + corrupted_data + "\n"
            output += "Bozma Yöntemi        : " + corruption_method + "\n"
            output += "Durum                : Hata enjekte edildi\n"
        else:
            corrupted_data = data
            output += "Durum                : Veri bozulmadan iletildi\n"

        output += "Paket İstemci 2'ye iletildi\n"
        output += "=" * 50 + "\n\n"

        computed_control = get_control_info(corrupted_data, method)
        status = "VERİ DOĞRU" if control_info == computed_control else "VERİ BOZUK"

        output += "=" * 50 + "\n"
        output += "İstemci 2 - Alınan Paket\n"
        output += "=" * 50 + "\n"
        output += "Alınan Veri          : " + corrupted_data + "\n"
        output += "Yöntem               : " + method + "\n"
        output += "Gönderilen Kontrol   : " + control_info + "\n"
        output += "Hesaplanan Kontrol   : " + computed_control + "\n"
        output += "Durum                : " + status + "\n"
        output += "=" * 50 + "\n"

        self.result_text.insert('1.0', output)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()

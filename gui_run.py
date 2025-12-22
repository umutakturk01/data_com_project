import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
from client1_sender import send_to_server
from client2_receiver import receive_from_server, get_control_info

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

        self.result_text = scrolledtext.ScrolledText(root, width=120, height=60,
                                                      font=('Consolas', 15),
                                                      bg='#000000', fg="#FFFFFF",
                                                      wrap=tk.WORD, insertbackground='white')
        self.result_text.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def send(self):
        data = self.data_entry.get().strip()

        if not data:
            messagebox.showwarning("Uyarı", "Veri girin!")
            return

        method = self.method_var.get()
        self.result_text.delete('1.0', tk.END)

        def process():
            try:
                output = "=" * 50 + "\n"
                output += "Client 1 - Paket Gönderiliyor\n"
                output += "=" * 50 + "\n"

                packet, control_info = send_to_server(data, method)

                output += "Oluşturulan Paket    : " + packet + "\n"
                output += "Veri                 : " + data + "\n"
                output += "Yöntem               : " + method + "\n"
                output += "Kontrol Bilgisi      : " + control_info + "\n"
                output += "=" * 50 + "\n"
                output += "Paket sunucuya başarıyla gönderildi!\n"
                output += "=" * 50 + "\n\n"

                self.result_text.insert(tk.END, output)

                output = "=" * 50 + "\n"
                output += "Client 2 - Sunucudan Paket Alınıyor\n"
                output += "=" * 50 + "\n"

                received_packet = receive_from_server()
                parts = received_packet.split("|")

                if len(parts) == 4:
                    received_data, received_method, original_control, corruption_info = parts

                    output += "Alınan Veri          : " + received_data + "\n"
                    output += "Yöntem               : " + received_method + "\n"
                    output += "Gönderilen Kontrol   : " + original_control + "\n"

                    if corruption_info != "BOZULMADI":
                        output += "Bozma Yöntemi        : " + corruption_info + "\n"

                    computed_control = get_control_info(received_data, received_method)
                    output += "Hesaplanan Kontrol   : " + computed_control + "\n"

                    status = "VERİ DOĞRU" if original_control == computed_control else "VERİ BOZUK"
                    output += "Durum                : " + status + "\n"
                    output += "=" * 50 + "\n"

                    self.result_text.insert(tk.END, output)
            except Exception as e:
                messagebox.showerror("Hata", f"Sunucu bağlantı hatası:\n{str(e)}\n\nÖnce server_corruptor.py'yi çalıştırın!")

        threading.Thread(target=process, daemon=True).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleGUI(root)
    root.mainloop()

import db
from gui import CanteenApp
import tkinter as tk

if __name__ == "__main__":
    db.connect_db()
    db.insert_menu_items()

    root = tk.Tk()
    root.title("☕ Modern Café Billing System")

    # ✅ Fullscreen mode
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

    app = CanteenApp(root)

    # ✅ Exit button (visible bottom-right)
    exit_btn = tk.Button(
        root,
        text="🚪 Exit",
        bg="#b22222",
        fg="white",
        font=("Arial", 13, "bold"),
        padx=10,
        pady=5,
        command=root.destroy
    )
    exit_btn.place(relx=0.95, rely=0.95, anchor="se")

    root.mainloop()

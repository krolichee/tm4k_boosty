import tm4k_status_label


def updateStatus(message:str):
    print("status: ",message)
    tm4k_status_label.status_label.config(text=message)
    tm4k_status_label.status_label.update_idletasks()
    # tm4k_modal_root.root.mainloop()
    # tm4k_status_label.status_label.mainloop()

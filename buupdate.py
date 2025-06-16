import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime
import os

DATA_FILE = "src/lib/data/metadata.json"
SECTIONS = ["writing", "code", "curricula", "music", "video"]
BOOL_OPTIONS = ["True", "False"]

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def is_filled(value):
    return isinstance(value, str) and value.strip() != ""

def validate_data(raw_inputs, editing=False):
    required_fields = ["id", "category", "title", "date", "description", "local", "url", "tags"]
    for field in required_fields:
        if field == "local":
            continue
        if not is_filled(raw_inputs[field]):
            return False, f"The field '{field}' must be filled."

    if raw_inputs["local"] not in ["True", "False"]:
        return False, "Local must be selected as either True or False."

    if not is_valid_date(raw_inputs["date"]):
        return False, "Date must be in the format YYYY-MM-DD."

    if not editing:
        data = load_data()
        used_ids = {item.get("id") for item in data}
        if raw_inputs["id"] in used_ids:
            return False, f"The ID '{raw_inputs['id']}' is already in use."

    return True, ""

def open_form(mode="add", existing=None):
    form = tk.Toplevel()
    form.title(f"{mode.capitalize()} Entry")
    form.configure(padx=20, pady=20)

    original_id = existing.get("id") if existing else None

    vars = {
        "id": tk.StringVar(value=existing.get("id", "") if existing else ""),
        "category": tk.StringVar(value=existing.get("category", SECTIONS[0]) if existing else SECTIONS[0]),
        "title": tk.StringVar(value=existing.get("title", "") if existing else ""),
        "date": tk.StringVar(value=existing.get("date", "") if existing else ""),
        "description": tk.StringVar(value=existing.get("description", "") if existing else ""),
        "local": tk.StringVar(value=str(existing.get("local", True)) if existing else "True"),
        "url": tk.StringVar(value=existing.get("url", "") if existing else ""),
        "tags": tk.StringVar(value=",".join(existing.get("tags", [])) if existing else ""),
        "username": tk.StringVar(value=existing.get("username", "") if existing else ""),
    }

    def on_submit():
        raw = {k: v.get() for k, v in vars.items()}
        valid, error = validate_data(raw, editing=(mode == "edit"))
        if not valid:
            messagebox.showerror("Invalid Input", error, parent=form)
            return

        entry = {
            **raw,
            "local": raw["local"] == "True",
            "tags": [t.strip() for t in raw["tags"].split(",")]
        }

        data = load_data()
        if mode == "edit":
            for i, item in enumerate(data):
                if item["id"] == original_id:
                    data[i] = entry
                    break
        else:
            data.append(entry)

        save_data(data)
        messagebox.showinfo("Success", f"Entry {mode}ed successfully.", parent=form)
        form.destroy()

    fields = [
        ("ID", "id"),
        ("Category", "category"),
        ("Title", "title"),
        ("Date (YYYY-MM-DD)", "date"),
        ("Description", "description"),
        ("Local (True/False)", "local"),
        ("URL", "url"),
        ("Tags (comma-separated)", "tags"),
        ("Username (optional)", "username"),
    ]

    for i, (label, key) in enumerate(fields):
        tk.Label(form, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=4)
        if key == "category":
            ttk.Combobox(form, textvariable=vars[key], values=SECTIONS, state="readonly", width=47)\
                .grid(row=i, column=1, padx=5, pady=4)
        elif key == "local":
            ttk.Combobox(form, textvariable=vars[key], values=BOOL_OPTIONS, state="readonly", width=47)\
                .grid(row=i, column=1, padx=5, pady=4)
        else:
            entry_field = tk.Entry(form, textvariable=vars[key], width=50)
            if mode == "edit" and key == "id":
                entry_field.config(state="disabled")
            entry_field.grid(row=i, column=1, padx=5, pady=4)

    tk.Button(form, text="Submit", command=on_submit)\
        .grid(row=len(fields), columnspan=2, pady=15)

def select_id(mode):
    ids_window = tk.Toplevel()
    ids_window.title(f"{mode.capitalize()} Entry")
    ids_window.configure(padx=20, pady=20)

    data = load_data()
    ids = [entry["id"] for entry in data]

    def on_select(event):
        selected_id = listbox.get(listbox.curselection())

        if mode == "edit":
            entry = next(item for item in data if item["id"] == selected_id)
            ids_window.destroy()
            open_form("edit", existing=entry)

        elif mode == "delete":
            ids_window.destroy()  
            confirm = messagebox.askyesno("Confirm Delete",
                                          f"Delete entry with ID '{selected_id}'?",
                                          parent=ids_window)
            if confirm:
                new_data = [item for item in data if item["id"] != selected_id]
                save_data(new_data)
                messagebox.showinfo("Deleted", f"Entry '{selected_id}' deleted.")

    tk.Label(ids_window, text=f"Select ID to {mode}:").pack(pady=(0, 10))
    listbox = tk.Listbox(ids_window, width=50)
    listbox.pack(padx=10, pady=10)

    for item_id in ids:
        listbox.insert(tk.END, item_id)

    listbox.bind("<<ListboxSelect>>", on_select)

def main_window():
    root = tk.Tk()
    root.title("JSON Entry Manager")
    root.configure(padx=40, pady=30)

    tk.Label(root, text="Choose an action:", font=("Arial", 12, "bold")).pack(pady=(0, 20))

    tk.Button(root, text="Add Entry", width=25, command=lambda: open_form("add")).pack(pady=10)
    tk.Button(root, text="Edit Entry", width=25, command=lambda: select_id("edit")).pack(pady=10)
    tk.Button(root, text="Delete Entry", width=25, command=lambda: select_id("delete")).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_window()

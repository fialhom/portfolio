# BASIC METADATA UPDATE TOOL
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
    accepted_formats = ["%Y-%m", "%Y-%m-%d", "%b%Y", "%b %Y", "%B%Y", "%B %Y", "%Y"]
    for fmt in accepted_formats:
        try:
            datetime.strptime(date_str.strip(), fmt)
            return True
        except ValueError:
            continue
    return False

def is_filled(value):
    return isinstance(value, str) and value.strip() != ""

def validate_data(raw_inputs, editing=False):
    required_fields = ["id", "category", "title", "date", "description", "local", "url", "tags", "image"]
    for field in required_fields:
        if field in ["local", "image"]:
            continue
        if not is_filled(raw_inputs[field]):
            return False, f"The field '{field}' must be filled."

    if raw_inputs["local"] not in BOOL_OPTIONS:
        return False, "Local must be selected as either True or False."

    if raw_inputs["image"] not in BOOL_OPTIONS:
        return False, "Image must be selected as either True or False."

    if not is_valid_date(raw_inputs["date"]):
        return False, "Date must be in the format YYYY-MM or YYYY-MM-DD or like Dec2023."

    # Image URL logic
    if raw_inputs["image"] == "True" and not is_filled(raw_inputs["image_url"]):
        return False, "Image URL must be filled when image is True."
    if raw_inputs["image"] == "False" and is_filled(raw_inputs["image_url"]):
        return False, "Image URL must be blank when image is False."

    # Validate that local file exists if local == True
    if raw_inputs.get("local") == "True":
        local_url = raw_inputs.get("url", "").strip()
        if not local_url.startswith("/src"):
            local_url = f"/static/files/{raw_inputs["category"]}/" + ("/" + local_url.lstrip("/")) if local_url else ""

        full_path = os.path.abspath(local_url.lstrip("/"))  # remove leading slash for relative path
        if not os.path.isfile(full_path):
            return False, f"The local file '{full_path}' does not exist."


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
    existing_data = load_data()
    all_tags = sorted({tag for entry in existing_data for tag in entry.get("tags", [])})

    vars = {
        "id": tk.StringVar(value=existing.get("id", "") if existing else ""),
        "category": tk.StringVar(value=existing.get("category", SECTIONS[0]) if existing else SECTIONS[0]),
        "title": tk.StringVar(value=existing.get("title", "") if existing else ""),
        "date": tk.StringVar(value=existing.get("date", "") if existing else ""),
        "description": tk.StringVar(),
        "local": tk.StringVar(value=str(existing.get("local", True)) if existing else "True"),
        "url": tk.StringVar(value=existing.get("url", "") if existing else ""),
        "tags": tk.StringVar(value=",".join(existing.get("tags", [])) if existing else ""),
        "username": tk.StringVar(value=existing.get("username", "") if existing else ""),
        "image": tk.StringVar(value=str(existing.get("image", False)) if existing else "False"),
        "image_url": tk.StringVar(value=existing.get("image_url", "") if existing else ""),
    }

    text_widgets = {}
    tag_vars = {}
    image_url_entry = None  

    def update_image_url_state(*args):
        if vars["image"].get() == "True":
            image_url_entry.config(state="normal")
        else:
            image_url_entry.config(state="disabled")
            vars["image_url"].set("")

    vars["image"].trace_add("write", update_image_url_state)

    def on_submit():
        raw = {k: v.get() for k, v in vars.items()}
        if "description" in text_widgets:
            raw["description"] = text_widgets["description"].get("1.0", "end-1c").strip()

        # Normalize date
        for fmt in ["%Y-%m", "%Y-%m-%d", "%b%Y", "%b %Y", "%B%Y", "%B %Y", "%Y"]:
            try:
                parsed = datetime.strptime(raw["date"].strip(), fmt)
                raw["date"] = parsed.strftime("%Y-%m")
                break
            except ValueError:
                continue

        valid, error = validate_data(raw, editing=(mode == "edit"))
        if not valid:
            messagebox.showerror("Invalid Input", error, parent=form)
            return

        is_local = raw["local"] == "True"
        final_url = raw["url"].strip()
        if is_local and not final_url.startswith("/static/files/"):
            final_url = f"/files/{raw["category"]}/" + final_url.lstrip("/")

        entry = {
            **raw,
            "local": is_local,
            "url": final_url,
            "image": raw["image"] == "True",
            "tags": [t.strip() for t in raw["tags"].split(",") if t.strip()],
            "image_url": raw["image_url"].strip()
        }


        data = load_data()
        if mode == "edit":
            for i, item in enumerate(data):
                if item["id"] == original_id:
                    data[i] = entry
                    break
        else:
            summary = "\n".join(f"{k}: {v}" for k, v in entry.items())
            confirm = messagebox.askyesno("Confirm Add", f"Add this entry?\n\n{summary}", parent=form)
            if not confirm:
                return
            data.append(entry)

        save_data(data)
        messagebox.showinfo("Success", f"Entry {mode}ed successfully.", parent=form)
        form.destroy()

    fields = [
        ("ID", "id"),
        ("Category", "category"),
        ("Title", "title"),
        ("Date (e.g. 2023-08 or Dec 2023)", "date"),
        ("Description", "description"),
        ("Local (True/False)", "local"),
        ("URL", "url"),
        ("Tags (comma-separated)", "tags"),
        ("Username (optional)", "username"),
        ("Image (True/False)", "image"),
        ("Image URL", "image_url")
    ]

    for i, (label, key) in enumerate(fields):
        tk.Label(form, text=label).grid(row=i, column=0, sticky="ne", padx=5, pady=4)

        if key in ["category"]:
            ttk.Combobox(form, textvariable=vars[key], values=SECTIONS, state="readonly", width=47)\
                .grid(row=i, column=1, padx=5, pady=4)

        elif key in ["local", "image"]:
            ttk.Combobox(form, textvariable=vars[key], values=BOOL_OPTIONS, state="readonly", width=47)\
                .grid(row=i, column=1, padx=5, pady=4)

        elif key == "description":
            frame = tk.Frame(form)
            frame.grid(row=i, column=1, padx=5, pady=4, sticky="nsew")
            text = tk.Text(frame, width=50, height=5, wrap="word")
            text.insert("1.0", existing.get("description", "") if existing else "")
            text.pack(side="left", fill="both", expand=True)
            scrollbar = ttk.Scrollbar(frame, command=text.yview)
            scrollbar.pack(side="right", fill="y")
            text.configure(yscrollcommand=scrollbar.set)
            text_widgets[key] = text

        elif key == "tags":
            tag_frame = tk.Frame(form)
            tag_frame.grid(row=i, column=1, sticky="w", padx=5, pady=4)
            entry_field = tk.Entry(tag_frame, textvariable=vars[key], width=40)
            entry_field.pack(side="left", fill="x", expand=True)

            if all_tags:
                checkbox_frame = tk.Frame(form, relief="groove", bd=1)
                checkbox_frame.grid(row=i, column=2, padx=(10, 10), pady=4, sticky="ns")

                tk.Label(checkbox_frame, text="Previous Tags:").pack(anchor="w", padx=4, pady=(2, 4))
                canvas = tk.Canvas(checkbox_frame, width=120, height=100)
                scrollbar = ttk.Scrollbar(checkbox_frame, orient="vertical", command=canvas.yview)
                scroll_frame = tk.Frame(canvas)

                scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)

                for tag in all_tags:
                    var = tk.IntVar()
                    cb = tk.Checkbutton(scroll_frame, text=tag, variable=var, anchor="w", width=15)
                    cb.pack(anchor="w", padx=2)
                    tag_vars[tag] = var

                canvas.pack(side="left", fill="y")
                scrollbar.pack(side="right", fill="y")

                def add_selected_tags():
                    selected = [t for t, v in tag_vars.items() if v.get()]
                    current = [t.strip() for t in vars["tags"].get().split(",") if t.strip()]
                    for tag in selected:
                        if tag not in current:
                            current.append(tag)
                    vars["tags"].set(", ".join(current))

                tk.Button(checkbox_frame, text="Add Selected Tags", command=add_selected_tags).pack(pady=5)

        elif key == "image_url":
            image_url_entry = tk.Entry(form, textvariable=vars[key], width=50)
            image_url_entry.grid(row=i, column=1, padx=5, pady=4)
            update_image_url_state()

        else:
            entry_field = tk.Entry(form, textvariable=vars[key], width=50)
            if mode == "edit" and key == "id":
                entry_field.config(state="disabled")
            entry_field.grid(row=i, column=1, padx=5, pady=4)

    tk.Button(form, text="Submit", command=on_submit).grid(row=len(fields), columnspan=2, pady=15)

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
            confirm = messagebox.askyesno("Confirm Delete", f"Delete entry with ID '{selected_id}'?", parent=ids_window)
            if confirm:
                ids_window.destroy()
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
    root.title("Portfolio Content Manager")
    root.configure(padx=40, pady=30)

    tk.Label(root, text="Choose an action:", font=("Arial", 12, "bold")).pack(pady=(0, 20))
    tk.Button(root, text="Add Entry", width=25, command=lambda: open_form("add")).pack(pady=10)
    tk.Button(root, text="Edit Entry", width=25, command=lambda: select_id("edit")).pack(pady=10)
    tk.Button(root, text="Delete Entry", width=25, command=lambda: select_id("delete")).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_window()

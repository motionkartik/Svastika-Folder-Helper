import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from datetime import datetime


TAGS = [
    "Model", "Testimonial", "Craftsmanship", "BTS", "Unboxing", "Interview",
    "Dispatch", "Reaction", "Founder", "Trending", "Office", "Festive", "Lifestyle"
]


def clean(text):
    bad = '<>:"/\\|?*'
    return ''.join('_' if c in bad else c for c in text).strip()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kartik's Folder Helper - v2.0")
        self.geometry("750x690")
        self.resizable(True, True)
        
        # Configure modern style
        style = ttk.Style()
        style.theme_use('aqua')
        
        self.build_ui()


    # ---------------- UI ----------------
    def build_ui(self):
        # Main container
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Title
        title = ttk.Label(main_frame, text="Kartik's Folder Helper", font=("Helvetica", 18, "bold"))
        title.pack(anchor="w", pady=(0, 10))

        # Content area: three columns (left inputs, middle tags, right media/options)
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)

        # Left panel (inputs)
        left_panel = ttk.Frame(content_frame)
        left_panel.pack(side="left", fill="y", padx=(0, 12), pady=4)

        # Middle panel (tags)
        middle_panel = ttk.Frame(content_frame)
        middle_panel.pack(side="left", fill="both", expand=True, padx=8, pady=4)

        # Right panel (media + options)
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side="left", fill="y", padx=(12, 0), pady=4)

        # Step 1 - Choose Date (Optional)
        date_frame = ttk.LabelFrame(left_panel, text="Step 1 - Choose Date (Optional)", padding=10)
        date_frame.pack(fill="x", pady=(0, 12))
        
        self.use_date = tk.BooleanVar(value=False)
        ttk.Checkbutton(date_frame, text="Use Date Folder", variable=self.use_date)\
            .pack(anchor="w", pady=(0, 8))

        today = datetime.now()
        self.day = tk.StringVar(value=str(today.day))
        self.months = ["January","February","March","April","May","June","July","August",
                       "September","October","November","December"]
        self.month = tk.StringVar(value=self.months[today.month-1])
        self.year = tk.StringVar(value="2026")

        date_input_frame = ttk.Frame(date_frame)
        date_input_frame.pack(fill="x")
        
        ttk.Combobox(date_input_frame, textvariable=self.day, values=[str(i) for i in range(1,32)],
                     width=4, state="readonly").pack(side="left", padx=2)
        ttk.Combobox(date_input_frame, textvariable=self.month, values=self.months, width=10,
                     state="readonly").pack(side="left", padx=2)
        ttk.Combobox(date_input_frame, textvariable=self.year, values=["2025","2026","2027","2028","2029","2030"],
                     width=4, state="readonly").pack(side="left", padx=2)

        # Step 2 - Choose the Subject
        subject_frame = ttk.LabelFrame(left_panel, text="Step 2 - Choose the Subject", padding=10)
        subject_frame.pack(fill="x", pady=(0, 12))
        
        ttk.Label(subject_frame, text="Type").pack(anchor="w", pady=(0, 4))
        self.subject_type = tk.StringVar(value="SKU")
        self.subject_type_cb = ttk.Combobox(subject_frame, textvariable=self.subject_type, values=["SKU","COL","GEN"],
                 width=20, state="readonly")
        self.subject_type_cb.pack(fill="x", pady=(0, 8))

        # Dynamic label: Code / Name / Type
        self.subject_label = ttk.Label(subject_frame, text="Code")
        self.subject_label.pack(anchor="w", pady=(0, 4))
        self.subject_code = tk.StringVar()
        ttk.Entry(subject_frame, textvariable=self.subject_code, width=30).pack(fill="x")
        # Update label when subject type changes
        self.subject_type.trace_add('write', lambda *args: self._update_subject_label())

        # Step 3 - Enter STE Code (Optional)
        ste_frame = ttk.LabelFrame(left_panel, text="Step 3 - Enter STE Code (Optional)", padding=10)
        ste_frame.pack(fill="x", pady=(0, 12))
        
        self.ste_code = tk.StringVar()
        ttk.Entry(ste_frame, textvariable=self.ste_code, width=30).pack(fill="x")

        # Step 4 - Choose Media Type
        media_frame = ttk.LabelFrame(left_panel, text="Step 4 - Choose Media Type", padding=10)
        media_frame.pack(fill="x", pady=(0, 12))
        
        self.media = tk.StringVar(value="Video")
        ttk.Combobox(media_frame, textvariable=self.media, values=["Video","Image","Both"],
                 width=20, state="readonly").pack(fill="x")

        # Options Section
        options_frame = ttk.LabelFrame(left_panel, text="Step 5 - Create Folders", padding=10)
        options_frame.pack(fill="x", pady=(0, 12))
        
        self.ok_var = tk.BooleanVar(value=True)
        self.ng_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Create OK_Shots", variable=self.ok_var).pack(anchor="w", pady=4)
        ttk.Checkbutton(options_frame, text="Create NG_Shots", variable=self.ng_var).pack(anchor="w")

        tag_frame = ttk.LabelFrame(middle_panel, text="Step 6 - Select Tags", padding=10)
        tag_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tag_frame)
        scrollbar.pack(side="right", fill="y")

        self.tagbox = tk.Listbox(tag_frame, selectmode="multiple",
                                 yscrollcommand=scrollbar.set, font=("Helvetica", 15))
        self.tagbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.tagbox.yview)

        for t in TAGS:
            self.tagbox.insert("end", t)

        # Custom tag input
        custom_frame = ttk.Frame(tag_frame)
        custom_frame.pack(fill="x", pady=(8, 0))
        self.new_tag_var = tk.StringVar()
        ttk.Entry(custom_frame, textvariable=self.new_tag_var).pack(side="left", fill="x", expand=True, padx=(0,6))
        ttk.Button(custom_frame, text="Add Tag", command=self.add_tag).pack(side="right")

        # Button Section (placed last)
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(12, 4))

        create_btn = ttk.Button(button_frame, text="Create Structure", command=self.create)
        create_btn.pack(fill="x", padx=2, pady=6)


    # ---------------- Create Folder Logic ----------------
    def create(self):
        base = filedialog.askdirectory(title="Select Base Folder")
        if not base:
            return

        # DATE
        if self.use_date.get():
            date_folder = f"{self.day.get()} {self.month.get()} {self.year.get()}"
        else:
            date_folder = None

        # SUBJECT
        subject = clean(self.subject_code.get().strip())
        if subject:
            subject_folder = f"{self.subject_type.get()}-{subject}"
        else:
            subject_folder = None

        # STE
        ste = clean(self.ste_code.get().strip())
        if ste and not ste.upper().startswith("STE-"):
            ste = "STE-" + ste
        ste = ste.upper() if ste else ""

        # Media(s) and tags
        selected_media = self.media.get()
        medias = ["Video", "Image"] if selected_media == "Both" else [selected_media]

        tags = [self.tagbox.get(i) for i in self.tagbox.curselection()]

        created_paths = []
        for m in medias:
            media_block = m
            if tags:
                media_block += "_" + "_".join(tags)

            final_name = f"{ste}_{media_block}" if ste else media_block

            # BUILD PATH STRUCTURE for this media
            path = Path(base)
            if date_folder: path /= date_folder
            if subject_folder: path /= subject_folder
            path = path / clean(final_name)

            path.mkdir(parents=True, exist_ok=True)

            folders_created = []
            if self.ok_var.get():
                (path/"OK_Shots").mkdir(exist_ok=True)
                folders_created.append("OK_Shots")
            if self.ng_var.get():
                (path/"NG_Shots").mkdir(exist_ok=True)
                folders_created.append("NG_Shots")

            created_paths.append((path, folders_created))

        # Build success message
        lines = ["✓ Successfully Created:\n"]
        for p, folders in created_paths:
            lines.append(str(p))
            if folders:
                lines.append("  Folders:")
                for f in folders:
                    lines.append(f"    • {f}")
            lines.append("")

        messagebox.showinfo("Success", "\n".join(lines))

    def _update_subject_label(self):
        v = self.subject_type.get()
        if v == 'SKU':
            text = 'Code'
        elif v == 'COL':
            text = 'Name'
        else:
            text = 'Type'
        try:
            self.subject_label.config(text=text)
        except Exception:
            pass

    def add_tag(self):
        new_tag = self.new_tag_var.get().strip()
        if not new_tag:
            return
        clean_tag = clean(new_tag)
        # avoid duplicates
        existing = [self.tagbox.get(i) for i in range(self.tagbox.size())]
        if clean_tag in existing:
            # select existing
            idx = existing.index(clean_tag)
            self.tagbox.selection_clear(0, 'end')
            self.tagbox.selection_set(idx)
            self.tagbox.see(idx)
            self.new_tag_var.set("")
            return
        # add to listbox
        self.tagbox.insert('end', clean_tag)
        idx = self.tagbox.size() - 1
        self.tagbox.selection_clear(0, 'end')
        self.tagbox.selection_set(idx)
        self.tagbox.see(idx)
        self.new_tag_var.set("")


if __name__ == "__main__":
    App().mainloop()

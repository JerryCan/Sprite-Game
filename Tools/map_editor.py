import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import os

class DelimitedMapEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("RPG Map Editor met Delimiter Support")
        self.root.geometry("1200x800")
        
        # Standaard mapgrootte
        self.width = 40
        self.height = 30
        
        # Delimiter voor het bestandsformaat
        self.delimiter = "|"
        
        # Huidige geselecteerde terreintype
        self.current_terrain = "G"  # gras
        
        # Voor ongedaan maken van acties
        self.last_cell = None  # (row, col, oude_waarde)
        
        # Terreintypen en hun beschrijvingen, gecategoriseerd
        self.terrain_categories = {
            "Basis terrein": {
                "G": "Gras",
                "W": "Water",
                "P": "Pad",
                "Br": "Brug",
                "Be": "Berg"
            },
            "Gebouwen": {
                "H": "Huis", 
                "Te": "Tempel/Ashram"
            },
            "Vegetatie": {
                "Tr": "Boom"
            },
            "NPC's": {
                "NE": "Dorpsoudste",
                "NH": "Handelaar",
                "NJ": "Jongere",
                "NS": "Spirituele meester",
                "V": "Handelaar (oude aanduiding)"
            },
            "Overig": {
                " ": "Leeg"
            }
        }
        
        # Platte lijst maken van alle terreintypen
        self.terrain_types = {}
        for category in self.terrain_categories.values():
            self.terrain_types.update(category)
        
        # Map data - nu een 2D-array van strings in plaats van karakters
        self.map_data = [["G" for _ in range(self.width)] for _ in range(self.height)]
        
        # Huidige bestandsnaam
        self.current_file = None
        
        # UI opzetten
        self.setup_ui()
        
    def setup_ui(self):
        # Hoofdframe
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame voor terreintypen met scrollbar
        terrain_outer_frame = tk.Frame(main_frame, bd=2, relief=tk.RAISED)
        terrain_outer_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Canvas met scrollbar voor terrein paneel
        terrain_canvas = tk.Canvas(terrain_outer_frame, width=250)
        terrain_scrollbar = tk.Scrollbar(terrain_outer_frame, orient="vertical", command=terrain_canvas.yview)
        terrain_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        terrain_canvas.pack(side=tk.LEFT, fill=tk.Y, expand=True)
        terrain_canvas.configure(yscrollcommand=terrain_scrollbar.set)
        
        # Frame in canvas voor terreintypen
        terrain_frame = tk.Frame(terrain_canvas)
        terrain_canvas.create_window((0, 0), window=terrain_frame, anchor="nw")
        
        # Label voor terrein selectie
        tk.Label(terrain_frame, text="Terreintypen:", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Knoppen voor terreintypen, georganiseerd per categorie
        for category_name, types in self.terrain_categories.items():
            # Categorie label
            category_label = tk.Label(terrain_frame, text=category_name, font=("Arial", 10, "bold"))
            category_label.pack(fill=tk.X, padx=5, pady=(10, 5))
            
            # Terreintype knoppen in deze categorie
            for char, desc in types.items():
                button = tk.Button(
                    terrain_frame, 
                    text=f"{char} - {desc}", 
                    width=25,
                    command=lambda c=char: self.set_terrain(c)
                )
                button.pack(fill=tk.X, padx=5, pady=2)
        
        # Update canvas scroll region als terrain_frame verandert
        terrain_frame.update_idletasks()
        terrain_canvas.config(scrollregion=terrain_canvas.bbox("all"))
            
        # Geselecteerde terrein indicator
        self.terrain_indicator = tk.Label(terrain_frame, 
                                         text=f"Geselecteerd: {self.current_terrain} - {self.terrain_types[self.current_terrain]}",
                                         font=("Arial", 10))
        self.terrain_indicator.pack(pady=10)
        
        # Frame voor kaartgebied
        map_frame = tk.Frame(main_frame)
        map_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Afmetingen indicator
        self.dimensions_label = tk.Label(map_frame, 
                                         text=f"Kaartafmetingen: {self.width}x{self.height} tiles",
                                         font=("Arial", 10))
        self.dimensions_label.pack(pady=5)
        
        # Canvas voor de kaart
        self.canvas = tk.Canvas(map_frame, bg="white", bd=2, relief=tk.SUNKEN)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse events
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<B1-Motion>", self.canvas_drag)
        self.canvas.bind("<Button-3>", self.undo_last_change)  # Rechtermuisknop voor ongedaan maken
        self.canvas.bind("<Configure>", self.redraw_map)
        
        # Menu opzetten
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bestand", menu=file_menu)
        file_menu.add_command(label="Nieuw", command=self.new_map)
        file_menu.add_command(label="Openen", command=self.open_map)
        file_menu.add_command(label="Opslaan", command=self.save_map)
        file_menu.add_command(label="Opslaan als", command=self.save_map_as)
        file_menu.add_separator()
        file_menu.add_command(label="Importeren van tekst", command=self.import_from_string)
        file_menu.add_command(label="Importeren van ASCII", command=self.import_from_ascii)
        file_menu.add_command(label="Exporteren voor code", command=self.show_export_dialog)
        file_menu.add_separator()
        file_menu.add_command(label="Afsluiten", command=self.root.quit)
        
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Bewerken", menu=edit_menu)
        edit_menu.add_command(label="Kaartgrootte wijzigen", command=self.resize_map)
        edit_menu.add_command(label="Alles vullen met huidig terrein", command=self.fill_all)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Gereed", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def set_terrain(self, terrain_char):
        self.current_terrain = terrain_char
        self.terrain_indicator.config(text=f"Geselecteerd: {self.current_terrain} - {self.terrain_types[self.current_terrain]}")
        
    def canvas_click(self, event):
        # Bepaal welke cel is aangeklikt
        cell_width = self.canvas.winfo_width() / self.width
        cell_height = self.canvas.winfo_height() / self.height
        
        col = int(event.x / cell_width)
        row = int(event.y / cell_height)
        
        # Alleen verwerken als de cel binnen de grenzen van de kaart ligt
        if 0 <= row < self.height and 0 <= col < self.width:
            # Bewaar de huidige waarde voor ongedaan maken
            self.last_cell = (row, col, self.map_data[row][col])
            
            # Update de cel met het huidige terreintype
            self.map_data[row][col] = self.current_terrain
            
            # Update alleen de gewijzigde cel voor betere performance
            self.update_cell(row, col)
            
    def canvas_drag(self, event):
        # Dezelfde functionaliteit als canvas_click voor slepen
        self.canvas_click(event)
        
    def undo_last_change(self, event):
        """Maakt de laatste celwijziging ongedaan met rechtermuisknop"""
        if self.last_cell:
            row, col, old_value = self.last_cell
            # Herstel de oude waarde
            self.map_data[row][col] = old_value
            # Update de cel
            self.update_cell(row, col)
            # Reset last_cell
            self.last_cell = None
            # Update statusbalk
            self.status_bar.config(text=f"Laatste wijziging ongedaan gemaakt")
            
    def update_cell(self, row, col):
        """Update alleen de specifieke cel voor betere performance"""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        cell_width = canvas_width / self.width
        cell_height = canvas_height / self.height
        
        x1 = col * cell_width
        y1 = row * cell_height
        x2 = x1 + cell_width
        y2 = y1 + cell_height
        
        # Verwijder bestaande inhoud van de cel
        for item in self.canvas.find_overlapping(x1+1, y1+1, x2-1, y2-1):
            self.canvas.delete(item)
        
        # Bepaal kleur op basis van terreintype
        terrain = self.map_data[row][col]
        color = self.get_terrain_color(terrain)
        
        # Teken cel
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
        
        # Teken terrein symbool - nu aangepast voor leesbaarheid
        if len(terrain) > 1:  # Voor meerkarakter terreintypen
            # Teken de eerste letter groter en de rest kleiner eronder
            self.canvas.create_text(x1 + cell_width/2, y1 + cell_height/3, 
                                  text=terrain[0], font=("Arial", int(min(cell_width, cell_height)/3)))
            self.canvas.create_text(x1 + cell_width/2, y1 + 2*cell_height/3, 
                                  text=terrain[1:], font=("Arial", int(min(cell_width, cell_height)/4)))
        else:
            # Enkelkarakter terreintypen gewoon in het midden
            self.canvas.create_text(x1 + cell_width/2, y1 + cell_height/2, 
                                  text=terrain, font=("Arial", int(min(cell_width, cell_height)/2.5)))
    
    def redraw_map(self, event=None):
        self.canvas.delete("all")
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        cell_width = canvas_width / self.width
        cell_height = canvas_height / self.height
        
        # Teken de cellen
        for row in range(self.height):
            for col in range(self.width):
                x1 = col * cell_width
                y1 = row * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                
                # Bepaal kleur op basis van terreintype
                terrain = self.map_data[row][col]
                color = self.get_terrain_color(terrain)
                
                # Teken cel
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
                
                # Teken terrein symbool
                if len(terrain) > 1:  # Voor meerkarakter terreintypen
                    # Teken de eerste letter groter en de rest kleiner eronder
                    self.canvas.create_text(x1 + cell_width/2, y1 + cell_height/3, 
                                         text=terrain[0], font=("Arial", int(min(cell_width, cell_height)/3)))
                    self.canvas.create_text(x1 + cell_width/2, y1 + 2*cell_height/3, 
                                         text=terrain[1:], font=("Arial", int(min(cell_width, cell_height)/4)))
                else:
                    # Enkelkarakter terreintypen gewoon in het midden
                    self.canvas.create_text(x1 + cell_width/2, y1 + cell_height/2, 
                                         text=terrain, font=("Arial", int(min(cell_width, cell_height)/2.5)))
                                          
        # Teken gridlijnen voor betere zichtbaarheid
        for row in range(self.height + 1):
            y = row * cell_height
            self.canvas.create_line(0, y, canvas_width, y, fill="gray", width=1)
            
        for col in range(self.width + 1):
            x = col * cell_width
            self.canvas.create_line(x, 0, x, canvas_height, fill="gray", width=1)
            
    def get_terrain_color(self, terrain):
        # Kleuren voor verschillende terreintypen
        colors = {
            "G": "#90EE90",     # Lichtgroen voor gras
            "W": "#ADD8E6",     # Lichtblauw voor water
            "P": "#DEB887",     # Beige voor pad
            "Tr": "#228B22",    # Donkergroen voor boom
            "H": "#CD853F",     # Zandkleur voor huis
            "Te": "#FFD700",    # Goud voor tempel/ashram
            "Br": "#8B4513",    # Donkerbruin voor brug
            "Be": "#A0522D",    # Bruin voor berg
            "NE": "#4169E1",    # Royal blue voor dorpsoudste
            "NH": "#FFD700",    # Goud voor handelaar
            "NJ": "#32CD32",    # Lime green voor jongere
            "NS": "#9932CC",    # Paars voor spirituele meester
            "V": "#FFD700",     # Goud voor handelaar (oude aanduiding)
            " ": "#FFFFFF"      # Wit voor leeg
        }
        return colors.get(terrain, "#CCCCCC")  # Grijs voor onbekende types
            
    def new_map(self):
        if messagebox.askyesno("Nieuw", "Weet je zeker dat je een nieuwe kaart wilt maken? Niet-opgeslagen wijzigingen gaan verloren."):
            self.width = 40
            self.height = 30
            self.map_data = [["G" for _ in range(self.width)] for _ in range(self.height)]
            self.current_file = None
            self.redraw_map()
            
            # Update dimensions label
            self.dimensions_label.config(text=f"Kaartafmetingen: {self.width}x{self.height} tiles")
            
            self.status_bar.config(text="Nieuwe kaart gemaakt")
            
    def resize_map(self):
        # Vraag nieuwe dimensies
        new_width = simpledialog.askinteger("Breedte", "Nieuwe breedte:", initialvalue=self.width, minvalue=5, maxvalue=100)
        if new_width is None:
            return
            
        new_height = simpledialog.askinteger("Hoogte", "Nieuwe hoogte:", initialvalue=self.height, minvalue=5, maxvalue=100)
        if new_height is None:
            return
            
        # Maak nieuwe map_data met behoud van bestaande data waar mogelijk
        new_map_data = [[" " for _ in range(new_width)] for _ in range(new_height)]
        
        for row in range(min(self.height, new_height)):
            for col in range(min(self.width, new_width)):
                new_map_data[row][col] = self.map_data[row][col]
                
        self.width = new_width
        self.height = new_height
        self.map_data = new_map_data
        self.redraw_map()
        
        # Update dimensions label
        self.dimensions_label.config(text=f"Kaartafmetingen: {self.width}x{self.height} tiles")
        
        self.status_bar.config(text=f"Kaart herschaald naar {self.width}x{self.height}")
    
    def fill_all(self):
        if messagebox.askyesno("Vullen", f"Weet je zeker dat je de hele kaart wilt vullen met '{self.current_terrain}'?"):
            self.map_data = [[self.current_terrain for _ in range(self.width)] for _ in range(self.height)]
            self.redraw_map()
            self.status_bar.config(text=f"Kaart gevuld met '{self.current_terrain}'")
            
    def open_map(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Kaartbestanden", "*.map"), ("Tekstbestanden", "*.txt"), ("Alle bestanden", "*.*")]
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                
                # Filter commentaarregels en lege regels
                lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('//')]
                
                # Bepaal dimensies
                self.height = len(lines)
                
                # Controleer of er een delimiter in de regels zit
                if self.delimiter in lines[0]:
                    # Gesplitste kaart
                    first_row = lines[0].split(self.delimiter)
                    self.width = len(first_row)
                    
                    # Maak nieuwe map_data
                    self.map_data = [[" " for _ in range(self.width)] for _ in range(self.height)]
                    
                    # Vul met data uit bestand
                    for row, line in enumerate(lines):
                        cells = line.split(self.delimiter)
                        for col, cell in enumerate(cells):
                            if col < self.width:
                                self.map_data[row][col] = cell
                else:
                    # Oude stijl ASCII-kaart (één karakter per cel)
                    self.width = max(len(line) for line in lines)
                    
                    # Maak nieuwe map_data
                    self.map_data = [[" " for _ in range(self.width)] for _ in range(self.height)]
                    
                    # Vul met data uit bestand - een karakter per cel
                    for row, line in enumerate(lines):
                        for col, char in enumerate(line):
                            if col < self.width:
                                self.map_data[row][col] = char
                
                self.current_file = file_path
                # Update dimensions label
                self.dimensions_label.config(text=f"Kaartafmetingen: {self.width}x{self.height} tiles")
                
                self.redraw_map()
                self.status_bar.config(text=f"Geopend: {os.path.basename(file_path)}")
                
        except Exception as e:
            messagebox.showerror("Fout bij openen", str(e))
            
    def save_map(self):
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self.save_map_as()
            
    def save_map_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".map",
            filetypes=[("Kaartbestanden", "*.map"), ("Tekstbestanden", "*.txt"), ("Alle bestanden", "*.*")]
        )
        
        if not file_path:
            return
            
        self._save_to_file(file_path)
        self.current_file = file_path
            
    def _save_to_file(self, file_path):
        try:
            with open(file_path, 'w') as file:
                # Voeg een header toe met info
                file.write(f"// RPG Map Editor - Delimited Map File\n")
                file.write(f"// Grootte: {self.width}x{self.height}\n")
                file.write(f"// Delimiter: {self.delimiter}\n")
                file.write(f"// Legenda:\n")
                
                # Voeg alle terreintypen toe aan de legenda
                for category, types in self.terrain_categories.items():
                    file.write(f"// {category}:\n")
                    for code, desc in types.items():
                        if code != " ":  # Skip leeg
                            file.write(f"//   {code} = {desc}\n")
                
                file.write("\n")
                
                # Schrijf de kaartdata met delimiter
                for row in self.map_data:
                    file.write(self.delimiter.join(row) + "\n")
                    
            self.status_bar.config(text=f"Opgeslagen als: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Fout bij opslaan", str(e))
    
    def import_from_string(self):
        """Importeert een kaart vanuit een string met delimiters"""
        # Maak een dialoogvenster
        dialog = tk.Toplevel(self.root)
        dialog.title("Importeren van Map met Delimiters")
        dialog.geometry("600x400")
        
        # Instructie label
        tk.Label(dialog, text=f"Plak je kaart hieronder (gebruik '{self.delimiter}' als scheidingsteken):").pack(pady=(10, 5))
        
        # Tekstgebied met scrollbars
        frame = tk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar_y = tk.Scrollbar(frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        text_area = tk.Text(frame, wrap=tk.NONE, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        text_area.pack(fill=tk.BOTH, expand=True)
        
        scrollbar_y.config(command=text_area.yview)
        scrollbar_x.config(command=text_area.xview)
        
        # Probeer automatisch te plakken uit klembord
        try:
            text_area.insert(tk.END, dialog.clipboard_get())
        except:
            pass  # Geen probleem als klembord leeg is
        
        # Knoppenpaneel
        button_frame = tk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=10)
        
        cancel_button = tk.Button(button_frame, text="Annuleren", command=dialog.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)
        
        import_button = tk.Button(
            button_frame, 
            text="Importeren", 
            command=lambda: self._process_imported_text(text_area.get("1.0", tk.END), dialog)
        )
        import_button.pack(side=tk.RIGHT)

    def import_from_ascii(self):
        """Importeert een kaart vanuit een niet-gedelimiteerde ASCII-string"""
        # Maak een dialoogvenster
        dialog = tk.Toplevel(self.root)
        dialog.title("Importeren van ASCII Map")
        dialog.geometry("600x400")
        
        # Instructie label
        tk.Label(dialog, text="Plak je ASCII map hieronder (één karakter per cel):").pack(pady=(10, 5))
        
        # Tekstgebied met scrollbars
        frame = tk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar_y = tk.Scrollbar(frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        text_area = tk.Text(frame, wrap=tk.NONE, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        text_area.pack(fill=tk.BOTH, expand=True)
        
        scrollbar_y.config(command=text_area.yview)
        scrollbar_x.config(command=text_area.xview)
        
        # Probeer automatisch te plakken uit klembord
        try:
            text_area.insert(tk.END, dialog.clipboard_get())
        except:
            pass  # Geen probleem als klembord leeg is
        
        # Knoppenpaneel
        button_frame = tk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=10)
        
        cancel_button = tk.Button(button_frame, text="Annuleren", command=dialog.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=10)
        
        import_button = tk.Button(
            button_frame, 
            text="Importeren", 
            command=lambda: self._process_imported_ascii(text_area.get("1.0", tk.END), dialog)
        )
        import_button.pack(side=tk.RIGHT)
    
    def _process_imported_text(self, text, dialog):
        """Verwerkt de geïmporteerde tekst met delimiters naar een nieuwe kaart"""
        lines = text.splitlines()
        
        # Filter lege regels en commentaarregels
        lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('//')]
        
        if not lines:
            messagebox.showerror("Fout", "Geen geldige kaartdata gevonden!")
            return
            
        # Bepaal dimensies
        self.height = len(lines)
        
        # Controleer of er een delimiter in de regels zit
        if self.delimiter in lines[0]:
            # Gesplitste kaart
            first_row = lines[0].split(self.delimiter)
            self.width = len(first_row)
            
            # Maak nieuwe map_data
            self.map_data = [[" " for _ in range(self.width)] for _ in range(self.height)]
            
            # Vul met data uit geïmporteerde tekst
            for row, line in enumerate(lines):
                cells = line.split(self.delimiter)
                for col, cell in enumerate(cells):
                    if col < self.width:
                        self.map_data[row][col] = cell
        else:
            # Geen delimiters gevonden - waarschuw gebruiker
            if not messagebox.askyesno("Geen delimiters", 
                                     f"Geen '{self.delimiter}' delimiters gevonden in de invoer. Wil je deze importeren als ASCII (één karakter per cel)?"):
                return
            
            # Importeer als ASCII
            self._process_imported_ascii(text, dialog, skip_confirmation=True)
            return
        
        # Sluit het dialoogvenster
        dialog.destroy()
        
        # Update dimensions label
        self.dimensions_label.config(text=f"Kaartafmetingen: {self.width}x{self.height} tiles")
        
        # Update de weergave
        self.redraw_map()
        self.status_bar.config(text=f"Kaart geïmporteerd met delimiters: {self.width}x{self.height}")
    
    def _process_imported_ascii(self, text, dialog, skip_confirmation=False):
        """Verwerkt de geïmporteerde ASCII-tekst naar een nieuwe kaart"""
        lines = text.splitlines()
        
        # Filter lege regels en commentaarregels
        lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith('//')]
        
        if not lines:
            messagebox.showerror("Fout", "Geen geldige kaartdata gevonden!")
            return
            
        # Bepaal dimensies
        self.height = len(lines)
        self.width = max(len(line) for line in lines)
        
        # Kaart converteren?
        convert_map = (not skip_confirmation and 
                     messagebox.askyesno("ASCII Conversie", 
                                       "Wil je de volgende ASCII-naar-terreintype conversies toepassen?\n\n" +
                                       "T -> Tr (Boom)\n" +
                                       "M -> Te (Tempel)\n" +
                                       "E -> NE (Dorpsoudste)\n" +
                                       "Y -> NJ (Jongere)\n" +
                                       "S -> NS (Spirituele meester)"))
        
        # Maak nieuwe map_data
        self.map_data = [[" " for _ in range(self.width)] for _ in range(self.height)]
        
        # Conversie mapping indien gewenst
        conversion_map = {
            "T": "Tr",  # Boom
            "M": "Te",  # Tempel
            "E": "NE",  # Dorpsoudste
            "Y": "NJ",  # Jongere
            "S": "NS"   # Spirituele meester
        }
        
        # Vul met data uit geïmporteerde tekst
        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                if col < self.width:
                    if convert_map and char in conversion_map:
                        # Converteer karakter naar terreintype
                        self.map_data[row][col] = conversion_map[char]
                    else:
                        # Gebruik karakter direct
                        self.map_data[row][col] = char
        
        # Sluit het dialoogvenster
        dialog.destroy()
        
        # Update dimensions label
        self.dimensions_label.config(text=f"Kaartafmetingen: {self.width}x{self.height} tiles")
        
        # Update de weergave
        self.redraw_map()
        self.status_bar.config(text=f"ASCII Kaart geïmporteerd: {self.width}x{self.height}")
    
    def export_to_string(self):
        """Exporteert de huidige map als string met delimiters voor gebruik in code"""
        result = [
            "// RPG Map Editor - Delimited Map File",
            f"// Grootte: {self.width}x{self.height}",
            f"// Delimiter: {self.delimiter}",
            "// Legenda:",
        ]
        
        # Voeg legenda toe
        for category_name, types in self.terrain_categories.items():
            result.append(f"// {category_name}:")
            for char, desc in types.items():
                if char != " ":  # Skip leeg
                    result.append(f"//   {char} = {desc}")
        
        result.append("")
        
        # Voeg map data toe met delimiters
        for row in self.map_data:
            result.append(self.delimiter.join(row))
        
        return '\n'.join(result)
    
    def show_export_dialog(self):
        """Toont een dialoog met de geëxporteerde map als string"""
        export_string = self.export_to_string()
        
        # Maak een dialoogvenster
        dialog = tk.Toplevel(self.root)
        dialog.title("Geëxporteerde Map")
        dialog.geometry("600x400")
        
        # Tekstgebied met scrollbars
        frame = tk.Frame(dialog)
        frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scrollbar_y = tk.Scrollbar(frame)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        text_area = tk.Text(frame, wrap=tk.NONE, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        text_area.pack(fill=tk.BOTH, expand=True)
        
        scrollbar_y.config(command=text_area.yview)
        scrollbar_x.config(command=text_area.xview)
        
        # Voeg de geëxporteerde tekst toe
        text_area.insert(tk.END, export_string)
        
        # Kopieerknop
        copy_button = tk.Button(dialog, text="Kopieer naar klembord", command=lambda: self.copy_to_clipboard(export_string))
        copy_button.pack(pady=5)
        
    def copy_to_clipboard(self, text):
        """Kopieert tekst naar het klembord"""
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        messagebox.showinfo("Gekopieerd", "De map is gekopieerd naar het klembord!")

# Hoofdfunctie
def main():
    root = tk.Tk()
    app = DelimitedMapEditor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
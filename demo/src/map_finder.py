# map_finder.py - Helpt bij het vinden van mapbestanden in verschillende locaties
import os

def find_map_file(map_filename):
    """
    Zoekt een mapbestand in verschillende mogelijke locaties
    
    Args:
        map_filename (str): Naam van het mapbestand
    
    Returns:
        str: Volledig pad naar het mapbestand of None als niet gevonden
    """
    # Mogelijke locaties om te zoeken
    possible_locations = [
        os.path.join("Maps", map_filename),                  # ./Maps/
        os.path.join("..", "Maps", map_filename),            # ../Maps/
        os.path.join(".", map_filename),                     # ./
        os.path.join("..", map_filename),                    # ../
        os.path.join(os.path.dirname(__file__), "..", "..", "Maps", map_filename), # Vanaf script locatie
        map_filename                                         # Direct pad
    ]
    
    # Controleer elke mogelijke locatie
    for location in possible_locations:
        if os.path.exists(location):
            print(f"Map bestand gevonden: {location}")
            return os.path.abspath(location)
    
    # Niet gevonden
    print(f"WAARSCHUWING: Map bestand niet gevonden: {map_filename}")
    print(f"Gezocht in: {possible_locations}")
    return None

def list_available_maps(base_paths=None):
    """
    Zoekt en toont alle beschikbare .map bestanden in de gegeven basislocaties
    
    Args:
        base_paths (list): Lijst met paden om te zoeken, standaard is ["Maps", ".", ".."]
    
    Returns:
        list: Lijst met gevonden mapbestanden (volledige paden)
    """
    if base_paths is None:
        base_paths = ["Maps", ".", ".."]
    
    found_maps = []
    
    # Zoek .map bestanden in alle basislocaties
    for base_path in base_paths:
        if os.path.exists(base_path) and os.path.isdir(base_path):
            for filename in os.listdir(base_path):
                if filename.endswith(".map"):
                    full_path = os.path.join(base_path, filename)
                    found_maps.append(os.path.abspath(full_path))
    
    # Toon resultaten
    if found_maps:
        print(f"Gevonden mapbestanden ({len(found_maps)}):")
        for i, map_path in enumerate(found_maps):
            print(f"  {i+1}. {os.path.basename(map_path)} - {map_path}")
    else:
        print("Geen .map bestanden gevonden in de opgegeven paden.")
    
    return found_maps
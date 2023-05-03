import locationtagger

def compose_message(message, result):
    """Return a custom message object."""
    return {
        "message": message,
        "success": result
    }

def extract_location_from_question(input):
    """Extract location entities from string
    
    :Parameters:
        - `input`: String. Input string.
    """
    place_entity = locationtagger.find_locations(text=input)
    named_entities = place_entity.countries + place_entity.regions + place_entity.cities
    if(named_entities):
        print(named_entities)
        return named_entities[0]
    return None
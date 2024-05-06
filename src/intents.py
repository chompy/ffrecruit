INTENTS = {
    "Looking For Group": "LFG",
    "Looking For Members": "LFM",
    "Free Company": "FC",
    "Other": "OTHER"
}

def intent_to_abbr(intent : str) -> str:
    if intent in INTENTS: return INTENTS[intent]
    return intent
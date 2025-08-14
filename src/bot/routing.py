def classify_image_intent(image_bytes, caption_text):
    """
    Decide which agent should handle the image.
    If caption or context gives a clue, use it.
    Otherwise, do a quick model-based guess.
    """
    if caption_text:
        text = caption_text.lower()
        if "waste" in text or "garbage" in text or "trash" in text:
            return "Sanita", "waste"
        if "bin" in text or "container" in text:
            return "Sanita", "bin"
        if "map" in text or "location" in text or "route" in text:
            return "Qumy", "map"
    # Fallback: placeholder for actual image model
    pred = dummy_image_classifier(image_bytes)
    if pred == "waste":
        return "Sanita", "waste"
    if pred == "bin":
        return "Sanita", "bin"
    if pred == "map":
        return "Qumy", "map"
    return "Brenda", "unknown"

def dummy_image_classifier(image_bytes):
    # TODO: Replace with real model call
    return "waste"  # Always returns waste for now
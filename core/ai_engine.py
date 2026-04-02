from difflib import SequenceMatcher
from core.dom_analyzer import extract_elements


class AIEngine:

    @staticmethod
    def similarity(a, b):
        if not a or not b:
            return 0
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    @staticmethod
    def score_element(target, element):
        score = 0

        score += AIEngine.similarity(target, element.get("text", "")) * 5
        score += AIEngine.similarity(target, element.get("id", "")) * 3
        score += AIEngine.similarity(target, element.get("class", "")) * 2
        score += AIEngine.similarity(target, element.get("placeholder", "")) * 4
        score += AIEngine.similarity(target, element.get("aria", "")) * 4

        return score

    @staticmethod
    def heal_locator(page, failed_selector):
        print(f"[AI] Healing selector: {failed_selector}")

        elements = extract_elements(page)

        best_match = None
        best_score = 0

        for el in elements:
            score = AIEngine.score_element(failed_selector, el)

            if score > best_score:
                best_score = score
                best_match = el

        if not best_match:
            raise Exception("No suitable match found")

        print(f"[AI] Best match: {best_match}")

        # Build new selector
        if best_match.get("id"):
            return f"#{best_match['id']}"

        if best_match.get("name"):
            return f"[name='{best_match['name']}']"

        if best_match.get("placeholder"):
            return f"[placeholder='{best_match['placeholder']}']"

        if best_match.get("aria"):
            return f"[aria-label='{best_match['aria']}']"

        if best_match.get("text"):
            return f"text={best_match['text']}"

        raise Exception("Unable to generate healed selector")
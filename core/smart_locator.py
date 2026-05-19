import json
import requests
from core.ai_engine import AIEngine
from bs4 import BeautifulSoup, Comment

def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")

    # Remove HTML comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()

    # Remove SVG elements that are not useful for selector healing
    for svg_tag in ["path", "circle", "clipPath"]:
        for tag in soup.find_all(svg_tag):
            tag.decompose()

    for tag in soup.find_all(True):

        attrs_to_remove = []

        for attr in tag.attrs:
            if (
                attr.startswith("_ngcontent")
                or attr.startswith("_nghost")
                or attr == "style"
                or attr == "clip-path"
            ):
                attrs_to_remove.append(attr)

        for attr in attrs_to_remove:
            del tag.attrs[attr]

    return str(soup)

class SmartActions:
    
    def __init__(self, page):
        self.page = page

    def _get_page(self):
        """Return the raw Playwright page from a wrapped page object."""
        if hasattr(self.page, 'current_page') and hasattr(self.page.current_page, '_playwright'):
            return self.page.current_page
        return self.page

    def heal_with_mistral(self, failed_selector):
        """
        Use Mistral model via Ollama to analyze the page and find the element.
        """
        try:
            page = self._get_page()
            
            # Get page content and current state
            page_content = page.content()
            page_url = page.url

            # Extract only body content to reduce prompt size
            import re
            body_match = re.search(r'<body[^>]*>(.*?)</body>', page_content, re.DOTALL | re.IGNORECASE)
            if body_match:
                page_content = body_match.group(1)
            else:
                # Fallback to full content if body tag not found
                page_content = page_content
            
            # Clean the HTML to remove unnecessary attributes
            page_content = clean_html(page_content)
            
            # Take a screenshot for visual context
            screenshot = page.screenshot()
            
            # Create a more focused prompt for Mistral
            # Get only relevant parts of the page content (limit size)
            if len(page_content) > 10000:  # Limit to 10k characters
                page_content = page_content[:10000] + "..."
            
            prompt = f"""
            You are an AI assistant helping to heal a failed web element selector.
            
            Failed selector: {failed_selector}
            Current page URL: {page_url}
            
            HTML Content (truncated):
            {page_content}
            
            Task: Find the element that matches the failed selector intent.
            Priority order: 1. id 2. name 3. aria-label 4. button text
            
            Return ONLY a valid CSS selector or XPath. No explanations.
            Examples: "button[type='submit']", "button:has-text('Submit')", "#submit-btn"
            """
            print(f"Prompt: {prompt}")

            # Call Ollama API - Use faster model with lower timeout
            response = requests.post(
                'http://172.27.13.150:11434/api/generate',
                json={
                    'model': 'llama2',  # Use faster model
                    'prompt': prompt,
                    'stream': False
                },
                timeout=(10, 500)
            )
        
            try:
                response_json = response.json()
                print(response_json)
                if response.status_code == 200:
                    result = response_json
                    # The AI response is a plain string containing the selector
                    ai_response_text = result['response'].strip()
                    
                    print(f"[Mistral AI] Generated selector: {ai_response_text}")
                    
                    return ai_response_text if ai_response_text else None
                else:
                    print(f"[Mistral AI] API call failed: {response.status_code}")
                    return None
            except Exception as e:
                print(f"Error parsing response: {e}")
                print(f"Response text: {response.text}")
                return None
                
        except Exception as e:
            print(f"[Mistral AI] Error calling Mistral: {repr(e)}")
            return None

  
    def click(self, selector):
        page = self._get_page()
        try:
            locator = page.locator(selector)
            locator.wait_for(state="visible")
            locator.click()
            return
        except Exception:
            print(f"[SmartActions] Original selector failed: {selector}")
            
            # First try with Mistral AI
            mistral_healed = self.heal_with_mistral(selector)
            if mistral_healed:
                try:
                    print(f"[SmartActions] Trying Mistral AI healed selector: {mistral_healed}")
                    locator = page.locator(mistral_healed)
                    locator.wait_for(state="visible")
                    locator.click()
                    print(f"[SmartActions] Successfully clicked using Mistral AI selector!")
                    return
                except Exception as e:
                    print(f"[SmartActions] Mistral AI selector failed: {str(e)}")
            
            # Fallback to original AI engine
            print(f"[SmartActions] Falling back to traditional AI healing...")
            healed = AIEngine.heal_locator(page, selector)
            print(f"[SmartActions] Using traditional AI healed selector: {healed}")
            
            locator = page.locator(healed)
            locator.wait_for(state="visible")
            locator.click()
            print(f"[SmartActions] Successfully clicked using traditional AI selector!")
    
    def fill(self, selector, value):
        page = self._get_page()
        try:
            locator = page.locator(selector)
            locator.wait_for(state="visible")
            locator.fill(value)
            return
        except Exception:
            print(f"[SmartActions] Original selector failed: {selector}")

            # First try with Mistral AI
            mistral_healed = self.heal_with_mistral(selector)
            if mistral_healed:
                try:
                    print(f"[SmartActions] Trying Mistral AI healed selector: {mistral_healed}")
                    locator = page.locator(mistral_healed)
                    locator.wait_for(state="visible")
                    locator.fill(value)
                    print(f"[SmartActions] Successfully filled using Mistral AI selector!")
                    return
                except Exception as e:
                    print(f"[SmartActions] Mistral AI selector failed: {str(e)}")

            # Fallback to traditional AI healing
            print(f"[SmartActions] Falling back to traditional AI healing...")
            healed = AIEngine.heal_locator(page, selector)
            print(f"[SmartActions] Using traditional AI healed selector: {healed}")

            locator = page.locator(healed)
            locator.wait_for(state="visible")
            locator.fill(value)

    def locator(self, selector):
        try:
            page = self._get_page()
            locator = page.locator(selector)
            locator.wait_for(state="visible")
            return locator
        except Exception:
            print(f"[SmartActions] Original selector failed: {selector}")
            
            # Try with Mistral AI
            mistral_healed = self.heal_with_mistral(selector)
            if mistral_healed:
                try:
                    print(f"[SmartActions] Trying Mistral AI healed selector: {mistral_healed}")
                    page = self._get_page()
                    locator = page.locator(mistral_healed)
                    locator.wait_for(state="visible")
                    print(f"[SmartActions] Successfully located using Mistral AI selector!")
                    return locator
                except Exception as e:
                    print(f"[SmartActions] Mistral AI selector failed: {str(e)}")
            
            # Fallback to original AI engine
            print(f"[SmartActions] Falling back to traditional AI healing...")
            page = self._get_page()
            healed = AIEngine.heal_locator(page, selector)
            print(f"[SmartActions] Using traditional AI healed selector: {healed}")
            
            locator = page.locator(healed)
            locator.wait_for(state="visible")
            return locator

    def locatorMultipleElements(self, selector1, selector2=None, selector3=None):
        """
        Get multiple elements as a list.
        If selector2 is provided, returns nested elements from selector1.
        If selector2 is None, returns all elements matching selector1.
        
        Args:
            selector1: Primary selector to find parent elements
            selector2: Optional nested selector within each element
            
        Returns:
            List of inner text from matched elements
        """
        try:
            page = self._get_page()
            locator = page.locator(selector1)
            elements_list = []
            
            for i in range(locator.count()):
                try:
                    if selector2:
                        # Get nested element
                        nested_element1 = locator.nth(i).locator(selector2).first
                        text1 = nested_element1.inner_text()
                        if selector3:
                            nested_element2 = locator.nth(i).locator(selector3).first
                            text2 = nested_element2.inner_text()
                            text = f"{text1} - {text2}"
                        else:
                            text = text1
                    else:
                        # Get element directly
                        text = locator.nth(i).inner_text()
                    
                    elements_list.append(text)
                    print(f"[SmartActions] Element {i}: {text}")
                except Exception as e:
                    print(f"[SmartActions] Failed to extract element {i}: {str(e)}")
            
            print(f"[SmartActions] Extracted {len(elements_list)} elements")
            return elements_list
        except Exception as e:
            print(f"[SmartActions] Error in locatorMultipleElements: {str(e)}")
            return []

    def is_visible(self, selector):
        """
        Check if element is visible using the given selector
        """
        try:
            page = self._get_page()
            locator = page.locator(selector)
            # Use first() to get a single element and check visibility
            element = locator.first
            return element.is_visible()
        except Exception as e:
            print(f"[SmartActions] Error checking visibility for selector {selector}: {str(e)}")
            return False

    def press(self, key):
        """
        Press a keyboard key on the current page
        """
        try:
            page = self._get_page()
            page.press('body', key)
        except Exception as e:
            print(f"[SmartActions] Error pressing key {key}: {str(e)}")
            raise

    def hover(self, selector):
        """
        Hover over an element using the given selector
        """
        page = self._get_page()
        try:
            locator = page.locator(selector)
            locator.wait_for(state="visible")
            locator.hover()
        except Exception:
            print(f"[SmartActions] Original selector failed: {selector}")
            
            healed = AIEngine.heal_locator(page, selector)
            print(f"[SmartActions] Using healed selector: {healed}")
            
            locator = page.locator(healed)
            locator.wait_for(state="visible")
            locator.hover()
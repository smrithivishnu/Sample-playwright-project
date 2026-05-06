import json
import requests
from core.ai_engine import AIEngine

class SmartActions:

    def __init__(self, page):
        self.page = page

    def heal_with_mistral(self, failed_selector):
        """
        Use Mistral model via Ollama to analyze the page and find the element.
        """
        try:
            # Get page content and current state
            page_content = self.page.content()
            page_url = self.page.url
            
            # Extract only body content to reduce prompt size
            import re
            body_match = re.search(r'<body[^>]*>(.*?)</body>', page_content, re.DOTALL | re.IGNORECASE)
            if body_match:
                page_content = body_match.group(1)
            else:
                # Fallback to full content if body tag not found
                page_content = page_content
            
            # Take a screenshot for visual context
            screenshot = self.page.screenshot()
            
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
                    'model': 'llama3:8b',  # Use faster model
                    'prompt': prompt,
                    'stream': False
                },
                timeout=120  # Reduced timeout for faster response
            )
            print("=========== full resp===============")
            print(response.json())
            print("=========== full resp===============")
            if response.status_code == 200:
                result = response.json()
                ai_response = json.loads(result['response'])
                
                print(f"[Mistral AI] Analysis: {ai_response.get('analysis', 'No analysis provided')}")
                print(f"[Mistral AI] New selector: {ai_response.get('new_selector', 'No selector generated')}")
                print(f"[Mistral AI] Confidence: {ai_response.get('confidence', 0)}")
                print(f"[Mistral AI] Explanation: {ai_response.get('explanation', 'No explanation provided')}")
                
                return ai_response.get('new_selector')
            else:
                print(f"[Mistral AI] API call failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"[Mistral AI] Error calling Mistral: {str(e)}")
            return None

    def click(self, selector):
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible")
            locator.click()
        except Exception:
            print(f"[SmartActions] Original selector failed: {selector}")
            
            # First try with Mistral AI
            mistral_healed = self.heal_with_mistral(selector)
            if mistral_healed:
                try:
                    print(f"[SmartActions] Trying Mistral AI healed selector: {mistral_healed}")
                    locator = self.page.locator(mistral_healed)
                    locator.wait_for(state="visible")
                    locator.click()
                    print(f"[SmartActions] Successfully clicked using Mistral AI selector!")
                    return
                except Exception as e:
                    print(f"[SmartActions] Mistral AI selector failed: {str(e)}")
            
            # # Fallback to original AI engine
            # print(f"[SmartActions] Falling back to traditional AI healing...")
            # healed = AIEngine.heal_locator(self.page, selector)
            # print(f"[SmartActions] Using traditional AI healed selector: {healed}")
            
            # locator = self.page.locator(healed)
            # locator.wait_for(state="visible")
            # locator.click()
            # print(f"[SmartActions] Successfully clicked using traditional AI selector!")

    def fill(self, selector, value):
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible")
            locator.fill(value)
        except Exception:
            healed = AIEngine.heal_locator(self.page, selector)

            print(f"[AI] Using healed selector: {healed}")

            locator = self.page.locator(healed)
            locator.wait_for(state="visible")
            locator.fill(value)

    def locator(self, selector):
        try:
            locator = self.page.locator(selector)
            locator.wait_for(state="visible")
            return locator
        except Exception:
            print(f"[SmartActions] Original selector failed: {selector}")
            
            # Try with Mistral AI
            mistral_healed = self.heal_with_mistral(selector)
            if mistral_healed:
                try:
                    print(f"[SmartActions] Trying Mistral AI healed selector: {mistral_healed}")
                    locator = self.page.locator(mistral_healed)
                    locator.wait_for(state="visible")
                    print(f"[SmartActions] Successfully located using Mistral AI selector!")
                    return locator
                except Exception as e:
                    print(f"[SmartActions] Mistral AI selector failed: {str(e)}")
            
            # Fallback to original AI engine
            # print(f"[SmartActions] Falling back to traditional AI healing...")
            # healed = AIEngine.heal_locator(self.page, selector)
            # print(f"[SmartActions] Using traditional AI healed selector: {healed}")
            
            # locator = self.page.locator(healed)
            # locator.wait_for(state="visible")
            # return locator
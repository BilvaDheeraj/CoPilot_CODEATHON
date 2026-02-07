import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

class LLMClient:
    def __init__(self):
        # Default to a mock if no key, or use Google Gemini if key exists
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            self.llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=api_key,
                temperature=0.7,
                max_retries=0
            )
        else:
            self.llm = None

    async def generate_response(self, system_prompt: str, user_input: str) -> str:
        # Fallback if no LLM configured
        if not self.llm:
            return self._generate_mock_response(system_prompt, user_input)
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input),
        ]
        try:
            # Set a timeout for the API call to prevent hanging
            response = await self.llm.ainvoke(messages, config={"timeout": 5})
            return response.content
        except Exception as e:
            # Log error and fallback to mock
            print(f"LLM Error (Timeout/Quota): {e}. Falling back to mock.")
            return self._generate_mock_response(system_prompt, user_input, error_msg=str(e))

    def _generate_mock_response(self, system_prompt: str, user_input: str, error_msg: str = None) -> str:
        import random
        
        base_mock = f"[MOCK RESP] System: {system_prompt} \n User: {user_input}"
        if error_msg:
             base_mock += f"\n[NOTE: AI failed ({error_msg}). Used Mock.]"
        
        system_prompt_lower = system_prompt.lower()
        
        # Mock Questions
        if "question" in system_prompt_lower:
            if "star method" in system_prompt_lower: # Behavioural
                questions = [
                    "Tell me about a time you handled a difficult situation with a coworker.",
                    "Describe a project where you had to meet a tight deadline.",
                    "Give me an example of a time you failed and what you learned from it.",
                    "Tell me about a time you showed leadership skills.",
                    "Describe a conflict you had with a supervisor and how you resolved it.",
                    "Tell me about a time you had to learn a new technology quickly.",
                    "Describe a situation where you had to persuade someone to see things your way.",
                    "Give an example of a goal you reached and tell me how you achieved it.",
                    "Tell me about a time you made a mistake at work. How did you handle it?",
                    "Describe a time when you went above and beyond for a project."
                ]
                return random.choice(questions)
            elif "logical" in system_prompt_lower: # Logical
                questions = [
                    "If you have a 3-gallon jug and a 5-gallon jug, how do you measure exactly 4 gallons?",
                    "A prompt appears on screen. Valid or Invalid? Explain your reasoning.",
                    "Find the next number in the sequence: 2, 6, 12, 20, 30, ...",
                    "You have 8 balls, one is heavier. How many weighings to find it with a balance scale?",
                    "Explain how you would debug a crash that only happens on production.",
                    "Three light bulbs are in a room. You are outside with 3 switches. You can only enter once. How do you know which switch controls which bulb?",
                    "A man looks at a picture and says 'Brothers and sisters I have none, but that man's father is my father's son.' Who is in the picture?",
                    "If 5 machines take 5 minutes to make 5 widgets, how long would it take 100 machines to make 100 widgets?",
                    "You have two ropes that burn in exactly one hour. They are non-uniform. How do you measure 45 minutes?",
                    "Why are manhole covers round?"
                ]
                return random.choice(questions)
            elif "aptitude" in system_prompt_lower: # Aptitude
                questions = [
                    "If a train creates a delay of 5 minutes every hour, how late is it after 12 hours?",
                    "What is 15% of 80?",
                    "A car travels 60mph for 2 hours, then 30mph for 1 hour. What is the average speed?",
                    "If x + y = 10 and x - y = 2, what is x * y?",
                    "A work costs $100. If price increases by 10% then decreases by 10%, what is final price?",
                    "The sum of two numbers is 25 and their difference is 13. Find their product.",
                    "A train 120 meters long produces a delay of 5 minutes every 2 hours... (Wait, simpler query): A train 240m long passes a pole in 24 seconds. How long will it take to pass a platform 650m long?",
                    "If the radius of a circle is increased by 50%, what is the percentage increase in its area?",
                    "A and B can do a piece of work in 12 days. B and C in 15 days. C and A in 20 days. How long would A take separately?",
                    "What is the probability of getting at least one head when tossing 3 coins?"
                ]
                return random.choice(questions)
            else:
                return "Tell me about yourself."

        # Mock Evaluation
        if "evaluate" in system_prompt_lower:
             import json
             scores = {
                 "situation": random.randint(3, 5),
                 "task": random.randint(3, 5),
                 "action": random.randint(2, 5),
                 "result": random.randint(3, 5),
                 "feedback": random.choice([
                     "Good structure, but could be more specific on the result.",
                     "Excellent use of STAR method.",
                     "Action was clear, but the situation needed more context.",
                     "Result was impressive but try to quantify it next time.",
                     "Solid answer, good communication skills."
                 ])
             }
             if "correctness" in system_prompt_lower: # Logical/Aptitude
                 scores = {
                     "correctness": random.randint(3, 5),
                     "logic_quality": random.randint(3, 5),
                     "feedback": random.choice(["Logically sound.", "Correct answer but steps were unclear.", "Good approach."])
                 }
                 
             return json.dumps(scores)
             
        return base_mock

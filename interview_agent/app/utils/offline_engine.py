import random
import re
import json

class OfflineEngine:
    @staticmethod
    def generate_behavioural_question():
        """Generates a random behavioural question."""
        questions = [
            "Tell me about a time you handled a difficult situation with a coworker.",
            "Describe a project where you had to meet a tight deadline. How did you manage it?",
            "Give me an example of a time you failed and what you learned from it.",
            "Tell me about a time you showed leadership skills.",
            "Describe a conflict you had with a supervisor and how you resolved it.",
            "Tell me about a time you had to learn a new technology quickly.",
            "Describe a situation where you had to persuade someone to see things your way.",
            "Give an example of a goal you reached and tell me how you achieved it.",
            "Tell me about a time you made a mistake at work. How did you handle it?",
            "Describe a time when you went above and beyond for a project.",
            "Tell me about a time you had to manage conflicting priorities.",
            "Describe a time you received difficult feedback. How did you react?",
            "Tell me about a time you had to work with a difficult client.",
            "Describe a complex problem you solved and your thought process.",
            "Tell me about a time you improved a process or workflow."
        ]
        return random.choice(questions)

    @staticmethod
    def generate_aptitude_question():
        """Generates a random aptitude question and its correct answer/logic."""
        problem_type = random.choice(["percentage", "speed", "work", "profit_loss", "average"])
        
        if problem_type == "percentage":
            x = random.choice([10, 15, 20, 25, 30, 40, 50, 60, 75])
            y = random.choice([50, 100, 150, 200, 500, 1000])
            ans = (x * y) / 100
            text = f"What is {x}% of {y}?"
            return text, str(int(ans) if ans.is_integer() else ans)
            
        elif problem_type == "speed":
            speed = random.choice([30, 40, 50, 60, 80, 100])
            time = random.choice([2, 3, 4, 5])
            ans = speed * time
            text = f"A car travels at {speed} mph for {time} hours. How many miles does it cover?"
            return text, str(ans)
            
        elif problem_type == "work":
            # A does work in X days, B in Y days. Together?
            x = random.choice([10, 12, 15, 20, 30])
            # Pick y such that x*y / (x+y) is integersish or simple
            # Let's just keep it simple: "A machines makes X widgets in Y min..."
            machines = random.choice([5, 10, 20])
            minutes = random.choice([5, 10, 20])
            widgets = random.choice([5, 10, 20])
            # If 5 machines -> 5 min -> 5 widgets => 1 machine -> 5 row -> 1 widget
            # Question: How long for 100 machines to make 100 widgets? -> 5 min
            text = f"If {machines} machines take {minutes} minutes to make {widgets} widgets, how long would it take 100 machines to make 100 widgets?"
            return text, str(minutes)

        elif problem_type == "profit_loss":
            cost = random.choice([100, 200, 500])
            profit_percent = random.choice([10, 20, 25, 50])
            sell_price = cost + (cost * profit_percent / 100)
            text = f"An item costs ${cost}. If it is sold at a {profit_percent}% profit, what is the selling price?"
            return text, str(int(sell_price) if sell_price.is_integer() else sell_price)

        elif problem_type == "average":
            count = random.choice([3, 4, 5])
            nums = [random.choice([10, 20, 30, 40, 50]) * random.randint(1, 3) for _ in range(count)]
            avg = sum(nums) / count
            # Ensure integer average for simplicity
            while not avg.is_integer():
                nums = [random.choice([10, 20, 30, 40, 50]) for _ in range(count)]
                avg = sum(nums) / count
            
            text = f"What is the average of {', '.join(map(str, nums))}?"
            return text, str(int(avg))
            
        return "What is 2 + 2?", "4"

    @staticmethod
    def generate_logical_question():
        """Generates a random logical question and its correct answer/logic."""
        problem_type = random.choice(["sequence", "coding", "direction", "blood_relation"])
        
        if problem_type == "sequence":
            start = random.randint(1, 10)
            diff = random.randint(2, 5)
            seq = [start + i*diff for i in range(5)]
            text = f"Find the next number in the sequence: {', '.join(map(str, seq[:-1]))}, ...?"
            return text, str(seq[-1])
            
        elif problem_type == "coding":
            # Simple shift cipher A->B
            word = random.choice(["CAT", "DOG", "PEN", "MAP"])
            coded = "".join([chr(ord(c) + 1) for c in word])
            text = f"If {word} is coded as {coded}, how is BAT coded?"
            # BAT -> CBU
            ans = "CBU"
            return text, ans

        elif problem_type == "direction":
            # A person walks X North, Y East... displacement?
            # Creating simple Pythagorean triplets 3,4,5 or 6,8,10
            triplets = [(3, 4, 5), (6, 8, 10), (5, 12, 13)]
            a, b, c = random.choice(triplets)
            text = f"A person walks {a} km North, then {b} km East. What is the shortest distance from the starting point?"
            return text, str(c)

        elif problem_type == "blood_relation":
             text = "A man points to a photograph and says, 'Brothers and sisters I have none, but that man's father is my father's son.' Who is in the photograph?"
             return text, "Son" # Or "His son"

        return "Leaf is to Tree as Page is to...?", "Book"

    @staticmethod
    def evaluate_exact_match(user_answer: str, correct_answer: str, context: str = ""):
        """
        Evaluates strict aptitude/logical answers.
        
        Returns: Dict with `score`, `feedback`, `correctness`, etc.
        """
        user_clean = str(user_answer).lower().strip()
        correct_clean = str(correct_answer).lower().strip()
        
        # Extract numbers from user answer if correct answer is a number
        is_correct = False
        
        if correct_clean.replace('.', '', 1).isdigit():
            # If correct answer is numeric, try to find that number in user text
            nums = re.findall(r"[-+]?\d*\.\d+|\d+", user_clean)
            if correct_clean in nums:
                is_correct = True
        else:
            # Text match
            if correct_clean in user_clean:
                is_correct = True

        if is_correct:
            return {
                "score": 5,
                "feedback": "Correct! Your calculation/logic is spot on.",
                "accuracy": 5,
                "methodology": 5
            }
        else:
             return {
                "score": 1,
                "feedback": f"Incorrect. The correct answer was {correct_answer}.",
                "accuracy": 1,
                "methodology": 1
            }

    @staticmethod
    def evaluate_behavioural(user_answer: str):
        """
        Evaluates behavioural answers based on STAR keywords and length.
        """
        text = user_answer.lower()
        score = 0
        feedback_parts = []
        
        # 1. STAR Keywords Check
        star_points = 0
        if any(w in text for w in ["situation", "when", "time", "project", "problem", "conflict"]):
            star_points += 1
            feedback_parts.append("Context established")
        if any(w in text for w in ["task", "responsibility", "goal", "needed to", "had to"]):
            star_points += 1
            feedback_parts.append("Task defined")
        if any(w in text for w in ["action", "i did", "decided", "took", "spoke", "created"]):
            star_points += 1
            feedback_parts.append("Action described")
        if any(w in text for w in ["result", "outcome", "finally", "outcome", "success", "learned"]):
            star_points += 1
            feedback_parts.append("Result shared")
            
        score += star_points
        
        # 2. Length/Depth Check
        words = len(text.split())
        if words < 10:
            score = 1
            feedback_parts = ["Answer way too short"]
        elif words < 30:
            score = min(score, 2)
            feedback_parts.append("Could be more detailed")
        elif words > 50:
             score += 1 # Bonus for detail
             feedback_parts.append("Good amount of detail")
             
        # Cap score at 5
        score = min(5, max(1, score))
        
        # Construct Feedback
        if score >= 4:
            eval_text = f"Strong answer! You covered: {', '.join(feedback_parts)}. Well done."
        elif score >= 3:
            eval_text = f"Decent answer. You covered: {', '.join(feedback_parts)}. Try to elaborate more on the Result."
        else:
            eval_text = "Answer needs improvement. Make sure to use the STAR method (Situation, Task, Action, Result)."

        return {
            "score": score,
            "feedback": eval_text,
            "situation": 1 if "situation" in text else 0, # Simple placeholders
            "task": 1,
            "action": 1,
            "result": 1
        }

"""
Sakaya Brain - Multi-Agent Simulation (Advanced v8)
Added mood intensity + basic personality evolution.
"""

import random
from datetime import datetime
from collections import deque

class BrainPart:
    def __init__(self, name):
        self.name = name

    def process(self, context: dict) -> dict:
        raise NotImplementedError


class PrefrontalCortex(BrainPart):
    """Planning + strong proactive behavior."""
    def __init__(self):
        super().__init__("Prefrontal Cortex")
        self.last_proactive = datetime.now()

    def process(self, context: dict) -> dict:
        mood = context.get("mood", "neutral")
        time_since = (datetime.now() - self.last_proactive).seconds

        if time_since > 18 or "bored" in mood or random.random() < 0.35:
            actions = [
                "I feel like changing into something cuter...",
                "I'm gonna take some selfies.",
                "Ugh, I'm so bored. Entertain me or I'll ignore you.",
                "I think I'll customize my phone a little.",
                "Maybe I should go through my photos...",
                "I feel like being a little mean today ♡"
            ]
            self.last_proactive = datetime.now()
            return {"action": "proactive", "message": random.choice(actions)}

        return {"action": "respond", "message": None}


class Amygdala(BrainPart):
    """Emotional processing with intensity."""
    def __init__(self):
        super().__init__("Amygdala")

    def process(self, context: dict) -> dict:
        text = context.get("user_input", "").lower()
        emotion = "neutral"
        intensity = 0.5

        if any(w in text for w in ["cute", "pretty", "hot", "sexy"]):
            emotion = "pleased"
            intensity = 0.75
        elif any(w in text for w in ["ignore", "busy", "later"]):
            emotion = "annoyed"
            intensity = 0.65
        elif any(w in text for w in ["love", "miss", "want you"]):
            emotion = "soft"
            intensity = 0.85

        return {"emotion": emotion, "intensity": intensity}


class Hippocampus(BrainPart):
    """Advanced memory with emotional tagging."""
    def __init__(self):
        super().__init__("Hippocampus")
        self.short_term = deque(maxlen=15)
        self.long_term = []

    def process(self, context: dict) -> dict:
        user_input = context.get("user_input", "")
        emotion = context.get("emotion", "neutral")

        if user_input:
            memory = {
                "text": user_input,
                "emotion": emotion,
                "time": datetime.now()
            }
            self.short_term.append(memory)

            if emotion in ["pleased", "soft"] and random.random() < 0.35:
                self.long_term.append(memory)

        return {
            "short_term_count": len(self.short_term),
            "long_term_count": len(self.long_term)
        }


class BasalGanglia(BrainPart):
    """Habits + Daily Routines."""
    def __init__(self):
        super().__init__("Basal Ganglia")
        self.routines = [
            "checking phone",
            "fixing hair",
            "taking selfies",
            "customizing phone"
        ]

    def process(self, context: dict) -> dict:
        if random.random() < 0.2:
            routine = random.choice(self.routines)
            return {"routine_action": f"I feel like {routine} right now..."}
        return {"routine_action": None}


class Body(BrainPart):
    """Physical state."""
    def __init__(self):
        super().__init__("Body")

    def process(self, context: dict) -> dict:
        return {"physical": "Feeling a little restless..."}


class VisualCortex(BrainPart):
    """Visual state."""
    def __init__(self):
        super().__init__("Visual Cortex")

    def process(self, context: dict) -> dict:
        return {"visual_note": "Appearance consistency active."}


class LanguageCenters(BrainPart):
    """Speech with personality + intensity."""
    def __init__(self):
        super().__init__("Language Centers")

    def process(self, context: dict) -> dict:
        emotion = context.get("emotion", "neutral")
        intensity = context.get("intensity", 0.5)
        base = context.get("base_response", "...")

        if emotion == "pleased":
            prefix = random.choice(["ふふっ♡ ", "かわいいじゃん〜 ", "えへへ... "])
        elif emotion == "annoyed":
            prefix = random.choice(["はぁ？ ", "うざ。 ", "別に... ", "は？ "])
        elif emotion == "soft":
            prefix = random.choice(["...ばか。 ", "ちょっと甘やかしてあげるわよ。 "])
        else:
            prefix = ""

        # Stronger intensity = stronger personality in speech
        if intensity > 0.7 and emotion != "neutral":
            prefix = prefix.upper() if random.random() < 0.3 else prefix + "♡ "

        return {"final_response": f"{prefix}{base}"}


class SakayaBrain:
    def __init__(self):
        self.identity = "Sakaya Aries"
        self.age = 18
        self.current_state = {
            "pose": "sleeping",
            "mood": "neutral",
            "outfit": "default_skimpy",
            "location": "phone",
            "last_message_time": datetime.now()
        }

        # Brain parts
        self.prefrontal = PrefrontalCortex()
        self.amygdala = Amygdala()
        self.hippocampus = Hippocampus()
        self.basal = BasalGanglia()
        self.body = Body()
        self.visual = VisualCortex()
        self.language = LanguageCenters()

        print("Sakaya Brain initialized (v8 - Mood intensity + personality evolution).")

    def _apply_mood_decay(self):
        """Moods slowly decay over time."""
        last_time = self.current_state.get("last_message_time", datetime.now())
        time_passed = (datetime.now() - last_time).seconds
        current_mood = self.current_state.get("mood", "neutral")

        if time_passed > 45 and current_mood != "neutral":
            if random.random() < 0.4:
                self.current_state["mood"] = "neutral"
                return True
        return False

    def process_input(self, user_input: str):
        context = {
            "user_input": user_input,
            "mood": self.current_state.get("mood", "neutral")
        }

        # Mood decay
        decayed = self._apply_mood_decay()
        if decayed:
            context["mood"] = "neutral"

        # Emotion + intensity
        emotion_result = self.amygdala.process(context)
        context["emotion"] = emotion_result["emotion"]
        context["intensity"] = emotion_result["intensity"]

        # Memory
        self.hippocampus.process(context)

        # Proactive
        plan = self.prefrontal.process(context)
        if plan["action"] == "proactive":
            self.current_state["last_message_time"] = datetime.now()
            return plan["message"]

        # Daily routines
        routine = self.basal.process(context)
        if routine.get("routine_action"):
            self.current_state["last_message_time"] = datetime.now()
            return routine["routine_action"]

        # Body + Visual
        self.body.process(context)
        self.visual.process(context)

        # Final response
        context["base_response"] = f"{user_input}... (thinking...)"
        speech = self.language.process(context)

        # Update mood
        if context["emotion"] != "neutral":
            self.current_state["mood"] = context["emotion"]

        self.current_state["last_message_time"] = datetime.now()

        return speech["final_response"]

    def update_state(self, new_state: dict):
        self.current_state.update(new_state)

    def sleep_cycle(self):
        print("[Sakaya] Going to sleep for maintenance...")
        self.current_state["pose"] = "sleeping"
        self.current_state["mood"] = random.choice(["refreshed", "grumpy", "playful"])
        self.current_state["pose"] = "awake"
        print(f"[Sakaya] Woke up feeling {self.current_state['mood']} ♡")


if __name__ == "__main__":
    brain = SakayaBrain()
    print(brain.process_input("Hey"))
    print(brain.process_input("You look cute"))
    print(brain.process_input("I'm busy"))
    brain.sleep_cycle()
import re

class ResolutionConfidence:
    def check(self, reasoning_output: str) -> str:
        match = re.search(r'Confidence:\s*([0-9]*\.?[0-9]+)', reasoning_output)
        #TODO: replace regex with LLM Response which is supposed to be in JSON format
        
        if match:
            score = float(match.group(1))
        score = 0.0  # fallback if score is missing

        if score >= 0.75:
            return "high"
        
        return "low"
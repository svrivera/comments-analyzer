import re
from typing import List, Set, Tuple

class TextProcessor:
    def __init__(self):
        self.negation_words = {
            'not', 'no', "n't", 'never', 'nothing', 'nowhere', 'noone', 'none', 'dont',
            'cant', 'wont', 'shouldnt', 'wouldnt', 'couldnt', 'hasnt', 'havent', 'hadnt'
        }
        
    def tokenize(self, text: str) -> List[str]:
        """Convert text to lowercase and split into words."""
        return re.findall(r'\b\w+\b', text.lower())
        
    def get_ngrams(self, tokens: List[str], n: int = 2) -> List[Tuple[str, ...]]:
        """Generate n-grams from tokens."""
        return list(zip(*[tokens[i:] for i in range(n)]))
        
    def handle_negations(self, tokens: List[str]) -> List[str]:
        """Handle negations in text by marking following words."""
        processed = []
        negate = False
        
        for token in tokens:
            if token in self.negation_words:
                negate = True
                processed.append(token)
                continue
                
            if negate:
                processed.append(f"NOT_{token}")
            else:
                processed.append(token)
                
            # Reset negation after punctuation or after 3 words
            if len(processed) >= 3 and negate:
                negate = False
                
        return processed
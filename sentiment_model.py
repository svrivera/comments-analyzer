import re

class SentimentAnalyzer:
    def __init__(self):
        self.positive_words = {
            'good', 'great', 'awesome', 'excellent', 'happy',
            'love', 'wonderful', 'fantastic', 'nice', 'best',
            'amazing', 'perfect', 'beautiful', 'thank', 'thanks',
            'helpful', 'positive', 'recommend', 'recommended'
        }
        
    def analyze_comments(self, comments):
        if not comments:
            return 0.0
            
        total_positive = 0
        
        for comment in comments:
            words = set(re.findall(r'\w+', comment.lower()))
            if words & self.positive_words:
                total_positive += 1
                
        return (total_positive / len(comments)) * 100

# Example usage
if __name__ == "__main__":
    analyzer = SentimentAnalyzer()
    
    test_comments = [
        "This is really good!",
        "I don't like this at all",
        "Great experience, very helpful",
        "Could be better",
        "Absolutely fantastic service!"
    ]
    
    result = analyzer.analyze_comments(test_comments)
    print(f"Positive sentiment: {result:.1f}%")
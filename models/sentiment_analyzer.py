import statistics
from typing import List, Dict, Union
from data.sentiment_lexicon import SENTIMENT_LEXICON
from utils.text_processor import TextProcessor

class EnhancedSentimentAnalyzer:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.lexicon = SENTIMENT_LEXICON
        
    def _calculate_comment_score(self, comment: str) -> float:
        """Calculate sentiment score for a single comment."""
        tokens = self.text_processor.tokenize(comment)
        processed_tokens = self.text_processor.handle_negations(tokens)
        
        scores = []
        for token in processed_tokens:
            if token.startswith('NOT_'):
                # Invert sentiment for negated words
                base_word = token[4:]
                if base_word in self.lexicon:
                    scores.append(-1 * self.lexicon[base_word])
            elif token in self.lexicon:
                scores.append(self.lexicon[token])
                
        if not scores:
            return 0.0
            
        # Use weighted average with more emphasis on stronger sentiments
        weighted_scores = [score * abs(score) for score in scores]
        return statistics.mean(weighted_scores) if weighted_scores else 0.0
        
    def analyze_comments(self, comments: List[str]) -> Dict[str, Union[float, List[float]]]:
        """Analyze an array of comments and return detailed sentiment metrics."""
        if not comments:
            return {
                'positive_percentage': 0.0,
                'average_sentiment': 0.0,
                'sentiment_distribution': [],
                'confidence_score': 0.0
            }
            
        comment_scores = [self._calculate_comment_score(comment) for comment in comments]
        
        # Calculate metrics
        positive_comments = sum(1 for score in comment_scores if score > 0)
        average_sentiment = statistics.mean(comment_scores)
        
        # Calculate confidence based on sentiment strength and consistency
        sentiment_std = statistics.stdev(comment_scores) if len(comment_scores) > 1 else 0
        confidence_score = (abs(average_sentiment) / 5.0) * (1 - (sentiment_std / 10))
        
        return {
            'positive_percentage': (positive_comments / len(comments)) * 100,
            'average_sentiment': average_sentiment,
            'sentiment_distribution': comment_scores,
            'confidence_score': min(max(confidence_score * 100, 0), 100)
        }

# Example usage
if __name__ == "__main__":
    analyzer = EnhancedSentimentAnalyzer()
    
    test_comments = [
        "This product is absolutely amazing and works perfectly!",
        "I don't like this at all, it's very disappointing",
        "The service was great but the price is a bit expensive",
        "Not bad, but could be better",
        "This is the worst experience I've ever had",
        "While it's not perfect, I'm very satisfied with the results",
        "The customer support team was incredibly helpful and responsive"
    ]
    
    results = analyzer.analyze_comments(test_comments)
    print(f"\nAnalysis Results:")
    print(f"Positive Sentiment: {results['positive_percentage']:.1f}%")
    print(f"Average Sentiment Score: {results['average_sentiment']:.2f}")
    print(f"Confidence Score: {results['confidence_score']:.1f}%")
    print("\nSentiment Distribution:", 
          [f"{score:.2f}" for score in results['sentiment_distribution']])
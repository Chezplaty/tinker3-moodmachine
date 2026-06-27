# mood_analyzer.py
"""
Rule based mood analyzer for short text snippets.

This class starts with very simple logic:
  - Preprocess the text
  - Look for positive and negative words
  - Compute a numeric score
  - Convert that score into a mood label
"""

import re
import string
from typing import List, Dict, Tuple, Optional

from dataset import POSITIVE_WORDS, NEGATIVE_WORDS


class MoodAnalyzer:
    """
    A very simple, rule based mood classifier.
    """

    def __init__(
        self,
        positive_words: Optional[List[str]] = None,
        negative_words: Optional[List[str]] = None,
    ) -> None:
        # Use the default lists from dataset.py if none are provided.
        positive_words = positive_words if positive_words is not None else POSITIVE_WORDS
        negative_words = negative_words if negative_words is not None else NEGATIVE_WORDS

        # Store as sets for faster lookup.
        self.positive_words = set(w.lower() for w in positive_words)
        self.negative_words = set(w.lower() for w in negative_words)

    # ---------------------------------------------------------------------
    # Preprocessing
    # ---------------------------------------------------------------------

    def preprocess(self, text: str) -> List[str]:
        """
        Convert raw text into a list of tokens the model can work with.

        TODO: Improve this method.

        Right now, it does the minimum:
          - Strips leading and trailing whitespace
          - Converts everything to lowercase
          - Splits on spaces

        Ideas to improve:
          - Remove punctuation
          - Handle simple emojis separately (":)", ":-(", "🥲", "😂")
          - Normalize repeated characters ("soooo" -> "soo")
        """
        # Text emoticons to normalize before punctuation is stripped
        emoticon_map = {
            ":)": "happy", ":-)": "happy", ":D": "happy",
            ":(": "sad", ":-(": "sad",
            ":/": "unsure", ":-/": "unsure",
        }
        for emoticon, word in emoticon_map.items():
            text = text.replace(emoticon, f" {word} ")

        # Pull out Unicode emojis as their own tokens before punctuation removal
        emoji_pattern = re.compile(
            "[\U0001F600-\U0001F64F"   # emoticons
            "\U0001F300-\U0001F5FF"    # symbols & pictographs
            "\U0001F680-\U0001F6FF"    # transport & map
            "\U0001F900-\U0001F9FF"    # supplemental symbols
            "\U00002700-\U000027BF"    # dingbats
            "]+",
            flags=re.UNICODE,
        )
        emojis = emoji_pattern.findall(text)
        text = emoji_pattern.sub(" ", text)

        # Collapse runs of 3+ identical characters down to 2: "soooo" -> "soo"
        text = re.sub(r"(.)\1{2,}", r"\1\1", text)

        # Strip punctuation, lowercase, split
        text = text.translate(str.maketrans("", "", string.punctuation))
        tokens = text.strip().lower().split()

        # Append emoji tokens at the end (scored if added to dataset word lists)
        tokens.extend(emojis)
        return tokens

    # ---------------------------------------------------------------------
    # Scoring logic
    # ---------------------------------------------------------------------

    def score_text(self, text: str) -> Tuple[int, int]:
        """Returns (pos_score, neg_score) separately so mixed sentiment isn't lost."""
        # Apostrophes are stripped by preprocess, so "don't" becomes "dont"
        negation_words = {
            "not", "never", "no", "neither",
            "dont", "doesnt", "didnt", "wont", "cant", "couldnt", "shouldnt", "wouldnt",
        }
        emphasis_words = {"so", "very", "really", "extremely", "absolutely", "super", "totally"}

        tokens = self.preprocess(text)
        pos_score = 0
        neg_score = 0
        for i, token in enumerate(tokens):
            negated = i > 0 and tokens[i - 1] in negation_words
            emphasized = i > 0 and tokens[i - 1] in emphasis_words
            if token in self.positive_words:
                delta = -1 if negated else 1
                delta = delta * 2 if emphasized else delta
                if delta > 0:
                    pos_score += delta
                else:
                    neg_score += delta
            elif token in self.negative_words:
                delta = 1 if negated else -1
                delta = delta * 2 if emphasized else delta
                if delta < 0:
                    neg_score += delta
                else:
                    pos_score += delta
        return pos_score, neg_score

    # ---------------------------------------------------------------------
    # Label prediction
    # ---------------------------------------------------------------------

    def predict_label(self, text: str) -> str:
        """
        Turn the numeric score for a piece of text into a mood label.
        """
        pos, neg = self.score_text(text)
        if pos > 0 and neg < 0:
            return "mixed"
        elif pos > 0:
            return "positive"
        elif neg < 0:
            return "negative"
        else:
            return "neutral"

    # ---------------------------------------------------------------------
    # Explanations (optional but recommended)
    # ---------------------------------------------------------------------

    def explain(self, text: str) -> str:
        """
        Return a short string explaining WHY the model chose its label.

        TODO:
          - Look at the tokens and identify which ones counted as positive
            and which ones counted as negative.
          - Show the final score.
          - Return a short human readable explanation.

        Example explanation (your exact wording can be different):
          'Score = 2 (positive words: ["love", "great"]; negative words: [])'

        The current implementation is a placeholder so the code runs even
        before you implement it.
        """
        tokens = self.preprocess(text)

        positive_hits: List[str] = []
        negative_hits: List[str] = []
        score = 0

        for token in tokens:
            if token in self.positive_words:
                positive_hits.append(token)
                score += 1
            if token in self.negative_words:
                negative_hits.append(token)
                score -= 1

        return (
            f"Score = {score} "
            f"(positive: {positive_hits or '[]'}, "
            f"negative: {negative_hits or '[]'})"
        )

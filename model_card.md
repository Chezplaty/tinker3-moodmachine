# Model Card: Mood Machine

This model card is for the Mood Machine project, which includes **two** versions of a mood classifier:

1. A **rule based model** implemented in `mood_analyzer.py`
2. A **machine learning model** implemented in `ml_experiments.py` using scikit learn

You may complete this model card for whichever version you used, or compare both if you explored them.

## 1. Model Overview

**Model type:**  
I compared both models.

**Intended purpose:**  

The model is taking short text messages and based on certain words/phrases, identify the mood of the message.

**How it works (brief):**  
For the rule based version, describe the scoring rules you created.  

Some words are labeled as positive and others negative. For each message/post, the model goes through and either adds one or subtracts one depending on their label. Some words combined with others with cause a slightly different effect such as negation or emphasis. The total score determines what label the message is given.

For the ML version, describe how training works at a high level (no math needed).

The model looks at those word counts and learns which words tend to appear in "happy" posts, which in "sad" posts, etc. It adjusts internal weights for each word until its predictions match the true labels as closely as possible. The more times a word like "amazing" appears in posts labeled "happy," the more weight it gets toward predicting "happy."


## 2. Data

**Dataset description:**  
Summarize how many posts are in `SAMPLE_POSTS` and how you added new ones.

There are 16 sample posts and I had AI think of 5 and I thought of 5. I edited the ones AI put in if I thought they were too unrealistic/not really said by people.

**Labeling process:**  
Explain how you chose labels for your new examples.  
Mention any posts that were hard to label or could have multiple valid labels.

I chose labels based on how I would see it. Posts that were hard to label were ones that could either be mixed or neutral.

**Important characteristics of your dataset:**  
Examples you might include:  

- Contains slang or emojis  
- Includes sarcasm  
- Some posts express mixed feelings  
- Contains short or ambiguous messages

**Possible issues with the dataset:**  
Think about imbalance, ambiguity, or missing kinds of language.

There are definitely a lot of missing kinds of language. A lack of data is the biggest reason why the model tends to be inaccurate.

## 3. How the Rule Based Model Works (if used)

**Your scoring rules:**  
Describe the modeling choices you made.  
Examples:  

Positive and negative words increase and decrease the score by 1. Negation words would flip the score of the next word and add it. Emphasis would add an additional score to the word. Emojis were handled by translating them into words first. Words with repeating characters were cut to have a maxiumum to two consecutive repeating characters.

The threshold for score was the default > 0 positive, < 0 negative, and just 0 meant neutral. However two scores are kept, one tracking the positive and one the negative. If the postive and negative score equaled each other (its absolute value), the message would be labeled as mixed.

**Strengths of this approach:**  
Where does it behave predictably or reasonably well?

It behaves predictably on messages that are obviously positive or negative.

**Weaknesses of this approach:**  
Where does it fail?  

This approach does not catch sarcasm and unfamiliar slang as the model has no way to determine context.

## 4. How the ML Model Works (if used)

**Features used:**  
Describe the representation.  
Example: “Bag of words using CountVectorizer.”

**Training data:**  
The model trained on `SAMPLE_POSTS` and `TRUE_LABELS`.

**Training behavior:**  

More examples often lead to better accuracy

**Strengths and weaknesses:**  
Strengths might include learning patterns automatically.  
Weaknesses might include overfitting to the training data or picking up spurious cues.

## 5. Evaluation

**How you evaluated the model:**  
I ran both models against the 16 labeled posts in `dataset.py`. The rule-based model got 12/16 correct (75% accuracy). The ML model got 16/16 correct (100%), but that number is misleading because it trained and tested on the exact same data — it basically just memorized the posts rather than actually learning to generalize.

**Examples of correct predictions:**  
- "I love this class so much" → positive ✓ — "love" is directly in the positive word list, nothing complicated going on, both models handled it easily.
- "I am not happy about this" → negative ✓ — the rule-based model actually caught the negation here, which I was kind of surprised by. "not happy" flipped the score correctly.
- "Today was a terrible day" → negative ✓ — "terrible" is in the negative word list, pretty straightforward for both.

**Examples of incorrect predictions:**  
- "I absolutely love sitting in traffic for an hour 🙄" → rule-based predicted positive, true label is negative. This is sarcasm and the model had no way to know that. It saw "absolutely love" and just went positive. The ML model got it right, but only because it saw the label during training.
- "finally done with that project, I need a nap" → rule-based predicted neutral, true label is mixed. Neither "done" nor "nap" are in the word lists, so the model saw nothing to score and defaulted to neutral instead of picking up that there's relief + exhaustion happening.
- "feeling okay I guess, just tired" → rule-based predicted negative (just from "tired"), true label is mixed. It missed that "okay" softens everything. The model doesn't really understand hedging language like "I guess."

## 6. Limitations

Describe the most important limitations.  

- The dataset is small  
- The model does not generalize to longer posts  
- It cannot detect sarcasm reliably  
- It depends heavily on the words you chose or labeled
- It has no way to capture context


## 7. Ethical Considerations

Discuss any potential impacts of using mood detection in real applications.  

- Misclassifying a message expressing distress  
- Misinterpreting mood for certain language communities  
- Privacy considerations if analyzing personal messages

## 8. Ideas for Improvement

List ways to improve either model.  

- Add more labeled data  
- Use TF IDF instead of CountVectorizer  
- Add better preprocessing for emojis or slang  
- Use a small neural network or transformer model  
- Improve the rule based scoring method  
- Add a real test set instead of training accuracy only

from random import choice
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import defaultdict
import numpy as np
from dotenv import load_dotenv
import os
import math

load_dotenv()

class TwitterTarotReader:
    CARD_GROUPS = {
        'growth_and_potential': [
            'The Fool', 'Ace of Wands', 'Page of Wands', 'The Star', 
            'The World', 'The Magician'
        ],
        'leadership_and_authority': [
            'The Emperor', 'King of Wands', 'King of Swords',
            'The Chariot', 'Queen of Wands'
        ],
        'learning_and_wisdom': [
            'The Hierophant', 'The Hermit', 'Page of Swords',
            'The High Priestess', 'Queen of Swords'
        ],
        'transformation_and_change': [
            'Death', 'The Tower', 'The World', 'Judgement',
            'Six of Swords'
        ],
        'success_and_achievement': [
            'The Sun', 'Six of Wands', 'The World',
            'The Chariot', 'Ten of Wands'
        ],
        'challenges_and_obstacles': [
            'Five of Wands', 'Seven of Wands', 'Five of Swords',
            'The Tower', 'The Devil'
        ]
    }

    TAROT_CARDS = {
    "The Fool": {
        "meaning": "New beginnings, spontaneity, free spirit, potential.",
        "career_advice": "Take that leap into a new technology or role - your fresh perspective is valuable.",
    },
    "The Magician": {
        "meaning": "Manifestation, resourcefulness, power, inspired action.",
        "career_advice": "Time to showcase your technical skills and take initiative on projects.",
    },
    "The High Priestess": {
        "meaning": "Intuition, subconscious, mystery, divine femininity.",
        "career_advice": "Trust your instincts when solving complex problems.",
    },
    "The Empress": {
        "meaning": "Abundance, creativity, nurture, fertility.",
        "career_advice": "Nurture your team's growth and foster creative solutions.",
    },
    "The Emperor": {
        "meaning": "Authority, structure, stability, father figure.",
        "career_advice": "Establish strong coding standards and best practices.",
    },
    "The Hierophant": {
        "meaning": "Tradition, spirituality, guidance, education.",
        "career_advice": "Seek mentorship and share knowledge with others.",
    },
    "The Lovers": {
        "meaning": "Love, harmony, partnerships, alignment of values.",
        "career_advice": "Focus on team collaboration and partnership projects.",
    },
    "The Chariot": {
        "meaning": "Control, willpower, determination, success.",
        "career_advice": "Drive projects forward with clear technical direction.",
    },
    "Strength": {
        "meaning": "Courage, confidence, compassion, inner strength.",
        "career_advice": "Take on challenging technical problems with confidence.",
    },
    "The Hermit": {
        "meaning": "Introspection, solitude, inner guidance, reflection.",
        "career_advice": "Focus on deep work and independent projects.",
    },
    "Wheel of Fortune": {
        "meaning": "Luck, karma, cycles of life, turning points.",
        "career_advice": "Be ready to adapt to technological changes.",
    },
    "Justice": {
        "meaning": "Fairness, truth, law, accountability.",
        "career_advice": "Ensure code quality and ethical considerations.",
    },
    "The Hanged Man": {
        "meaning": "Pause, surrender, letting go, new perspective.",
        "career_advice": "Step back and review your technical approach.",
    },
    "Death": {
        "meaning": "Transformation, endings, new beginnings, transition.",
        "career_advice": "Time for major technical transitions or stack changes.",
    },
    "Temperance": {
        "meaning": "Balance, moderation, patience, harmony.",
        "career_advice": "Balance technical debt with new development.",
        "tech_focus": "Optimize system integration and compatibility."
    },
    "The Devil": {
        "meaning": "Addiction, materialism, entrapment, shadow self.",
        "career_advice": "Don't get trapped by outdated technologies.",
        "tech_focus": "Address technical debt and dependencies."
    },
    "The Tower": {
        "meaning": "Sudden change, upheaval, chaos, revelation.",
        "career_advice": "Be prepared for technical challenges and system failures.",
        "tech_focus": "Time to rebuild and refactor problematic systems."
    },
    "The Star": {
        "meaning": "Hope, inspiration, renewal, spirituality.",
        "career_advice": "Great time for learning and starting new projects.",
        "tech_focus": "Explore emerging technologies and innovative solutions."
    },
    "The Moon": {
        "meaning": "Illusion, fear, intuition, subconscious.",
        "career_advice": "Don't let imposter syndrome hold you back.",
        "tech_focus": "Look beyond surface-level solutions to find root causes."
    },
    "The Sun": {
        "meaning": "Positivity, success, joy, vitality.",
        "career_advice": "Your technical achievements will be recognized and celebrated.",
        "tech_focus": "Share your knowledge and contribute to open source."
    },
    "Judgement": {
        "meaning": "Reflection, reckoning, awakening, inner calling.",
        "career_advice": "Evaluate your technical journey and future direction.",
        "tech_focus": "Audit and improve your technical skills."
    },
    "The World": {
        "meaning": "Completion, accomplishment, travel, integration.",
        "career_advice": "Celebrate project completions and plan next challenges.",
        "tech_focus": "Integration and deployment of complete systems."
    },
    
    "Ace of Wands": {
        "meaning": "Inspiration, new opportunities, creativity, potential.",
        "career_advice": "Start new technical initiatives with enthusiasm.",
        "tech_focus": "Experiment with innovative technologies."
    },
    "Two of Wands": {
        "meaning": "Planning, progress, decisions, discovery.",
        "career_advice": "Plan your technical roadmap carefully.",
        "tech_focus": "Research and compare technical solutions."
    },
    "Ace of Swords": {
        "meaning": "Breakthrough, clarity, sharp mind, new ideas.",
        "career_advice": "Cut through technical complexity with clear thinking.",
        "tech_focus": "Focus on algorithmic problem-solving."
    },
    "Two of Swords": {
        "meaning": "Indecision, choices, stalemate, difficult decisions.",
        "career_advice": "Evaluate technical trade-offs carefully.",
        "tech_focus": "Compare competing technical solutions."
    }
    }

    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

    def get_similar_cards(self, card_name):
        """Return list of cards with similar traits"""
        similar_cards = []
        for group, cards in self.CARD_GROUPS.items():
            if card_name in cards:
                similar_cards.extend(cards)
        return list(set(similar_cards))  # Remove duplicates

    def select_card_from_group(self, primary_card):
        """Select either the primary card or a similar one randomly"""
        similar_cards = self.get_similar_cards(primary_card)
        if similar_cards:
            return choice(similar_cards)
        return primary_card

    def get_card_reading(self, card_name):
        """Get a reading for a card, potentially selecting from similar cards"""
        selected_card = self.select_card_from_group(card_name)
        return {
            "selected_card": selected_card,
            "reading": self.TAROT_CARDS[selected_card],
            "similar_cards": self.get_similar_cards(card_name)
        }

    def get_tweets(self, screenname):
        url = f"http://127.0.0.1:5000/user/tweets?username={screenname}"
        print(f"Fetching tweets for {screenname} from {url}")
        response = requests.get(url)
        print(f"Response status code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()

            if 'tweets' not in data or not data['tweets']:
                print("No tweets found in the response.")
                return []

            return [{
                'text': tweet.get('text', ''),
                'hashtags': [
                    word[1:] for word in tweet.get('text', '').split() 
                    if word.startswith('#')
                ],
                'views': tweet.get('views', 'Unknown'),
                'retweet_count': tweet.get('retweet_count', 0),
                'quote_count': tweet.get('quote_count', 0),
                'reply_count': tweet.get('reply_count', 0),
            } for tweet in data['tweets']]
        else:
            print(f"Error fetching tweets: {response.status_code}")
            raise Exception(f"Error fetching tweets: {response.status_code}")
 
        
    def analyze_personality(self, tweets):
        themes = defaultdict(int)
        sentiments = []
        
        theme_keywords = {
            # Professional Growth
            'technical_growth': {
                # Core Tech
                'code', 'programming', 'dev', 'data', 'ai', 'software', 'engineering', 'technology', 
                'coding', 'development',
                # Modern Tech Stack
                'machine learning', 'blockchain', 'cloud', 'devops', 'frontend', 'backend', 'fullstack',
                'python', 'javascript', 'typescript', 'react', 'node', 'kubernetes', 'docker',
                # Emerging Tech
                'web3', 'crypto', 'nft', 'artificial intelligence', 'neural networks', 'deep learning',
                'cybersecurity', 'iot', 'quantum', 'ar', 'vr', 'metaverse', 'generative ai'
            },
            'professional_development': {
                # Career
                'career', 'job', 'work', 'professional', 'business', 'industry', 'corporate', 
                'startup', 'entrepreneur', 'leadership', 'management',
                # Modern Workplace
                'remote work', 'hybrid', 'digital nomad', 'freelance', 'side hustle', 'passive income',
                'personal brand', 'networking', 'mentorship', 'career change', 'upskilling',
                # Business Focus
                'saas', 'b2b', 'b2c', 'product', 'marketing', 'sales', 'growth hacking',
                'venture capital', 'funding', 'bootstrapping', 'monetization', 'roi'
            },
            # Personal Growth
            'education': {
                # Traditional
                'learning', 'study', 'education', 'course', 'degree', 'university', 'college',
                'school', 'knowledge', 'skills', 'training', 'workshop',
                # Modern Learning
                'mooc', 'online course', 'bootcamp', 'certification', 'self-taught', 'tutorial',
                'documentation', 'learning path', 'roadmap', 'curriculum', 'mentoring',
                # Learning Platforms
                'udemy', 'coursera', 'edx', 'linkedin learning', 'pluralsight', 'codecademy'
            },
            'self_improvement': {
                # Growth
                'growth', 'goals', 'progress', 'improvement', 'development', 'motivation',
                'inspiration', 'success', 'achievement', 'mindset',
                # Modern Self-Help
                'productivity', 'time management', 'habit building', 'morning routine',
                'journaling', 'goal setting', 'accountability', 'personal development',
                # Mental Models
                'decision making', 'critical thinking', 'problem solving', 'cognitive bias',
                'systems thinking', 'first principles', 'mental models'
            },
            # Lifestyle & Interests
            'health_wellness': {
                # Physical Health
                'health', 'fitness', 'exercise', 'yoga', 'meditation', 'mindfulness', 'wellness',
                'nutrition', 'diet', 'mental health', 'self-care',
                # Modern Wellness
                'biohacking', 'intermittent fasting', 'keto', 'plant-based', 'supplements',
                'sleep optimization', 'recovery', 'stress management', 'immune system',
                # Mental Wellness
                'therapy', 'counseling', 'anxiety', 'depression', 'burnout', 'work-life balance',
                'digital wellbeing', 'mental fitness', 'emotional intelligence'
            },
            'creativity_arts': {
                # Traditional Arts
                'art', 'music', 'photography', 'writing', 'creative', 'design', 'drawing',
                'painting', 'dance', 'film', 'poetry', 'craft',
                # Digital Arts
                'digital art', 'graphic design', '3d modeling', 'animation', 'motion graphics',
                'ui design', 'ux design', 'web design', 'illustration', 'video editing',
                # Creative Tech
                'generative art', 'creative coding', 'procedural generation', 'digital sculpture',
                'virtual production', 'creative ai', 'nft art'
            },
            'travel_adventure': {
                # Travel
                'travel', 'adventure', 'explore', 'journey', 'wanderlust', 'vacation', 'trip',
                'destination', 'culture', 'experience',
                # Modern Travel
                'digital nomad', 'workation', 'slow travel', 'sustainable travel', 'local experience',
                'travel hacking', 'remote work travel', 'vanlife', 'backpacking',
                # Adventure Sports
                'hiking', 'camping', 'climbing', 'surfing', 'skydiving', 'scuba diving',
                'mountaineering', 'skiing', 'snowboarding'
            },
            # Social & Community
            'relationships': {
                # Personal
                'family', 'friends', 'relationship', 'love', 'partner', 'marriage', 'dating',
                'social', 'community', 'connection', 'support',
                # Modern Dating
                'online dating', 'dating apps', 'virtual dating', 'long distance', 'relationship goals',
                'conscious relationships', 'attachment styles', 'boundaries',
                # Community Building
                'community management', 'online communities', 'discord', 'slack', 'meetups',
                'networking events', 'mentorship', 'accountability partners'
            },
            'emotional_depth': {
                # Core Emotions
                'happy', 'joyful', 'delighted', 'elated', 'ecstatic', 'jubilant', 'cheerful', 'blissful',
                'content', 'pleased', 'thrilled', 'overjoyed', 'radiant', 'beaming', 'glowing', 'uplifted',
                'sad', 'melancholy', 'heartbroken', 'blue', 'down', 'depressed', 'gloomy', 'sorrowful',
                'grieving', 'mourning', 'tearful', 'hurting', 'devastated', 'lonely', 'hopeless', 'despair',
                'angry', 'frustrated', 'irritated', 'furious', 'outraged', 'enraged', 'bitter', 'resentful',
                'indignant', 'irate', 'hostile', 'annoyed', 'agitated', 'exasperated', 'livid', 'seething',
                
                # Complex Emotions
                'grateful', 'thankful', 'blessed', 'appreciative', 'moved', 'touched', 'humbled', 'honored',
                'indebted', 'recognized', 'valued', 'cherished', 'acknowledged', 'supported', 'seen', 'heard',
                'love', 'adore', 'cherish', 'treasure', 'devoted', 'smitten', 'passionate', 'affectionate',
                'tender', 'fond', 'warmth', 'caring', 'romantic', 'intimate', 'attached', 'connected',
                'excited', 'eager', 'anticipating', 'hopeful', 'optimistic', 'enthusiastic', 'motivated',
                'inspired', 'driven', 'ambitious', 'determined', 'focused', 'ready', 'energized',
                
                # Emotional Growth & Resilience
                'strong', 'resilient', 'brave', 'courageous', 'persevering', 'enduring', 'tenacious',
                'hardy', 'tough', 'unbreakable', 'steadfast', 'persistent', 'resolute', 'unwavering',
                'vulnerable', 'open', 'authentic', 'raw', 'honest', 'exposed', 'sensitive', 'fragile',
                'delicate', 'tender', 'emotional', 'genuine', 'transparent', 'real', 'true', 'unguarded',
                
                # Empathy & Connection
                'understanding', 'compassionate', 'empathetic', 'sympathetic', 'caring', 'kind',
                'considerate', 'thoughtful', 'nurturing', 'supportive', 'helping', 'comforting',
                'consoling', 'validating', 'accepting', 'embracing', 'bonded', 'close', 'united',
                'together', 'belonging', 'welcomed', 'understood',
                
                # Transformation & Healing
                'transforming', 'evolving', 'growing', 'changing', 'developing', 'progressing',
                'learning', 'improving', 'advancing', 'expanding', 'flourishing', 'thriving',
                'blooming', 'blossoming', 'emerging', 'becoming', 'healing', 'recovering', 'mending',
                'restoring', 'renewing', 'rebuilding', 'processing', 'overcoming', 'surviving',
                'coping', 'adapting', 'reconciling', 'accepting', 'forgiving', 'releasing',
                
                # Common Expression Words
                'feel', 'feeling', 'felt', 'emotion', 'mood', 'spirit', 'heart', 'soul',
                'mind', 'peace', 'calm', 'storm', 'light', 'dark', 'deep', 'shallow',
                'high', 'low', 'up', 'down', 'better', 'worse', 'good', 'bad',
                'positive', 'negative', 'intense', 'mild', 'strong', 'weak'
            },
            'social_causes': {
                # Traditional Causes
                'environment', 'sustainability', 'climate', 'social justice', 'equality',
                'diversity', 'inclusion', 'activism', 'volunteer',
                # Modern Movements
                'climate tech', 'renewable energy', 'zero waste', 'circular economy',
                'ethical consumption', 'fair trade', 'social impact', 'green tech',
                # Social Issues
                'mental health awareness', 'lgbtq+ rights', 'racial justice', 'gender equality',
                'accessibility', 'digital privacy', 'tech ethics', 'responsible ai'
            },
            # Entertainment & Media
            'entertainment': {
                # Traditional
                'movie', 'film', 'tv', 'show', 'series', 'game', 'gaming', 'book',
                'reading', 'literature', 'podcast', 'entertainment',
                # Modern Gaming
                'esports', 'streaming', 'twitch', 'youtube', 'content creation',
                'indie games', 'mobile gaming', 'vr gaming', 'game development',
                # Digital Media
                'streaming services', 'podcasting', 'audiobooks', 'digital content',
                'social media', 'influencer', 'creator economy', 'live streaming'
            },
            'sports': {
                # Traditional Sports
                'sports', 'football', 'basketball', 'soccer', 'tennis', 'athlete',
                'team', 'competition', 'fitness', 'workout',
                # Modern Sports
                'esports', 'fantasy sports', 'sports analytics', 'sports tech',
                'sports science', 'performance tracking', 'sports medicine',
                # Fitness Tech
                'wearables', 'fitness apps', 'smart equipment', 'virtual coaching',
                'connected fitness', 'fitness tracking', 'home gym'
            }
        }

        for tweet in tweets:
            text = tweet['text'].lower()
            # Sentiment analysis
            sentiment_scores = self.sentiment_analyzer.polarity_scores(text)
            sentiments.append(sentiment_scores['compound'])
            
            # Theme detection
            for theme, keywords in theme_keywords.items():
                if any(keyword in text for keyword in keywords):
                    themes[theme] += 1

        tweet_count = len(tweets)
        avg_sentiment = sum(sentiments)
        
        theme_distribution = {theme: count/tweet_count for theme, count in themes.items()}
        
        # Find dominant themes (top 3)
        sorted_themes = sorted(themes.items(), key=lambda x: x[1], reverse=True)
        dominant_themes = sorted_themes[:3] if sorted_themes else [('neutral', 0)]

        # Calculate personality indicators
        personality_indicators = {
            'growth_orientation': (themes['self_improvement'] + themes['education']),
            'social_engagement': (themes['relationships'] + themes['social_causes']),
            'emotional_expression': themes['emotional_depth'],
            'creativity_level': (themes['creativity_arts'] + themes['reflection']),
            'professional_focus': (themes['professional_development'] + themes['technical_growth']),
            'lifestyle_balance': (themes['health_wellness'] + themes['entertainment'] + themes['sports'])
        }
        
        # Enhanced emotional analysis
        emotional_analysis = {
            'positivity_ratio': len([s for s in sentiments if s > 0]),
            'emotional_volatility': np.std(sentiments),
            'emotional_depth': themes['emotional_depth']
        }

        return {
            'sentiment': {
                'average': avg_sentiment,
                'positivity_ratio': emotional_analysis['positivity_ratio'],
                'emotional_volatility': emotional_analysis['emotional_volatility']
            },
            'dominant_themes': [{'theme': theme, 'frequency': count/tweet_count} 
                            for theme, count in dominant_themes],
            'theme_distribution': theme_distribution,
            'personality_indicators': personality_indicators,
            'analysis_metadata': {
                'tweet_count': tweet_count,
                'unique_themes_detected': len([t for t in themes.values() if t > 0]),
                'engagement_diversity': len(themes) / len(theme_keywords)
            }
        }
    
    def fetch_user_details(self, username):
            """Fetch user details from the Twitter API."""
            url = "https://twitter154.p.rapidapi.com/user/details"
            querystring = {"username": username}  # Pass the username as a query parameter
            headers = {
                "x-rapidapi-host": os.environ.get("RAPIDAPI_HOST1"),
                "x-rapidapi-key": os.environ.get("RAPIDAPI_KEY1") # Replace with your RapidAPI key
            }

            try:
                response = requests.get(url, headers=headers, params=querystring)
                response.raise_for_status()  # Raise an exception for HTTP errors
                user_data = response.json()

                # Extract required fields
                user_details = {
                    "follower_count": user_data.get("follower_count", 0),
                    "number_of_tweets": user_data.get("number_of_tweets", 0)
                }
                return user_details

            except requests.exceptions.RequestException as e:
                print(f"Error fetching user details: {e}")
                return {"follower_count": 0, "number_of_tweets": 0}  # Return default values on error



    def select_tarot_card(self, analysis, user_scores, tweets, username):
        """Select appropriate tarot card based on a percentile ranking of cumulative scores."""
        sentiment = analysis.get('sentiment', {}).get('average', 0)
        dominant_theme = analysis.get('dominant_themes', [{}])[0].get('theme', 'neutral')
        theme_dist = analysis.get('theme_distribution', {})
        personality = analysis.get('personality_indicators', {})

        # Normalize scores for comparison
        def normalize(value, max_value=100):
            return value / max_value if max_value != 0 else 0

        # Calculate composite scores
        technical_score = normalize(theme_dist.get('technical_growth', 0) + personality.get('professional_focus', 0))
        creative_score = normalize(theme_dist.get('creativity_arts', 0) + personality.get('creativity_level', 0))
        growth_score = normalize(theme_dist.get('self_improvement', 0) + personality.get('growth_orientation', 0))
        emotional_score = normalize(theme_dist.get('emotional_depth', 0) + personality.get('emotional_expression', 0))
        social_score = normalize(personality.get('social_engagement', 0) + theme_dist.get('relationships', 0))
        balance_score = normalize(personality.get('lifestyle_balance', 0))

        # Fetch user details (follower_count and number_of_tweets)
        user_details = self.fetch_user_details(username)
        follower_count = user_details.get('follower_count', 0)
        number_of_tweets = user_details.get('number_of_tweets', 0)

        print(follower_count)
        print(number_of_tweets)

        # Calculate engagement metrics with error handling for None values
        total_views = sum(tweet.get('views', 0) or 0 for tweet in tweets)
        total_retweets = sum(tweet.get('retweet_count', 0) or 0 for tweet in tweets)
        total_quotes = sum(tweet.get('quote_count', 0) or 0 for tweet in tweets)
        total_replies = sum(tweet.get('reply_count', 0) or 0 for tweet in tweets)

        # Normalize engagement metrics (assuming max values for normalization)
        max_views = max((tweet.get('views', 0) or 0 for tweet in tweets), default=1)
        max_retweets = max((tweet.get('retweet_count', 0) or 0 for tweet in tweets), default=1)
        max_quotes = max((tweet.get('quote_count', 0) or 0 for tweet in tweets), default=1)
        max_replies = max((tweet.get('reply_count', 0) or 0 for tweet in tweets), default=1)

        # Calculate engagement score with logarithmic scaling for follower_count
        engagement_score = (
            normalize(total_views, max_views) * 0.3 +
            normalize(total_retweets, max_retweets) * 0.25 +
            normalize(total_quotes, max_quotes) * 0.15 +
            normalize(total_replies, max_replies) * 0.10 +
            normalize(math.log1p(follower_count), math.log1p(1000000)) * 0.15 +  # Logarithmic scaling for follower_count
            normalize(number_of_tweets, 10000) * 0.05  # Normalize number_of_tweets
        )

        # Calculate cumulative overall score (weighted average)
        cumulative_score = (
            technical_score * 0.2 +
            creative_score * 0.2 +
            growth_score * 0.15 +
            emotional_score * 0.15 +
            social_score * 0.15 +
            balance_score * 0.10 +
            engagement_score * 0.05  # Engagement contributes 5% to the overall score
        )

        print(f"Dominant theme: {dominant_theme}")
        print(f"Cumulative overall score: {cumulative_score:.2f}")
        print(f"Engagement score: {engagement_score:.2f}")

        # Rank the user's cumulative score relative to others
        def calculate_percentile(user_score, all_scores):
            if not all_scores:
                return 0
            sorted_scores = sorted(all_scores)
            for i, score in enumerate(sorted_scores):
                if user_score <= score:
                    return i / len(sorted_scores)
            return 1.0

        # Calculate percentile for the user
        percentile = calculate_percentile(cumulative_score, user_scores)
        print(f"Percentile: {percentile:.2f}")

        # Map percentile to tarot cards
        if percentile >= 0.95:
            return "The World"  # Completion, fulfillment, and success
        elif percentile >= 0.90:
            return "The Sun"  # Joy, success, and positivity
        elif percentile >= 0.85:
            return "The Star"  # Hope, inspiration, and aspiration
        elif percentile >= 0.80:
            return "The Empress"  # Creativity, abundance, and nurturing
        elif percentile >= 0.75:
            return "The Emperor"  # Authority, structure, and leadership
        elif percentile >= 0.70:
            return "The Hierophant"  # Tradition, community, and expertise
        elif percentile >= 0.65:
            return "The Magician"  # Mastery, skill, and personal growth
        elif percentile >= 0.60:
            return "The High Priestess"  # Intuition, creativity, and mystery
        elif percentile >= 0.55:
            return "The Fool"  # New beginnings, spontaneity, and potential
        elif percentile >= 0.50:
            return "The Chariot"  # Determination, willpower, and victory
        elif percentile >= 0.45:
            return "Justice"  # Fairness, balance, and truth
        elif percentile >= 0.40:
            return "The Wheel of Fortune"  # Change, cycles, and destiny
        elif percentile >= 0.35:
            return "The Lovers"  # Relationships, harmony, and choices
        elif percentile >= 0.30:
            return "Strength"  # Courage, inner strength, and resilience
        elif percentile >= 0.25:
            return "The Hermit"  # Solitude, introspection, and wisdom
        elif percentile >= 0.20:
            return "The Hanged Man"  # Perspective, surrender, and new viewpoints
        elif percentile >= 0.15:
            return "Death"  # Transformation, endings, and new beginnings
        elif percentile >= 0.10:
            return "Temperance"  # Balance, moderation, and harmony
        elif percentile >= 0.05:
            return "The Devil"  # Bondage, materialism, and shadow self
        else:
            return "The Tower"  # Sudden change, upheaval, and revelation

    def generate_reading(self, analysis, tweets, user_scores, username):
        """Generate a comprehensive tarot reading based on the analysis."""
        card_name = self.select_tarot_card(analysis, user_scores, tweets, username)
        card_info = self.TAROT_CARDS[card_name]

        # Extract sentiment value from the analysis
        sentiment_value = analysis.get('sentiment', {}).get('average', 0)
        sentiment_label = (
            'Positive' if sentiment_value > 0 
            else 'Negative' if sentiment_value < 0 
            else 'Neutral'
        )

        reading = {
            'card_name': card_name,
            'card_meaning': card_info['meaning'],
            'career_advice': card_info['career_advice'],
            'analysis_summary': {
                'dominant_theme': analysis.get('dominant_themes', []),
                'sentiment': sentiment_label,
                'theme_distribution': analysis.get('theme_distribution', {}),
                'engagement_metrics': analysis.get('analysis_metadata', {})
            }
        }
        return reading

def main():
    try:
        reader = TwitterTarotReader()
        
        screenname = input("Enter Twitter screen name: ")
        print(f"\nFetching tweets for @{screenname}...")
        tweets = reader.get_tweets(screenname)
        analysis = reader.analyze_personality(tweets)
        user_scores = [0.12, 0.18, 0.05, 0.22, 0.15, 0.10, 0.08, 0.20, 0.25, 0.30]
        reading = reader.generate_reading(analysis, tweets, user_scores, screenname)
        
        print("\n🌟 Your Technical Twitter Tarot Reading 🌟")
        print("=" * 50)
        print(f"Selected Card: {reading['card_name']}")
        print(f"Meaning: {reading['card_meaning']}")
        print(f"\nCareer Insight: {reading['career_advice']}")
        
        print("\nBased on your Twitter activity:")
        print(f"- Primary Theme: {reading['analysis_summary']['dominant_theme']}")
        print(f"- Overall Sentiment: {reading['analysis_summary']['sentiment']}")

        print("\nEngagement Metrics:")
        for metric, score in reading['analysis_summary']['engagement_metrics'].items():
            if isinstance(score, float):
                print(f"- {metric.replace('_', ' ').title()}: {score:.2%}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
import random
import datetime
import math
import json
import os
import textwrap
from collections import defaultdict, Counter

class CryptoSentimentAnalysis:
    def __init__(self):
        # Define top 10 cryptocurrencies
        self.cryptocurrencies = [
            {"name": "Bitcoin", "symbol": "BTC", "current_price": 76408.41},
            {"name": "Ethereum", "symbol": "ETH", "current_price": 3345.88},
            {"name": "Tether", "symbol": "USDT", "current_price": 1.00},
            {"name": "XRP", "symbol": "XRP", "current_price": 0.57},
            {"name": "Binance Coin", "symbol": "BNB", "current_price": 541.40},
            {"name": "Solana", "symbol": "SOL", "current_price": 184.32},
            {"name": "USD Coin", "symbol": "USDC", "current_price": 1.00},
            {"name": "Cardano", "symbol": "ADA", "current_price": 0.46},
            {"name": "Dogecoin", "symbol": "DOGE", "current_price": 0.17},
            {"name": "Avalanche", "symbol": "AVAX", "current_price": 34.29}
        ]
        
        # Common words for sentiment generation
        self.positive_words = [
            "bullish", "growth", "opportunity", "potential", "innovation", 
            "adoption", "profit", "gain", "partnership", "breakthrough", 
            "rally", "surge", "milestone", "success", "revolution", 
            "future", "confidence", "mainstream", "institutional", "whale"
        ]
        
        self.negative_words = [
            "bearish", "crash", "risk", "regulation", "ban", "sell", 
            "dump", "fraud", "scam", "bubble", "correction", "decline", 
            "volatile", "uncertainty", "concern", "overvalued", "criticism", 
            "warning", "hack", "competition"
        ]
        
        # Generate data for the past 30 days
        self.end_date = datetime.datetime.now()
        self.start_date = self.end_date - datetime.timedelta(days=30)
        self.dates = [self.start_date + datetime.timedelta(days=i) for i in range(31)]
        
        # Generate sentiment data
        self.generate_data()
    
    def generate_data(self):
        """Generate simulated sentiment data for each cryptocurrency"""
        self.sentiment_data = {}
        
        for crypto in self.cryptocurrencies:
            sentiment_by_date = {}
            
            # Base sentiment bias (some coins are more popular/controversial)
            if crypto["symbol"] in ["BTC", "ETH", "SOL"]:
                base_positive_bias = random.uniform(0.6, 0.8)
            elif crypto["symbol"] in ["DOGE", "XRP"]:
                base_positive_bias = random.uniform(0.45, 0.65)
            else:
                base_positive_bias = random.uniform(0.4, 0.6)
            
            # Choose random trends for this crypto
            trend_pattern = random.choice([
                "uptrend", "downtrend", "volatile", "stable", "recovery", "correction"
            ])
            
            # Track price changes for correlation with sentiment
            price_changes = []
            prices = []
            current_price = crypto["current_price"]
            
            for i, date in enumerate(self.dates):
                date_str = date.strftime("%Y-%m-%d")
                
                # Apply trend pattern to sentiment
                if trend_pattern == "uptrend":
                    trend_modifier = min(0.15, 0.005 * i)
                elif trend_pattern == "downtrend":
                    trend_modifier = max(-0.15, -0.005 * i)
                elif trend_pattern == "volatile":
                    trend_modifier = 0.15 * math.sin(i/5)
                elif trend_pattern == "recovery":
                    trend_modifier = 0.15 * (1 - math.exp(-i/15))
                elif trend_pattern == "correction":
                    trend_modifier = -0.10 * (1 - math.exp(-i/10))
                else:  # stable
                    trend_modifier = 0
                
                # Add some randomness
                daily_random = random.uniform(-0.1, 0.1)
                
                # Calculate positive sentiment
                positive_sentiment = base_positive_bias + trend_modifier + daily_random
                positive_sentiment = max(0.1, min(0.9, positive_sentiment))
                
                # Calculate negative sentiment
                negative_sentiment = 1 - positive_sentiment
                
                # Generate engagement metrics (mentions, posts, likes)
                base_mentions = random.randint(5000, 50000)
                if crypto["symbol"] in ["BTC", "ETH"]:
                    base_mentions *= 3
                elif crypto["symbol"] in ["SOL", "BNB", "XRP"]:
                    base_mentions *= 2
                
                mentions = int(base_mentions * (1 + trend_modifier + daily_random))
                posts = int(mentions * random.uniform(0.2, 0.4))
                likes = int(posts * random.uniform(3, 15))
                
                # Simulated daily price change based on sentiment
                price_change_pct = (positive_sentiment - 0.5) * 2 * random.uniform(0.5, 2.0)
                if random.random() < 0.2:  # Sometimes price moves against sentiment
                    price_change_pct *= -1
                price_change = current_price * price_change_pct / 100
                current_price += price_change
                
                price_changes.append(price_change_pct)
                prices.append(current_price)
                
                # Generate word clouds
                pos_word_counts = {}
                neg_word_counts = {}
                
                for word in self.positive_words:
                    if random.random() < positive_sentiment:
                        pos_word_counts[word] = random.randint(1, int(mentions * 0.01))
                
                for word in self.negative_words:
                    if random.random() < negative_sentiment:
                        neg_word_counts[word] = random.randint(1, int(mentions * 0.01))
                
                # Store data for this date
                sentiment_by_date[date_str] = {
                    "positive_sentiment": positive_sentiment,
                    "negative_sentiment": negative_sentiment,
                    "mentions": mentions,
                    "posts": posts,
                    "likes": likes,
                    "price": current_price,
                    "price_change_pct": price_change_pct,
                    "positive_words": pos_word_counts,
                    "negative_words": neg_word_counts,
                    "trend": trend_pattern
                }
            
            # Calculate sentiment-price correlation
            self.sentiment_data[crypto["symbol"]] = {
                "name": crypto["name"],
                "symbol": crypto["symbol"],
                "data": sentiment_by_date,
                "trend": trend_pattern,
                "sentiment_price_correlation": self.calculate_correlation(
                    [sentiment_by_date[date.strftime("%Y-%m-%d")]["positive_sentiment"] for date in self.dates],
                    price_changes
                ),
                "avg_daily_mentions": sum(sentiment_by_date[date.strftime("%Y-%m-%d")]["mentions"] for date in self.dates) / len(self.dates),
                "top_positive_words": self.get_top_words(sentiment_by_date, "positive_words"),
                "top_negative_words": self.get_top_words(sentiment_by_date, "negative_words")
            }
    
    def calculate_correlation(self, a, b):
        """Calculate Pearson correlation coefficient between two lists"""
        n = len(a)
        if n != len(b) or n == 0:
            return 0
        
        sum_a = sum(a)
        sum_b = sum(b)
        sum_ab = sum(x*y for x, y in zip(a, b))
        sum_a2 = sum(x*x for x in a)
        sum_b2 = sum(y*y for y in b)
        
        try:
            numerator = n * sum_ab - sum_a * sum_b
            denominator = math.sqrt((n * sum_a2 - sum_a * sum_a) * (n * sum_b2 - sum_b * sum_b))
            return numerator / denominator if denominator != 0 else 0
        except:
            return 0
    
    def get_top_words(self, sentiment_by_date, word_type):
        """Get most common words across all dates"""
        all_words = Counter()
        for date_data in sentiment_by_date.values():
            for word, count in date_data[word_type].items():
                all_words[word] += count
        return all_words.most_common(5)
    
    def generate_ascii_chart(self, values, width=50, height=10, title="", labels=None):
        """Generate an ASCII chart from a list of values"""
        if not values:
            return "No data to display"
        
        min_val = min(values)
        max_val = max(values)
        value_range = max_val - min_val
        
        if value_range == 0:
            value_range = 1  # Avoid division by zero
        
        # Characters for drawing
        chars = " ▁▂▃▄▅▆▇█"
        
        # Calculate scaled values
        scaled_values = [int((val - min_val) / value_range * (height - 1)) for val in values]
        
        # Build chart
        chart = []
        chart.append(f"┌{'─' * width}┐")
        chart.append(f"│ {title:<{width-2}} │")
        chart.append(f"├{'─' * width}┤")
        
        for i in range(height - 1, -1, -1):
            line = "│"
            for val in scaled_values:
                if val >= i:
                    line += "█"
                else:
                    line += " "
            line += "│"
            chart.append(line)
        
        chart.append(f"└{'─' * width}┘")
        
        # Add labels if provided
        if labels:
            label_str = ""
            step = max(1, len(labels) // (width - 2))
            for i in range(0, len(labels), step):
                if i < len(labels):
                    label_str += f"{labels[i]}"
                    if i + step < len(labels):
                        spaces = step - len(labels[i])
                        label_str += " " * spaces
            chart.append(label_str[:width])
        
        return "\n".join(chart)
    
    def generate_horizontal_bar(self, value, max_width=40, label="", percent=True):
        """Generate a horizontal bar chart for a single value"""
        bar_width = int(value * max_width)
        
        if percent:
            value_display = f"{value*100:.1f}%"
        else:
            value_display = f"{value:.2f}"
            
        bar = f"{label:15} │{'█' * bar_width}{' ' * (max_width - bar_width)}│ {value_display}"
        return bar
    
    def generate_report(self):
        """Generate a comprehensive report with sentiment analysis"""
        report = []
        
        # Title
        report.append("=" * 80)
        report.append("CRYPTOCURRENCY SOCIAL MEDIA SENTIMENT ANALYSIS REPORT".center(80))
        report.append(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(80))
        report.append("=" * 80)
        report.append("")
        
        # Introduction
        report.append("INTRODUCTION")
        report.append("-" * 80)
        report.append("This report analyzes social media sentiment for the top 10 cryptocurrencies over")
        report.append("the past 30 days. The data includes positive and negative sentiment ratios,")
        report.append("social media mentions, engagement, and correlation with price movements.")
        report.append("")
        
        # Overall sentiment comparison
        report.append("OVERALL SENTIMENT COMPARISON")
        report.append("-" * 80)
        report.append("Positive sentiment ratio across cryptocurrencies:")
        report.append("")
        
        # Sort cryptocurrencies by average positive sentiment
        avg_sentiments = []
        for symbol, data in self.sentiment_data.items():
            avg_pos_sentiment = sum(day_data["positive_sentiment"] for day_data in data["data"].values()) / len(data["data"])
            avg_sentiments.append((symbol, avg_pos_sentiment))
        
        avg_sentiments.sort(key=lambda x: x[1], reverse=True)
        
        for symbol, avg_sentiment in avg_sentiments:
            report.append(self.generate_horizontal_bar(
                avg_sentiment, 
                label=f"{symbol}",
                max_width=40
            ))
        
        report.append("")
        report.append("INSIGHTS:")
        most_positive = avg_sentiments[0][0]
        least_positive = avg_sentiments[-1][0]
        report.append(f"• {self.sentiment_data[most_positive]['name']} ({most_positive}) has the most positive sentiment overall.")
        report.append(f"• {self.sentiment_data[least_positive]['name']} ({least_positive}) has the least positive sentiment overall.")
        
        # Add insights about why some might be more positive than others
        if most_positive in ["BTC", "ETH", "SOL"]:
            report.append(f"• Major cryptocurrencies like {most_positive} tend to have more positive sentiment due")
            report.append("  to their established market position and wider adoption.")
        
        report.append("")
        
        # Sentiment trends over time
        report.append("SENTIMENT TRENDS OVER TIME")
        report.append("-" * 80)
        report.append("The following charts show how positive sentiment has changed over the past 30 days")
        report.append("for selected cryptocurrencies:")
        report.append("")
        
        # Select a few interesting cryptocurrencies to show trends
        trend_cryptos = ["BTC", "ETH", "SOL", "DOGE", "XRP"]
        
        for symbol in trend_cryptos:
            data = self.sentiment_data[symbol]
            dates = list(data["data"].keys())[-14:]  # Last 14 days for readability
            values = [data["data"][date]["positive_sentiment"] for date in dates]
            short_dates = [date[-5:] for date in dates]  # MM-DD format
            
            chart = self.generate_ascii_chart(
                values, 
                width=60, 
                height=8, 
                title=f"{data['name']} ({symbol}) Positive Sentiment", 
                labels=short_dates
            )
            report.append(chart)
            report.append("")
            
            # Add trend insight
            trend = data["trend"]
            if trend == "uptrend":
                report.append(f"➤ {symbol} shows an upward sentiment trend, indicating growing community optimism.")
            elif trend == "downtrend":
                report.append(f"➤ {symbol} displays a declining sentiment trend, suggesting increasing community concern.")
            elif trend == "volatile":
                report.append(f"➤ {symbol} exhibits volatile sentiment, reflecting market uncertainty and mixed opinions.")
            elif trend == "recovery":
                report.append(f"➤ {symbol} demonstrates sentiment recovery, indicating improving community perception.")
            elif trend == "correction":
                report.append(f"➤ {symbol} shows sentiment correction after previous highs, suggesting market normalization.")
            else:
                report.append(f"➤ {symbol} maintains relatively stable sentiment throughout the period.")
            
            report.append("")
        
        # Sentiment-Price Correlation
        report.append("SENTIMENT-PRICE CORRELATION")
        report.append("-" * 80)
        report.append("Correlation between positive sentiment and price changes:")
        report.append("")
        
        # Sort cryptocurrencies by correlation
        correlations = [(symbol, data["sentiment_price_correlation"]) 
                         for symbol, data in self.sentiment_data.items()]
        correlations.sort(key=lambda x: abs(x[1]), reverse=True)
        
        for symbol, correlation in correlations:
            report.append(self.generate_horizontal_bar(
                abs(correlation), 
                label=f"{symbol}",
                max_width=40,
                percent=False
            ))
            direction = "positive" if correlation > 0 else "negative"
            strength = "strong" if abs(correlation) > 0.7 else "moderate" if abs(correlation) > 0.3 else "weak"
            report.append(f"   Direction: {direction}, Strength: {strength}")
            report.append("")
        
        report.append("INSIGHTS:")
        high_corr_crypto = correlations[0][0]
        high_corr_value = correlations[0][1]
        report.append(f"• {self.sentiment_data[high_corr_crypto]['name']} ({high_corr_crypto}) shows the strongest")
        report.append(f"  {'positive' if high_corr_value > 0 else 'negative'} correlation between sentiment and price movements.")
        
        if any(abs(corr) < 0.2 for _, corr in correlations):
            low_corr_cryptos = [symbol for symbol, corr in correlations if abs(corr) < 0.2]
            report.append(f"• {', '.join(low_corr_cryptos)} show weak correlation between sentiment and price,")
            report.append("  suggesting other factors may be more influential for these assets.")
        
        report.append("")
        
        # Social Media Engagement
        report.append("SOCIAL MEDIA ENGAGEMENT")
        report.append("-" * 80)
        report.append("Average daily mentions across social media platforms:")
        report.append("")
        
        # Sort cryptocurrencies by average mentions
        mentions = [(symbol, data["avg_daily_mentions"]) 
                     for symbol, data in self.sentiment_data.items()]
        mentions.sort(key=lambda x: x[1], reverse=True)
        
        max_mentions = max(m for _, m in mentions)
        
        for symbol, avg_mentions in mentions:
            normalized = avg_mentions / max_mentions
            report.append(self.generate_horizontal_bar(
                normalized, 
                label=f"{symbol}",
                max_width=40,
                percent=False
            ) + f" ({int(avg_mentions):,} mentions)")
        
        report.append("")
        report.append("INSIGHTS:")
        most_mentioned = mentions[0][0]
        least_mentioned = mentions[-1][0]
        report.append(f"• {self.sentiment_data[most_mentioned]['name']} ({most_mentioned}) dominates social media")
        report.append(f"  conversations with approximately {int(mentions[0][1]):,} daily mentions.")
        report.append(f"• Despite having lower mentions, {least_mentioned} still generates significant")
        report.append(f"  engagement with {int(mentions[-1][1]):,} daily mentions.")
        
        # Add insight about market leaders
        if mentions[0][0] in ["BTC", "ETH"]:
            report.append("• Market leaders typically dominate social media conversations, reflecting their")
            report.append("  larger community size and broader market influence.")
        
        report.append("")
        
        # Popular Terms Analysis
        report.append("POPULAR TERMS IN SOCIAL MEDIA DISCUSSIONS")
        report.append("-" * 80)
        
        # Select a few cryptocurrencies for detailed word analysis
        word_analysis_cryptos = ["BTC", "ETH", "SOL", "DOGE"]
        
        for symbol in word_analysis_cryptos:
            data = self.sentiment_data[symbol]
            report.append(f"{data['name']} ({symbol}):")
            
            report.append("  Positive terms:")
            for word, count in data["top_positive_words"]:
                report.append(f"    • {word}: {count:,} mentions")
            
            report.append("  Negative terms:")
            for word, count in data["top_negative_words"]:
                report.append(f"    • {word}: {count:,} mentions")
            
            report.append("")
        
        # Conclusion and Recommendations
        report.append("CONCLUSION AND INSIGHTS")
        report.append("-" * 80)
        
        # Identify most positive trending crypto
        uptrend_cryptos = [symbol for symbol, data in self.sentiment_data.items() 
                          if data["trend"] in ["uptrend", "recovery"]]
        
        downtrend_cryptos = [symbol for symbol, data in self.sentiment_data.items() 
                            if data["trend"] in ["downtrend", "correction"]]
        
        report.append("Key findings from the sentiment analysis:")
        report.append("")
        
        if uptrend_cryptos:
            report.append(f"• Positive sentiment trends: {', '.join(uptrend_cryptos)}")
            report.append("  These cryptocurrencies show improving sentiment, potentially indicating")
            report.append("  growing community support and positive market perception.")
        
        if downtrend_cryptos:
            report.append(f"• Negative sentiment trends: {', '.join(downtrend_cryptos)}")
            report.append("  These cryptocurrencies show declining sentiment, which might suggest")
            report.append("  decreasing confidence or emerging concerns in the community.")
        
        # Find cryptos with strong positive correlation
        strong_pos_corr = [symbol for symbol, data in self.sentiment_data.items() 
                          if data["sentiment_price_correlation"] > 0.5]
        
        if strong_pos_corr:
            report.append(f"• Strong positive sentiment-price correlation: {', '.join(strong_pos_corr)}")
            report.append("  For these assets, social media sentiment appears to be a leading indicator")
            report.append("  of price movements, suggesting potential predictive value.")
        
        report.append("")
        report.append("METHODOLOGY NOTE")
        report.append("-" * 80)
        report.append("This report uses simulated data to demonstrate sentiment analysis techniques.")
        report.append("In a real-world application, data would be sourced from social media platforms,")
        report.append("news sources, and specialized crypto sentiment analysis services like LunarCrush,")
        report.append("Santiment, or the Crypto Fear and Greed Index.")
        report.append("")
        
        return "\n".join(report)
    
    def save_report(self, filename="crypto_sentiment_report.txt"):
        """Save the report to a text file"""
        report = self.generate_report()
        with open(filename, "w") as f:
            f.write(report)
        return f"Report saved to {filename}"
    
    def save_data(self, filename="crypto_sentiment_data.json"):
        """Save the generated data to a JSON file for further analysis"""
        with open(filename, "w") as f:
            json.dump(self.sentiment_data, f, indent=2)
        return f"Data saved to {filename}"


def main():
    analyzer = CryptoSentimentAnalysis()
    report = analyzer.generate_report()
    print(report)
    
    # Save report and data files
    print(analyzer.save_report())
    print(analyzer.save_data())


if __name__ == "__main__":
    main()

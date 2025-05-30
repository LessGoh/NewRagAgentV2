from typing import Optional
from llama_index.core.tools import FunctionTool
from utils.llama_client import LlamaIndexClient

class FinanceTools:
    """Инструменты для финансового анализа"""
    
    def __init__(self):
        self.llama_client = LlamaIndexClient()
    
    def search_indicator_strategies(self, 
                                  indicator_name: str, 
                                  timeframe: str = "any") -> str:
        """
        Поиск торговых стратегий для конкретного технического индикатора.
        
        Args:
            indicator_name: Название индикатора (RSI, MACD, SMA, EMA, Bollinger Bands, etc.)
            timeframe: Таймфрейм (1min, 5min, 15min, 1h, 4h, 1d, etc.)
        
        Returns:
            Подробная информация о стратегиях с использованием индикатора
        """
        try:
            timeframe_filter = None if timeframe == "any" else timeframe
            result = self.llama_client.search_indicators(indicator_name, timeframe_filter)
            
            if result.get("error"):
                return f"Ошибка поиска: {result['error']}"
            
            response = result.get("response", "")
            sources = result.get("source_nodes", [])
            
            # Форматирование ответа
            formatted_response = f"""
📊 **Стратегии с использованием {indicator_name.upper()}**

{response}

📚 **Источники:**
"""
            for i, source in enumerate(sources[:3], 1):
                if hasattr(source, 'metadata'):
                    title = source.metadata.get('title', 'Неизвестная статья')
                    formatted_response += f"{i}. {title}\n"
            
            return formatted_response
            
        except Exception as e:
            return f"Ошибка при поиске стратегий: {str(e)}"
    
    def compare_strategies(self, strategy1: str, strategy2: str) -> str:
        """
        Сравнение двух торговых стратегий или подходов.
        
        Args:
            strategy1: Первая стратегия для сравнения
            strategy2: Вторая стратегия для сравнения
        
        Returns:
            Детальное сравнение стратегий
        """
        try:
            query = f"сравнение стратегий {strategy1} против {strategy2} преимущества недостатки"
            result = self.llama_client.query(query, top_k=6)
            
            if result.get("error"):
                return f"Ошибка поиска: {result['error']}"
            
            response = result.get("response", "")
            
            formatted_response = f"""
⚖️ **Сравнение: {strategy1.title()} vs {strategy2.title()}**

{response}

💡 **Рекомендация:** Выбор стратегии зависит от ваших торговых целей, уровня риска и рыночных условий.
"""
            return formatted_response
            
        except Exception as e:
            return f"Ошибка при сравнении стратегий: {str(e)}"
    
    def analyze_market_conditions(self, 
                                market_type: str, 
                                analysis_type: str = "technical") -> str:
        """
        Анализ стратегий для определенных рыночных условий.
        
        Args:
            market_type: Тип рынка (trending, sideways, volatile, bearish, bullish, crisis)
            analysis_type: Тип анализа (technical, fundamental, behavioral, quantitative)
        
        Returns:
            Анализ подходящих стратегий для данных условий
        """
        try:
            result = self.llama_client.search_strategies(
                f"{analysis_type} анализ", 
                market_type
            )
            
            if result.get("error"):
                return f"Ошибка поиска: {result['error']}"
            
            response = result.get("response", "")
            
            formatted_response = f"""
📈 **Анализ для {market_type.upper()} рынка ({analysis_type} подход)**

{response}

⚠️ **Важно:** Всегда учитывайте риски и используйте стоп-лоссы при торговле.
"""
            return formatted_response
            
        except Exception as e:
            return f"Ошибка при анализе рыночных условий: {str(e)}"
    
    def find_research_papers(self, topic: str, year_from: int = 2020) -> str:
        """
        Поиск научных исследований по финансовой тематике.
        
        Args:
            topic: Тема исследования (например: "machine learning trading", "behavioral finance")
            year_from: Год начала поиска (по умолчанию 2020)
        
        Returns:
            Информация о релевантных исследованиях
        """
        try:
            result = self.llama_client.search_research(topic, year_from)
            
            if result.get("error"):
                return f"Ошибка поиска: {result['error']}"
            
            response = result.get("response", "")
            sources = result.get("source_nodes", [])
            
            formatted_response = f"""
🔬 **Исследования по теме: {topic.title()}**

{response}

📄 **Найденные статьи:**
"""
            for i, source in enumerate(sources[:5], 1):
                if hasattr(source, 'metadata'):
                    title = source.metadata.get('title', 'Неизвестная статья')
                    authors = source.metadata.get('authors', 'Неизвестные авторы')
                    formatted_response += f"{i}. **{title}** - {authors}\n"
            
            return formatted_response
            
        except Exception as e:
            return f"Ошибка при поиске исследований: {str(e)}"
    
    def get_tools(self):
        """Возвращает список инструментов для агента"""
        return [
            FunctionTool.from_defaults(self.search_indicator_strategies),
            FunctionTool.from_defaults(self.compare_strategies),
            FunctionTool.from_defaults(self.analyze_market_conditions),
            FunctionTool.from_defaults(self.find_research_papers)
        ]

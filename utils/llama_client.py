import requests
import json
from typing import Dict, Any, Optional
from config import Config

class LlamaIndexClient:
    """Клиент для работы с LlamaIndex API"""
    
    def __init__(self):
        self.base_url = Config.LLAMA_INDEX_URL.rstrip('/')
        self.api_key = Config.LLAMA_INDEX_API_KEY
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def query(self, 
              query: str, 
              top_k: int = 5, 
              similarity_threshold: float = 0.7) -> Dict[str, Any]:
        """
        Выполнение запроса к LlamaIndex
        
        Args:
            query: Текст запроса
            top_k: Количество результатов
            similarity_threshold: Порог схожести
            
        Returns:
            Ответ от LlamaIndex API
        """
        try:
            payload = {
                "query": query,
                "top_k": top_k,
                "similarity_threshold": similarity_threshold
            }
            
            response = requests.post(
                f"{self.base_url}/query",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Ошибка API запроса: {str(e)}",
                "response": None,
                "source_nodes": []
            }
    
    def search_indicators(self, 
                         indicator: str, 
                         timeframe: Optional[str] = None) -> Dict[str, Any]:
        """Специализированный поиск по индикаторам"""
        
        query_parts = [f"технический индикатор {indicator}"]
        if timeframe:
            query_parts.append(f"таймфрейм {timeframe}")
        
        query_parts.extend([
            "торговая стратегия",
            "условия входа и выхода",
            "параметры настройки",
            "бэктестинг результаты"
        ])
        
        query = " ".join(query_parts)
        return self.query(query, top_k=7)
    
    def search_strategies(self, 
                         strategy_type: str, 
                         market_condition: Optional[str] = None) -> Dict[str, Any]:
        """Поиск торговых стратегий"""
        
        query_parts = [f"торговая стратегия {strategy_type}"]
        if market_condition:
            query_parts.append(f"рыночные условия {market_condition}")
        
        query_parts.extend([
            "риск менеджмент",
            "исторические результаты",
            "практическое применение"
        ])
        
        query = " ".join(query_parts)
        return self.query(query, top_k=8)
    
    def search_research(self, topic: str, year_from: int = 2020) -> Dict[str, Any]:
        """Поиск исследований"""
        
        query = f"исследование {topic} год {year_from} методология результаты"
        return self.query(query, top_k=10)

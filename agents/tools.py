from typing import Optional
from llama_index.core.tools import FunctionTool
import os

# Проверяем, доступен ли LlamaIndex клиент
try:
    from utils.llama_client import LlamaIndexClient
    LLAMA_AVAILABLE = True
except ImportError:
    LLAMA_AVAILABLE = False

class FinanceTools:
    """Инструменты для финансового анализа"""
    
    def __init__(self):
        if LLAMA_AVAILABLE and os.getenv("LLAMA_INDEX_URL"):
            try:
                self.llama_client = LlamaIndexClient()
                self.use_llamaindex = True
            except Exception as e:
                print(f"Ошибка подключения к LlamaIndex: {e}")
                self.use_llamaindex = False
        else:
            self.use_llamaindex = False
    
    def search_indicator_strategies(self, indicator_name: str, timeframe: str = "any") -> str:
        """Поиск торговых стратегий для технического индикатора"""
        
        if not self.use_llamaindex:
            return f"""
🔍 **Поиск стратегий для {indicator_name.upper()}** (Тестовый режим)

⚠️ **Внимание:** LlamaIndex база знаний не подключена. 
Для получения реальных данных из ArXiv статей настройте:
- LLAMA_INDEX_URL 
- LLAMA_INDEX_API_KEY

**Пример стратегии {indicator_name.upper()}:**
- Покупка при RSI < 30 (перепроданность)
- Продажа при RSI > 70 (перекупленность)
- Используйте дополнительные фильтры для снижения ложных сигналов
"""
        
        try:
            query = f"торговые стратегии {indicator_name} технический анализ {timeframe if timeframe != 'any' else ''} условия входа выхода"
            result = self.llama_client.query(query, top_k=7)
            
            if result.get("error"):
                return f"❌ Ошибка поиска в базе знаний: {result['error']}"
            
            response = result.get("response", "")
            sources = result.get("source_nodes", [])
            
            formatted_response = f"""
📊 **Стратегии с использованием {indicator_name.upper()}** (из базы знаний ArXiv)

{response}

📚 **Источники из научных статей:**
"""
            
            for i, source in enumerate(sources[:3], 1):
                if hasattr(source, 'metadata'):
                    title = source.metadata.get('title', 'Неизвестная статья')
                    formatted_response += f"{i}. {title}\n"
            
            return formatted_response
            
        except Exception as e:
            return f"❌ Ошибка при работе с базой знаний: {str(e)}"

"""
Универсальный ИИ-агент для всестороннего анализа вопросов
"""
from typing import List, Dict, Any, Optional, TypedDict, Annotated
from langchain_ollama import OllamaLLM
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages
import logging
import json
from datetime import datetime

from config import settings
from tools.search_tools import web_search_tool, url_content_tool

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentState(TypedDict):
    """Состояние агента для LangGraph"""
    messages: Annotated[List, add_messages]
    original_question: str
    analysis_results: Dict[str, Any]
    current_aspect: str
    aspects_to_process: List[str]
    processed_aspects: List[str]
    research_data: List[Dict[str, Any]]
    final_insights: List[str]
    iteration_count: int


class UniversalAgent:
    """Универсальный ИИ-агент для глубокого анализа вопросов"""
    
    def __init__(self):
        """Инициализация агента с настройкой LLM и инструментов"""
        self.llm = OllamaLLM(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            temperature=0.7
        )
        
        # Создаем инструменты для агента
        self.tools = [
            self._create_web_search_tool(),
            self._create_url_content_tool()
        ]
        
        # Создаем граф состояний
        self.graph = self._create_agent_graph()
    
    def _create_web_search_tool(self):
        """Создает инструмент поиска в интернете для LangChain"""
        def web_search(query: str) -> str:
            """
            Выполняет поиск в интернете по заданному запросу
            
            Args:
                query: Поисковый запрос
                
            Returns:
                JSON-строка с результатами поиска
            """
            results = web_search_tool.search(query)
            return json.dumps(results, ensure_ascii=False, indent=2)
        
        return {
            "name": "web_search",
            "description": "Поиск информации в интернете с использованием DuckDuckGo",
            "function": web_search
        }
    
    def _create_url_content_tool(self):
        """Создает инструмент загрузки URL для LangChain"""
        def load_url(url: str) -> str:
            """
            Загружает и анализирует содержимое веб-страницы
            
            Args:
                url: URL для загрузки
                
            Returns:
                JSON-строка с содержимым страницы
            """
            result = url_content_tool.load_url(url)
            return json.dumps(result, ensure_ascii=False, indent=2)
        
        return {
            "name": "load_url",
            "description": "Загружает и анализирует содержимое веб-страницы по URL",
            "function": load_url
        }
    
    def _create_analysis_prompt(self) -> ChatPromptTemplate:
        """Создает промпт для анализа и разбиения вопроса"""
        template = """
Ты - опытный аналитик с 20-летним стажем. Твоя задача - всесторонне проанализировать заданный вопрос.

ВОПРОС ДЛЯ АНАЛИЗА: {question}

Проведи глубокий анализ этого вопроса, рассмотрев:

1. МОТИВАЦИЯ И КОНТЕКСТ:
   - Почему этот вопрос важен?
   - Какие факторы могли привести к его появлению?
   - Какие скрытые потребности за ним стоят?

2. РАЗБИЕНИЕ НА АСПЕКТЫ:
   - На какие ключевые составляющие можно разбить этот вопрос?
   - Какие подвопросы возникают из основного вопроса?
   - Какие темы требуют отдельного изучения?

3. ПЛАН ИССЛЕДОВАНИЯ:
   - Какие аспекты нужно изучить в первую очередь?
   - Какие источники информации могут быть полезны?
   - Какие вопросы требуют дополнительного исследования?

Верни ответ в формате JSON:
{{
    "motivation": "анализ мотивации и контекста",
    "aspects": ["аспект1", "аспект2", "аспект3"],
    "research_questions": ["вопрос1", "вопрос2", "вопрос3"],
    "priority_aspects": ["приоритетный_аспект1", "приоритетный_аспект2"]
}}
"""
        return ChatPromptTemplate.from_template(template)
    
    def _create_research_prompt(self) -> ChatPromptTemplate:
        """Создает промпт для исследования конкретного аспекта"""
        template = """
Ты - исследователь, изучающий конкретный аспект вопроса.

ОРИГИНАЛЬНЫЙ ВОПРОС: {original_question}
ТЕКУЩИЙ АСПЕКТ: {current_aspect}
ДОСТУПНЫЕ ДАННЫЕ: {research_data}

Проанализируй предоставленные данные и сформулируй выводы по данному аспекту.

Верни ответ в формате JSON:
{{
    "key_findings": ["ключевое_находка1", "ключевое_находка2"],
    "insights": ["инсайт1", "инсайт2"],
    "follow_up_questions": ["дополнительный_вопрос1", "дополнительный_вопрос2"],
    "confidence_level": "высокий/средний/низкий"
}}
"""
        return ChatPromptTemplate.from_template(template)
    
    def _create_synthesis_prompt(self) -> ChatPromptTemplate:
        """Создает промпт для синтеза всех результатов"""
        template = """
Ты - эксперт, синтезирующий результаты всестороннего исследования.

ОРИГИНАЛЬНЫЙ ВОПРОС: {original_question}
РЕЗУЛЬТАТЫ АНАЛИЗА: {analysis_results}
ДАННЫЕ ИССЛЕДОВАНИЯ: {research_data}
ОБРАБОТАННЫЕ АСПЕКТЫ: {processed_aspects}

Создай итоговый отчет, включающий:

1. КРАТКИЙ ОТВЕТ на основной вопрос
2. КЛЮЧЕВЫЕ ВЫВОДЫ по каждому аспекту
3. ОБЩИЕ ИНСАЙТЫ
4. РЕКОМЕНДАЦИИ для дальнейшего изучения
5. УРОВЕНЬ УВЕРЕННОСТИ в выводах

Верни структурированный ответ в формате JSON:
{{
    "summary": "краткий ответ на основной вопрос",
    "key_conclusions": ["вывод1", "вывод2", "вывод3"],
    "insights": ["инсайт1", "инсайт2"],
    "recommendations": ["рекомендация1", "рекомендация2"],
    "confidence": "высокий/средний/низкий",
    "sources_used": ["источник1", "источник2"]
}}
"""
        return ChatPromptTemplate.from_template(template)
    
    def analyze_question(self, state: AgentState) -> AgentState:
        """Анализирует вопрос и разбивает его на аспекты"""
        logger.info("Начинаю анализ вопроса")
        
        prompt = self._create_analysis_prompt()
        messages = prompt.format_messages(question=state["original_question"])
        
        response = self.llm.invoke(messages)
        
        try:
            analysis_data = json.loads(response.content)
            state["analysis_results"] = analysis_data
            state["aspects_to_process"] = analysis_data.get("aspects", [])
            state["processed_aspects"] = []
            state["research_data"] = []
            state["iteration_count"] = 0
            
            logger.info(f"Вопрос разбит на {len(state['aspects_to_process'])} аспектов")
            
        except json.JSONDecodeError:
            logger.error("Ошибка парсинга JSON ответа от LLM")
            state["analysis_results"] = {"error": "Ошибка анализа"}
            state["aspects_to_process"] = []
        
        return state
    
    def research_aspect(self, state: AgentState) -> AgentState:
        """Исследует конкретный аспект вопроса"""
        if not state["aspects_to_process"]:
            return state
        
        current_aspect = state["aspects_to_process"].pop(0)
        state["current_aspect"] = current_aspect
        state["iteration_count"] += 1
        
        logger.info(f"Исследую аспект: {current_aspect}")
        
        # Формируем поисковые запросы для аспекта
        search_queries = [
            f"{state['original_question']} {current_aspect}",
            current_aspect,
            f"что такое {current_aspect}",
            f"{current_aspect} анализ"
        ]
        
        aspect_research_data = []
        
        # Выполняем поиск по каждому запросу
        for query in search_queries[:2]:  # Ограничиваем количество запросов
            try:
                search_results = web_search_tool.search(query)
                aspect_research_data.extend(search_results)
                
                # Загружаем содержимое первых 2-3 URL
                for result in search_results[:2]:
                    if result.get("url"):
                        url_content = url_content_tool.load_url(result["url"])
                        if url_content.get("success"):
                            aspect_research_data.append(url_content)
                
            except Exception as e:
                logger.error(f"Ошибка при исследовании аспекта {current_aspect}: {e}")
        
        # Анализируем собранные данные
        research_prompt = self._create_research_prompt()
        messages = research_prompt.format_messages(
            original_question=state["original_question"],
            current_aspect=current_aspect,
            research_data=json.dumps(aspect_research_data, ensure_ascii=False)
        )
        
        try:
            response = self.llm.invoke(messages)
            aspect_analysis = json.loads(response.content)
            
            # Сохраняем результаты
            aspect_data = {
                "aspect": current_aspect,
                "research_data": aspect_research_data,
                "analysis": aspect_analysis,
                "timestamp": datetime.now().isoformat()
            }
            
            state["research_data"].append(aspect_data)
            state["processed_aspects"].append(current_aspect)
            
            logger.info(f"Аспект {current_aspect} обработан")
            
        except Exception as e:
            logger.error(f"Ошибка анализа аспекта {current_aspect}: {e}")
            state["processed_aspects"].append(current_aspect)
        
        return state
    
    def should_continue(self, state: AgentState) -> str:
        """Определяет, нужно ли продолжать исследование"""
        if (state["iteration_count"] >= settings.max_iterations or 
            not state["aspects_to_process"]):
            return "synthesize"
        return "research"
    
    def synthesize_results(self, state: AgentState) -> AgentState:
        """Синтезирует все результаты исследования"""
        logger.info("Синтезирую результаты исследования")
        
        synthesis_prompt = self._create_synthesis_prompt()
        messages = synthesis_prompt.format_messages(
            original_question=state["original_question"],
            analysis_results=json.dumps(state["analysis_results"], ensure_ascii=False),
            research_data=json.dumps(state["research_data"], ensure_ascii=False),
            processed_aspects=json.dumps(state["processed_aspects"], ensure_ascii=False)
        )
        
        try:
            response = self.llm.invoke(messages)
            final_results = json.loads(response.content)
            state["final_insights"] = final_results
            
            logger.info("Синтез результатов завершен")
            
        except Exception as e:
            logger.error(f"Ошибка синтеза результатов: {e}")
            state["final_insights"] = {"error": "Ошибка синтеза"}
        
        return state
    
    def _create_agent_graph(self) -> StateGraph:
        """Создает граф состояний для агента"""
        workflow = StateGraph(AgentState)
        
        # Добавляем узлы
        workflow.add_node("analyze", self.analyze_question)
        workflow.add_node("research", self.research_aspect)
        workflow.add_node("synthesize", self.synthesize_results)
        
        # Добавляем рёбра
        workflow.set_entry_point("analyze")
        workflow.add_edge("analyze", "research")
        workflow.add_conditional_edges(
            "research",
            self.should_continue,
            {
                "research": "research",
                "synthesize": "synthesize"
            }
        )
        workflow.add_edge("synthesize", END)
        
        return workflow.compile()
    
    def process_question(self, question: str) -> Dict[str, Any]:
        """
        Обрабатывает вопрос и возвращает всесторонний анализ
        
        Args:
            question: Вопрос для анализа
            
        Returns:
            Словарь с результатами анализа
        """
        logger.info(f"Начинаю обработку вопроса: {question}")
        
        # Инициализируем состояние
        initial_state = {
            "messages": [HumanMessage(content=question)],
            "original_question": question,
            "analysis_results": {},
            "current_aspect": "",
            "aspects_to_process": [],
            "processed_aspects": [],
            "research_data": [],
            "final_insights": [],
            "iteration_count": 0
        }
        
        # Запускаем граф
        try:
            final_state = self.graph.invoke(initial_state)
            logger.info("Обработка вопроса завершена")
            return final_state
        except Exception as e:
            logger.error(f"Ошибка при обработке вопроса: {e}")
            return {
                "error": str(e),
                "original_question": question
            }
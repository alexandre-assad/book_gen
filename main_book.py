

from app.orchestrator.agent_orchestrator import AgentOrchestrator
from domain.enum.book_type import BookType


AgentOrchestrator().orchestrate('Write a book about Eneagram, arround 500 words', BookType.PersonnalDevelopment)
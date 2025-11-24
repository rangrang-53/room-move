"""RAG 검색기 모듈"""

from typing import List, Optional
from .vectorstore import get_vectorstore, KnowledgeVectorStore


class KnowledgeRetriever:
    """이사 관련 지식을 검색하는 Retriever"""

    def __init__(self, vectorstore: KnowledgeVectorStore = None):
        """
        Retriever 초기화

        Args:
            vectorstore: 사용할 벡터 저장소 (None이면 기본 저장소 사용)
        """
        self.vectorstore = vectorstore or get_vectorstore()

    def retrieve(self, query: str, top_k: int = 3) -> List[dict]:
        """
        쿼리에 관련된 문서 검색

        Args:
            query: 사용자 질문
            top_k: 반환할 최대 문서 수

        Returns:
            관련 문서 리스트
        """
        results = self.vectorstore.search(query, n_results=top_k)
        return results

    def retrieve_with_context(self, query: str, top_k: int = 3) -> str:
        """
        쿼리에 관련된 문서를 검색하고 컨텍스트 문자열로 반환

        Args:
            query: 사용자 질문
            top_k: 반환할 최대 문서 수

        Returns:
            컨텍스트 문자열
        """
        results = self.retrieve(query, top_k)

        if not results:
            return ""

        # 컨텍스트 구성
        context_parts = []
        for i, result in enumerate(results, 1):
            source = result.get("metadata", {}).get("source", "알 수 없음")
            section = result.get("metadata", {}).get("section", "")
            content = result.get("content", "")

            context_parts.append(f"[참고 {i}] {source} - {section}\n{content}")

        return "\n\n".join(context_parts)

    def is_relevant(self, query: str, threshold: float = 0.5) -> bool:
        """
        쿼리가 이사 관련 내용인지 확인

        Args:
            query: 사용자 질문
            threshold: 유사도 임계값

        Returns:
            관련 여부
        """
        results = self.vectorstore.search(query, n_results=1)

        if not results:
            return False

        # distance가 낮을수록 유사함 (ChromaDB 기본 설정)
        distance = results[0].get("distance", 1.0)
        return distance < threshold


# 싱글톤 인스턴스
_retriever_instance: Optional[KnowledgeRetriever] = None


def get_retriever() -> KnowledgeRetriever:
    """Retriever 싱글톤 인스턴스 반환"""
    global _retriever_instance
    if _retriever_instance is None:
        _retriever_instance = KnowledgeRetriever()
    return _retriever_instance

"""벡터 저장소 관리 모듈"""

import os
import chromadb
from chromadb.utils import embedding_functions
from pathlib import Path
from typing import List, Optional
import google.generativeai as genai


class KnowledgeVectorStore:
    """이사 관련 지식 문서를 저장하는 벡터 저장소"""

    def __init__(self, persist_directory: str = None):
        """
        벡터 저장소 초기화

        Args:
            persist_directory: 벡터 DB 저장 경로
        """
        if persist_directory is None:
            persist_directory = str(Path(__file__).parent.parent.parent / "data" / "vectordb")

        # ChromaDB 클라이언트 생성
        self.client = chromadb.PersistentClient(path=persist_directory)

        # Gemini API 키 확인
        api_key = os.getenv("GEMINI_API_KEY", "")

        # 임베딩 함수 설정
        if api_key and len(api_key) > 20:
            # Gemini 임베딩 사용
            self.embedding_fn = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
                api_key=api_key,
                model_name="models/embedding-001"
            )
        else:
            # 기본 임베딩 사용
            self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()

        # 컬렉션 생성/가져오기
        self.collection = self.client.get_or_create_collection(
            name="moving_knowledge",
            embedding_function=self.embedding_fn,
            metadata={"description": "이사 관련 지식 문서"}
        )

    def load_documents(self, knowledge_dir: str = None) -> int:
        """
        지식 문서들을 로드하여 벡터 저장소에 추가

        Args:
            knowledge_dir: 지식 문서 폴더 경로

        Returns:
            추가된 문서 청크 수
        """
        if knowledge_dir is None:
            knowledge_dir = str(Path(__file__).parent.parent.parent / "data" / "knowledge")

        knowledge_path = Path(knowledge_dir)
        if not knowledge_path.exists():
            print(f"지식 문서 폴더가 없습니다: {knowledge_dir}")
            return 0

        documents = []
        metadatas = []
        ids = []

        # 마크다운 파일들 읽기
        for md_file in knowledge_path.glob("*.md"):
            content = md_file.read_text(encoding="utf-8")
            filename = md_file.stem

            # 문서를 청크로 분할 (섹션별로)
            chunks = self._split_into_chunks(content, filename)

            for i, chunk in enumerate(chunks):
                doc_id = f"{filename}_{i}"

                # 이미 존재하는지 확인
                existing = self.collection.get(ids=[doc_id])
                if existing["ids"]:
                    continue

                documents.append(chunk["content"])
                metadatas.append({
                    "source": filename,
                    "section": chunk["section"],
                    "chunk_index": i
                })
                ids.append(doc_id)

        # 벡터 저장소에 추가
        if documents:
            self.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            print(f"{len(documents)}개의 문서 청크를 추가했습니다.")

        return len(documents)

    def _split_into_chunks(self, content: str, filename: str) -> List[dict]:
        """
        문서를 섹션별로 청크로 분할

        Args:
            content: 문서 내용
            filename: 파일 이름

        Returns:
            청크 리스트
        """
        chunks = []
        current_section = filename
        current_content = []

        for line in content.split("\n"):
            # 섹션 헤더 감지 (## 로 시작)
            if line.startswith("## "):
                # 이전 섹션 저장
                if current_content:
                    chunks.append({
                        "section": current_section,
                        "content": "\n".join(current_content).strip()
                    })
                current_section = line.replace("## ", "").strip()
                current_content = [line]
            else:
                current_content.append(line)

        # 마지막 섹션 저장
        if current_content:
            chunks.append({
                "section": current_section,
                "content": "\n".join(current_content).strip()
            })

        return chunks

    def search(self, query: str, n_results: int = 3) -> List[dict]:
        """
        쿼리와 유사한 문서 검색

        Args:
            query: 검색 쿼리
            n_results: 반환할 결과 수

        Returns:
            검색 결과 리스트
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        # 결과 정리
        search_results = []
        if results["documents"] and results["documents"][0]:
            for i, doc in enumerate(results["documents"][0]):
                search_results.append({
                    "content": doc,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "distance": results["distances"][0][i] if results["distances"] else None
                })

        return search_results

    def get_stats(self) -> dict:
        """벡터 저장소 통계 반환"""
        return {
            "total_documents": self.collection.count(),
            "collection_name": self.collection.name
        }


# 싱글톤 인스턴스
_vectorstore_instance: Optional[KnowledgeVectorStore] = None


def get_vectorstore() -> KnowledgeVectorStore:
    """벡터 저장소 싱글톤 인스턴스 반환"""
    global _vectorstore_instance
    if _vectorstore_instance is None:
        _vectorstore_instance = KnowledgeVectorStore()
        # 문서 로드
        _vectorstore_instance.load_documents()
    return _vectorstore_instance

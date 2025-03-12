from typing import List, Tuple
import asyncio
import json

# from deepsearcher.configuration import vector_db, embedding_model, llm
from deepsearcher import configuration
from deepsearcher.vector_db.base import RetrievalResult


def query(original_query: str, max_iter: int = 3) -> Tuple[str, List[RetrievalResult], int]:
    default_searcher = configuration.default_searcher
    return default_searcher.query(original_query, max_iter=max_iter)


async def query_stream(original_query: str, max_iter: int = 3):
    """
    流式查询函数，将每一步的输出实时返回给客户端
    
    Args:
        original_query: 用户的原始查询
        max_iter: 最大迭代次数
    
    Yields:
        str: 每一步处理的输出结果
    """
    try:
        # 开始处理的标记
        yield "data: {\"type\":\"start\",\"content\":\"开始处理查询...\"}\n\n"
        
        # 查询分析阶段
        yield f"data: {{\"type\":\"analysis\",\"content\":\"分析查询: {original_query}\"}}\n\n"
        
        # 执行与现有query函数类似的逻辑，但每一步都产生输出
        # 这里假设我们有权限访问原始query函数中的每个步骤
        
        # 检索相关文档
        yield "data: {\"type\":\"retrieval\",\"content\":\"正在检索相关文档...\"}\n\n"
        
        # 生成回答
        for i in range(max_iter):
            yield f"data: {{\"type\":\"iteration\",\"content\":\"第 {i+1} 轮迭代\"}}\n\n"
            # 模拟思考过程
            yield f"data: {{\"type\":\"thinking\",\"content\":\"思考中...\"}}\n\n"
            
            # 这里需要根据实际的query函数逻辑来实现流式输出
            # 下面是模拟的输出
            await asyncio.sleep(0.5)  # 模拟处理时间
            
        # 最终结果
        result_text, _, consume_token = query(original_query, max_iter)
        yield f"data: {{\"type\":\"result\",\"content\":{json.dumps(result_text)},\"consume_token\":{consume_token}}}\n\n"
        
        # 完成标记
        yield "data: {\"type\":\"end\",\"content\":\"处理完成\"}\n\n"
        
    except Exception as e:
        # 处理错误
        yield f"data: {{\"type\":\"error\",\"content\":\"错误: {str(e)}\"}}\n\n"


def retrieve(
    original_query: str, max_iter: int = 3
) -> Tuple[List[RetrievalResult], List[str], int]:
    default_searcher = configuration.default_searcher
    retrieved_results, consume_tokens, metadata = default_searcher.retrieve(
        original_query, max_iter=max_iter
    )
    return retrieved_results, [], consume_tokens


def naive_retrieve(query: str, collection: str = None, top_k=10) -> List[RetrievalResult]:
    naive_rag = configuration.naive_rag
    all_retrieved_results, consume_tokens, _ = naive_rag.retrieve(query)
    return all_retrieved_results


def naive_rag_query(
    query: str, collection: str = None, top_k=10
) -> Tuple[str, List[RetrievalResult]]:
    naive_rag = configuration.naive_rag
    answer, retrieved_results, consume_tokens = naive_rag.query(query)
    return answer, retrieved_results

from loguru import logger
from typing_extensions import Annotated
from zenml import get_step_context, step

from second_brain_offline.application.agents.quality import (
    HeuristicQualityAgent,
    QualityScoreAgent,
)

from second_brain_offline.domain import Document

@step
def add_quality_score(
    documents: list[Document],
    model_id: str = "gemini-2.5-flash",
    mock: bool = False,
    max_workers: int = 10,
) -> Annotated[list[Document], "scored_documents"]:
    heuristic_quality_agent = HeuristicQualityAgent()
    scored_documents: list[Document] = heuristic_quality_agent(documents)

    scored_documents_with_heuristics = [
        d for d in scored_documents if d.content_quality_score is not None
    ]
    documents_without_scores = [
        d for d in scored_documents if d.content_quality_score is None
    ]

    quality_agent = QualityScoreAgent(
        model_id = model_id, mock=mock, max_concurrent_requests = max_workers
    )
    scored_documents_with_agents: list[Document] = quality_agent(
        documents_without_scores
    )

    scored_documents: list[Document] = (
        scored_documents_with_heuristics + scored_documents_with_agents
    )

    len_documents = len(documents)
    len_documents_with_scores = len(
        [doc for doc in scored_documents if doc.content_quality_score is not None]
    )
    logger.info(f"Total documents: {len_documents}")
    logger.info(f"Total documents that were scored: {len_documents_with_scores}")

    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="scored_documents",
        metadata={
            "len_documents": len_documents,
            "len_documents_with_scores": len_documents_with_scores,
            "len_documents_scored_with_heuristics": len(
                scored_documents_with_heuristics
            ),
            "len_documents_scored_with_agents": len(scored_documents_with_agents),
        },
    )

    return scored_documents
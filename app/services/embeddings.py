import asyncio
import json
import boto3
from app.config import settings

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = boto3.client("bedrock-runtime", region_name=settings.AWS_REGION)
    return _client


def menu_item_blurb(name: str, description: str | None, category_name: str | None, is_vegetarian: bool) -> str:
    parts = [name]
    if category_name:
        parts.append(category_name)
    if description:
        parts.append(description)
    parts.append("vegetarian" if is_vegetarian else "non-vegetarian")
    return ". ".join(parts)


async def embed_text(text: str) -> list[float]:
    """Embeds text via Bedrock Titan (amazon.titan-embed-text-v2:0) — returns a 1024-dim vector."""
    client = _get_client()

    def _invoke():
        response = client.invoke_model(
            modelId=settings.BEDROCK_EMBED_MODEL_ID,
            body=json.dumps({"inputText": text}),
        )
        body = json.loads(response["body"].read())
        return body["embedding"]

    return await asyncio.to_thread(_invoke)

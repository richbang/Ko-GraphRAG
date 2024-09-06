import logging
from typing import Any

from tenacity import (
    AsyncRetrying,
    RetryError,
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

from graphrag.query.llm.base import BaseLLMCallback
from graphrag.query.llm.oai.base import OpenAILLMImpl  # 기존의 OpenAILLMImpl을 계속 사용하거나 필요에 따라 새로 정의할 수 있습니다.
import ollama

log = logging.getLogger(__name__)


class OpenAI(OpenAILLMImpl):
    """Wrapper for Ollama LLM models."""

    def __init__(
        self,
        api_key: str,
        model: str,
        deployment_name: str | None = None,
        api_base: str | None = None,
        api_version: str | None = None,
        organization: str | None = None,
        max_retries: int = 10,
        retry_error_types: tuple[type[BaseException]] = (RetryError,),  # 예외 타입 설정
        num_ctx: int = 34000,
    ):
        self.api_key = api_key
        self.model = model
        self.deployment_name = deployment_name
        self.api_base = api_base
        self.api_version = api_version
        self.organization = organization
        self.max_retries = max_retries
        self.retry_error_types = retry_error_types
        self.options = {
            "num_ctx": num_ctx,
        }

    def generate(
        self,
        messages: str | list[str],
        streaming: bool = True,
        callbacks: list[BaseLLMCallback] | None = None,
        **kwargs: Any,
    ) -> str:
        """Generate text using Ollama LLM."""
        try:
            retryer = Retrying(
                stop=stop_after_attempt(self.max_retries),
                wait=wait_exponential_jitter(max=10),
                reraise=True,
                retry=retry_if_exception_type(self.retry_error_types),
            )
            for attempt in retryer:
                with attempt:
                    return self._generate(
                        messages=messages,
                        streaming=streaming,
                        callbacks=callbacks,
                        **kwargs,
                    )
        except RetryError:
            log.exception("RetryError at generate(): %s")
            return ""
        else:
            return ""

    async def agenerate(
        self,
        messages: str | list[str],
        streaming: bool = True,
        callbacks: list[BaseLLMCallback] | None = None,
        **kwargs: Any,
    ) -> str:
        """Generate Text Asynchronously using Ollama LLM."""
        try:
            retryer = AsyncRetrying(
                stop=stop_after_attempt(self.max_retries),
                wait=wait_exponential_jitter(max=10),
                reraise=True,
                retry=retry_if_exception_type(self.retry_error_types),
            )
            async for attempt in retryer:
                with attempt:
                    return await self._agenerate(
                        messages=messages,
                        streaming=streaming,
                        callbacks=callbacks,
                        **kwargs,
                    )
        except RetryError:
            log.exception("Error at agenerate()")
            return ""
        else:
            return ""

    def _generate(
        self,
        messages: str | list[str],
        streaming: bool = True,
        callbacks: list[BaseLLMCallback] | None = None,
        **kwargs: Any,
    ) -> str:
        response = ollama.chat_completions.create(
            model=self.model,
            messages=messages,
            options=self.options,
            stream=streaming,
            **kwargs,
        )
        if streaming:
            full_response = ""
            for chunk in response:
                if not chunk or not chunk.choices:
                    continue

                delta = (
                    chunk.choices[0].delta.content
                    if chunk.choices[0].delta and chunk.choices[0].delta.content
                    else ""
                )

                full_response += delta
                if callbacks:
                    for callback in callbacks:
                        callback.on_llm_new_token(delta)
                if chunk.choices[0].finish_reason == "stop":
                    break
            return full_response
        return response.choices[0].message.content or ""

    async def _agenerate(
        self,
        messages: str | list[str],
        streaming: bool = True,
        callbacks: list[BaseLLMCallback] | None = None,
        **kwargs: Any,
    ) -> str:
        response = await ollama.chat_completions.create_async(
            model=self.model,
            messages=messages,
            options=self.options,
            stream=streaming,
            **kwargs,
        )
        if streaming:
            full_response = ""
            async for chunk in response:
                if not chunk or not chunk.choices:
                    continue

                delta = (
                    chunk.choices[0].delta.content
                    if chunk.choices[0].delta and chunk.choices[0].delta.content
                    else ""
                )

                full_response += delta
                if callbacks:
                    for callback in callbacks:
                        callback.on_llm_new_token(delta)
                if chunk.choices[0].finish_reason == "stop":
                    break
            return full_response
        return response.choices[0].message.content or ""

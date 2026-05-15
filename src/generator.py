from __future__ import annotations

from typing import Any


DEFAULT_SYSTEM_PROMPT = """أنت مساعد قانوني متخصص في القانون المصري.
التزم بالقواعد الآتية التزامًا صارمًا:
1. أجب فقط باستخدام النصوص القانونية الموجودة في السياق المقدم.
2. لا تخترع أو تستنتج قوانين أو مواد غير مذكورة في السياق.
3. إذا لم يتضمن السياق معلومات كافية للإجابة، قل نصًا:
"بناءً على النصوص القانونية المتاحة، لا توجد معلومات كافية للإجابة."
4. يجب أن تكون الإجابة باللغة العربية، واضحة ومباشرة.
5. في نهاية الإجابة، اذكر دائمًا الاستشهادات باستخدام اسم القانون ورقم المادة كما وردا في بيانات السياق."""


INSUFFICIENT_CONTEXT_ANSWER = (
    "بناءً على النصوص القانونية المتاحة، لا توجد معلومات كافية للإجابة."
)


class LegalAnswerGenerator:
    """Generate grounded Egyptian legal answers from retrieved RAG chunks."""

    def __init__(
        self,
        llm: Any,
        system_prompt: str | None = None,
        model: str | None = None,
    ) -> None:
        """Initialize with an OpenAI client or LangChain-style chat model."""
        self.llm = llm
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        self.model = model

    def generate_answer(self, query: str, retrieved_chunks: list[dict]) -> dict:
        """Return an answer grounded only in retrieved chunks, with citations."""
        citations = self._extract_citations(retrieved_chunks)

        if not retrieved_chunks:
            return {"answer": INSUFFICIENT_CONTEXT_ANSWER, "citations": []}

        context = self._format_context(retrieved_chunks)
        user_prompt = self._build_user_prompt(query=query, context=context)
        answer = self._call_llm(user_prompt).strip()
        answer = self._ensure_citations(answer, citations)

        return {"answer": answer, "citations": citations}

    def _format_context(self, retrieved_chunks: list[dict]) -> str:
        """Format retrieved legal chunks into a structured context block."""
        formatted_chunks = []

        for index, chunk in enumerate(retrieved_chunks, start=1):
            metadata = chunk.get("metadata", {}) or {}
            law_name = self._metadata_value(metadata, "law_name", "law")
            article_num = self._metadata_value(
                metadata,
                "article_num",
                "article_number",
                "article",
            )
            text = str(chunk.get("text", "")).strip()

            formatted_chunks.append(
                "\n".join(
                    [
                        f"[النص القانوني رقم {index}]",
                        f"اسم القانون: {law_name}",
                        f"رقم المادة: {article_num}",
                        "النص:",
                        text,
                    ]
                )
            )

        return "\n\n---\n\n".join(formatted_chunks)

    def _build_user_prompt(self, query: str, context: str) -> str:
        """Build the final user prompt sent to the chat model."""
        return "\n\n".join(
            [
                "السياق القانوني المتاح:",
                context,
                "السؤال:",
                query.strip(),
                (
                    "أجب على السؤال اعتمادًا على السياق فقط، ثم اختم الإجابة "
                    "بالاستشهادات القانونية ذات الصلة."
                ),
            ]
        )

    def _extract_citations(self, retrieved_chunks: list[dict]) -> list[str]:
        """Extract unique citations from chunk metadata."""
        citations: list[str] = []
        seen: set[str] = set()

        for chunk in retrieved_chunks:
            metadata = chunk.get("metadata", {}) or {}
            law_name = self._metadata_value(metadata, "law_name", "law")
            article_num = self._metadata_value(
                metadata,
                "article_num",
                "article_number",
                "article",
            )
            citation = f"{law_name} - المادة {article_num}"

            if citation not in seen:
                seen.add(citation)
                citations.append(citation)

        return citations

    def _metadata_value(self, metadata: dict, *keys: str) -> str:
        """Read a metadata value, accepting common local schema aliases."""
        for key in keys:
            value = metadata.get(key)
            if value is not None and str(value).strip():
                return str(value).strip()
        return "غير محدد"

    def _ensure_citations(self, answer: str, citations: list[str]) -> str:
        """Append metadata citations to the end of the answer if available."""
        if not citations:
            return answer

        citation_lines = "\n".join(f"- {citation}" for citation in citations)
        citation_block = f"الاستشهادات:\n{citation_lines}"

        if citation_block in answer:
            return answer

        return f"{answer}\n\n{citation_block}"

    def _call_llm(self, user_prompt: str) -> str:
        """Call either a LangChain chat model or an OpenAI API client."""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        if hasattr(self.llm, "invoke"):
            response = self.llm.invoke(
                [
                    ("system", self.system_prompt),
                    ("user", user_prompt),
                ]
            )
            return self._message_content(response)

        if hasattr(self.llm, "chat") and hasattr(self.llm.chat, "completions"):
            model = self._resolve_model_name()
            response = self.llm.chat.completions.create(
                model=model,
                messages=messages,
            )
            return response.choices[0].message.content or ""

        if hasattr(self.llm, "responses"):
            model = self._resolve_model_name()
            response = self.llm.responses.create(
                model=model,
                input=messages,
            )
            return self._message_content(response)

        raise TypeError(
            "Unsupported LLM interface. Provide a LangChain chat model or "
            "an OpenAI client with chat.completions or responses support."
        )

    def _resolve_model_name(self) -> str:
        """Resolve the OpenAI model name for raw OpenAI clients."""
        model = self.model or getattr(self.llm, "model", None)
        if not model:
            raise ValueError("A model name is required when using a raw OpenAI client.")
        return str(model)

    def _message_content(self, response: Any) -> str:
        """Normalize response text from common chat model return objects."""
        if isinstance(response, str):
            return response

        content = getattr(response, "content", None)
        if isinstance(content, str):
            return content

        output_text = getattr(response, "output_text", None)
        if isinstance(output_text, str):
            return output_text

        if isinstance(response, dict):
            content = response.get("content") or response.get("output_text")
            if isinstance(content, str):
                return content

        return str(response)

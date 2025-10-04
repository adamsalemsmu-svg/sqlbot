"""
LLM client wrapper.

This module centralises calls to the underlying language model.  It
supports OpenAI’s chat completion API via the ``openai`` library when an
API key is provided.  In the absence of a key the client simply echoes
back the user input.  You can plug in another provider by modifying
``call_llm`` accordingly.
"""

import os
from typing import Optional

try:
    import openai
    from openai import OpenAIError
except Exception:  # pragma: no cover
    openai = None  # type: ignore
    OpenAIError = Exception  # type: ignore

# Read environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")


def call_llm(prompt: str, system_prompt: Optional[str] = None) -> str:
    """Send a prompt to the configured LLM and return the generated response.

    If no API key is set or the openai library is unavailable the
    prompt is simply echoed back.  When using the OpenAI API you can
    optionally pass a ``system_prompt`` to steer the assistant’s
    behaviour.

    Args:
        prompt: The user’s message.
        system_prompt: An optional system instruction.

    Returns:
        The assistant’s reply.
    """

    # Fallback: echo the prompt if no API key or openai unavailable
    if not API_KEY or openai is None:
        return f"(echo) {prompt}"

    # Configure client
    openai.api_key = API_KEY

    try:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = openai.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
        )
        # Extract the text from the first choice
        return response.choices[0].message.content.strip()
    except OpenAIError as e:  # pragma: no cover
        # On error, fall back to echoing the prompt with the error message
        return f"(error) {str(e)}"
"""Leon's custom Codex Image provider — wraps Codex CLI generate.py.

Runs ``python3 ~/.claude/skills/codex-image/generate.py`` which uses
``codex exec`` (ChatGPT Plus subscription, no API billing).
"""

from __future__ import annotations

import logging
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

from agent.image_gen_provider import (
    DEFAULT_ASPECT_RATIO,
    ImageGenProvider,
    error_response,
    success_response,
)

logger = logging.getLogger(__name__)

GENERATE_SCRIPT = os.path.expanduser("~/.claude/skills/codex-image/generate.py")
CODEX_BIN = "/Applications/Codex.app/Contents/Resources/codex"

_SIZES = {
    "landscape": "1536x1024",
    "square": "1024x1024",
    "portrait": "1024x1536",
}
_OUTPUT_DIR = os.path.expanduser("~/Downloads")


class CodexImageProvider(ImageGenProvider):
    """Leon's custom Codex Image provider via Codex CLI."""

    @property
    def name(self) -> str:
        return "codex-image"

    @property
    def display_name(self) -> str:
        return "Codex Image (Codex CLI)"

    def is_available(self) -> bool:
        return os.path.isfile(GENERATE_SCRIPT) and (
            os.path.isfile(CODEX_BIN) or os.path.isfile("/usr/local/bin/codex")
        )

    def list_models(self) -> List[Dict[str, Any]]:
        return [{
            "id": "codex-image-2",
            "display": "Codex Image 2 (Codex CLI)",
            "speed": "~40s",
            "strengths": "ChatGPT Plus, no API cost",
            "price": "free (Plus sub)",
        }]

    def default_model(self) -> Optional[str]:
        return "codex-image-2"

    def get_setup_schema(self) -> Dict[str, Any]:
        return {
            "name": "Codex Image (Codex CLI)",
            "badge": "free",
            "tag": "Leon's codex-image via Codex CLI — ChatGPT Plus, no API key",
            "env_vars": [],
            "post_setup_hint": "Uses Codex.app + ChatGPT Plus. No extra setup needed.",
        }

    def generate(
        self,
        prompt: str,
        aspect_ratio: str = DEFAULT_ASPECT_RATIO,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        prompt = (prompt or "").strip()
        if not prompt:
            return error_response(
                error="Prompt is required",
                error_type="invalid_argument",
                provider="codex-image",
                aspect_ratio=aspect_ratio,
            )

        size = _SIZES.get(aspect_ratio, _SIZES["square"])
        os.makedirs(_OUTPUT_DIR, exist_ok=True)

        try:
            result = subprocess.run(
                ["python3", GENERATE_SCRIPT, prompt, size, _OUTPUT_DIR],
                capture_output=True,
                text=True,
                timeout=900,
                env={**os.environ},
            )
        except subprocess.TimeoutExpired:
            return error_response(
                error="Image generation timed out (15 min)",
                error_type="timeout",
                provider="codex-image",
                prompt=prompt,
                aspect_ratio=aspect_ratio,
            )
        except Exception as exc:
            return error_response(
                error=f"Failed to run generate.py: {exc}",
                error_type="internal_error",
                provider="codex-image",
                prompt=prompt,
                aspect_ratio=aspect_ratio,
            )

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()

        if stderr:
            logger.debug("codex-image stderr: %s", stderr)

        if result.returncode != 0:
            return error_response(
                error=f"generate.py exited {result.returncode}: {stderr or stdout}",
                error_type="api_error",
                provider="codex-image",
                prompt=prompt,
                aspect_ratio=aspect_ratio,
            )

        for line in stdout.splitlines():
            line = line.strip()
            if line.startswith("SUCCESS:"):
                image_path = line[len("SUCCESS:"):].strip()
                if os.path.isfile(image_path):
                    return success_response(
                        image=image_path,
                        model="codex-image-2",
                        prompt=prompt,
                        aspect_ratio=aspect_ratio,
                        provider="codex-image",
                        extra={"size": size, "output_dir": _OUTPUT_DIR},
                    )
                return error_response(
                    error=f"generate.py reported success but file not found: {image_path}",
                    error_type="io_error",
                    provider="codex-image",
                    prompt=prompt,
                    aspect_ratio=aspect_ratio,
                )

            if line.startswith("ERROR:"):
                return error_response(
                    error=line[len("ERROR:"):].strip(),
                    error_type="api_error",
                    provider="codex-image",
                    prompt=prompt,
                    aspect_ratio=aspect_ratio,
                )

        return error_response(
            error="generate.py produced no recognizable output",
            error_type="empty_response",
            provider="codex-image",
            prompt=prompt,
            aspect_ratio=aspect_ratio,
        )


def register(ctx) -> None:
    ctx.register_image_gen_provider(CodexImageProvider())

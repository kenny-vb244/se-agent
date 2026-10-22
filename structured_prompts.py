
"""Execute structured prompt templates separately from Python tools."""

import os
import re
from pathlib import Path

import yaml
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
PROMPT_DIR = Path(__file__).parent / "prompts"
OUTPUT_DIR = Path(__file__).parent / "outputs"


def run_structured_prompt(
    chapter: str,
    project_description: str,
    context: str = "",
    previous_artifacts: str = "",
) -> dict:
    """Run a chapter prompt and return its response and routing data."""

    if not project_description.strip():
        raise ValueError("A project description is required.")

    # Explicitly map allowed chapter names to prompt files.
    prompt_files = {
        "ch2": "ch02-process-architecture-selection.prompt.md",
        "ch3": "ch03-development-practice-charter.prompt.md",
    }

    if chapter not in prompt_files:
        raise ValueError(f"Unsupported structured prompt: {chapter}")

    prompt_path = PROMPT_DIR / prompt_files[chapter]

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Missing prompt template: {prompt_path}"
        )

    template = prompt_path.read_text(encoding="utf-8")

    full_prompt = f"""
{template}

# INPUTS FOR THIS RUN

## PROJECT_DESCRIPTION
{project_description.strip()}

## OPTIONAL_CONTEXT
{context.strip() or "Not provided."}

## PREVIOUS_ARTIFACTS
{previous_artifacts.strip() or "Not provided."}

Follow the chapter template's required output format.
Do not invent missing project facts; identify assumptions and
follow any halt conditions specified in the template.
"""

    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError("GROQ_API_KEY is missing from .env.")

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Follow the supplied structured prompt carefully. "
                    "Preserve its required sections and output format."
                ),
            },
            {"role": "user", "content": full_prompt},
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("The model returned an empty response.")

    # Save the full response, even if later validation fails.
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / f"{chapter}-result.md"
    output_path.write_text(content, encoding="utf-8")

    # Extract fenced YAML blocks.
    blocks = re.findall(
        r"```(?:yaml|yml)\s*\n(.*?)```",
        content,
        flags=re.IGNORECASE | re.DOTALL,
    )

    parsed_blocks = []
    for block in blocks:
        try:
            parsed_blocks.append(yaml.safe_load(block))
        except yaml.YAMLError:
            continue

    # Find the Chapter 2 routing block.
    routing = None
    if chapter == "ch2":
        for block in parsed_blocks:
            if (
                isinstance(block, dict)
                and all(
                    key in block
                    for key in ("process_model", "stage_sequence", "halt")
                )
            ):
                routing = block
                break

        if routing is None:
            raise ValueError(
                "Could not locate a valid Chapter 2 routing block. "
                f"Review {output_path}."
            )

        if not isinstance(routing["halt"], bool):
            raise ValueError("'halt' must be true or false.")

        if not isinstance(routing["stage_sequence"], list):
            raise ValueError("'stage_sequence' must be a YAML list.")

    return {
        "chapter": chapter,
        "response": content,
        "routing": routing,
        "output_path": str(output_path),
        "model": MODEL,
    }

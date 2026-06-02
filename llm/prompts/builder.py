"""

OMEGA DRAKON • SYSTEMS

Tecnologia que respira.

Módulo: Prompt Builder

Descrição: Construção de prompts estruturados do runtime NV.

Interface Viva: Nicky Virthy

Arquiteto: Alex Projeti

"""

from llm.prompts.messages import Message


class PromptBuilder:

    @staticmethod
    def build(messages: list[Message]) -> str:

        prompt = ""

        for message in messages:

            prompt += (
                f"<|im_start|>{message.role}\n"
                f"{message.content}\n"
                f"<|im_end|>\n"
            )

        prompt += "<|im_start|>assistant\n"

        return prompt

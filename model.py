import openai
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TestingGenerator:
    def __init__(self, api_key, llm_model):
        self.api_key = api_key
        openai.api_key = self.api_key
        self.llm_model = llm_model

    def request(self, messages):
        try:
            response = openai.chat.completions.create(
                model=self.llm_model,
                messages=messages
            )
            return response
        except Exception as e:
            logger.error(f"Error during model create: {e}")
            raise Exception(f"Error during model create: {e}")

    def improve_prompt(self, prompt):
        prompt_instruction = f"""
           Sua tarefa é analisar uma função fornecida e gerar testes unitários abrangentes.
           Escolha o framework de teste mais adequado com base na linguagem usada na função. Certifique-se de:
        
            1. Cobrir os casos de uso principais da função.
            2. Incluir cenários de borda (edge cases).
            3. Validar entradas inválidas ou casos de erro, se aplicável.
            4. Criar testes claros, bem comentados e organizados.

            Aqui está o código da função:
            
            ```
            {prompt}
            ```

            Aplique os padrões GRASP  no teste gerado.

            Retorne apenas os códigos, sem explicações ou comentários adicionais.
            """

        return prompt_instruction

    def generate(self, prompt):
        messages = [
            {"role": "developer", "content": "Você é um desenvolvedor de software especialista em testes e padrões de projetos GRASP."},
            {"role": "user", "content": self.improve_prompt(prompt)}
        ]
        response = self.request(messages=messages)
        try:
            if response:
                message = response.choices[0].message
                content = message.content if hasattr(
                    message, "content") else message["content"]
                return content
            else:
                logger.error("Error during code generation: No message")
                raise Exception("Error during code generation: No message")
        except Exception as e:
            logger.error(f"Error during code generation: {e}")
            raise Exception(f"Error during code generation: {e}")

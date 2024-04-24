from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from config import Config
from recruitment_post import RecruitmentPost
from errors import BotMalformedResponseException, InvalidArgumentException, RecruitmentPostValidationException

class Chatbot():

    MAX_RETRIES = 3
    EMPTY_STRING_RESPONSES = ["not specified", "n/a"]

    def __init__(self, config : Config):
        self.config = config
        llm = self._get_llm()
        system_prompt = self.config.get_system_prompt()     
        if not system_prompt: raise InvalidArgumentException("no system prompt has been configured, cannot invoke bot")
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ])
        self.chain = prompt | llm | StrOutputParser()

    def _get_llm(self):
        if self.config.default_provider == "ollama":
            return ChatOllama(base_url=self.config.ollama.get("base_url"), model_name=self.config.ollama.get("model", "llama2"))
        return ChatOpenAI(
            api_key=self.config.openai.get("api_key"), base_url=self.config.openai.get("base_url"),
            model=self.config.openai.get("model", "gpt-3.5-turbo-0125")
        )

    def _parse_bot_response(self, resp : str) -> dict:
        mode = 0
        current_key = ""
        current_value = ""
        out = {}

        for pos in range(len(resp)):
            char = resp[pos]
            # build key
            if mode == 0:
                if char == ":":
                    mode = 1
                    continue
                elif char == "\n":
                    current_key = ""
                    continue
                current_key += char

            # build content
            elif mode == 1:
                if char == "\n" and pos+1 < len(resp):
                    next_line = resp[pos+1:].splitlines()[0].strip()
                    if next_line.endswith(":") and next_line.upper() == next_line:
                        current_value = current_value.strip()
                        if current_value.lower() in Chatbot.EMPTY_STRING_RESPONSES:
                            current_value = ""
                        out[current_key.strip().lower()] = current_value.strip()
                        mode = 0
                        current_key = ""
                        current_value = ""
                        continue
                current_value += char 

        return out       

    def _send_prompt_and_parse(self) -> Optional[dict]:
        bot_response = self.chain.invoke({"messages": self.messages})
    
        self.messages.append(AIMessage(content=bot_response))
        try:
            return self._parse_bot_response(bot_response)
        except Exception as e:
            raise e

    def _update_post_from_bot_response(self, resp : dict, post : RecruitmentPost):
        post.summary = resp.get("summary", "")
        post.schedule = resp.get("schedule", "")
        post.discord = list(filter(None, resp.get("discord", "").split(",")))
        post.tags = list(filter(None, resp.get("tags", "").split(",")))
        post.intent = resp.get("intent", "")
        post.jobs = list(filter(None, resp.get("jobs", "").split(",")))
        post.validate()

    def process_post(self, post : RecruitmentPost):

        # prepare prompt
        user_prompt = post.inject_into_prompt(self.config.get_user_prompt()).strip()
        if not user_prompt: raise InvalidArgumentException("no user prompt has been configured, cannot invoke bot")
        self.messages = [HumanMessage(content=user_prompt)]

        # send to bot and update post
        bot_resp = None
        for i in range(Chatbot.MAX_RETRIES):
            bot_resp = self._send_prompt_and_parse()
            if not bot_resp:
                print(" - Bot response was malformed")
                self.messages.append(HumanMessage(content="I couldn't understand your response. Please reformat your response and try again."))
                continue
            try:
                self._update_post_from_bot_response(bot_resp, post)
                return
            except RecruitmentPostValidationException as e:
                print(" - Bot response failed to validate: %s" % str(e))
                print(bot_resp)
                self.messages.append(HumanMessage(content="I couldn't validate your response, this is the error I got: %s" % str(e)))

        raise BotMalformedResponseException("recieved maximum allowed (%d) malformed responses from the bot" % Chatbot.MAX_RETRIES)


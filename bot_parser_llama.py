import time
import os
import datetime
import json
from llama_cpp import Llama, LlamaGrammar
from src.config import Config
from src.recruitment_post import RecruitmentPost

INPUT_PATH = "data/bot_input_queue"
OUTPUT_PATH = "data/output"

config = Config()

print("> Load grammar file.")
grammar = LlamaGrammar.from_file("conf/grammar.gbnf")

print("> Init Llama.cpp.")
llm = Llama.from_pretrained(
    #repo_id="bartowski/Hermes-2-Pro-Mistral-10.7B-GGUF",
    #filename="*Q6_K.gguf",
    #repo_id="MaziyarPanahi/Meta-Llama-3-70B-Instruct-GGUF",
    #filename="*Q2_XS.gguf",
    #repo_id="TheBloke/zephyr-7B-beta-GGUF",
    #filename="*Q5_K_S.gguf",
    repo_id="MaziyarPanahi/Llama-3-13B-Instruct-v0.1-GGUF",
    filename="*Q4_K_S.gguf",
    verbose=False,
    n_ctx=8000,
    n_gpu_layers=9999,
    top_p=0.1,
    do_sample=True,
    top_k=10,
    access_token=config.huggingface.get("access_token")
)


print("> Start processing.")
for file in os.scandir(INPUT_PATH):

    print("  - %s" % file.name)

    post = None
    with open(file, "r", encoding="utf-8") as f:
        post_dict = json.load(f)
        post = RecruitmentPost.from_dict(post_dict)
    if not post:
        print("\tERROR: couldn't parse")
        continue
    path_to = os.path.join(OUTPUT_PATH, file.name)
    if os.path.exists(path_to):
        print("\tSKIPPED: already processed")
        continue

    messages = [
        {"role": "system", "content": config.prompts.get("system", "")},
        {"role": "user", "content": "Here is a recruitment post that I need you to process:\n\n" + post.original_message}
    ]

    start_time = datetime.datetime.now()
    res = llm.create_chat_completion(
        messages=messages,
        grammar=grammar,
        temperature=0,
        max_tokens=4096
    )
    end_time = datetime.datetime.now()
    duration = end_time - start_time

    resp_dict = {}
    try:
        resp_dict = json.loads(res.get("choices", [{}])[0].get("message", {}).get("content", ""))
    except json.decoder.JSONDecodeError:
        print(res.get("choices", [{}])[0].get("message", {}).get("content", ""))
        print("\tERROR: json decode error, skipped")
        continue
    

    print("\tDONE: %d seconds" % (duration.seconds))

    post.intent = resp_dict.get("intent", "")
    post.schedule = resp_dict.get("schedule", "")
    post.summary = resp_dict.get("summary", "")
    post.tags = resp_dict.get("tags", [])
    post.roles = resp_dict.get("roles", [])
    resp_contact = resp_dict.get("contact", "")
    if resp_contact and not post.contact: post.contact = resp_contact
    post.fflogs = resp_dict.get("fflogs", [])
    post.open_slots = resp_dict.get("open_slots", 0)\

    with open(path_to, "w", encoding="utf-8") as f:
        json.dump(post.to_dict(), f)

import time
import os
import datetime
import json
from llama_cpp import Llama
from src.config import Config
from src.recruitment_post import RecruitmentPost

INPUT_PATH = "data/input"
OUTPUT_PATH = "data/output"

config = Config()

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

print("> Load schema.")
schema = {}
with open("conf/schema.json", "r", encoding="utf-8") as f:
    schema = json.load(f)
tools = [
    {
        "type" : "function",
        "function" : {
            "name" : "extract_data",
            "description" : "Extract data from a recruitment posting",
            "parameters": schema
        }
    }
]

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
        temperature=0,
        max_tokens=4096,
        tools=tools,
        tool_choice={
            "type": "function", "function": {"name": "extract_data"}
        }
    )
    end_time = datetime.datetime.now()
    duration = end_time - start_time

    print("\tDONE: %d seconds" % (duration.seconds))

    post_data = json.loads(res.get("choices", [{}])[0].get("message", {}).get("function_call", {}).get("arguments", {}))
    
    post.intent = post_data.get("intent", "")
    post.schedule = post_data.get("schedule", "")
    post.summary = post_data.get("summary", "")
    post.tags = post_data.get("tags", [])
    post.roles = post_data.get("roles", [])
    resp_contact = post_data.get("contact", "")
    if resp_contact and not post.contact: post.contact = resp_contact
    post.clean_up()

    with open(path_to, "w", encoding="utf-8") as f:
        json.dump(post.to_dict(), f)
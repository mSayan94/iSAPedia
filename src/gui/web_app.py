import chainlit as cl
from api_query import get_api_response


@cl.author_rename
def rename(orig_author: str):
    rename_dict = {"generate_llm_response": "Run LLMChain", "Chatbot": "iSAPedia"}
    return rename_dict.get(orig_author, orig_author)


@cl.on_chat_start
async def main():
    msg = cl.Message(content="Enter your question")
    await msg.send()


@cl.step
async def generate_llm_response(message):
    output = await get_api_response(message.content)
    return output


@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()

    response = await generate_llm_response(message)

    msg.content = response
    await msg.update()

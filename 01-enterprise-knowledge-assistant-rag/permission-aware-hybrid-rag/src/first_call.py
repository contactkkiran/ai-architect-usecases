from dotenv import load_dotenv
import anthropic

# Read ANTHROPIC_API_KEY from the .env file
load_dotenv()

client = anthropic.Anthropic()  # picks up the key from the environment

response = client.messages.create(
    model="claude-sonnet-5-5",
    max_tokens=300,
    messages=[
        {
            "role": "user",
            "content": "In two sentences, explain what a company policy assistant does.",
        }
    ],
)

# The response is a list of blocks; keep only the text ones
reply = "".join(block.text for block in response.content if block.type == "text")

print("Block types:", [block.type for block in response.content])
print("Reply:", reply)
print("Input tokens:", response.usage.input_tokens)
print("Output tokens:", response.usage.output_tokens)

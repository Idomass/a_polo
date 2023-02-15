import openai

model_engine = "text-davinci-003"
openai.api_key = "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"

def GPT(query):
    completion = openai.Completion.create(
    engine=model_engine,
    prompt=query,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
    )

    response = completion.choices[0].text
    return response

# Specify you exit condition
exit_conditions = (":q", "quit", "exit")


while True:
    query = input("> ")
    if query in exit_conditions:
        break
    else:
        print ("ChatGPT: %s " % (GPT(query)))



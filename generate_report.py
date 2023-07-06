import openai
from time import time, sleep
from halo import Halo
import textwrap
import yaml



prompts = [
'Can you give me a very clear explanation of the core assertions, implications, and mechanics elucidated in this paper?',

"Can you explain the value of this in basic terms? Like you're talking to a CEO. So what? What's the bottom line here?",

'Can you give me an analogy or metaphor that will help explain this to a broad audience.',
]



###     file operations


def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)



def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()


def save_yaml(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True)


def open_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    return data


###     API functions


def chatbot(conversation, model="gpt-4-0613", temperature=0):
    max_retry = 7
    retry = 0
    while True:
        try:
            spinner = Halo(text='Thinking...', spinner='dots')
            spinner.start()
            
            response = openai.ChatCompletion.create(model=model, messages=conversation, temperature=temperature)
            text = response['choices'][0]['message']['content']

            spinner.stop()
            
            return text, response['usage']['total_tokens']
        except Exception as oops:
            print(f'\n\nError communicating with OpenAI: "{oops}"')
            if 'maximum context length' in str(oops):
                a = conversation.pop(0)
                print('\n\n DEBUG: Trimming oldest message')
                continue
            retry += 1
            if retry >= max_retry:
                print(f"\n\nExiting due to excessive errors in API: {oops}")
                exit(1)
            print(f'\n\nRetrying in {2 ** (retry - 1) * 5} seconds...')
            sleep(2 ** (retry - 1) * 5)



def chat_print(text):
    formatted_lines = [textwrap.fill(line, width=120, initial_indent='    ', subsequent_indent='    ') for line in text.split('\n')]
    formatted_text = '\n'.join(formatted_lines)
    print('\n\n\nCHATBOT:\n\n%s' % formatted_text)




if __name__ == '__main__':
    # instantiate chatbot, variables
    openai.api_key = open_file('key_openai.txt').strip()
    paper = open_file('input.txt')
    if len(paper) > 22000:
        paper = paper[0:22000]
    ALL_MESSAGES = [{'role':'system', 'content': paper}]
    report = ''
    for p in prompts:
        ALL_MESSAGES.append({'role':'user', 'content': p})
        response, tokens = chatbot(ALL_MESSAGES)
        chat_print(response)
        ALL_MESSAGES.append({'role':'assistant', 'content': response})
        report += '\n\n\n\nQ: %s\n\nA: %s' % (p, response)
    filename = 'reports/report_%s.txt' % time()
    save_file(filename, report.strip())
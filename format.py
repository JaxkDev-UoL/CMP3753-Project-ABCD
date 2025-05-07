import json
import os

actions = []

"""

This was created manually by looking at the actions in the dataset and removing
the ones that are not needed or looked like they were not needed as individual
actions. This is not a full list of all actions, but it is a good start to have
specific actions like <<account_pulled>> and <<account_update>> that occur regularly.

"""
def format_action(action):
    # Uncomment for raw_actions file.
    # if action not in actions:
    #     actions.append(action)
    # return action

    # If action starts with FAQ, remove it for now.
    if action.startswith('FAQ'):
        return

    # if action ends with 'has been noted.' remove it
    if action.endswith('has been noted.'):
        return

    if action.endswith('have been entered.'):
        return

    if action.startswith('Agent is looking for solutions'):
        return

    if action.endswith('has been recorded.'):
        return
    
    if action.startswith('System Action: search '):
        return

    if action.startswith('Querying the system for '):
        return
    
    if action.startswith('Purchase validation '):
        return

    if action.startswith('Searching the FAQ pages'):
        return
    
    if action.startswith('Identity verification'):
        return
    
    if action in ['A link will be sent.', 'A password has been generated.', 'A promo code has been created.']:
        return
    
    # if action is 'A purchase of * was made.'
    if action.startswith('A purchase of') and action.endswith('was made.'):
        action = '<<purchase_item>>'

    if action.startswith('Account has been updated'):
        action = '<<account_update>>'
    
    if action.startswith('Account has been pulled up'):
        action = '<<account_pulled>>'
    
    if action.startswith('A refund has been made for the amount of '):
        action = '<<refund>>'
    
    if action.endswith('has been notified.'):
        action = '<<send_notification>>'
    
    if action.startswith('Order has been updated with'):
        action = '<<order_update>>'
    

    if action not in actions:
        actions.append(action)
    
    return action

# Process conversation and format for the llama model used in the project.
def process_conversation_llama(convo):
    processed_entries = []
    for turn in convo['original']:
        speaker, utterance = turn[0], turn[1]
        # Handle action turns
        if speaker == 'action':
            speaker = 'agent'
            action = format_action(utterance.strip())
            if not action: #skip actions that are not needed
                continue
            utterance = action
        # Determine the role (user/assistant) based on the speaker
        role = 'user' if speaker == 'customer' else 'assistant'
        processed_entries.append({'role': role, 'content': utterance.strip()})
    
    #json.dump(actions, open('raw_actions.json', 'w'), indent=4)
    
    # Skip leading assistant messages until the first user
    # All assistant messages before the first user message are ignored.
    # As realistically the user will always be the first to speak.
    start_index = None
    for idx, entry in enumerate(processed_entries):
        if entry['role'] == 'user':
            start_index = idx
            break
    if start_index is None: # Dont need to skip anything, user is first..
        return []
    filtered_entries = processed_entries[start_index:]
    
    # Merge consecutive entries with the same role
    # Here we merge all the entries into a single entry for each role each turn.
    # As discussed in the paper, this is done to reduce the number of tokens used.
    # as well as improve the performance of the model.
    merged = []
    current_role = None
    current_content = []
    for entry in filtered_entries:
        if entry['role'] == current_role:
            current_content.append(entry['content'])
        else:
            if current_role is not None:
                merged.append({'role': current_role, 'content': '\n'.join(current_content)})
            current_role = entry['role']
            current_content = [entry['content']]
    if current_role is not None:
        merged.append({'role': current_role, 'content': '\n'.join(current_content)})
    
    # Ensure the conversation ends with an assistant message,
    # the model always needs to respond to the user.
    if merged and merged[-1]['role'] == 'user':
        merged.append({'role': 'assistant', 'content': ''})
    
    # Pair user and assistant turns to match the Transformers chat template.
    # {'user': 'content', 'assistant': 'assistant content'}
    paired_data = []
    i = 0
    while i < len(merged):
        if merged[i]['role'] != 'user':
            i += 1
            continue
        user_content = merged[i]['content']
        assistant_content = ''
        if i + 1 < len(merged) and merged[i+1]['role'] == 'assistant':
            assistant_content = merged[i+1]['content']
            i += 2
        else:
            i += 1
        paired_data.append({
            'user': user_content,
            'assistant': assistant_content
        })
    
    return paired_data

def process_conversation_olmo(convo):
    #todo
    return convo

# Process the entire dataset
data = None
with open('abcd_v1.1.json', 'r') as f:
    data = json.load(f)
data = data['train'] + data['dev'] + data['test']

if not os.path.exists('datasets'):
    os.makedirs('datasets')

# processed_conversations = []
# for type in processed_conversations.keys():
#     for convo in data[type]:
#         processed_conversations.append((process_conversation_llama(convo['original']),))
#     f = open('datasets/abcd/abcd_v1.1_processed.json', 'w')
#     json.dump(processed_conversations[type], f, indent=4)
#     f.close()

# json.dump(actions, open('datasets/abcd/abcd_v1.1_actions.json', 'w'), indent=4)

print('Done processing ABCD dataset, saved to datasets/abcd_v1.1_processed.jsonl - (Conversations: {})'.format(len(data)))

with open('datasets/abcd_v1.1_processed.jsonl', 'w') as out_f, open('datasets/abcd_v1.1_tokens.json', 'w') as token_f:
    convos = [process_conversation_llama(conv) for conv in data]

    # Write all formatted conversations to file
    # Each line is a JSON object representing a conversation
    for conv in convos:
        out_f.write(json.dumps(conv) + "\n")

    # Write special tokens to token file
    json.dump(sorted(actions), token_f)
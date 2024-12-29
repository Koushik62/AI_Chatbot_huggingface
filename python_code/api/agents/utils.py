def get_chatbot_response(client,model_name,messages,temperature=0):
    input_messages = []
    for message in messages:
        input_messages.append({"role": message["role"], "content": message["content"]})

    response = client.chat.completions.create(
        model=model_name,
        messages=input_messages,
        temperature=temperature,
        top_p=0.8,
        max_tokens=2000,
    ).choices[0].message.content
    
    return response



def get_embedding(embedding_client,model_name,text_input):
    output = embedding_client.embeddings.create(input = text_input,model=model_name)
    
    embedings = []
    for embedding_object in output.data:
        embedings.append(embedding_object.embedding)

    return embedings

# def double_check_json_output(client,model_name,json_string):
#     prompt = f""" You will check this json string and correct any mistakes that will make it invalid. Then you will return the corrected json string. Nothing else. 
#     If the Json is correct just return it.

#     if there is any text before order after the json string , remove it. 
#     Do NOT return a single letter outside of the json string.
#     The first thing you write should be open curly brace of the json and the last letter you write should be closing curly brace.
    
#     You should  check the follwring json one weather correct or not between 'start (content) end':
#     ' start 
#     {json_string}
#     end
#     ' 
#     """

#     messages = [{"role": "user", "content": prompt}]

#     response = get_chatbot_response(client,model_name,messages)
    
#     response = response.replace("```", "")

#     return response


def double_check_json_output(client, model_name, json_string):
    
    prompt = f"""
        You will check the following JSON string for any errors and correct them. Your task:
        1. Correct any issues that would make it invalid JSON.
        2. If the JSON is correct, return it without modification.
        3. Ensure the output starts with an open curly brace (`{{`) and ends with a closing curly brace (`}}`).
        4. Remove any text outside the JSON structure (e.g., extra text before or after the JSON).
        5. Ensure all keys and values are properly quoted and formatted.

        Here is the JSON string you need to check: {json_string}


        Output ONLY the corrected JSON string, with no additional text or explanations.
    """

    # Prepare the messages for the chatbot
    messages = [{"role": "user", "content": prompt}]

    # Get the response from the chatbot
    response = get_chatbot_response(client, model_name, messages)

    # Clean up any artifacts like backticks and strip extra whitespace

    return response


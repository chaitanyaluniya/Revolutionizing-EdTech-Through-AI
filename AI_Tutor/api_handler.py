#Changes for the new API of gemini
import google.generativeai as genai
import time
import os
from google.api_core.exceptions import GoogleAPIError

def send_query_get_response(user_question, model_config, files_info):
    try:
        # Set up the model based on configuration
        model = genai.GenerativeModel(
            model_name=model_config['model_name'],
            generation_config=model_config['generation_config']
        )
        
        # Enhance the user question with instructions for file references
        enhanced_question = user_question + ' and tell me which file are the top results based on your similarity search (an example of can be you can refer to the course material titled "Present Value Relations" in the file "Lec 2-3.pdf" under slides 20-34.)'
        
        # Create chat history with file information as context
        chat = model.start_chat(history=[])
        
        # Prepare context about available files
        if files_info and len(files_info) > 0:
            files_context = "Available reference files:\n"
            for idx, file_info in enumerate(files_info):
                files_context += f"{idx+1}. {file_info['name']} - {file_info['description']}\n"
            
            # Add the files context as a system message first
            chat.send_message(f"[SYSTEM] {files_context}")
        
        # Set a timeout for response
        start_time = time.time()
        timeout = 60  # 60 seconds timeout
        
        # Send the user question and get a response
        response = chat.send_message(enhanced_question)
        
        # Check if we got a response within the timeout
        if time.time() - start_time > timeout:
            return "The request took too long to process. Please try again with a more specific question."
        
        # Return the model's response text
        return response.text
    
    except GoogleAPIError as e:
        # Handle API-specific errors
        return f"Error with Google AI API: {str(e)}"
    except Exception as e:
        # Handle any other exceptions
        return f"An error occurred: {str(e)}"


# from openai import OpenAI
# import time


# def send_query_get_response(client,user_question,assistant_id):
#     # Create a new thread for the query
#     thread = client.beta.threads.create()
#     thread_id = thread.id

#     user_question=user_question+ ' and tell me which file are the top results based on your similarity search (an example of can be you can refer to the course material titled "Present Value Relations" in the file "Lec 2-3.pdf" under slides 20-34.)'

#     # Send the user's question to the thread
#     client.beta.threads.messages.create(
#         thread_id=thread_id,
#         role="user",
#         content=user_question,
#     )

#     # Create and start a run for the thread
#     run = client.beta.threads.runs.create(
#         thread_id=thread_id,
#         assistant_id=assistant_id,
#     )

#     # Initialize a timer to limit the response wait time
#     start_time = time.time()

#     # Continuously check the run status
#     run_status = None
#     while run_status != 'completed':
#         run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
#         run_status = run.status

#         # Time check to break the loop if it runs more than 60 seconds
#         if time.time() - start_time > 60:
#             print("Final run status:", run_status)
#             print("Took too long time")
#             break

#     # Fetch and print the entire conversation history
#     messages = client.beta.threads.messages.list(
#         thread_id=thread_id,
#         order='asc'
#     )

#     # Return the last response from the thread
#     message=messages.data[-1]
#     message_content=message.content[0].text
#     response=message_content.value

#     return response if messages.data else "Server issue, try again"




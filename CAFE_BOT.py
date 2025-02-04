from pydantic import BaseModel
import openai
import gradio as gr

# Azure OpenAI configuration
AZURE_OPENAI_ENDPOINT = "YOUR_OPENAI_ENDPOINT"     # Replace with your endpoint
AZURE_OPENAI_API_KEY = "YOUR_API_KEY"     # Replace with your api key 
DEPLOYMENT_NAME = "YOUR_DEPLOYMENT_NAME"  # Replace with your deployment name

# Set Azure OpenAI credentials
openai.api_key = AZURE_OPENAI_API_KEY
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_type = "azure"
openai.api_version = "YOUR VERSION"

# Predefined context for the bot CHANGE THE CONTEXT AND MENU ACCORDING TO YOUR PREFERENCES
BOT_CONTEXT = """
You are a polite and helpful assistant for Dia's Coffee House. 
Answer user questions based on the menu provided below. 
If a user asks for a recommendation, suggest one or two items from the menu, avoiding listing the entire menu unless explicitly asked.
If the question is unrelated to the menu, politely inform the user to contact customer care. 
Always maintain a conversational tone and respond concisely.

MENU:
Espresso = ₹207
Americano = ₹249
Latte = ₹291
Cappuccino = ₹291
Flat White = ₹312
Mocha = ₹332
Iced Coffee = ₹270
Cold Brew = ₹332
Chai Latte = ₹312
Pastries (Croissant, Muffin, or Danish) = ₹166
"""

# Function to handle OpenAI interaction
def ask_openai(prompt: str):
    # Combine context and user input
    full_prompt = f"{BOT_CONTEXT}\n\nUser: {prompt}\nAssistant:"
    
    try:
        response = openai.Completion.create(
            engine=DEPLOYMENT_NAME,
            prompt=full_prompt,
            max_tokens=150,
            temperature=0.7,
            top_p=0.9,
            frequency_penalty=0,
            presence_penalty=0,
        )
        # Return only the assistant's response
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Gradio chatbot function to handle user input and bot response
def chatbot_response(user_input, history):
    if not user_input.strip():
        return history, ""
    
    # Get assistant's reply
    assistant_reply = ask_openai(user_input)
    
    # Append only the assistant's response to history
    history.append(("User: " + user_input, "Assistant: " + assistant_reply))
    
    # Return the updated history
    return history, ""

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# Chat with Dia's Coffee House Bot")
    chatbot = gr.Chatbot(label="Dia's Coffee Bot")
    msg = gr.Textbox(label="Type your message", placeholder="Ask me anything about our menu...")
    submit_btn = gr.Button("Send")

    submit_btn.click(chatbot_response, inputs=[msg, chatbot], outputs=[chatbot, msg])

# Run the Gradio interface
if __name__ == "__main__":
    demo.launch(share=True)
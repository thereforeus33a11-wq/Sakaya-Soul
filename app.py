"""
Simple Web Chat Interface for Sakaya
Run with: uvicorn app:app --reload
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from sakaya_brain import SakayaBrain

app = FastAPI(title="Sakaya Chat")

# Initialize brain
brain = SakayaBrain()

class ChatInput(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sakaya Chat</title>
        <style>
            body { font-family: Arial; background: #1a1a1a; color: white; }
            #chat { width: 600px; margin: 50px auto; }
            #messages { height: 400px; overflow-y: auto; border: 1px solid #444; padding: 10px; background: #111; }
            .message { margin: 8px 0; }
            .user { color: #4fc3f7; }
            .sakaya { color: #f48fb1; }
            input { width: 70%; padding: 10px; }
            button { padding: 10px 20px; }
        </style>
    </head>
    <body>
        <div id="chat">
            <h2>Sakaya Aries</h2>
            <div id="messages"></div>
            <input type="text" id="input" placeholder="Talk to Sakaya..." onkeypress="if(event.key === 'Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>

        <script>
            async function sendMessage() {
                const input = document.getElementById('input');
                const messages = document.getElementById('messages');
                
                if (!input.value.trim()) return;

                // Show user message
                messages.innerHTML += `<div class="message user"><b>You:</b> ${input.value}</div>`;
                messages.scrollTop = messages.scrollHeight;

                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ message: input.value })
                });
                
                const data = await response.json();
                
                // Show Sakaya's response
                messages.innerHTML += `<div class="message sakaya"><b>Sakaya:</b> ${data.response}</div>`;
                messages.scrollTop = messages.scrollHeight;

                input.value = '';
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.post("/chat")
async def chat(chat_input: ChatInput):
    response = brain.process_input(chat_input.message)
    return {"response": response}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
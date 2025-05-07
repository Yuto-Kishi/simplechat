# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS設定（Lambdaやフロントエンドからアクセス可能にする）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(request: Request):
    data = await request.json()
    message = data.get("message")
    history = data.get("conversationHistory", [])

    # 仮の応答（Amazon Bedrock の部分は後で差し替え）
    return {
        "response": f"こんにちは！あなたのメッセージは「{message}」ですね。",
        "conversationHistory": history + [{"role": "user", "content": message}]
    }

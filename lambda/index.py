# lambda/index.py
import json
import os
import re
import urllib.request


def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        # 認証情報のログ（任意）
        user_info = None
        if 'requestContext' in event and 'authorizer' in event['requestContext']:
            user_info = event['requestContext']['authorizer']['claims']
            print(f"Authenticated user: {user_info.get('email') or user_info.get('cognito:username')}")

        # リクエストボディの解析
        body = json.loads(event['body'])
        message = body['message']
        conversation_history = body.get('conversationHistory', [])

        # ngrok経由のFastAPIのURLを環境変数から取得
        api_url = os.environ.get("NGROK_API_URL")  # 例: https://xxxx.ngrok.io/predict
        if not api_url:
            raise Exception("NGROK_API_URL not set in environment variables.")

        # API呼び出し用のリクエストボディ
        payload = {
            "message": message,
            "conversationHistory": conversation_history
        }

        # HTTPリクエストの作成
        req = urllib.request.Request(
            api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )

        # レスポンス取得
        with urllib.request.urlopen(req) as res:
            result = json.load(res)

        # 結果を取得
        assistant_response = result.get("response", "")
        updated_history = result.get("conversationHistory", [])

        # 成功レスポンスの返却
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant_response,
                "conversationHistory": updated_history
            })
        }

    except Exception as error:
        print("Error:", str(error))
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            "body": json.dumps({
                "success": False,
                "error": str(error)
            })
        }


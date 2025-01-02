from flask import Flask, render_template, request, jsonify
import os
import logging
from database import (
    initialize_database,
    save_character_background,
    save_chat_message,
    get_chat_history,
)

app = Flask(__name__)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="app.log",
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 创建文件处理器
file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
)

# 添加处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Initialize database
initialize_database()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/save_background", methods=["POST"])
def save_background():
    try:
        data = request.json
        background = data.get("background")
        if background:
            character_id = save_character_background(background)
            logger.info(f"成功保存角色背景，角色ID: {character_id}")
            return jsonify({"success": True, "character_id": character_id})
        logger.warning("保存背景失败：背景文本为空")
        return jsonify({"success": False, "error": "Background text is required"}), 400
    except Exception as e:
        logger.error(f"保存背景时发生错误: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/send_message", methods=["POST"])
def send_message():
    try:
        data = request.json
        character_id = data.get("character_id")
        message = data.get("message")

        if not character_id or not message:
            logger.warning("发送消息失败：缺少角色ID或消息内容")
            return (
                jsonify(
                    {"success": False, "error": "Character ID and message are required"}
                ),
                400,
            )

        # 保存用户消息
        save_chat_message(character_id, message, is_user=True)
        logger.info(f"角色ID {character_id} 收到用户消息: {message}")

        # TODO: 处理消息并生成响应
        response = "This is a placeholder response"

        # 保存角色响应
        save_chat_message(character_id, response, is_user=False)
        logger.info(f"角色ID {character_id} 发送响应: {response}")

        return jsonify({"success": True, "response": response})
    except Exception as e:
        logger.error(f"处理消息时发生错误: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/get_chat_history/<int:character_id>", methods=["GET"])
def get_chat_history(character_id):
    try:
        history = get_chat_history(character_id)
        logger.info(f"成功获取角色ID {character_id} 的聊天历史")
        return jsonify({"success": True, "history": history})
    except Exception as e:
        logger.error(f"获取聊天历史时发生错误: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=13752)

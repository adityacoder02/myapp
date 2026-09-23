import os
import requests

from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json

        prompt = data.get("prompt")
        mode = data.get("mode")

        if not prompt:
            return jsonify({
                "error": "Prompt is required"
            }), 400

        if mode == "summarize":
            instruction = """
    You are a study assistant.

    Summarize the student's material in a clear and organized way.

    Requirements:
    - Start with a short overview.
    - Extract the most important concepts.
    - Use bullet points.
    - Highlight important terms.
    - Remove unnecessary repetition.
    - Do not add information that is not supported by the material.
    """

        elif mode == "explain":
            instruction = """
    You are a patient and friendly teacher.

    Explain the student's topic so that a beginner can understand it.

    Requirements:
    - Start with a simple definition.
    - Explain the concept step by step.
    - Use a simple real-world analogy when useful.
    - Give an example.
    - End with the key points to remember.
    - Avoid unnecessarily complicated terminology.
    """

        elif mode == "quiz":
            instruction = """
    You are a study quiz generator.

    Create a quiz based ONLY on the student's material.

    Requirements:
    - Create 5 questions.
    - Mix multiple-choice and short-answer questions.
    - Number every question.
    - For multiple-choice questions, provide 4 options.
    - Put the answers at the end.
    - Briefly explain why each answer is correct.
    """

        elif mode == "rewrite":
         instruction = """
    You are an expert study-notes editor.

    Rewrite the student's notes so they are easier to study.

    Requirements:
    - Keep the original meaning.
    - Organize the information using headings.
    - Use bullet points where appropriate.
    - Correct obvious grammar and spelling issues.
    - Remove unnecessary repetition.
    - Make important concepts easy to find.
    - Do not invent facts.
    """

        elif mode == "plan":
            instruction = """
    You are an academic study planner.

    Create a practical study plan based on the student's material.

    Requirements:
    - Break the material into logical topics.
    - Create a day-by-day study plan.
    - Include revision sessions.
    - Include active-recall or practice sessions.
    - Include short breaks where appropriate.
    - End with a quick revision strategy.
    """

        else:
            return jsonify({
                "error": "Invalid mode selected"
            }), 400

        # Send request to OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openrouter/free",
                "messages": [
                    {
                        "role": "system",
                        "content": instruction
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        )

        if response.status_code != 200:
            print("OpenRouter error:", response.text)

            return jsonify({
                "error": "AI service returned an error"
            }), 500

        result = response.json()

        ai_response = result["choices"][0]["message"]["content"]

        return jsonify({
            "response": ai_response
        })

    except Exception as error:
        print("Server error:", error)

        return jsonify({
            "error": "Something went wrong on the server"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
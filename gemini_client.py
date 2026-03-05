import subprocess


def run_gemini(prompt: str):
    """
    Send a prompt to Gemini CLI.
    """

    result = subprocess.run(["gemini", prompt], capture_output=True, text=True)

    return result.stdout


if __name__ == "__main__":

    question = "What tables exist in the database?"

    response = run_gemini(question)

    print(response)

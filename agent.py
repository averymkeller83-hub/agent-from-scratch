"""agent-from-scratch v1 — my own AI agent, no frameworks.

THE WHOLE PROGRAM IN FOUR STEPS:
  1. You type something.
  2. It gets added to a list that holds the whole conversation.
  3. The whole list is sent to the brain (hermes-avery via Ollama).
     The brain sends back its next message.
  4. The brain's answer joins the list too, and gets printed. Repeat.

The list is the memory. The brain remembers NOTHING between calls —
re-sending the whole conversation every time is what makes it a chat.
"""

# ============================================================
# IMPORTS — both built into Python, nothing to install
# ============================================================
import json             # models talk in JSON ({"key": "value"} text)
import urllib.request   # makes web requests

# ============================================================
# THE BRAIN — change these TWO lines to swap brains.
# This is the "swappable seam": the rest of the file never
# knows or cares which model is behind it.
# ============================================================
OLLAMA_URL = "http://localhost:11434/api/chat"   # Ollama's door on this Mac
MODEL = "hermes-avery"                           # which brain answers


# ============================================================
# ask_model — the phone line to the brain.
# IN:  the whole conversation so far (a list of messages)
# OUT: the brain's next message (a dict: role + content)
# ============================================================
def ask_model(messages):
    """Send the conversation to the brain, get its next message back."""

    # pack the request as JSON text — which model, the whole chat,
    # and stream=False meaning "whole answer at once, not word by word"
    body = json.dumps({"model": MODEL, "messages": messages, "stream": False})

    # build the web request and label it as JSON
    req = urllib.request.Request(OLLAMA_URL, data=body.encode(),
                                 headers={"Content-Type": "application/json"})

    # send it — this line is the moment the Mac talks to the brain
    with urllib.request.urlopen(req) as resp:
        # unpack the JSON reply, return just the message part
        return json.loads(resp.read())["message"]


# ============================================================
# ask_model_streaming — v1.1, AVERY'S BUILD.
# Same phone line, but the answer shows up word by word.
# Fill in code under each ---- memo ----. The old ask_model
# above keeps working until this one is finished.
# ============================================================
def ask_model_streaming(messages):

    # ---- pack the request — stream=True means "send the answer ----
    # ---- in little pieces as you think, don't wait"             ----
    body = json.dumps({"model": MODEL, "messages": messages, "stream": True})   # <- Avery wrote this

    # ---- build the web request — identical to ask_model ----
    req = urllib.request.Request(OLLAMA_URL, data=body.encode(),
                                 headers={"Content-Type": "application/json"})

    # ---- the collector — every piece gets glued on, so the ----
    # ---- whole sentence exists at the end (Q2's total, but words) ----
    full_text = ""

    # ---- open the line and read piece by piece AS the brain thinks ----
    with urllib.request.urlopen(req) as resp:
        for line in resp:                       # one line = one little JSON chunk

            # ---- unpack the chunk ----
            chunk = json.loads(line)

            # ---- grab its bit of text (.get with "" keeps us safe: ----
            # ---- the final "done" chunk carries no words)           ----
            word = chunk.get("message", {}).get("content", "")

            # ---- show it NOW — no newline, no waiting ----
            print(word, end="", flush=True)

            # ---- and glue a copy onto the collector ----
            full_text += word

    # ---- brain finished: end the line, hand back the complete ----
    # ---- message so the memory list can store it               ----
    print()
    return {"role": "assistant", "content": full_text}



# ============================================================
# main — the loop. This is the agent's heartbeat:
# listen -> remember -> think -> remember -> speak -> repeat
# ============================================================
def main():

    # ---- the memory ----
    # every message of the chat, in order. Empty = fresh start.
    messages = []

    print("agent v1 - type 'quit' to exit")

    while True:   # loop forever — the exit lives INSIDE (the break below)

        # ---- get input from the user ----
        user_text = input("you: ")

        # ---- the exit — every loop needs one (Q2 lesson) ----
        if user_text.strip().lower() == "quit":
            break

        # ---- remember what YOU said ----
        messages.append({"role": "user", "content": user_text})

        # ---- think OUT LOUD: label the line, then the streaming ----
        # ---- call prints the words live as the brain makes them ----
        print("agent: ", end="", flush=True)
        reply = ask_model_streaming(messages)

        # ---- remember what the BRAIN said (delete this line and
        #      the agent forgets everything it ever answered) ----
        messages.append(reply)


# ============================================================
# Start the loop ONLY when run directly (python3 agent.py).
# When another file imports our functions, this stays quiet.
# ============================================================
if __name__ == "__main__":
    main()

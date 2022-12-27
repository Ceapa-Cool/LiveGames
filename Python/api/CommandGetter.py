import pytchat
import re
import CommandStream
import threading



def listen(live_id, command_formats: dict[str, str]) -> CommandStream.CommandStream:

    stream = CommandStream.CommandStream()

    chat = pytchat.create(video_id=live_id)

    lst = threading.Thread(target=listening, args=(stream, chat, command_formats))
    lst.daemon = True
    lst.start()

    return stream

def listening(stream: CommandStream.CommandStream, chat, command_formats: dict[str, str]):

    while chat.is_alive():
        for c in chat.get().sync_items():
            for t in command_formats:
                if re.fullmatch(command_formats[t], c.message):
                    stream.write(c.author.name, t, c.message)

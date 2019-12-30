def DEBUG(message):
    with open('debug', 'a') as f:
        f.write(str(message))

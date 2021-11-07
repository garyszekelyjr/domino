# HackUMassIX
## Names: 
- Ray Castillo
- Gary Szekely
## Project Name:
- Domino

## Directories

### /Chaos
- **/chaos.py**  
    Does various tasks meant to attack the victim. You can move there mouse so that it will click and drag in random directions. You can play an audio onto there computer from an existing MP3 or do a text-to-speech where you input text and it will read it aloud. You can also play videos on the victums screen. You can put a pop up with your personal message. And you can type through their keyboard, and input key commands. 

### /ImgLogger
- **/camlogger.py**  
    Using CV it takes snapshots from the computers native Web Cam. It then compbines all the the images that are saved within a folder and combines them to become an image. The images are named with numbers as to keep there order and play chronologically. The video is saved as an MP4 and can be played. All that needs to be passed is the time in seconds you want to record.

- **/imglogger.py**  
    Does a very similar thing to the camlogger.py except for this case it takes screen shot of your computer do it can see what you are doing on there. All that needs to be passes is the time in seconds you wanna record. 

### /KeyLogger
- **/keylogger.py**  
    This captures all the keystrokes and saves it to a text file. It also filters some of the stroke and converts them to strings. For example Key.Space just becomes ' '. All the inputs to the keylogger.txt are time stamped as well. 

### /MaliciousConnection
- **/attacker.py**
    The attacker script for a malicious connection. This allows connection to a worm inside of a victims computer that allows for various commands to be executed as defined above. It also gives the attacker full access to the victim's file system including file transfer to and from. All of this occurs unannouced to the victim.

- **/victim.py**  
    The victim script for a malicious connection. This allows for the attacker.py script to connect to a victim's computer and commit malicious acts.

- **/stolen_files**  
    Directory for the files "stolen" from the victims computer via the **get** command

### /FileTransfer
- **/client.py**  
    The client script for a file transfer protocol. Allows a client to connect to a server and to one other peer for file transfer. The client specifies whether they are a **Sender** or **Receiver** (two clients connected cannot be of the same type, that is one has to be a **Sender** and the other a **Receiver**).

- **/server.py**  
    The server script for a file transfer protocol. Allows for two clients to connect and transfer files between them. Maintains clients being of a different type as well as a middle ground for files before being fully transferred to the client.

### Virtual Machine
We used AWS to host a Linux machine with a Amazon Linux distro. This was utilized to run the server for the file transfer protocol as well as the attacker's server to provide a level of anonymity when attacking another computer.
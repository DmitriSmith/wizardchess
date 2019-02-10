# wizardchess
HackKU project - Chess powered by Alexa, a Raspi, motors, and magnets
Group members:
Dmitri Smith (Computer Engineering)
Chauncey Hester (Computer Engineering)
Jordan Hirsekorn (Electrical Engineering)
Denzel Richmond (Computer Engineering)

Project created for HackKU 2019. 

Though we ordinary mortals might never know how it feels to have the awesome power of magic at our fingertips,
with this project we might get a taste of it, as our voice commands the chess pieces to move of their own volition.
Plus, it has magnets, which are basically magic.

The theme was social accessibility. After deliberation, we decided to stray from the common 
theme of video games and try our hand at hacking a board game. Of course, what game is more well known than chess?
For chess fans, it provides a novel method to play their favorite game. Even peope who aren't fans of chess can
enjoy ordering pawns and kings around the field using nothing more than the power of their voice.

State of the project:
The Alexa skill has been created, but the code to connect the Alexa to the raspberry pi is incomplete. Thugh unfinished,
Flask-Ask is leveraged to communicate between alexa and pi.
The chess board and piece logic is handled on the pi, and the entire project is written in Python.
The pieces each have a small but powerful magnet in their base. Below the board, two stepper motors connected to 
all-thread rods move an electromagnet that is used to drag the pieces as if by magic.

TODO:
Add pictures of the setup
Add a proper schematic
Finish Alexa-Pi interaction code
Clean up code




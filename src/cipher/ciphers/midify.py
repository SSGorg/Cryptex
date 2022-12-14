"""
Author: marvhus and Shawty
Concept: Chilz
"""
from cipher import Cipher
import mido

class Midify(Cipher):

    name = 'midify' 
    type = 'cipher'

    @staticmethod
    def encode(args):
        text = args.text
        path = args.output
        
        if not text:
            return {'text': "No input text", 'success': False}

        if not path:
            return {'text': "No output file path", 'success': False}

        # List of ascii values of text
        vals = [ord(c) for c in text]
        
        # pattern
        pattern = mido.MidiFile()
        
        # track
        track = mido.MidiTrack()
        pattern.tracks.append(track)
        
        # tempo
        tempo = mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(120))
        track.append(tempo)
        
        midoNoteMessage = lambda m, n, t : mido.Message(m, note=n, velocity=127, time=t)
        
        for val in vals:
            on = midoNoteMessage("note_on", val, 0) 
            off = midoNoteMessage("note_off", val, 100)
            
            track.append(on)
            track.append(off)
            
        pattern.save(path)

        return {'text': f"Saved midi file at {path}", 'success': True}

    @staticmethod
    def decode(args):
        path = args.input

        if not path:
            return {'text': "No input file path", 'success': False}

        mid = mido.MidiFile(path)

        text = ""
        for track in mid.tracks:
            for msg in track:
                if msg.type == 'note_on':
                    text += chr(msg.note)

        return {'text': text, 'success': True}

    @staticmethod
    def print_options():
        #Edit this section as needed for your specific encoding / decoding.
        print(''' 
        ### Modes
        -d / --decode ---- decode
        -e / --encode ---- encode

        ### Input
        -t / --text ------ input text
        -i / --input ----- input file path
        -o / --output ---- output file path

        ### Examples
        python main.py midify -e -t 'hello' -o 'message.mid'
        python main.py midify -d -i 'message.mid'
        ''')

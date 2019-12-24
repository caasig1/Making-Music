"""CSC148 Assignment 1 - Making Music

=== CSC148 Summer 2019 ===
Department of Computer Science,
University of Toronto

=== Module Description ===

This file contains classes that describe sound waves, instruments that play
these sounds and a function that plays multiple instruments simultaneously.

As discussed in the handout, you may not change any of the public behaviour
(attributes, methods) given in the starter code, but you can definitely add
new attributes, functions, classes and methods to complete your work here.

"""
from __future__ import annotations
import typing
import csv
import numpy
from helpers import play_sound, play_sounds, make_sine_wave_array


class SimpleWave:
    """ This creates a Simple Sine Wave.

    Sounds are composed of sine waves so we are using numpy arrays to simulate
    how sound waves are played

    This simple wave class takes in frequency, duration, and amplitude to create
    a sine wave that emits that sound frequency.

    == Attributes ==
    frequency: the frequency of the wave
    duration: how long the sound should play for
    amplitude: the volume of the wave
    """

    frequency: int
    duration: float
    amplitude: float

    def __init__(self, frequency: int,
                 duration: float, amplitude: float) -> None:
        """ Initialize a Simple Wave with the three attributes

        Preconditions:
        amplitude: must be between 0 and 1
        """
        self.frequency = frequency
        self.duration = duration
        self.amplitude = amplitude

    def __eq__(self, other: SimpleWave) -> bool:
        """ Checks if two Simple Waves are the same in all aspects """
        return (other.frequency == self.frequency) and (
            other.duration == self.duration) and (
                other.amplitude == self.amplitude)

    def __ne__(self, other: SimpleWave) -> bool:
        """ Checks if two Simple Waves have anything that differ  """
        return (other.frequency != self.frequency) or (
            other.duration != self.duration) or (
                other.amplitude != self.amplitude)

    def __add__(self,
                other: ANYWAVE) -> ComplexWave:
        """ Adds two Simple Waves together to create a Complex Wave """
        return ComplexWave([self, other])

    def get_duration(self) -> float:
        """ Return the duration of the wave """
        return self.duration

    def play(self) -> numpy.ndarray:
        """ Play the sound that corresponds to the sine wave.
        We are using numpy arrays to aid with this process so a numpy array
        is returned """
        result = make_sine_wave_array(self.frequency, self.duration)
        result = self.amplitude * result
        return result


class ComplexWave:
    """ This creates a Complex Wave.
    Complex Waves are composed of two or more Simple Waves.
    This class uses composition since it HAS multiple simple waves although it
    clearly IS NOT a simple wave.

    Complex Waves take two Simple Waves and sums them vertically.
    Remember, amplitude must stay below 1.

    == Attributes ==
    waves: a list of waves that are summed together
    duration: how long the sound should play for
    amplitude: how loud the sound should be
    """

    waves: typing.List[SimpleWave]
    duration: float
    amplitude: float

    def __init__(self, waves: typing.List[SimpleWave]) -> None:
        """ Initialize a Complex wave with a list of waves as its input. """
        self.waves = waves
        self.duration = 0
        self.amplitude = 0
        for wave in waves:
            if wave.duration > self.duration:
                self.duration = wave.duration

    def __add__(self,
                other: ANYWAVE) -> ComplexWave:
        """ Add two waves of any type
        """
        if not isinstance(other, SimpleWave):
            result_waves = self.waves + other.waves
            return ComplexWave(result_waves)
        else:
            result_waves = self.waves + [other]
            return ComplexWave(result_waves)

    def complexity(self) -> int:
        """ Find the complexity of the complex waves
         In other words, the number of different Simple Waves """
        return len(self.waves)

    def play(self) -> numpy.ndarray:
        """ Play the sound of the complex waves.
        We use numpy to help play the sound.
        Also, the volume is already controlled in the Simple wave so there is
        no need to multiply by amplitude here """
        first_wave = self.waves[0]
        return_wave = self.waves[0].play()
        self.waves.pop(0)
        for wave in self.waves:
            return_wave += wave.play()
        self.waves.append(first_wave)
        if max(return_wave) > 1 or min(return_wave) < -1:
            return_wave = return_wave / (
                max(max(return_wave), abs(min(return_wave))))
        return return_wave

    def get_waves(self) -> typing.List[SimpleWave]:
        """ Return the waves that create this complex wave """
        return self.waves

    def get_duration(self) -> float:
        """ Return the duration of this complex wave """
        return self.duration

    def simplify(self) -> None:
        """
            REMEMBER: this is not a required part of the assignment
        """
        pass


class Note:
    """ This creates a note using Simple and Complex Waves.
    Notes are several waves (Simple and Complex) placed one after the other in
    order to mimic a melody.

    Notes take a list of waves and when played, puts them one after the other.
    This is different from the addition in Complex Wave because there, you add
    the waves vertically whereas here, the waves are added horizontally.

    == Attributes ==
    amplitude: the volume of the note
    waves: the waves of the note/consecutive notes
    """
    amplitude: float
    waves: typing.List[ANYWAVE]

    # has waves, not is a

    def __init__(self, waves: typing.List[ANYWAVE]) -> None:
        """ Initialize a Note.
         We automatically assign amplitude to 1 and waves can be any wacve type.
         """
        self.amplitude = 1.0
        for i in range(len(waves)):
            if waves[i].get_duration() < 0.00001:
                waves.pop(i)
        self.waves = waves

    def __add__(self, other: Note) -> Note:
        """ We add notes together. As mentioned in the class docstring, it is
        different from Complex waves additions since here we add them
        horizontally """
        combined_list = self.waves + other.waves
        s = Note(combined_list)
        s.amplitude = max(self.amplitude, other.amplitude)
        return s

    def get_waves(self) -> typing.List[ANYWAVE]:
        """ Return the list of waves that are placed in order for the note. """
        return self.waves

    def get_duration(self) -> float:
        """ Return the duration of the note """
        duration = 0
        for wave in self.waves:
            duration += wave.get_duration()
        return duration

    def play(self) -> numpy.ndarray:
        """ Play the note and return it as a numpy array """
        result = numpy.array([])
        for wave in self.waves:
            result = numpy.hstack([result, wave.play()])
            result = self.amplitude * result
        return result


class SawtoothWave(ComplexWave):
    """ Create a Sawtooth Wave. A sawtooth wave is a complex wave so it is only
    natural that it is a subclass of the Complex Wave.
    Sawtooth waves are a special type of wave where the wave is comprised of
    several Simple waves, each of varying frequency and amplitude.
    The frequencies and amplitudes are i times of the frequency and 1/i
    amplitude, i representing each iteration starting at 1.

    == Attributes ==
    frequency: the frequency of the first sine wave of the sawtooth wave
    duration: the duration of the sawtooth wave
    amplitude: the volume of the wave
    waves: the list of simple waves that make up the Sawtooth Wave
    """
    frequency: int
    duration: float
    amplitude: float
    waves: typing.List[SimpleWave]

    def __init__(self, frequency: int,
                 duration: float, amplitude: float) -> None:
        """ Initializes a Sawtooth wave as described in the class docstring.

        Preconditions:
        amplitude: must be between 0 and 1
        """
        waves = []
        for i in range(1, 11):
            waves.append(SimpleWave(i * frequency, duration,
                                    amplitude / i))
        super().__init__(waves)
        self.frequency = frequency
        self.duration = duration
        self.amplitude = amplitude

    def __add__(self,
                other: ANYWAVE) -> ComplexWave:
        """ Adds this Sawtooth Wave with any other wave """
        return super().__add__(other)

    def complexity(self) -> int:
        """ Finds the complexity of the Sawtooth Wave """
        return super().complexity()

    def play(self) -> numpy.ndarray:
        """ Plays the Sawtooth Wave returned as a numpy array """
        return super().play()

    def get_waves(self) -> typing.List[SimpleWave]:
        """ Retrieves the Simple Waves that make up the Sawtooth Wave """
        return super().get_waves()

    def get_duration(self) -> float:
        """ Gets the duration of the Sawtooth Wave """
        return super().get_duration()

    def simplify(self) -> None:
        """
            REMEMBER: this is not a required part of the assignment
        """
        pass


class SquareWave(ComplexWave):
    """ Create a Square Wave. A square wave is a complex wave so it is only
    natural that it is a subclass of the Complex Wave.
    Square waves are a special type of wave where the wave is comprised of
    several Simple waves, each of varying frequency and amplitude.
    The frequencies and amplitudes are (2i - 1) times of the frequency and
    1/(2i-1) of amplitude, i representing each iteration starting at 1.

    == Attributes ==
    frequency: the frequency of the first sine wave of the square wave
    duration: the duration of the square wave
    amplitude: the volume of the wave
    waves: the list of simple waves that make up the Square Wave
    """
    frequency: int
    duration: float
    amplitude: float
    waves: typing.List[SimpleWave]

    def __init__(self, frequency: int,
                 duration: float, amplitude: float) -> None:
        """ Initializes a Square wave as described in the class docstring.

        Preconditions:
        amplitude: must be between 0 and 1
        """
        waves = []
        for i in range(1, 11):
            waves.append(SimpleWave((2 * i - 1) * frequency, duration,
                                    amplitude / (2 * i - 1)))
        super().__init__(waves)
        self.frequency = frequency
        self.duration = duration
        self.amplitude = amplitude

    def __add__(self,
                other: ANYWAVE) -> ComplexWave:
        """ Adds this Square Wave with any other wave """
        return super().__add__(other)

    def complexity(self) -> int:
        """ Finds the complexity of the Square Wave """
        return super().complexity()

    def play(self) -> numpy.ndarray:
        """ Plays the Square Wave returned as a numpy array """
        return super().play()

    def get_waves(self) -> typing.List[SimpleWave]:
        """ Retrieves the Simple Waves that make up the Square Wave """
        return super().get_waves()

    def get_duration(self) -> float:
        """ Gets the duration of the Square Wave """
        return super().get_duration()

    def simplify(self) -> None:
        """
            REMEMBER: this is not a required part of the assignment
        """
        pass


class Rest(ComplexWave):
    """ Creates a Rest Wave.
    A Rest Wave is a special Complex Wave that is comprised of only 0 frequency
    Simple waves.

    == Attributes ==
    duration: the duration of the rest
    waves: the list of simple waves that make up the Rest Wave
    """
    duration: float
    waves: typing.List[SimpleWave]

    def __init__(self, duration: float) -> None:
        """ Initializes a Rest wave """
        self.duration = duration
        waves = [SimpleWave(0, self.duration, 0)]
        super().__init__(waves)

    def __add__(self,
                other: ANYWAVE) -> ComplexWave:
        """ Adds this Rest Wave with any other wave """
        return super().__add__(other)

    def complexity(self) -> int:
        """ Finds the complexity of the Rest Wave """
        return super().complexity()

    def play(self) -> numpy.ndarray:
        """ Plays the Rest Wave returned as a numpy array """
        return super().play()

    def get_waves(self) -> typing.List[SimpleWave]:
        """ Retrieves the Simple Waves that make up the Rest Wave """
        return super().get_waves()

    def get_duration(self) -> float:
        """ Gets the duration of the Rest Wave """
        return super().get_duration()

    def simplify(self) -> None:
        """
            REMEMBER: this is not a required part of the assignment
        """
        pass


class StutterNote(Note):
    """ A Stutter Note is a note that stutters. Naturally, this means that it is
    a subclass of the Note class.
    We are using the Sawtooth and Rest Waves to stutter between.
    The stutters will occur so that 20 of each are played every second.

    == Attributes ==
    frequency: the frequency of the first sine wave of the sawtooth wave
    duration: the duration of the sawtooth wave
    amplitude: the volume of the wave
    waves: the list of simple waves that make up the Sawtooth Wave
    """
    frequency: int
    duration: float
    amplitude: float
    waves: typing.List[SimpleWave]

    def __init__(self, frequency: int,
                 duration: float, amplitude: float) -> None:
        """ Initializes a Stutter Note as described in the class docstring

        Preconditions:
        amplitude: must be between 0 and 1"""
        self.frequency = frequency
        self.duration = duration
        self.amplitude = amplitude
        waves = []
        i = 0
        while i < int(self.duration * 20):
            waves.append(Rest(1 / 40))
            waves.append(SawtoothWave(self.frequency, 1 / 40, self.amplitude))
            i += 1
        super().__init__(waves)

    def __add__(self, other: Note) -> Note:
        """ Adds two Stutter Notes together """
        return super().__add__(other)

    def get_waves(self) -> typing.List[ANYWAVE]:
        """ Retrieves the waves that make up the Stutter Note """
        return super().get_waves()

    def get_duration(self) -> float:
        """ Retrieves the duration of the Stutter Note """
        return super().get_duration()

    def play(self) -> numpy.ndarray:
        """ Plays the Stutter Note as a numpy array """
        return super().play()


class Instrument:
    """ An Instrument is normally an object that creates different pitches of
    sound to create music. Here, we are using the instrument as something that
    creates different pitches through the use of different types of waves
    beginning at different frequencies.

    == Attributes ==
    frequency: the frequency the Instrument will naturally play as. I
        arbitrarily set this value to be 100 but will be changed in subclasses
        of the Instrument.
    melody: a Note type that represents the notes that the instrument will play
        when the play method is run
    duration: the duration that the Instrument will be playing
    waves: the list of waves that the Instrument will be playing
    type: The type of wave that will be played
    >>> bal = Gaffophone()
    >>> bal.next_notes([("1:1", 1, 1)]) #1 second at a time
    >>> l = SquareWave(131, 1, 1) + SquareWave(196, 1, 1)
    >>> play_sound(bal)
    >>> play_sound(l)
    """
    frequency: int
    melody: Note
    duration: float
    waves: typing.List[ANYWAVE]
    wtype: ANYWAVE or StutterNote

    def __init__(self, wtype: str) -> None:
        """ Initializes an Instrument
        The type is chosen between Sawtooth, Square and Stutter but more can be
        added if more wave types are created.
        The default if type does not match any is the Stutter Note.
        """
        self.frequency = 100
        self.melody = Note([])
        self.duration = 0.0
        self.waves = []
        if wtype == 'Sawtooth':
            self.wtype = SawtoothWave
        elif wtype == 'Square':
            self.wtype = SquareWave
        else:
            self.wtype = StutterNote

    def next_notes(self,
                   note_info: typing.List[typing.Tuple[str, float, float]]
                   ) -> None:
        """ The next notes of the instrument for the next second.
        self.waves is reset because we do not want to keep replaying the same
        notes if next notes is called multiple times."""
        for note in note_info:
            if note[0] == 'rest':
                self.waves.append(Rest(note[2]))
            else:
                parts = note[0].split(':')
                freq = round(self.frequency * (int(parts[0]) / int(parts[1])))
                self.waves.append(
                    self.wtype(freq, note[2], note[1]))
        self.melody = Note(self.waves)
        self.waves = []

    def get_duration(self) -> float:
        """ Retrieve the duration for which the Instrument plays """
        return self.melody.get_duration()

    def play(self) -> numpy.ndarray:
        """ Plays the Instrument and returns as a numpy array """
        return self.melody.play()


class Baliset(Instrument):
    """ Initializes a Baliset Instrument.
    The Baliset Instrument plays Sawtooth Waves and naturally plays at a
    frequency of 196

    == Attributes ==
    See Parent Class
    """
    frequency: int

    def __init__(self) -> None:
        """ Initializes a Baliset as described in the class docstring """
        super().__init__('Sawtooth')
        self.frequency = 196

    def get_duration(self) -> float:
        """ See Parent Class """
        return super().get_duration()

    def next_notes(self,
                   note_info: typing.List[typing.Tuple[str, float, float]]
                   ) -> None:
        """ See Parent Class """
        super().next_notes(note_info)

    def play(self) -> numpy.ndarray:
        """ See Parent Class """
        return super().play()


class Holophonor(Instrument):
    """ Initializes a Holophonor Instrument.
    The Holophonor Instrument plays Stutter Waves and naturally plays at a
    frequency of 65

    == Attributes ==
    See Parent Class
    """
    frequency: int

    def __init__(self) -> None:
        """ Initializes a Holophonor as described in the class docstring """
        super().__init__('Stutter')
        self.frequency = 65

    def get_duration(self) -> float:
        """ See Parent Class """
        return super().get_duration()

    def next_notes(self,
                   note_info: typing.List[typing.Tuple[str, float, float]]
                   ) -> None:
        """ See Parent Class """
        super().next_notes(note_info)

    def play(self) -> numpy.ndarray:
        """ See Parent Class """
        return super().play()


class Gaffophone(Instrument):
    """ Initializes a Gaffophone Instrument.
    The Gaffophone Instrument plays tw Square Waves and naturally plays at a
    frequency of 131
    The two waves have the bottom wave as the specified frequency and the upper
    wave at 1.5 times the bottom wave's frequency

    == Attributes ==
    See Parent Class
    """
    frequency: int
    melody: Note
    waves: typing.List[ANYWAVE]

    def __init__(self) -> None:
        """ Initializes a Gaffophone as described in the class docstring """
        super().__init__('Square')
        self.frequency = 131

    def get_duration(self) -> float:
        """ See Parent Class """
        return super().get_duration()

    def next_notes(self,
                   note_info: typing.List[typing.Tuple[str, float, float]]
                   ) -> None:
        """ See Parent Class """
        for note in note_info:
            if note[0] == 'rest':
                self.waves.append(Rest(note[2]))
            else:
                parts = note[0].split(':')
                freq = round(self.frequency * (int(parts[0]) / int(parts[1])))
                self.waves.append(
                    SquareWave(freq, note[2], note[1]) + SquareWave(
                        round(freq * 3 / 2), note[2], note[1]))
        self.melody = Note(self.waves)
        self.waves = []

    def play(self) -> numpy.ndarray:
        """ See Parent Class """
        return super().play()


def helper_read_file(song_file: str) -> typing.List[str]:
    """ Reads the csv file and returns it as a list """
    with open(song_file, 'r') as csv_file:
        reader = csv.reader(csv_file)
        file = []
        for row in reader:
            file.append(row)
    csv_file.close()
    return file


def helper_change_beat(notes_list: typing.List[typing.List[str]],
                       beat: float) -> None:
    """ Helper method to change the integers and floats from the csv file
    from string into their various types.
    The csv file must be written as stated below in play_song function. """
    for note in notes_list:
        if note[0] == 'rest':
            note[1] = float(note[1]) * beat
        elif note[0] != '':
            note[0] = int(note[0])
            note[1] = int(note[1])
            note[2] = float(note[2])
            note[3] = float(note[3]) * beat


def helper_play_song(notes_list: typing.List[typing.List[int or str]],
                     instrument: Instrument) -> None:
    """ Helper Method that adds the next 1 second on notes that a specified
    instrument will be playing """
    i = 0
    notes = []
    while i < 1:
        if len(notes_list) == 0:
            notes.append(('rest', 0.0, 1 - i))
            instrument.next_notes(notes)
            return
        elif notes_list[0][0] == 'rest' or notes_list[0][0] == '':
            if notes_list[0][0] == '':
                notes.append(('rest', 0.0, 1 - i))
                notes_list.remove(notes_list[0])
                instrument.next_notes(notes)
                return
            elif i + notes_list[0][1] > 1:
                notes_list[0][1] = notes_list[0][1] - (1 - i)
                notes.append(('rest', 0.0, 1 - i))
                instrument.next_notes(notes)
                return
            elif i + notes_list[0][1] == 1.0:
                notes_list.remove(notes_list[0])
                notes.append(('rest', 0.0, 1 - i))
                instrument.next_notes(notes)
                return
            else:
                notes.append(('rest', 0.0, notes_list[0][1]))
                i += notes_list[0][1]
                notes_list.remove(notes_list[0])
        else:
            if i + notes_list[0][3] < 1.0:
                notes.append(
                    ('%s:%s' % (notes_list[0][0], notes_list[0][1]),
                     notes_list[0][2], notes_list[0][3]))
                i += notes_list[0][3]
                notes_list.remove(notes_list[0])
            elif i + notes_list[0][3] == 1.0:
                notes.append(
                    ('%s:%s' % (notes_list[0][0], notes_list[0][1]),
                     notes_list[0][2], 1 - i))
                notes_list.remove(notes_list[0])
                instrument.next_notes(notes)
                return
            else:
                notes.append(
                    ('%s:%s' % (notes_list[0][0], notes_list[0][1]),
                     notes_list[0][2], 1 - i))
                notes_list[0][3] = notes_list[0][3] - (1 - i)
                instrument.next_notes(notes)
                return


def play_song(song_file: str, beat: float) -> None:
    """ Plays a song from the csv song file.

    Precondition:
    The csv file must be in this format. The first line represents the
    instrument that column will be played as and is separated by commas.
    The next lines will either have 4 integers separated by colons or
    'rest':integer or nothing at all.
    The 4 integers are formatted so that the first two represent the fraction of
    the original frequency that the note will be played at. The third shows the
    amplitude of the note and the last is the duration.
    For rests, the integer represents the duration and nothing at all means
    the instrument is done for the remainder of the song.
    >>> play_song('scale.csv', 0.1)
    """
    file = helper_read_file(song_file)
    bal = Baliset()
    gaf = Gaffophone()
    holo = Holophonor()
    for instrument in file[0]:
        if 'B' in instrument:
            b = file[0].index('Baliset')
        elif 'G' in instrument:
            g = file[0].index('Gaffophone')
        else:
            h = file[0].index('Holophonor')
    bal_notes = []
    gaf_notes = []
    holo_notes = []
    for line in file[1:]:
        if 'b' in vars():
            bal_notes.append(line[b].split(':'))
        if 'g' in vars():
            gaf_notes.append(line[g].split(':'))
        if 'h' in vars():
            holo_notes.append(line[h].split(':'))
    helper_change_beat(bal_notes, beat)
    helper_change_beat(gaf_notes, beat)
    helper_change_beat(holo_notes, beat)
    while (len(bal_notes) != 0 and bal_notes != ['']) or (
            len(gaf_notes) != 0 and gaf_notes != ['']) != 0 or (
                len(holo_notes) != 0 and holo_notes[0] != ['']):
        instruments = []
        if len(bal_notes) != 0 and bal_notes != ['']:
            helper_play_song(bal_notes, bal)
            instruments.append(bal)
        if len(gaf_notes) != 0 and gaf_notes != ['']:
            helper_play_song(gaf_notes, gaf)
            instruments.append(gaf)
        if len(holo_notes) != 0 and holo_notes[0] != ['']:
            helper_play_song(holo_notes, holo)
            instruments.append(holo)
        play_sounds(instruments)


# This is a custom type for type annotations that
# refers to any of the following classes (do not
# change this code)
ANYWAVE = typing.TypeVar('ANYWAVE',
                         SimpleWave,
                         ComplexWave,
                         SawtoothWave,
                         SquareWave,
                         Rest)

if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['helpers',
                                                  'typing',
                                                  'csv',
                                                  'numpy'],
                                'disable': ['E9997', 'E9998', 'W0611']})

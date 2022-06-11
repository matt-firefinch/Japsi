# import required libraries
import scipy.io.wavfile
from pydub import AudioSegment
from pydub.playback import play
import soundfile as sf
import pyloudnorm as pyln

def match_target_amplitude(sound, target_dBFS, measured_dbFS):
    change_in_dBFS = target_dBFS - measured_dbFS
    return sound.apply_gain(change_in_dBFS)

data, rate = sf.read("unprocessed.wav") # load audio (with shape (samples, channels))
meter = pyln.Meter(rate) # create BS.1770 meter
loudness = meter.integrated_loudness(data) # measure loudness
print("BS1770 loudness:", loudness)

wav_file = AudioSegment.from_file(file="unprocessed.wav", format="wav")
print("dBFS:", wav_file.dBFS)

normalized_sound = match_target_amplitude(wav_file, -19.0, loudness)
print("new dBFS:", normalized_sound.dBFS)

#normalized_sound = normalized_sound - 1
#print("new dBFS:", normalized_sound.dBFS)

# Play the audio file
#play(wav_file[:5000])
#play(normalized_sound[:5000])

normalized_sound.export(out_f="outNow.wav",format="wav")

data, rate = sf.read("outNow.wav") # load audio (with shape (samples, channels))
meter = pyln.Meter(rate) # create BS.1770 meter
loudness = meter.integrated_loudness(data) # measure loudness
print("New BS1770 loudness:", loudness)
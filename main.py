import soundfile as sd
from matplotlib import pyplot
import numpy
from scipy.fftpack import fft, ifft
import os

if not os.path.exists("sounds"):
    os.makedirs("sounds")

audio_file = "base.wav"
sound_array, sample_rate = sd.read(audio_file)

sample_duration = 5

sample_lenght = sample_duration * sample_rate
altitude_up = 5

samples = []
for q in range(0, len(sound_array), sample_lenght):
    sound = sound_array[q:q+sample_lenght]
    # result =[[0,0] for i in range(100000)] + numpy.fft.fft(sound).real.tolist()[:-100000]
    # pyplot.plot(sound)
    # pyplot.show()
    print(sound[:,0])

    result1 = fft(sound[:,0]).real.tolist()
    result2 = fft(sound[:,1]).real.tolist()
    pyplot.plot(result1)
    pyplot.show()
    break
    result = numpy.fft.ifft(result).real
    # array = sound.tolist()
    # # print(array[0])
    # result = []

    # for i in array:
    #     for j in range(altitude_up):
    #         result.append(i)
        
    # result = numpy.array(result)
    sd.write(f"sounds\\{q}.wav", result, sample_rate)


print("eee")
    
    

import wave
import numpy as np
import pyaudio


def readWavFile(wav_path):
    """
    :param wav_path: 需要读取的文件路径
    :return: （声道，量化位数，采样率，帧数，数据)
    """
    read_file = wave.open(wav_path, "rb")
    params = read_file.getparams()
    nchannels, sampwidth, framerate, nframes = params[:4]
    total_time = int(nframes / framerate * 1000)  # wav文件时长(ms)
    # logger.info("{0} 总时长 {1} ms".format(wav_path, total_time))
    data = read_file.readframes(nframes)
    wave_data = np.fromstring(data, dtype=np.short)
    if nchannels == 2:
        wave_data = wave_data[range(0, int(nframes * nchannels), 2)]
    return nchannels, sampwidth, framerate, nframes, wave_data


if __name__ == '__main__':
    nchannels, sampwidth, framerate, nframes, wave_data = readWavFile("source.wav")
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(sampwidth),
                    channels=1,
                    rate=framerate,
                    output=True)
    # wave_data = np.asarray(wave_data * 32768, np.short)
    # wave_data = np.maximum(np.minimum(wave_data, 32767), -32768)
    # plt.plot(wave_data[2000:2100])
    # plt.show()
    data = wave_data[:1600].tobytes()
    i = 1
    while data != b'':
        stream.write(data)
        data = wave_data[int(i * 1600):int(i * 1600 + 1600)].tobytes()
        i += 1
    print()

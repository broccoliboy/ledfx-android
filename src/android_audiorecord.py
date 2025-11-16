# Wrapper for the [Android Visualizer API](https://developer.android.com/reference/android/media/audiofx/Visualizer)

import logging
from jnius import autoclass

logger = logging.getLogger(__name__)


class AndroidAudioRecord:
    """
    Class interface to the Android AudioRecord API
    """
    
    name = 'Microphone'
    hostapi = 'Android AudioRecord API'
    channels = 1

    def __init__(self, session_id=0, capture_size=None):
        """
        Initialize
        """
        self.session_id = session_id
        self.capture_size = capture_size
        self.sampling_rate = 44100  # Standard sample rate
        self._waveform = None
        self.recorder = None
        
    def __enter__(self, *args, **kwargs):
        return self.start()

    def __exit__(self, *args, **kwargs):
        self.stop()
    
    def start(self):
        """
        Configure native Android AudioRecord and start capture
        """
        NativeAudioRecord = autoclass('android.media.AudioRecord')
        AudioFormat = autoclass('android.media.AudioFormat')
        AudioSource = autoclass('android.media.MediaRecorder$AudioSource')

        # Set parameters
        audio_format = AudioFormat.ENCODING_PCM_8BIT
        channels = AudioFormat.CHANNEL_IN_MONO
        self.buffer_size = NativeAudioRecord.getMinBufferSize(
            self.sampling_rate,
            channels,
            audio_format
        )
        if self.capture_size is not None and self.capture_size > self.buffer_size:
            self.buffer_size = self.capture_size

        logger.debug(f'Using AudioRecord buffer size: {self.buffer_size}')

        # Create AudioRecord instance
        self.recorder = NativeAudioRecord(
            AudioSource.MIC,
            self.sampling_rate,
            channels,
            audio_format,
            self.buffer_size
        )
        self._waveform = bytearray(self.buffer_size)  # 8-bit PCM, so 1 byte per sample
        self.recorder.startRecording()
        logger.debug('AudioRecord started')
        return self

    def stop(self):
        """
        Stop and release native Android AudioRecord
        """
        try:
            self.recorder.stop()
            self.recorder.release()
        except Exception as e:
            logger.debug(f'Error stopping AudioRecord: {e}')
        self.recorder = None
        logger.debug('AudioRecord stopped')
    
    @property
    def waveform(self):
        """
        Property for retrieving current PCM waveform data from AudioRecord
        """
        # Read PCM data into the buffer
        self.recorder.read(self._waveform, 0, len(self._waveform))
        return self._waveform

# Wrapper for the [Android Visualizer API](https://developer.android.com/reference/android/media/audiofx/Visualizer)

import time
import logging
from jnius import autoclass, PythonJavaClass, java_method

logger = logging.getLogger(__name__)


class AndroidVisualizer:
    """
    Class interface to the Android Visualizer API
    """
    
    name = 'Stereo Mix'
    hostapi = 'Android Visualizer API'
    channels = 1
    session_id = 0  # default audio session ID for capturing output audio (stereo mix)

    def __init__(self, capture_size=None):
        """
        Initialize
        """
        self.capture_size = capture_size
        self.sampling_rate = 0
        self.vis = None
        self._waveform = None
        self._fft = None
        
    def __enter__(self, *args, **kwargs):
        return self.start()

    def __exit__(self, *args, **kwargs):
        self.stop()
    
    def start(self):
        """
        Configure native Android Visualizer and start capture
        """
        
        NativeAndroidVisualizer = autoclass('android.media.audiofx.Visualizer')

        # create native Android Visualizer object on the chosen session ID. Default session id is 0 (stereo mix)
        logger.debug(f'Starting visualizer on session ID {self.session_id}')
        self.vis = NativeAndroidVisualizer(self.session_id)
        logger.debug(f'Got NativeAndroidVisualizer: {self.vis}')

        # disable visualizer while we configure it
        self.vis.setEnabled(False)
        
        capture_size_range = self.vis.getCaptureSizeRange()
        default_capture_size = self.vis.getCaptureSize() or capture_size_range[-1]
        logger.debug(f'Capture size range: {capture_size_range}')
        logger.debug(f'Default capture size: {default_capture_size}')
        
        # try to use requested capture size but fall back to default/max capture size if it fails
        try:
            self.vis.setCaptureSize(self.capture_size or default_capture_size)
        except Exception as e:
            logger.warning(f'Error setting capture size {self.capture_size}: {e}')
            logger.warning('Falling back to default or max capture size')
            self.vis.setCaptureSize(default_capture_size)
        
        self.capture_size = self.vis.getCaptureSize()
        logger.debug(f'Using capture size of {self.capture_size}')
        
        # init empty bytearrays to hold captured waveform and fft data
        self._waveform = bytearray(self.capture_size)
        self._fft = bytearray(self.capture_size)

        # save sampling rate used by the visualizer (typically 44100 Hz)
        self.sampling_rate = self.vis.getSamplingRate() / 1000  # divide by 1000 because Android Visualizer provides sampling rate in millihertz
        
        logger.debug(f'Sampling rate: {self.sampling_rate} Hz')
        
        # use normalized scaling (waveform output is not scaled by device volume setting)
        self.vis.setScalingMode(NativeAndroidVisualizer.SCALING_MODE_NORMALIZED)

        # tell Android that we don't want any RMS measurements
        self.vis.setMeasurementMode(NativeAndroidVisualizer.MEASUREMENT_MODE_NONE)

        # Abandoned callback method, but leaving here as an example of how this could be done if someone wants to revisit this
        # See below for definition of PythonOnDataCaptureListener
        # log.d('Setting data capture listener')
        # self.capture_rate = self.vis.getMaxCaptureRate()
        # log.d(f'Capture rate set to max: {self.capture_rate/1000} Hz')
        # self.vis.setDataCaptureListener(
        #     PythonOnDataCaptureListener(
        #         self.on_waveform_data,
        #         self.on_fft_data
        #     ),
        #     self.capture_rate,
        #     self.get_waveform,  # get waveform data?
        #     self.get_fft  # get fft data?
        # )
        
        # enable the visualizer
        self.vis.setEnabled(True)
        logger.debug('Visualizer enabled')

        return self

    def stop(self):
        """
        Disable and release native Android Visualizer
        """
        if self.vis is not None:
            try:
                self.vis.setEnabled(False)
            except Exception as e:
                logger.warning(f'Error disabling visualizer: {e}')
            try:
                self.vis.release()
                time.sleep(0.5)  # seems to improve stability to wait for a bit after releasing
            except Exception as e:
                logger.warning(f'Error releasing visualizer: {e}')
            self.vis = None
            self._waveform = None
            self._fft = None
            logger.debug('Visualizer disabled')
    
    @property
    def waveform(self):
        """
        Property for retrieving current waveform data
        https://developer.android.com/reference/android/media/audiofx/Visualizer#getWaveForm(byte[])
        """
        self.vis.getWaveForm(self._waveform)
        return self._waveform
    
    @property
    def fft(self):
        """
        Property for retrieving current fft data
        https://developer.android.com/reference/android/media/audiofx/Visualizer#getFft(byte[])
        """
        self.vis.getFft(self._fft)
        return self._fft


# This was my first attempt at accessing android visualizer waveform data using the callback method.
# It caused significant instability and irregular crashes. I replaced this with a threaded polling approach
# calling getWaveForm() on the Visualizer object regularly, which has much better performance and allows
# polling at higher frequency compared to the callback method which only allows up to 20 Hz capture rate.
# However, the returned waveform data is still limited to 1 KB per poll on most Android systems. This seems to
# be okay and can still achieve high quality visualizations.
# class PythonOnDataCaptureListener(PythonJavaClass):
#     __javainterfaces__ = ['android/media/audiofx/Visualizer$OnDataCaptureListener']
#     __javacontext__ = 'app'

#     def __init__(self, waveform_data_callback, fft_data_callback):
#         super().__init__()
#         self.waveform_data_callback = waveform_data_callback
#         self.fft_data_callback = fft_data_callback
    
#     @java_method((  # wrap these strings in () to concat
#         '('  # start argument list
#         'Landroid/media/audiofx/Visualizer;'  # class android.media.audiofx.Visualizer
#         '[B'  # byte array
#         'I'  # int
#         ')'  # end argument list
#         'V'  # return void
#     ))
#     def onFftDataCapture(self, visualizer, fft, sampling_rate):
#         try:
#             self.fft_data_callback(fft, sampling_rate)
#         except:
#             pass

#     @java_method((  # wrap these strings in () to concat
#         '('  # start argument list
#         'Landroid/media/audiofx/Visualizer;'  # class android.media.audiofx.Visualizer
#         '[B'  # byte array
#         'I'  # int
#         ')'  # end argument list
#         'V'  # return void
#     ))
#     def onWaveFormDataCapture(self, visualizer, wave, sampling_rate):
#         try:
#             self.waveform_data_callback(wave, sampling_rate)
#         except:
#             pass
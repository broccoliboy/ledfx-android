# ledfx-android

This project is an Android port of the amazing [LedFx](https://github.com/LedFx/LedFx) audio reactive LED controller library, allowing visualization of **any audio** playing from your android device. Yes, that means Spotify, YouTube, Radio Apps, etc. It doesn't require root or any funny business on the phone and runs as any typical app does. All you have to do is add your LED strip devices, activate an effect, and press play! This project is intended to work on both mobile and Android TV devices.

## Android TV

Android TV devices like NVIDIA shield are often the central hub in a living room media experience. The original goal of this project was to enable LedFx here so it could visualize music from the apps I normally use to stream music (Spotify, YT, etc.) AND music that is **cast** to the Android TV from a mobile device. This app has been tested on a 2019 NVIDIA Shield Pro so your results may vary with other devices.

There are a few differences in building apps for mobile compared to Android TV, most importantly the fact that users interact with your app using a remote control rather than a touch screen or mouse/keyboard. Enter [Leanback Mode](https://developer.android.com/design/ui/tv/guides/foundations/design-for-tv). When running on Android TV, LedFx doesn't show its default UI but instead shows a QR code that points mobile devices to the LedFx server running on the Android TV device.

The same apk will run on both mobile and TV and will automatically determine which mode to run in, and automatically determine the TV IP address for displaying the QR code.

## Getting system audio into LedFx

The secret to visualizing **any** audio on your android device lies in the [Android Visualizer API](https://developer.android.com/reference/android/media/audiofx/Visualizer). This API exposes methods to access raw PCM waveform data of any audio currently playing from your device (at a reduced quality and capture rate). I found it adequate for LedFx visuals. LedFx typically relies on [python-sounddevice](https://github.com/spatialaudio/python-sounddevice/) for audio data input, which is build on PortAudio. Unfortunately PortAudio doesn't support Android. My solution was to write a mock sounddevice.py module to feed LedFx data from Android Visualizer API calls. This works for now, but is susceptible to upstream changes in the way LedFx interfaces with python-sounddevice.

## Quirks

### Background service priority

This implementation runs the LedFx server as a background process on Android so it can continue sending LED data when the user switches to their favorite music app. Typically, Android OS is fairly aggressive at pausing apps that are sent to the background to save memory, which would cause serious problems for LedFx. To minimize the chances of this, the LedFx server runs in a [foreground service](https://developer.android.com/develop/background-work/services/fgs). This tells Android to try its best to keep the service running because it's doing important things in the background. However, this is never a guarantee. If Android decides it's running low on memory, it can always pause/kill the LedFx service to prioritize an app that the user is actually interacting with. As far as I can tell, there's no way for a user space app to *guarantee* that a background process continues to run no matter what. For this reason, Android users (esp those on older hardware) may see performance issues when LedFx is running in the background.

Additionally, the foreground service is set to "sticky" which tells android to always restart it if it should happen to die for some reason.

See here for more details on working with services in python-for-android: https://python-for-android.readthedocs.io/en/latest/services.html

### Hostname resolution

Some Android devices don't have mDNS support so auto discovery of WLED devices fails. I found that manually adding one by IP address works, then others are discovered and can be added as well. Could be helpful for upstream LedFx to fall back to IP address if hostname fails to resolve.

## Stack

The build system uses [Buildozer](https://github.com/kivy/buildozer) and [python-for-android](https://github.com/kivy/python-for-android/) which are part of the [Kivy](https://github.com/kivy/kivy) ecosystem. A minor change to python-for-android was needed to solve numpy build errors so a [custom fork](https://github.com/broccoliboy/python-for-android/) is used for this compilation.

Buildozer handles android build environment creation by automatically downloading required SDK, NDK, etc. First run will be slow because of this.

Python-for-android uses [recipes](https://python-for-android.readthedocs.io/en/latest/recipes.html) that tell the build system how to handle certain python libraries. This is necessary to help build libraries that have compiled components for the target architecture. The python-for-android project already has many recipes for common python libraries (like numpy) but some LedFx dependencies required custom or updated recipes. These can be found in the `recipes` folder. Aubio is one example of a library that required a custom recipe to get LedFx running on android.

## Getting started

- Python 3.12 recommended
- Clone this repo with submodules
  - `git clone --recurse-submodules --depth=1 https://github.com/broccoliboy/ledfx-android`
  - `deps/ledfx` submodule will be populated if `--recurse-submodules` flag is passed to git clone. This is needed before we run buildozer so we have access to version info and icons that are used in the Android build.
- Install latest buildozer from source
  - `pip install --upgrade git+https://github.com/kivy/buildozer`

### Build

- Build using `buildozer`
  - `buildozer android debug` or `buildozer android release`
    - Builds apk in debug/release mode
  - `buildozer android debug deploy run logcat`
    - Build apk, deploy to running emulator or real device connected through adb, start app, and start log viewer
  - `buildozer android clean`
    - Cleans build environment
- Optionally, set env var `SKIP_PREREQUISITES_CHECK=1` to speed up buildozer after you confirm all prerequisites are available

See [here](https://github.com/kivy/buildozer) for more information on using the buildozer environment

### Github Action

This repo includes a Github Action that will build an apk and trigger a new release any time a tagged version is committed. See [.github/workflows/build-apk.yml](.github/workflows/build-apk.yml) for details.

## Future work

- Support config file import/export. Currently doesn't work in Android webview.
- Improve LedFx Leanback Mode to allow more controls, like triggering LedFx Scenes or setting effects on known devices
- Automatic detection of music/audio playing using [Android Visualizer peak/RMS measurement mode](https://developer.android.com/reference/android/media/audiofx/Visualizer#getMeasurementPeakRms(android.media.audiofx.Visualizer.MeasurementPeakRms)) to enable/disable LedFx effects

## Gallery

### Mobile

<img src="img/ledfx-android-mobile.png" alt="Mobile" style="width: 200px;" />

### Android TV

<img src="img/ledfx-android-tv.png" alt="Android TV" style="width: 600px;" />

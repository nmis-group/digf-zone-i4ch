# Deployment on EDGE device

## Edge device

Device information()


Edge device information - the Stereolabs [ZED Box Xavier NX](https://www.stereolabs.com/zed-box/) comes with two NVIDIA® Jetson™ Module options. 


## System info

Reference [ZED Box Xavier NX](https://www.stereolabs.com/zed-box/) hardware information online.
a

## Deployment 

### 4 Deployment ZED SDK

https://www.stereolabs.com/docs/get-started-with-zed-box/

*If you know the jetpack version, skip this step and install the ZED SDK by type command from bash.*

Check nvidia Jetson version

```sh
apt-cache policy nvidia-jetpack
```

Here, the version is 

```sh
nvidia-jetpack:
  Installed: 4.6-b199
  Candidate: 4.6-b199
  Version table:
 *** 4.6-b199 500
        500 https://repo.download.nvidia.com/jetson/t194 r32.6/main arm64 Packages
        100 /var/lib/dpkg/status
     4.6-b197 500
        500 https://repo.download.nvidia.com/jetson/t194 r32.6/main arm64 Packages

```


Then, go to stereolabs.com/developers/release, click on the “SDK Downloads” tab and scroll down to ﬁnd the corresponding SDK for the Jetpack version of your NVIDIA® Jetson™ system.

Then we should download ZED SDK for [Jetpack 4.6](https://download.stereolabs.com/zedsdk/3.6/jp46/jetsons)

```sh
chmod +x ZED_SDK_<PLATFORM>_<VERSION>.run
    
./ZED_SDK_<PLATFORM>_<VERSION>.run
```



### 5 Hit:
  When use the ZED camera at the first time, the internet connection should be ensured in case of the downloading some module of ZED.




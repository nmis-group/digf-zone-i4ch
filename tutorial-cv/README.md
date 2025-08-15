<div id="top"></div>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![GNU GPL V3][license-shield]][license-url]
<!--[![LinkedIn][linkedin-shield]][linkedin-url]-->



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://www.nmis.scot">
    <img src="docs/resources/images/logo.png" alt="Logo" width="280" height="280">
  </a>

  <h3 align="center">NMIS COREF</h3>

  <p align="center">
    COREF Bolt Detection Tutorial
    <br />
    <a href="https://github.com/nmis-group"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/nmis-group/colab">View Colab</colab/a>
    ·
    <a href="https://github.com/nmis-group/issues">Report Bug</a>
    ·
    <a href="https://github.com/nmis-group/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
Project Name: Real-time Bolt Detection

In this repository, we only demostrate the real-time bolt detection tutoruial by using deep learning.

<div align="center">
<img src="docs/resources/images/screenshot.png" alt="Logo" width="280" height="280">
</div>
In this repository, a Computer Vision (CV) object detection system by using ZED camera and edge device and with a deep learning model is presented. According to the CV system structure, data collection annotation, EfficientDet model training, YOLOv5 model training and real time detection are illustrated separately. Finally, by deploying and integrating the system on the smart workbench, it successfully detects all bolts on the working process of assembly. The result reveals that the CV system has a high accuracy of bolts object detection according to the edge device and YOLOv5 model with deep learning.

<p align="right">(<a href="#top">back to top</a>)</p>


### Built With

This project build with docker-compose. Major frameworks/libraries are list below

* [Jupyter](https://jupyter.org/)
* [numpy](https://numpy.org/)
* [pandas](https://pandas.pydata.org/)
* [python](https://www.python.org/)
* [pytorch](https://pytorch.org)
* [pytorch-lightning](https://www.pytorchlightning.ai/)
* [opencv](https://opencv.org)
* [scikit-learn](https://scikit-learn.org)
* [matplotlib](https://matplotlib.org)
* [tensorboard](https://www.tensorflow.org/tensorboard)
* [effdet](https://pypi.org/project/effdet/)


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started
To get start, first clone this repository with the command into your local.

```
git clone https://github.com/nmis-group/digf-zone-i4ch.git
```
In tutorial-cv folder nevigate to gpu-jupyter folder within setup folder 
```
cd ~/digf-zone-i4ch/tutorial-cv/setup/gpu-jupyter
```
and run command
```
sudo docker-compose up
```
It will install nessesary development environment and dependency frameworks and libraries inside a docker container.


or else you can download the git repo : https://github.com/iot-salzburg/gpu-jupyter
and add additional python libraries in src/Dockerfile.usefulpackages and run
```
./generate-Dockerfile.sh --python-only

```
It will generate a new dockerfile and then run 
```
sudo docker-compose up
```
or to rebuild the container run
```
sudo docker-compose up --build
```

### Change owner for container accessibility
Before running above commands, user should changer the owner of some folders so that the container could access them.
```
cd ../tutorial-cv
sudo chown -R root:root notebooks/ src/ models/
sudo chmod -R 777 notebooks/ src/ models/
cd data/
sudo chown -R root:root interim/
sudo chmod -R 777 interim/
```

### Docker container

You can access the gpu-jupyter notebooks inside the container at http://localhost:8848
First, create a interim folder inside work folder to save interim results (e.g. dataset.csv) and then you can run all the builds inside the notebooks folder 

### Prerequisites

* [Docker](https://docs.docker.com/desktop/)

### Installation on edge device

* [Docs](./docs/Deployment/Deployment.MD)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [x] Make repository public
- [ ] Add tutorial on windows platform


See the [open issues](https://github.com/nmis-group/AFRC_CRAD_1718_COREF/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- LICENSE -->
## License

Distributed under the GNU GPL V3 License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

NMIS DIGITAL TEAM - [@National Manufacturing Institute Scotland](https://twitter.com/NMIS_group?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor) - anastasios.stamoulakatos@strath.ac.uk andrew.hamilton@strath.ac.uk syed.munawar@strath.ac.uk jianfeng.huang@strath.ac.uk

Project Link: [https://github.com/nmis-group/AFRC_CRAD_1718_COREF](https://github.com/nmis-group/AFRC_CRAD_1718_COREF)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Use this space to list resources you find helpful and would like to give credit to. I've included a few of my favorites to kick things off!

* [STEREO LABS ZED](https://github.com/stereolabs/)
* [Shield.io](https://shields.io/)
* [Best Readme Template](https://github.com/othneildrew/Best-README-Template)
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/nmis-group/AFRC_CRAD_1718_COREF.svg?style=for-the-badge
[contributors-url]: https://github.com/nmis-group/AFRC_CRAD_1718_COREF/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/nmis-group/AFRC_CRAD_1718_COREF.svg?style=for-the-badge
[forks-url]: https://github.com/nmis-group/AFRC_CRAD_1718_COREF/fork
[stars-shield]: https://img.shields.io/github/stars/nmis-group/AFRC_CRAD_1718_COREF.svg?style=for-the-badge
[stars-url]: https://github.com/nmis-group/AFRC_CRAD_1718_COREF/stargazers
[issues-shield]: https://img.shields.io/github/issues/nmis-group/AFRC_CRAD_1718_COREF.svg?style=for-the-badge
[issues-url]: https://github.com/nmis-group/AFRC_CRAD_1718_COREF/issues
[license-shield]: https://img.shields.io/badge/License-GPLv3-blue.svg
[license-url]: https://www.gnu.org/licenses/gpl-3.0
[product-screenshot]: resources/images/screenshot.png

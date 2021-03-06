[`HOME`](README.md) [`About us`](ABOUT_US.md) [`License`](LICENSE.md) [`Miscellaneous`](MISC.md)

# About us
We belong to Australian federal government agency responsible for scientific research called CSIRO [The Commonwealth Scientific and Industrial Research Organisation](https://www.csiro.au/).

Within this organisation, we are in a division called [Astronomy and Space](https://www.csiro.au/en/Research/Astronomy). We are involved in a project called [(Australian Square Kilometre Array Pathfinder)](https://www.csiro.au/en/Research/Facilities/ATNF/ASKAP?ref=/CSIRO/Website/Research/Astronomy/ASKAP-and-the-Square-Kilometre-Array/ASKAP). 

One of the software that we are working on is called ASKAPsoft. In an effort to make the code public, as a code called Yandasoft, we found that [Docker](https://www.docker.com/) container technology is very useful for our purpose. To cater for users who are running the code on HPC systems, it's best to download the Docker images using [Singularity ](https://sylabs.io/). One of the problems that we are facing is that the Docker images can be built only for certain MPI implementations, and that implementation must match that of the host machine it runs on. Our users have a range of MPI implemntations, and this means we have to make Docker images suited for those environment. Obviously we need a way to automate this. This code repository is aimed at creating a prototype of such solution. It's designed to be simple (relatively speaking) and generic, so that it can be used for any project.

![ASKAP antennas in Western Australia](ASKAP-night-6932-ACherney.jpg)


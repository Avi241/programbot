# Program Bot
Testing Program bot Simulation in docker

# Installation 
## Docker

You can find these installation instructions [here](https://docs.px4.io/master/en/test_and_ci/docker.html).

## Installing Docker

#### Install docker using [convenience script](https://docs.docker.com/install/linux/docker-ce/ubuntu/#install-using-the-convenience-script)
    
    sudo apt-get install curl
    curl -fsSL get.docker.com -o get-docker.sh
    sudo sh get-docker.sh

#### Steps to use docker without having to use sudo
    
    sudo groupadd docker
    # Add your user to the docker group.
    sudo usermod -aG docker $USER
    # Close the terminal or restart computer to see effects

# Setting up the workspace on users computer

    mkdir -p ~/programbot/home

   # enable access to xhost from the container
    xhost +

   # Run docker and open bash shell

    docker run -it --privileged --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" -v ~/programbot/home:/home/:rw --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" -p 14556:14556/udp --name=programbot avi241/programbot:updated bash
    
   # Try running gazebo
    gazebo
    
   # To open a new bash shell of this container
   
    docker exec -it drone bash
    
   # To Run Simulation
   roslaunch inter_iit_sbb_description empty_world.launch
   
   # To run controller
   rosrun inter_iit_sbb_description controller.py
   
   # To edit controller Code
   gedit ~/catkin_ws/src/inter_iit_sbb_description/scripts/controller.py
   

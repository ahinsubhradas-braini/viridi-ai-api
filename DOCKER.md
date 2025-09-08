Powershell comands

# Docker compose up

    docker-compose up --build

# To stop all containers

    docker stop $(docker ps -aq)

# To remove all containers

    docker rm $(docker ps -aq)

# To remove all images

    docker rmi $(docker images -q)

# To remove all unused images

    docker system prune -a -v
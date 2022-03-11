FROM ubuntu:21.04

ARG USERNAME=alex
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Update packages list & install missing packages
RUN apt-get update \
    && export DEBIAN_FRONTEND=noninteractive \
    # install missing packages
    && apt-get install -y sudo git curl wget make procps \
    python3-pip unzip nodejs npm vim dos2unix apt-transport-https ca-certificates \
    gnupg lsb-release

# Finish setting up $USERNAME (sudo, no password etc ...)
RUN echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Install Docker CLI
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

RUN  apt-get update \
      && apt-get install -y docker-ce-cli

# Python things: update pip
RUN python3 -m pip install pip --upgrade

# Install required librairies
COPY ./requirements.txt /home/$USERNAME/

RUN pip install -r /home/$USERNAME/requirements.txt

# Set $USERNAME as default user
USER $USERNAME

# Add custom bashrc
COPY --chown=$USERNAME:$USERNAME ./bashrc /home/$USERNAME/.bashrc_extension
RUN echo "source ~/.bashrc_extension" >> ~/.bashrc && dos2unix ~/.bashrc_extension

# Back to default shell
SHELL ["/bin/bash", "-c"]

CMD [ "sleep", "infinity" ]

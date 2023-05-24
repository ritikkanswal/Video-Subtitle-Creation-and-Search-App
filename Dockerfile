FROM joyzoursky/python-chromedriver
ARG SSH_PRIVATE_KEY
RUN apt-get update
COPY . /app
WORKDIR /app
# # Pass the content of the private key into the container
# RUN mkdir /root/.ssh/
# RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa
# #Github requires a private key with strict permission settings
# RUN chmod 600 /root/.ssh/id_rsa
# #Add Github to known hosts
# RUN touch /root/.ssh/known_hosts
# RUN ssh-keyscan bitbucket.org >> /root/.ssh/known_hosts
RUN pip install -r requirements.txt
RUN export DJANGO_SETTINGS_MODULE=SubtitleTimeTracker.settings

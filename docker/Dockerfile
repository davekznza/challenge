# Using node:10, had issues with node:16
FROM node:10

# Set environment variable which our app references
ENV FOOBAR="Foo Bar"

# Create our apps workdir
WORKDIR /app

# Copy our package.json across, wildcard used to ensure package-lock.json is also included
COPY package*.json ./

# Install dependecies and update
RUN npm install
RUN npm update

# Bundle app source
COPY . .

# App binds to 8080/tcp we'll expose that
EXPOSE 8080

# Run our app
CMD [ "node", "main.js" ]

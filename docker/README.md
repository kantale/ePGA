
### Directions to setup the service with docker 
1. Clone this repository
2. Go to folder: `docker/explore`
3. Build the explore image:

```bash
docker build -t explore .
```

4. Go to folder: `docker/translate`
5. Build the translate image:

```bash
docker build -t translate .
```

6. Run the explore image:

```bash
docker run -p 8200:8200 -t explore 
```

Validate that is working by visiting http://0.0.0.0:8200

7. Run the translate image:

```bash
docker run -p 8080:8080 -t translate
```

Validate that it is working by visiting http://0.0.0.0:8080

### Future work
Some additional work is required to make these containers collaborate.
1. Change the translate links in explore and vice versa 
2. Consider setting up a [docker compose](https://docs.docker.com/compose/) service 



### filplus-client-explorer

This repo is a Plotly Dash app (on Flask) that explores FIL+ client metrics. 

### Building the Docker container locally

Change directory to the top level of this repo. Then

```
docker build -t filplus-dash .
```

Then run

```
docker run -p 8050:8050 filplus-dash
```

Finally access localhost:8050
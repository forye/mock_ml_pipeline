### ML Pipeline

 This repository contains a microservice based mock that is managed by Airflow.
  
  It is not fully functional, but it should serve as a starting point for a real implementation.

### Implementation

1. The is implemented in a micro-service paradigm (even though it is local, but its a poc..) each component has a dockerfile and executed by itself using Airflow
2. The system support continues training of the model and uses the last trained clustering model
 

#### The following components are included in the mock:

1. daywise_sensorwise_chunker: This component takes in the input csv file and saves it to chunks. This simulates handling a stream or a heavy Spark job and moving it forward to the features_creator module.
2. features_creator: This module aggregates the data from the chunks into smaller sized data.
3. clustering_model: this module holds a clustering model, it sepratoed to 2 components predictions and training

## Running

### Docker
To run the mock, you can clone the repository and type
 
``` docker-compose up -build```

 (for the first time)

 ```and docker-compose up```

after it was built for the first time

```and docker-compose down```
  
to bring it down.


### To access airflow

browse to 

```localhost:8080```

#### Metrics
The following metrics are implemented upon others:

1. The shapes of the dataframes in the preprocessing stages.
2. The memory status in the feature creator stage.
3. The clusters distributions on the clustering stage.




#### What I would do if I had more time
If I had more time, I would do the following:

1. Fix bugs in the configuration.
2. Use a secure password for the PostgreSQL database.
3. Set up a local Docker and Airflow environment and test the code.
4. Solve the ambiguity in the source folder by setting the train/test csv file in a configuration management system.
5. Use a cloud storage instead of a local file system and run all processes as microservices on an AWS (or other) servers.
6. Implement the Observer module.
7. Do some refactoring.
8. Detach the postgress connector from the predicition code ( move it to utilities)
9. I would imlement a metric that compares the mean and std of the feature creator to past values and report
10. A verbose option (to silent some of the reports if needed as they can take resources sometimes)
11. I would make think of an option for the modules to stay alive and serve as a REST API from prediction, 
to prevent bringing up and down for every inference/transformation/training
12. make the Logging more uniform and organized


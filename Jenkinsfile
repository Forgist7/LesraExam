pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = 'forgist/lesta-exam'
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh "docker build -t ${DOCKER_HUB_REPO}:${IMAGE_TAG} ."
            }
        }

        stage('Test/Lint') {
            steps {
                sh 'docker run --rm ${DOCKER_HUB_REPO}:${IMAGE_TAG} flake8 /app/app.py'
            }
        }

        stage('Login to Docker Hub') {
           steps {
               withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', passwordVariable: 'DOCKERHUB_PASS', usernameVariable: 'DOCKERHUB_USER')]) {
                   sh 'echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin'
               }
           }
        }

        stage('Push') {
            steps {
                sh "docker push ${DOCKER_HUB_REPO}:${IMAGE_TAG}"
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker compose down'
                sh 'docker compose up -d'
            }
        }
    }
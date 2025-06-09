pipeline {
    agent any

    environment {
        DOCKER_HUB_REPO = 'forgist/lesta-exam'
        IMAGE_TAG = 'latest'
        REMOTE_DIR = '/home/ubuntu/app'
        REMOTE_HOST = '37.9.53.90'
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
                sh """
                    echo "Local workspace files:"
                    ls -la

                    mkdir -p ${REMOTE_DIR}

                    cp ./docker-compose.yaml ./app.py ./requirements.txt ./Dockerfile ${REMOTE_DIR}/

                    cd ${REMOTE_DIR} || { echo "Failed to cd to ${REMOTE_DIR}"; exit 1; }
                    echo "Files in ${REMOTE_DIR}:"
                    ls -la
                    echo "Checking permissions for ${REMOTE_DIR}:"
                    ls -ld ${REMOTE_DIR}

                    docker compose down || true
                    docker compose pull
                    docker compose up -d --build
                """
            }
        }
    }
}
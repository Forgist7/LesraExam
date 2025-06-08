pipeline {
    agent any

    environment {
        DOCKER_REGISTRY = 'registry:5000'
        IMAGE_NAME = "${DOCKER_REGISTRY}/myapp"
        COMPOSE_PROJECT_NAME = 'myapp'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'cat requirements.txt'
                sh 'docker build -t ${IMAGE_NAME} .'
            }
        }

        stage('Test/Lint') {
            steps {
                sh 'docker run --rm ${IMAGE_NAME} flake8 /app/app.py'
            }
        }

        stage('Push') {
            steps {
                sh 'docker push --tls-verify=false ${IMAGE_NAME}'
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker compose down'
                sh 'docker compose up -d'
            }
        }
    }

    post {
        always {
            sh 'docker compose logs'
        }
        failure {
            echo 'Pipeline failed, please check the logs.'
        }
    }
}
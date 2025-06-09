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
                withCredentials([sshUserPrivateKey(credentialsId: 'deploy-key', keyFileVariable: 'SSH_KEY', usernameVariable: 'SSH_USER')]) {
                    sh """
                        echo "Local workspace files:"
                        ls -la

                        mkdir -p ~/.ssh

                        ssh-keyscan -H ${REMOTE_HOST} >> ~/.ssh/known_hosts

                        scp -i \$SSH_KEY ./docker-compose.yaml ./app.py ./requirements.txt ./Dockerfile ${SSH_USER}@${REMOTE_HOST}:${REMOTE_DIR}/

                        ssh -i \$SSH_KEY ${SSH_USER}@${REMOTE_HOST} bash -c "\\
                            mkdir -p /home/ubuntu/app && \\
                            cd /home/ubuntu/app || { echo 'Failed to cd to /home/ubuntu/app'; exit 1; } && \\
                            echo 'Files in /home/ubuntu/app:' && \\
                            ls -la && \\
                            docker compose down || true && \\
                            docker compose pull && \\
                            docker compose up -d --build \\
                        "
                    """
                }
            }
        }
    }
}
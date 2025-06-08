pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/your-repo/project.git'
            }
        }
        stage('Build') {
            steps {
                sh 'docker build -t flask-app .'
            }
        }
        stage('Test/Lint') {
            steps {
                sh 'docker run --rm flask-app flake8 .'
            }
        }
        stage('Deploy') {
            steps {
                sshagent(credentials: ['your-ssh-credentials']) {
                    sh '''
                        scp -r . user@remote-machine:/path/to/project
                        ssh user@remote-machine "cd /path/to/project && docker-compose pull && docker-compose up -d"
                    '''
                }
            }
        }
    }
}
pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKER_HUB_USERNAME = 'alfredd25'
        BACKEND_IMAGE = "${DOCKER_HUB_USERNAME}/calorie-tracker-backend"
        FRONTEND_IMAGE = "${DOCKER_HUB_USERNAME}/calorie-tracker-frontend"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    docker compose -f docker-compose.test.yml up --abort-on-container-exit api_test
                    docker compose -f docker-compose.test.yml down
                '''
            }
        }

        stage('Build Images') {
            steps {
                sh '''
                    docker compose build api frontend
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh '''
                    echo $DOCKER_HUB_CREDENTIALS_PSW | docker login -u $DOCKER_HUB_CREDENTIALS_USR --password-stdin
                    docker tag calorie_tracker-api ${BACKEND_IMAGE}:latest
                    docker tag calorie_tracker-frontend ${FRONTEND_IMAGE}:latest
                    docker push ${BACKEND_IMAGE}:latest
                    docker push ${FRONTEND_IMAGE}:latest
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deployment step - will configure after AWS setup'
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            sh 'docker compose -f docker-compose.test.yml down || true'
        }
    }
}

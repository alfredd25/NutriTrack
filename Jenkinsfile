pipeline {
    agent any

    environment {
        DOCKER_HUB_CREDENTIALS = credentials('dockerhub-credentials')
        DOCKER_HUB_USERNAME = 'alfredd25'
        BACKEND_IMAGE = "${DOCKER_HUB_USERNAME}/calorie-tracker-backend"
        FRONTEND_IMAGE = "${DOCKER_HUB_USERNAME}/calorie-tracker-frontend"
        EC2_HOST = '13.236.134.144'
        EC2_USER = 'ubuntu'
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
                    docker compose build api
                    docker build \
                        --no-cache \
                        --build-arg NEXT_PUBLIC_API_URL=http://13.236.134.144/api \
                        -t calorie-tracker-frontend \
                        ./frontend
                '''
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh '''
                    echo $DOCKER_HUB_CREDENTIALS_PSW | docker login -u $DOCKER_HUB_CREDENTIALS_USR --password-stdin
                    docker tag calorie-tracker-api ${BACKEND_IMAGE}:latest
                    docker tag calorie-tracker-frontend ${FRONTEND_IMAGE}:latest
                    docker push ${BACKEND_IMAGE}:latest
                    docker push ${FRONTEND_IMAGE}:latest
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(['ec2-ssh-key']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "
                            cd ~/calorie-tracker &&
                            docker compose pull &&
                            docker compose up -d --force-recreate &&
                            docker exec calorie_api alembic upgrade head
                        "
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline succeeded! App deployed to EC2.'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            sh 'docker compose -f docker-compose.test.yml down || true'
        }
    }
}
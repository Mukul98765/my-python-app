pipeline {
    agent {
        docker {
            image 'python:3.10-slim'
        }
    }

    environment {
        IMAGE_NAME = "yourdockerhubusername/mukul-app"
        BUILD_TAG = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Test') {
            steps {
                sh 'mkdir -p reports'
                sh 'PYTHONPATH=. pytest --junitxml=reports/results.xml'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${BUILD_TAG} ."
            }
        }

        stage('Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin'
                    sh "docker push ${IMAGE_NAME}:${BUILD_TAG}"
                }
            }
        }

        stage('Slack Notify') {
            steps {
                slackSend channel: '#ci-cd-alerts', message: "✅ Mukul app build #${BUILD_TAG} passed!"
            }
        }
    }

    post {
        always {
            junit 'reports/results.xml'
        }
        failure {
            slackSend channel: '#ci-cd-alerts', message: "❌ Build failed: ${env.BUILD_URL}"
        }
    }
}


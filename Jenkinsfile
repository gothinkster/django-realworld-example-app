pipeline {
    agent any

    stages {
        stage('test') {
            steps {
                echo 'Hello World!'
                sh 'pip3 install -r requirements.txt'
            }
        }
        stage('build') {
            steps {
                echo 'buidling docker file!'
                sh 'docker build -t jenkins-demo:${BUILD_NUMBER}'
                sh 'docker images'
            }
        }
    }
}
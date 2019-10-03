pipeline {
  agent {
    docker {
      image 'python:3'
    }

  }
  stages {
    stage('version') {
      steps {
        sh 'python --version'
      }
    }
    stage('requirements') {
      steps {
        sh 'pip install requirements.txt'
      }
    }
  }
}
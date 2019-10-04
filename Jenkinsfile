pipeline {
  agent {
    docker {
      image 'edumco/sonar-scanner:slim'
    }

  }
  stages {
    stage('novo') {
      steps {
        sh 'ls'
        sh 'cd / && ls'
      }
    }
  }
}
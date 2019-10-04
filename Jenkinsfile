pipeline {
  agent {
    docker {
      image 'edumco/sonar-scanner'
    }

  }
  stages {
    stage('novo') {
      steps {
        sh 'ls'
        sh 'cd / && ls && cd home && ls'
      }
    }
  }
}
pipeline {
  agent {
    docker {
      image 'edumco/sonar-scanner:slim'
    }

  }
  stages {
    stage('analasys') {
      steps {
        node(label: 'docker') {
          sh 'ls'
        }

      }
    }
  }
}
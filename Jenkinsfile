pipeline {
  agent {
    docker {
      image 'edumco/sonar-scanner:slim'
    }

  }
  stages {
    stage('analasys') {
      steps {
        dockerNode(image: 'edumco/sonar-scanner:SLIM') {
          sh 'ls'
        }

      }
    }
  }
}
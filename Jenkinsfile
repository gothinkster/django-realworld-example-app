pipeline {
  agent none
  stages {
    stage('analasys') {
      agent {
        docker {
          image 'edumco/sonar-scanner'
        }

      }
      steps {
        dockerNode(image: 'edumco/sonar-scanner:slim') {
          sh 'ls'
        }

      }
    }
  }
}
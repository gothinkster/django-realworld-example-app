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
        sh 'ls'
        dockerNode(image: 'edumco/sonar-scanner') {
          sh 'ls'
        }

      }
    }
  }
}
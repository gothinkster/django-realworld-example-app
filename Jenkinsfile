pipeline {
  agent {
    docker {
      image 'edumco/sonar-scanner:slim'
    }

  }
  stages {
    stage('analasys') {
      steps {
        sh '/sonar-scanner-4.0.0.1744-linux/bin/sonar-scanner'
      }
    }
  }
}
pipeline {
  agent {
    dockerfile {
      filename 'Dockerfile.sonar'
    }

  }
  stages {
    stage('static-analasys') {
      agent {
        dockerfile {
          filename 'Dockerfile.sonar'
        }

      }
      steps {
        sh 'ls'
        sh './sonar-scanner-4.0.0.1744-linux/bin/sonar-scanner'
      }
    }
  }
}
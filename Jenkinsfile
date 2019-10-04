pipeline {
  agent none
  stages {
    stage('version') {
      agent {
        dockerfile {
          filename 'Dockerfile.pytest'
        }

      }
      steps {
        sh 'python --version'
        archiveArtifacts(allowEmptyArchive: true, onlyIfSuccessful: true, artifacts: '*')
      }
    }
    stage('static-analasys') {
      agent {
        dockerfile {
          filename 'Dockerfile.sonar'
        }

      }
      steps {
        sh 'ls'
        sh 'cd .. && ls && cd .. && ls'
        sh 'docker ps -a'
      }
    }
  }
}
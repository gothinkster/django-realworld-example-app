pipeline {
  agent {
    docker {
      image 'edumco/sonar-scanner:slim'
    }

  }
  stages {
    stage('analasys') {
      steps {
        dockerNode(image: 'cloudbees/jnlp-slave-with-java-build-tools') {
          git 'https://github.com/jglick/simple-maven-project-with-tests'
        }

      }
    }
  }
}
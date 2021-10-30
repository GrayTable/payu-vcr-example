pipeline {
  agent any
  stages {
    stage('Lint') {
      parallel {
        stage('Lint') {
          steps {
            sh 'sh \'pip install black && black ./payu\''
          }
        }

        stage('Type Check') {
          steps {
            sh 'sh \'pip install mypy && mypy ./payu\''
          }
        }

      }
    }

    stage('Test') {
      steps {
        sh 'sh \'pip install tox && tox\''
      }
    }

  }
}
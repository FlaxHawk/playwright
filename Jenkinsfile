pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.8'
        VENV_NAME = 'venv'
    }

    stages {
        stage('Setup Python') {
            steps {
                script {
                    sh """
                        python${PYTHON_VERSION} -m venv ${VENV_NAME}
                        . ${VENV_NAME}/bin/activate
                        python -m pip install --upgrade pip
                        pip install -r requirements.txt
                        playwright install
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    try {
                        sh """
                            . ${VENV_NAME}/bin/activate
                            pytest -v -n auto --html=reports/report.html --alluredir=reports/allure-results
                        """
                    } catch (Exception e) {
                        currentBuild.result = 'FAILURE'
                        error("Test execution failed: ${e.message}")
                    }
                }
            }
        }

        stage('Generate Reports') {
            steps {
                script {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        properties: [],
                        reportBuildPolicy: 'ALWAYS',
                        results: [[path: 'reports/allure-results']]
                    ])
                }
            }
        }

        stage('Deploy') {
            when {
                expression { currentBuild.result == 'SUCCESS' }
                branch 'main'
            }
            steps {
                echo 'Deploying...'
                // Add deployment steps here
            }
        }
    }

    post {
        always {
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'HTML Test Report'
            ])

            cleanWs()
        }

        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
            // Add notification steps here (e.g., email, Slack)
        }
    }
} 
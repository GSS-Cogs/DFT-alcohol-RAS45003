pipeline {
    agent {
        label 'master'
    }
    triggers {
        upstream(upstreamProjects: '../Reference/ref_alcohol',
                 threshold: hudson.model.Result.SUCCESS)
    }
    stages {
        stage('Clean') {
            steps {
                sh 'rm -rf out'
            }
        }
        stage('Transform') {
            agent {
                docker {
                    image 'cloudfluff/databaker'
                    reuseNode true
                }
            }
            steps {
                sh "jupyter-nbconvert --output-dir=out --ExecutePreprocessor.timeout=None --execute 'Estimated number of reported drink drive accidents and casualties in Great Britain 1979 - 2016.ipynb'"
                sh "jupyter-nbconvert --output-dir=out --ExecutePreprocessor.timeout=None --execute 'Reported road casualties in Great Britain, provisional estimates involving illegal alcohol levels.ipynb'"
            }
        }
        stage('Test') {
            agent {
                docker {
                    image 'cloudfluff/csvlint'
                    reuseNode true
                }
            }
            steps {
                script {
                    ansiColor('xterm') {
                        sh "csvlint -s RAS45003-schema.json"
                        sh "csvlint -s RAS51001-schema.json"
                    }
                }
            }
        }
        stage('Review') {
            steps {
                error "RAS51001.csv needs review and also need to understand whether these are distinct datasets"
            }
        }
    }
    post {
        always {
            script {
                archiveArtifacts 'out/*'
                updateCard "5b4f2a6f95cdf30512448eee"
                updateCard "5b4f29ecee119328508a6529"
            }
        }
    }
}

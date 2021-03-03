pipeline {
    agent {
      node { 
        label 'py-uniformes'
      }
    }
    
    options {
      buildDiscarder(logRotator(numToKeepStr: '5', artifactNumToKeepStr: '5'))
      disableConcurrentBuilds()
      skipDefaultCheckout()  
    }
    
        
  stages {
    stage('CheckOut') {
        steps {
          step([$class: 'GitHubSetCommitStatusBuilder'])
          checkout scm

        }
      }
      
    stage('Analise Codigo') {
          when {
            branch 'development'
          }
            steps {
                sh 'sonar-scanner \
                    -Dsonar.projectKey=SME-Imoveis-BackEnd \
                    -Dsonar.sources=. \
                    -Dsonar.host.url=http://sonar.sme.prefeitura.sp.gov.br \
                    -Dsonar.login=aad582cdfd5a6f174f87fcd53e52291198ac0728'
            }
       }
         
    stage('Docker build DEV') {
        when {
          branch 'development'
        }
          steps {
          // Start JOB Rundeck para build das imagens Docker
      
          script {
           step([$class: "RundeckNotifier",
              includeRundeckLogs: true,
                               
              //JOB DE BUILD
              jobId: "51155e1f-5357-4d5c-ab22-e1409fdc34c9",
              nodeFilters: "",
              //options: """
              //     PARAM_1=value1
               //    PARAM_2=value2
              //     PARAM_3=
              //     """,
              rundeckInstance: "Rundeck-SME",
              shouldFailTheBuild: true,
              shouldWaitForRundeckJob: true,
              tags: "",
              tailLog: true])
           }
        }
      }

    stage('Deploy DEV') {
        when {
          branch 'development'
        }
          steps {
            //Start JOB Rundeck para update de deploy Kubernetes DEV
         
            script {
                step([$class: "RundeckNotifier",
                  includeRundeckLogs: true,
                  jobId: "d1a0b66b-951e-4d19-9a4f-836dab708a71",
                  nodeFilters: "",
                  //options: """
                  //     PARAM_1=value1
                  //    PARAM_2=value2
                  //     PARAM_3=
                  //     """,
                  rundeckInstance: "Rundeck-SME",
                  shouldFailTheBuild: true,
                  shouldWaitForRundeckJob: true,
                  tags: "",
                  tailLog: true])
              }
          }
      }
		
	  stage('Docker build HOM') {
            when {
                branch 'homolog'
            }
            steps {
              // Start build das imagens Docker
      
          script {
            step([$class: "RundeckNotifier",
                includeRundeckLogs: true,
                    
                
                //JOB DE BUILD
                jobId: "1942978e-cf7b-4b3a-b20b-1a73837b4098",
                nodeFilters: "",
                //options: """
                //     PARAM_1=value1
                //    PARAM_2=value2
                //     PARAM_3=
                //     """,
                rundeckInstance: "Rundeck-SME",
                shouldFailTheBuild: true,
                shouldWaitForRundeckJob: true,
                tags: "",
                tailLog: true])
           }
          }
        }    
       
    stage('Deploy HOM') {
          when {
            branch 'homolog'
          }
          steps {
            
            timeout(time: 24, unit: "HOURS") {
               telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME} - Requer uma aprovação para deploy !!!\n Consulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)\n")
               input message: 'Deseja realizar o deploy?', ok: 'SIM', submitter: 'pedro_walter, calvin_rossinhole, rodolfo_lima, rodolpho_azeredo, anderson_morais'
            }
            //Start JOB Rundeck para update de imagens no host homologação 
         
            script {
                step([$class: "RundeckNotifier",
                includeRundeckLogs: true,
                jobId: "668a12b3-cb46-4edb-b608-cf1b95c6d4d5",
                nodeFilters: "",
                //options: """
                //     PARAM_1=value1
                //    PARAM_2=value2
                //     PARAM_3=
                //     """,
                rundeckInstance: "Rundeck-SME",
                shouldFailTheBuild: true,
                shouldWaitForRundeckJob: true,
                tags: "",
                tailLog: true])
            }
         }
        }
	    
	  stage('Docker build PROD') {
        when {
          branch 'master'
        }
        steps {
            
            // Start JOB Rundeck para build das imagens Docker
      
            script {
              step([$class: "RundeckNotifier",
                includeRundeckLogs: true,
                
                
                //JOB DE BUILD
                jobId: "3ca94df9-82a9-4563-b3c6-4a298fed1f42",
                nodeFilters: "",
                //options: """
                //     PARAM_1=value1
                //    PARAM_2=value2
                //     PARAM_3=
                //     """,
                rundeckInstance: "Rundeck-SME",
                shouldFailTheBuild: true,
                shouldWaitForRundeckJob: true,
                tags: "",
                tailLog: true])
            }
         }
      }           
    
    stage('Deploy PROD') {
            when {
                branch 'master'
            }
            steps {
                timeout(time: 24, unit: "HOURS") {
                telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME} - Requer uma aprovação para deploy !!!\n Consulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)\n")
                input message: 'Deseja realizar o deploy?', ok: 'SIM', submitter: 'calvin_rossinhole, pedro_walter, rodolfo_lima, rodolpho_azeredo, anderson_morais'
                }
                    
            
                script {
                    step([$class: "RundeckNotifier",
                    includeRundeckLogs: true,
                    jobId: "b9771bf1-278f-48b8-b51d-5e50adafe3d5",
                    nodeFilters: "",
                    //options: """
                    //     PARAM_1=value1
                    //    PARAM_2=value2
                    //     PARAM_3=
                    //     """,
                    rundeckInstance: "Rundeck-SME",
                    shouldFailTheBuild: true,
                    shouldWaitForRundeckJob: true,
                    tags: "",
                    tailLog: true])
                }
        
        
            }
        }
  }    


    
post {
        always {
          echo 'One way or another, I have finished'
        }
        success {
	  	    step([$class: 'GitHubCommitStatusSetter'])
          telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME} - Esta ok !!!\n Consulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)\n\n Uma nova versão da aplicação esta disponivel!!!")
        }
        unstable {
          step([$class: 'GitHubCommitStatusSetter'])
          telegramSend("O Build ${BUILD_DISPLAY_NAME} <${env.BUILD_URL}> - Esta instavel ...\nConsulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)")
        }
        failure {
          step([$class: 'GitHubCommitStatusSetter'])
          telegramSend("${JOB_NAME}...O Build ${BUILD_DISPLAY_NAME}  - Quebrou. \nConsulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)")
        }
        changed {
          echo 'Things were different before...'
        }
        aborted {
          step([$class: 'GitHubCommitStatusSetter'])
          telegramSend("O Build ${BUILD_DISPLAY_NAME} - Foi abortado.\nConsulte o log para detalhes -> [Job logs](${env.BUILD_URL}console)")
        }
    }
}
